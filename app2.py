# app.py
# import streamlit as st
# import asyncio
# from QuickAgent import run_conversation

# Streamlit UI
# st.title("Voice Chatbot with Streamlit")
# st.write("Press the button below to start a voice conversation with the chatbot.")

# Streamlit button to start the chatbot
# if st.button("Start Voice Chat"):
#     st.write("Starting the voice chatbot... Say 'goodbye' to end the session.")

    # Run the chatbot in the asyncio event loop
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)

    # try:
    #     loop.run_until_complete(run_conversation())
    # except Exception as e:
    #     st.error(f"An error occurred: {e}")
    # finally:
    #     loop.close()

    # st.write("Voice chatbot session ended.")


# # app2.py
# import streamlit as st
# import subprocess
# import os

# st.title("Multi-Python Environment Chatbot with Streamlit")
# st.write("Click the button to start the chatbot.")

# if st.button("Start Voice Chat"):
#     st.write("Starting the voice chatbot... Say 'goodbye' to end the session.")

#     # Path to the chatbot environment's Python interpreter
#     chatbot_python_path = os.path.expanduser(r"C:\Users\ADMIN\anaconda3\envs\venv\python.exe")

#     # Run QuickAgent.py in the chatbot environment
#     try:
#         result = subprocess.run(
#             [chatbot_python_path, "QuickAgent.py"], 
#             capture_output=True, 
#             text=True
#         )

#         # Display chatbot output
#         st.text_area("Chatbot Output", result.stdout)

#         # Display error if any
#         if result.stderr:
#             st.error(f"Error: {result.stderr}")

#     except Exception as e:
#         st.error(f"An error occurred: {e}")

#     st.write("Chatbot session ended.")

# #app2.py with continuous output from QuickAgent
# import streamlit as st
# import subprocess
# import os

# st.title("Multi-Python Environment Chatbot with Streamlit")
# st.write("Click the button to start the voice chatbot.")

# if st.button("Start Voice Chat"):
#     st.write("Starting the voice chatbot... Say 'goodbye' to end the session.")

#     # Path to the chatbot environment's Python interpreter
#     chatbot_python_path = os.path.expanduser(r"C:\Users\ADMIN\anaconda3\envs\venv\python.exe")

#     # Run QuickAgent.py in the chatbot environment using Popen for real-time output
#     try:
#         process = subprocess.Popen(
#             [chatbot_python_path, "QuickAgent.py"],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             bufsize=1,
#             universal_newlines=True,
#         )

#         # Display output in a Streamlit text area
#         output_area = st.empty()

#         # Read stdout line by line
#         while True:
#             # Read the next line of output
#             output_line = process.stdout.readline()

#             # If output line is not empty, update the Streamlit text area
#             if output_line:
#                 # Append the new line to the output area
#                 previous_text = output_area.text_area("Chatbot Output", height=300)
#                 output_area.text_area("Chatbot Output", previous_text + output_line)

#             # If the process is finished and no more output is left, break the loop
#             if process.poll() is not None and not output_line:
#                 break

#         # Check for any errors from stderr
#         error_output = process.stderr.read()
#         if error_output:
#             st.error(f"Error: {error_output}")

#     except Exception as e:
#         st.error(f"An error occurred: {e}")

#     st.write("Chatbot session ended.")


# #app2.py with unique key for text area..
# import streamlit as st
# import subprocess
# import os

# st.title("Multi-Python Environment Chatbot with Streamlit")
# st.write("Click the button to start the voice chatbot.")

# if st.button("Start Voice Chat"):
#     st.write("Starting the voice chatbot... Say 'goodbye' to end the session.")

#     # Path to the chatbot environment's Python interpreter
#     chatbot_python_path = os.path.expanduser(r"C:\Users\ADMIN\anaconda3\envs\venv\python.exe")

#     # Run QuickAgent.py in the chatbot environment using Popen for real-time output
#     try:
#         process = subprocess.Popen(
#             [chatbot_python_path, "QuickAgent.py"],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             bufsize=1,
#             universal_newlines=True,
#         )

#         # Create a placeholder for the chatbot output
#         output_area = st.empty()
#         full_output = ""  # To store all output for displaying

#         # Read stdout line by line
#         while True:
#             # Read the next line of output
#             output_line = process.stdout.readline()

#             # If output line is not empty, update the Streamlit text area
#             if output_line:
#                 # Append the new line to the accumulated output text
#                 full_output += output_line
#                 output_area.text_area("Chatbot Output", full_output, height=300, key="live_chat_output")

#             # If the process is finished and no more output is left, break the loop
#             if process.poll() is not None and not output_line:
#                 break

#         # Check for any errors from stderr
#         error_output = process.stderr.read()
#         if error_output:
#             st.error(f"Error: {error_output}")

#     except Exception as e:
#         st.error(f"An error occurred: {e}")

#     st.write("Chatbot session ended.")


#app2.py.....voice and terminal text displayed..
import streamlit as st
import subprocess
import os
import threading

st.title("Multi-Python Environment Chatbot with Streamlit")
st.write("Click the button to start the chatbot.")

def run_voice_chat():
    # Path to the chatbot environment's Python interpreter
    chatbot_python_path = os.path.expanduser(r"C:\Users\ADMIN\anaconda3\envs\venv\python.exe")

    # Run QuickAgent.py in the chatbot environment using Popen for real-time output
    try:
        process = subprocess.Popen(
            [chatbot_python_path, "QuickAgent.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        # Create a placeholder for the chatbot output
        output_area = st.empty()
        full_output = ""  # To store all output for displaying

        # Read stdout line by line and update output
        while True:
            # Read the next line of output
            output_line = process.stdout.readline()

            # If output line is not empty, update the Streamlit text area
            if output_line:
                full_output += output_line
                output_area.text_area("Chatbot Output", full_output, height=300, key="live_chat_output")

            # If the process is finished and no more output is left, break the loop
            if process.poll() is not None and not output_line:
                break

        # Check for any errors from stderr
        error_output = process.stderr.read()
        if error_output:
            st.error(f"Error: {error_output}")

    except Exception as e:
        st.error(f"An error occurred: {e}")

    st.write("Chatbot session ended.")

if st.button("Start Voice Chat"):
    st.write("Starting the voice chatbot... Say 'goodbye' to end the session.")
    
    # Start the voice chat function in a separate thread so audio and text can run concurrently
    threading.Thread(target=run_voice_chat).start()
