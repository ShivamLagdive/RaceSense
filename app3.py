#works fine with debug...but the terminal OP only shows after goodbye

import streamlit as st
import subprocess
import os
import threading
import sys

st.title("Multi-Python Environment Chatbot with Streamlit")
st.write("Click the button to start the voice chatbot. Say 'goodbye' to end the session.")

# Initialize session state to track chatbot status
if "chatbot_status" not in st.session_state:
    st.session_state.chatbot_status = ""

def run_voice_chat():
    # Path to the chatbot environment's Python interpreter
    chatbot_python_path = os.path.expanduser(r"C:\Users\ADMIN\anaconda3\envs\venv\python.exe")
    
    try:
        # Run QuickAgent.py in the chatbot environment using Popen for real-time output
        process = subprocess.Popen(
            [chatbot_python_path, "QuickAgent.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )
        
        # Read output line by line and print to terminal
        while True:
            output_line = process.stdout.readline()
            
            if output_line:
                sys.stdout.write(f"Subprocess Output: {output_line.strip()}\n")  # Write directly to terminal
                sys.stdout.flush()  # Ensure it appears immediately
            
            # If the process is finished and no more output, break
            if process.poll() is not None and not output_line:
                break
        
        # Check for any errors in stderr and print to terminal
        error_output = process.stderr.read()
        if error_output:
            sys.stderr.write(f"Subprocess Error: {error_output}\n")
            sys.stderr.flush()

    except Exception as e:
        sys.stderr.write(f"An error occurred: {e}\n")
        sys.stderr.flush()

# Button for starting the voice chatbot
if st.button("Start Voice Chat"):
    st.write("Starting the voice chatbot... Say 'goodbye' to end the session.")
    threading.Thread(target=run_voice_chat, daemon=True).start()

# Display session status (e.g., chatbot state)
if st.session_state.chatbot_status:
    st.write(st.session_state.chatbot_status)
