import pyaudio
import serial
import threading

global is_running

is_running = True

# --- Audio Configuration ---
CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000

# --- Serial Port Configuration ---
SERIAL_PORT = '/dev/ttyUSB4'  # Replace with your actual serial port
BAUD_RATE = 115200

# --- Audio Objects ---
p = pyaudio.PyAudio()
mic_stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
spk_stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

# --- Serial Port Object ---
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)


# --- Thread Functions ---
def mic_to_serial():
    global is_running
    # --- Reads audio from microphone and sends it to serial port ---
    print("mic initiated")
    while is_running:
        print("m1", end=" ")
        try:
            print("m2", end=" ")
            data = mic_stream.read(CHUNK)
            print("m3", end=" ")
            if not data is None:
                ser.write(data)
            print("mic")
        except Exception as e:
            print(f"Mic stream error: {e}")
    print("mic ended")

def serial_to_spk():
    global is_running
    # --- Reads data from serial port and sends it to speaker ---
    print("spk initiated")
    while is_running:
        print("s1", end=" ")
        try:
            print("s2", end=" ")
            data = ser.read(CHUNK)
            print("s3", end=" ")
            if not data is None:
                spk_stream.write(data)
            print("spk")
        except Exception as e:
            print(f"Speaker stream error: {e}")
    print("spk ended")


# --- Create and Start Threads ---
mic_thread = threading.Thread(target=mic_to_serial)
spk_thread = threading.Thread(target=serial_to_spk)
mic_thread.start()
spk_thread.start()


try:
    # --- Keep the main thread running (optional) ---
    while is_running:
        pass 
    
except KeyboardInterrupt:
    print("Stopped.")
    is_running = False
    mic_thread.join()
    spk_thread.join()
    
except Exception as e:
    is_running = False
    print(f"An error occurred: {e}")    

finally:
    print("Cleaning up")
    is_running = False
    mic_stream.stop_stream()
    mic_stream.close()
    spk_stream.stop_stream()
    spk_stream.close()
    p.terminate()
    ser.close()
