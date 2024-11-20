#app6.py is the final voice assist on streamlit code...

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

    # Generate a unique log file name based on timestamp
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
        st.write("Chatbot is now running... Say 'goodbye' to end the session.")
        keyword_detected = False  # Flag to monitor for the keyword
        while True:
            output_line = process.stdout.readline()
            if output_line == '' and process.poll() is not None:
                break
            if output_line:
                # Display the output in Streamlit
                st.text(f"Chatbot: {output_line.strip()}")

                # Log the output
                log_file.write(f"STDOUT: {output_line.strip()}\n")

                # Check for the termination keyword
                if "goodbye" in output_line.lower():
                    keyword_detected = True
                    break

        # Stop the process gracefully if keyword is detected
        if keyword_detected:
            st.write("Goodbye detected. Stopping the chatbot...")
            process.terminate()  # Terminate the process
            process.wait()       # Wait for the process to exit

        # Read and log any error output
        error_output = process.stderr.read()
        if error_output:
            st.text(f"Subprocess Error: {error_output}")
            log_file.write(f"STDERR: {error_output}\n")

        # Final log message
        st.text(f"Session ended. Logs are saved to: {log_filename}")

# Streamlit UI setup
st.title("Keyword-Triggered Chatbot with Streamlit")

# Start button to trigger the voice chat
if st.button("Start Voice Chat"):
    run_voice_chat()
