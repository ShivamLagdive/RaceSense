import subprocess
import sys

def run_test_subprocess():
    process = subprocess.Popen(
        ["python", "-c", "print('Hello from subprocess')"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    while True:
        output = process.stdout.readline()
        if output:
            sys.stdout.write(f"Subprocess Output: {output.strip()}\n")
            sys.stdout.flush()

        if process.poll() is not None:
            break

run_test_subprocess()
