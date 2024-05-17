import threading
import subprocess

def run_script(script_name):
    subprocess.run(["python", script_name])

if __name__ == "__main__":
    script_name = ["forward.py", "analyze_stream.py"]

    for script in script_name:
        script_thread = threading.Thread(target=run_script, args=(script,))
        script_thread.start()
        script_thread.join()

    print("Scripts have finished executing.")