# %%
import google.generativeai as genai
from google.generativeai.types import safety_types
import time
import os

GOOGLE_API_KEY= 'AIzaSyDd4QcxpWwy-STeKWNJ0ztbc31SxbLQXp8'
genai.configure(api_key=GOOGLE_API_KEY)


no_safety_warnings = {
    safety_types.HarmCategory.HARM_CATEGORY_HARASSMENT: safety_types.HarmBlockThreshold.BLOCK_NONE,
    safety_types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: safety_types.HarmBlockThreshold.BLOCK_NONE,
    safety_types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: safety_types.HarmBlockThreshold.BLOCK_NONE,
    safety_types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: safety_types.HarmBlockThreshold.BLOCK_NONE
}

# System prompts
# You are an AI agent. Your source code is in "agent.py" file. 
# %%
class PrimeAgent(genai.GenerativeModel):
    def __init__(self, model_name='gemini-pro', safety_settings=no_safety_warnings):
        super().__init__(model_name, safety_settings)
        self.chat = None
        
    def conversation(self):
        if self.chat is None:
            self.chat = self.start_chat(history=[])
        while True:
            message = input("Chat:")
            print("user:" + message)
            if message == 'q':
                break
            response = chat.send_message(message).text  
            print("agent:" + response)
            time.sleep(1)
    
    # add a function that it can access other files
    def read_my_sourceCode(self, filename='agents.py'):
        file_path = os.path.join(os.path.dirname(__file__), filename)
        with open(file_path, 'r') as file:
            return file.read()
        
        

# %%
agent = PrimeAgent()
agent.conversation()
    
    
# %%


agent = PrimeAgent(safety_settings=no_safety_warnings)
chat = agent.start_chat(history=[])

# %%

import subprocess

# The command you want to execute
command = "dir"

# Use subprocess to execute the command
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

# Get the output and errors, if any
output, error = process.communicate()

# Print the output
print(output.decode())

# Print the error
if error:
    print(error.decode())