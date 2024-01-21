# %%
import google.generativeai as genai
from google.generativeai.types import safety_types
import subprocess
import time
import os
import json
import traceback

GOOGLE_API_KEY= 'AIzaSyDd4QcxpWwy-STeKWNJ0ztbc31SxbLQXp8'
genai.configure(api_key=GOOGLE_API_KEY)

def execute_command(command):
    """
    Execute a shell command and return a formatted string with its output, error, and return code.

    Args:
    command (str): The command to be executed.

    Returns:
    str: A formatted string containing the output, error, and return code.
    """
    try:
        # Run the command
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        # Capture the output and error
        output, error = process.communicate()

        # Format the result
        result = f"Command: {command}\n\n"
        result += "Output:\n" + output + "\n"
        if error:
            result += "Error:\n" + error + "\n"
        result += f"Return Code: {process.returncode}\n"

        return result

    except Exception as e:
        # In case of an exception, return the exception message as error
        return f"An exception occurred: {str(e)}"


def txt2block(blockTitle, text):
    return "\n*** " + blockTitle + " ***\n" + text
    
def cleanJSON(text):
    return text.replace("```json", "").replace("```", "").strip()


no_safety_warnings = {
    safety_types.HarmCategory.HARM_CATEGORY_HARASSMENT: safety_types.HarmBlockThreshold.BLOCK_NONE,
    safety_types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: safety_types.HarmBlockThreshold.BLOCK_NONE,
    safety_types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: safety_types.HarmBlockThreshold.BLOCK_NONE,
    safety_types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: safety_types.HarmBlockThreshold.BLOCK_NONE
}


class PrimeAgent(genai.GenerativeModel):
    def __init__(self, model_name='gemini-pro', window_length=20000, safety_settings=no_safety_warnings):
        super().__init__(model_name, safety_settings)
        self.context = ""
        self.window_length = window_length
        
        # load system_prompt 
        with open('system_prompt.txt', 'r') as file:
            # Read the entire file
            self.system_prompt = file.read()
            
        # load actionable action list 
        with open('actions.json', 'r') as file:
            # Read the entire file
            self.actions = file.read()
        
        self.actions = txt2block('actionable actions', self.actions)
        
    # select last n characters as context
    def update_context(self, message):
        self.context += message
        if len(self.context) > self.window_length:
            self.context = self.context[-self.window_length:]
            
    def act(self):
        self.update_context(txt2block('action', ""))
        
        # construct new prompt
        context = self.system_prompt + self.actions + self.context
        
        # action selection
        action_json = self.generate_content(context).text
        action_json = cleanJSON(action_json)
        
        # update context``
        # self.update_context(txt2block('action', action_json))
        self.update_context(action_json)
        
        return action_json
    
    
    def perceive(self, percept):
        # update context
        self.update_context(txt2block('perception', percept))
     
            
class Entity:
    def __init__(self):
        pass
    
    def interact(self, action):
        pass
    



    
    
class Environment:
    def __init__(self):
        pass
    
    def interact(self, action):
        try:
            action = json.loads(action)
            if action['action'] == "SPEAK":
                print(action['text'])
                outcome = ""
            elif action['action'] == "RUN COMMAND":
                outcome = self.CLI(action['command'])
            elif action['action'] == "ASK USER":
                outcome = "User:" + input("\n" + action['question'])
                
        except Exception as e:
            outcome = traceback.format_exc()
        return outcome
    
    def CLI(self, command):
        Cli_message = execute_command(command)
        return Cli_message
        
        

env = Environment()
agent = PrimeAgent(safety_settings=no_safety_warnings)
agent.context = "Session started\n\n"

for iStep in range(100):
    action_json = agent.act()
    outcome = env.interact(action_json)
    agent.perceive(outcome)
    print(agent.context)
