#log files being stored....long chats are not saved and mulitple press of start button causes mutiple threads to start many subprocesses

import subprocess
import os
import streamlit as st
import time

# Function to run the voice chatbot and log its output
def run_voice_chat():
    # Create the logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Generate a unique log file name based on timestamp (with date and time at the end)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    log_filename = os.path.join(log_dir, f"chatbot_log_{timestamp}.txt")
    
    # Open the log file in write mode
    with open(log_filename, 'w') as log_file:
        # Define the process to run the chatbot script
        chatbot_python_path = os.path.expanduser(r"C:\Users\ADMIN\anaconda3\envs\venv\python.exe")
        process = subprocess.Popen(
            [chatbot_python_path, "QuickAgent.py"],  # Path to your chatbot script
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        # Read and display the output in real-time, while logging it
        while True:
            output_line = process.stdout.readline()
            if output_line == '' and process.poll() is not None:
                break
            if output_line:
                # Display to Streamlit
                st.text(f"Subprocess Output: {output_line.strip()}")
                
                # Log to file
                log_file.write(f"STDOUT: {output_line.strip()}\n")
        
        # After the process ends, read any error output and display/store it
        error_output = process.stderr.read()
        if error_output:
            st.text(f"Subprocess Error: {error_output}")
            log_file.write(f"STDERR: {error_output}\n")

        # Display final log message in Streamlit
        st.text(f"Subprocess completed. Logs are saved to: {log_filename}")

# Streamlit UI setup
st.title("Multi-Python Environment Chatbot with Streamlit")

# Start button to trigger the voice chat
start_button = st.button("Start Voice Chat")

if start_button:
    st.write("Starting the voice chatbot... Say 'goodbye' to end the session.")
    run_voice_chat()
