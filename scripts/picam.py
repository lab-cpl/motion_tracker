from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
from picamera2.outputs import FfmpegOutput
import time
import serial
import serial.tools.list_ports
import json
import warnings
import subprocess

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
try:
    while True:
        data_raw = ser.readline()
        try:
            data_decoded = data_raw.decode('latin-1')
            data_json = json.loads(data_raw)
            if type(data_json) == dict:
                if data_json['lick'] > 0 and flag_latency == "idle":
                    print("Start recording latency")
                    flag_trial = "idle"
                    flag_latency = "recording"
                elif data_json['lick'] == -1 and flag_trial == "idle":
                    print("Start recording trial")
                    flag_latency = "idle"
                    flag_trial = "recording"
        except json.decoder.JSONDecodeError:
            print("the string does not contain valid JSON")
        except UnicodeDecodeError:
            print("incorrect decoding")
        # for a json string this follow this form
        # if(dict_name["key1"]["following_status"]=="followed")
        # "following status" is within "key1"
        # to adapt the code I just need "new_event", "new_poke"
        # that way is easier to get a simple reading
        # so if this is to start recording after nosepoke
        # I read nosePoke_state
        # if nosePoke_state == TRUE
        # stop any previous recordings
        # start recording file is going to be called animal_date_T_trialnumber
        #if "START" in data_decoded:
        #    print("Start recording...")
        #    timestamp = str(time.time())
        #    picam2.start_recording(encoder, "out_"+timestamp+".mp4")
        # then here start a while loop
        # while bussy_sensor signal is FALSE keep doing pass
        # while (bussy_sensor_signal == 0):
        #   pass
        # after this stop recording, because this mean that animal triggered an event
        # replay this previously saved file in desktop
        # immediately start another recording with animal_date_L_(trialnumber - 1)
        #elif "STOP" in data_decoded:
        #    print("Stop recording...")
        #    picam2.stop_recording()
finally:
    print("Done")
        




