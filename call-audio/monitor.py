# Activate this script and keep it running
# It monitors journalctl entries to detect initiation of calls from the Gnome Calls app
# This script will call stream.py to do the audio streaming

import subprocess
from datetime import datetime, timedelta
import time
import signal
import os

CALL_ACTIVE = False
CHILD_PID = 0


def get_journalctl_entries(age_in_sec=1):
  try:
    now = datetime.now()
    one_second_ago = (now - timedelta(seconds=age_in_sec)).strftime("%Y-%m-%d %H:%M:%S")
    args = ["--since", one_second_ago]
    result = subprocess.run(["journalctl"] + args, capture_output=True, text=True, check=True)
    return result.stdout
  except subprocess.CalledProcessError as e:
    print(f"Error running journalctl: {e}")
    return None


def run_child_script(script_path):
    process = subprocess.Popen(["python3", script_path])
    return process.pid


def start_pcm_audio():
    global CHILD_PID
    command = r"mmcli -m {} --command=AT+CPCMREG=1".format(modem_number)
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True, check=True)
        print("Result code: ", result.returncode)
        print("Outcome:", result.stdout)
        time.sleep(0.5)
        print("Starting stream")
        script_path = "stream.py"  # Replace with the actual path

        CHILD_PID = run_child_script(script_path) 
        print(f"Child process started with PID: {CHILD_PID}")

    except subprocess.CalledProcessError as e:
        print(f"Error running mmcli command: {e}")
        

        
def stop_pcm_audio():
    
    global CHILD_PID
   
    try:
        command = r"mmcli -m {} --command=AT+CPCMREG=0".format(modem_number)
        result = subprocess.run(command.split(), capture_output=True, text=True, check=True)
        print("Result code: ", result.returncode)
        print("Outcome:", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running mmcli command: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    time.sleep(0.5)
    print("Stopping stream")
        
    try:
        print(f"Sending SIGTERM to child process with PID: {CHILD_PID}")
        os.kill(CHILD_PID, signal.SIGKILL) 
    except OSError:
        print(f"Failed to kill child process with PID: {CHILD_PID}")

    print("Parent process finished.")
        
    _, status = os.waitpid(CHILD_PID, 0) 
    print(f"Child process with PID {CHILD_PID} exited with status: {status}")    
        
        
# Stop ModemManager and restart in debug mode
# sudo systemctl stop ModemManager
# sudo /usr/sbin/ModemManager --debug
print("Make sure you stop ModemManager and restart it in debug mode first")

# Get the number of the current modem from Modem Manager
command = r"mmcli -L" 
result = subprocess.run(command.split(), capture_output=True, text=True, check=True)
print("Result code: ", result.returncode)
print("Outcome:", result.stdout)
response = result.stdout
# Output expected to look like:
# /org/freedesktop/ModemManager1/Modem/1 [QUALCOMM INCORPORATED] SIMCOM_SIM7600E-H
tx = response.split("Modem/")
tx = tx[1].split(" ")
modem_number = tx[0]
print(f"Modem number is: {modem_number}.")


try:
    while True:
        # Get the last 1 second of journal entries
        journal_output = get_journalctl_entries(1)

        if journal_output:
            if "ModemManager" in journal_output:
                print("mm found")
                if "call is started" in journal_output or "call is accepted" in journal_output:
                    if CALL_ACTIVE == False:
                        print("call started")
                        CALL_ACTIVE = True
                        start_pcm_audio()
                if "user request to hangup call" in journal_output or "-> terminated" in journal_output:
                    if CALL_ACTIVE == True:
                        print("call stopped")
                        CALL_ACTIVE = False
                        stop_pcm_audio()
                        
            else:
                print("-")
            
        time.sleep(1)
            
except KeyboardInterrupt:
    print("Stopped.")

except Exception as e:
    #print(e.errno)
    print(f"An error occurred: {e}")
