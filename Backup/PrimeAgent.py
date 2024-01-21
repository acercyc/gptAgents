import google.generativeai as genai
from google.generativeai.types import safety_types
import json


def txt2block(blockTitle, text):
    return "\n*** " + blockTitle + " ***\n" + text


def cleanJSON(text):
    return text.replace("```json", "").replace("```", "").strip()


def get_google_api_key():
    # Open the JSON file
    with open("config.json", "r") as f:
        # Load JSON data from file
        data = json.load(f)

    # extract the value of GOOGLE_API_KEY
    GOOGLE_API_KEY = data[0]["GOOGLE_API_KEY"]

    return GOOGLE_API_KEY


genai.configure(api_key=get_google_api_key())

no_safety_warnings = {
    safety_types.HarmCategory.HARM_CATEGORY_HARASSMENT: safety_types.HarmBlockThreshold.BLOCK_NONE,
    safety_types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: safety_types.HarmBlockThreshold.BLOCK_NONE,
    safety_types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: safety_types.HarmBlockThreshold.BLOCK_NONE,
    safety_types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: safety_types.HarmBlockThreshold.BLOCK_NONE,
}


class PrimeAgent(genai.GenerativeModel):
    def __init__(
        self,
        model_name="gemini-pro",
        window_length=30720*2,
        safety_settings=no_safety_warnings,
        init_prompt=txt2block("SESSION START", "session start from here"),
        temperature=0.5
    ):
        super().__init__(model_name, safety_settings)
        self.context = init_prompt
        self.window_length = window_length
        self.temperature = temperature
        self.generation_config = genai.types.GenerationConfig(

        # load system_prompt
        with open("system_prompt.txt", "r") as file:
            # Read the entire file
            self.system_prompt = file.read()

        # load actionable action list
        with open("actions.json", "r") as file:
            # Read the entire file
            self.actionable_actions = txt2block("actionable actions", file.read())

    def update_context(self, message):
        self.context += message
        if len(self.context) > self.window_length:
            self.context = self.context[-self.window_length :]

    def act(self):
        self.update_context(txt2block('ACTION', ""))
        
        # construct new prompt
        context = self.system_prompt + self.actionable_actions + self.context
        
        # action selection
        action_json = self.generate_content(context).text
        action_json = cleanJSON(action_json)
        
        # update context
        self.update_context(action_json)
        
        return action_json
    
    def perceive(self, percept):
        # update context
        self.update_context(txt2block('PERCEPTION', percept))
        

if __name__ == '__main__':
    agent = PrimeAgent()
    agent.act()
    print(agent.context)