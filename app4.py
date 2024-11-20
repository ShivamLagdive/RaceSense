#gives proper output..only after quickagent ends....but has some error after the program ends as the code still reads from stdout even after program end
import subprocess
import threading
import sys
import os
import streamlit as st

# Function to run the voice chatbot
def run_voice_chat():
    chatbot_python_path = os.path.expanduser(r"C:\Users\ADMIN\anaconda3\envs\venv\python.exe")
    process = subprocess.Popen(
        [chatbot_python_path, "QuickAgent.py"],  # Path to your chatbot script
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True,
    )

    # Function to read the subprocess output in a separate thread
    def read_output():
        while True:
            output_line = process.stdout.readline()
            if output_line:
                # Output the subprocess output to Streamlit
                st.text(f"Subprocess Output: {output_line.strip()}")
            if process.poll() is not None and not output_line:
                break

        # Read error output if any
        error_output = process.stderr.read()
        if error_output:
            st.text(f"Subprocess Error: {error_output}")

    # Start a separate thread to read subprocess output
    output_thread = threading.Thread(target=read_output)
    output_thread.daemon = True
    output_thread.start()

    process.communicate()  # Wait for the subprocess to finish

# Streamlit UI setup
st.title("Multi-Python Environment Chatbot with Streamlit")

# Start button to trigger the voice chat
start_button = st.button("Start Voice Chat")

if start_button:
    st.write("Starting the voice chatbot... Say 'goodbye' to end the session.")
    run_voice_chat()
