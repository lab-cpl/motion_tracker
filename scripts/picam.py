from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
from picamera2.outputs import FfmpegOutput
import time
import serial
import serial.tools.list_ports

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
ser.baudrate = 9600
print("Connection ready!")

# this loop searches for the arduino signal
try:
    while True:
        data_raw = ser.readline()
        data_decoded = data_raw.decode('latin-1')
        if "START" in data_decoded:
            print("Start recording...")
            timestamp = str(time.time())
            picam2.start_recording(encoder, "out_"+timestamp+".mp4")
        elif "STOP" in data_decoded:
            print("Stop recording...")
            picam2.stop_recording()
finally:
    print("Done")
        




