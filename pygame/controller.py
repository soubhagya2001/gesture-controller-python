import subprocess
import os
import signal
import time

def run_script(script_name):
    return subprocess.Popen(['python', script_name])

if __name__ == "__main__":
    # Run script1.py
    process1 = run_script('fourth.py')

    # Wait for a moment to ensure that script1.py has started before launching script2.py
    time.sleep(1)

    # Run script2.py
    process2 = run_script('main4.ipynb')

    try:
        # Wait for both processes to finish
        process1.wait()
        process2.wait()
    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C) to terminate both processes
        os.kill(process1.pid, signal.SIGTERM)
        os.kill(process2.pid, signal.SIGTERM)
