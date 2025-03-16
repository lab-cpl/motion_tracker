from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
from picamera2.outputs import FfmpegOutput
import time
import serial
import serial.tools.list_ports
import json
import warnings
import subprocess
from datetime import datetime
import os

# start the object and set video resolution
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size":(640,480)})
picam2.configure(video_config)

# set to 10M
encoder = H264Encoder(bitrate=10000000)

# loop to get info from lickometer

# first detect the FT232R this device connects arduino with pi
arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'FT232R' in p.description
]
if not arduino_ports:
    raise IOError("No arduino found")
if len(arduino_ports)>1:
    warnings.warn('Multiple Arduinon found - using the first')

print("Arduino found")

print("Opening arduino connection...")

# set this to match lickometer spec usual 115200 as baudrate
ser = serial.Serial(arduino_ports[0])
ser.baudrate = 115200
print("Connection ready!")

# this loop searches for the arduino signal
flag_latency = "idle"
flag_trial = "idle"
prev_event = 0
prev_sensor = 0
event = 0
sensor = 0
filename = "default"
DATE = datetime.today().strftime('%Y-%m-%d_%H:%M:%S')

try:
    while True:
    # this part reads the chunk from the serial bus
        data_raw = ser.readline()
        try:
            data_decoded = data_raw.decode('latin-1')
            # this unpacks the json chunk
            data_json = json.loads(data_raw)
            # when the reading is not good we skip it
            # good reads are always of the python dictionary type
            if type(data_json) == dict:
            # we first get the number of events and the sensor 
                event = data_json['event']
                sensor = data_json['sensor']
                ID = data_json['id']
                TIME = data_json['time']
                LICKS = data_json['lick']
                print("Event: " + str(event) + "Sensor: " + str(sensor) + "ID: " + str(ID) + "time: " + str(TIME) + "licks: " + str(LICKS))
                # create folder to store files
                DIR = "/home/pi/Desktop/" + str(ID) + "_" + str(DATE)
                if not os.path.exists(DIR):
                    os.makedirs(DIR)
            # if the number of event changes (using prev_event we know that)
            # and the number of licks is greater than 0 (-1 indicates nosepoke activity)
            # that means that the animal triggered an event and is in the 'latency' phase
            # so probably exploring, this phase ends when the animal does another nosepoke
                if event != prev_event and sensor == prev_sensor and data_json['lick'] >= 0:
                    if filename != "default":
                        # preview the newest file in the folder, that is, the previous recording
                        p = subprocess.Popen(["/usr/bin/vlc",filename, '--play-and-exit'])

                    print("Start recording latency")
                    # this is the filename
                    # animal id + time in ms + licks or -1 for nosepokes + sensor number + number of events
                    filename = DIR + "/" + "LATENCY"+"_"+str(ID)+"_"+str(TIME)+"_"+str(LICKS)+"_"+str(sensor)+"_"+str(event)+".mp4"
                    # idle means that phase is not active
                    flag_trial = "idle"
                    # the current phase becomes active by recording
                    flag_latency = "recording"
                    # stop recording previous trail
                    picam2.stop_recording()
                    # start recording latency, this should be later on re-encoded we skip ffmpeg on the fly output to be faster
                    output = FfmpegOutput(filename, audio=False)
                    picam2.start_recording(encoder, output)
            # here is the same idea but for nosepokes, if licks -1 and flag_trial === idle
            # which means that the previous phase was a triggered event, the we start recording
            # what comes after the nosepoke, this is important otherwise is would start multiple recordings
            # for the length that the animal does the nosepoke
                elif data_json['lick'] == -1 and flag_trial == "idle":
                    if filename != "default":
                        # preview the newest file in the folder, that is, the previous recording
                        p = subprocess.Popen(["/usr/bin/vlc",filename, '--play-and-exit'])
                    print("Start recording trial")
                    # animal id + time in ms + licks or -1 for nosepokes + sensor number + number of events
                    # notice here that event corresponds to the previous event as with nosepokes the event does not change
                    filename = DIR + "/" + "TRIAL"+"_"+str(ID)+"_"+str(TIME)+"_"+str(LICKS)+"_"+str(sensor)+"_"+str(prev_event)+".mp4"
                    flag_latency = "idle"
                    flag_trial = "recording"
                    # stop recording previous latency
                    picam2.stop_recording()
                    # start recording trial, this should be later on re-encoded we skip ffmpeg on the fly output to be faster
                    output = FfmpegOutput(filename, audio=False)
                    picam2.start_recording(encoder, output)
            # this stores the event number and the sensor so that comparisons can be made
            # for example with 2 sensor we have {0, 1} as possible sensor numbers
            # so if we get a lick in sensor 0 {event, sensor} is going to be
            # {0, 1}, {0, 2}, {0, 3} ... and so on, if the animal stays in the same sensor
            # we are going to get {0, 5} (event triggered after 5 licks) which is a new a events and that would trigger a latency recording
            # but if the animal does {0, 1..4} and then {1, 1..4} no event was triggered but the event is probably going to be different
            # between sensors, so we also neeed to check that the difference in event number is only considered when the readings
            # come from the same sensor.
                if (LICKS != -1):
                    prev_event = event
                    prev_sensor = sensor
                    
        except json.decoder.JSONDecodeError:
            print("the string does not contain valid JSON")
        except UnicodeDecodeError:
            print("incorrect decoding")
finally:
    print("Done")
        




