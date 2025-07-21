'''
File:   process_control.py

Spec:   This script runs all the necessary scripts in the FKW detection pipeline.
        This script makes sure that other scripts run in the correct order and complete
        their specific functions in a timely manner. 

Usage:  python3 system_control/process_control.py
'''

# TODO: this has just been specced out by chatgpt, not finished. 
import subprocess
import time
import sys

# Time tracking
start_time = time.time()
MAX_RUNTIME_SECONDS = 20 * 60  # 20 minutes

def check_runtime():
    elapsed = time.time() - start_time
    if elapsed > MAX_RUNTIME_SECONDS:
        print("Maximum runtime exceeded. Initiating shutdown...")
        subprocess.run(["sudo", "shutdown", "now"], check=False)
        sys.exit(1)

# --- Script 1 ---
print("Running script1.py...")
try:
    subprocess.run(["python3", "script1.py"], check=True)
    print("script1.py completed successfully.\n")
except subprocess.CalledProcessError:
    print("script1.py failed.")
    sys.exit(1)
check_runtime()

# --- Script 2 ---
print("Running script2.py...")
try:
    subprocess.run(["python3", "script2.py"], check=True)
    print("script2.py completed successfully.\n")
except subprocess.CalledProcessError:
    print("script2.py failed.")
    sys.exit(1)
check_runtime()

# --- Script 3 ---
print("Running script3.py...")
try:
    subprocess.run(["python3", "script3.py"], check=True)
    print("script3.py completed successfully.\n")
except subprocess.CalledProcessError:
    print("script3.py failed.")
    sys.exit(1)
check_runtime()

print("All scripts completed successfully within the time limit.")

