#subprocess OP displayed correctly in streamlit...but after i say goodbye.

import subprocess
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

    # Read output in the main thread
    while True:
        output_line = process.stdout.readline()
        if output_line == '' and process.poll() is not None:
            break
        if output_line:
            # Display the subprocess output in the Streamlit UI
            st.text(f"Subprocess Output: {output_line.strip()}")

    # After the process ends, read any error output
    error_output = process.stderr.read()
    if error_output:
        st.text(f"Subprocess Error: {error_output}")

# Streamlit UI setup
st.title("Multi-Python Environment Chatbot with Streamlit")

# Start button to trigger the voice chat
start_button = st.button("Start Voice Chat")

if start_button:
    st.write("Starting the voice chatbot... Say 'goodbye' to end the session.")
    run_voice_chat()
