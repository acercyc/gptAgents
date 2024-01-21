# %%

import pathlib
import textwrap

import google.generativeai as genai

# Used to securely store your API key
# from google.colab import userdata

from IPython.display import display
from IPython.display import Markdown
import os


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY= 'AIzaSyDd4QcxpWwy-STeKWNJ0ztbc31SxbLQXp8'

genai.configure(api_key=GOOGLE_API_KEY)

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
    
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
chat

#%%
response = chat.send_message('Hello, how are you?')


# %%
to_markdown(response.text)



# %%
class PrimeAgent(genai.GenerativeModel):
    def __init__(self, model_name='gemini-pro'):
        super().__init__(model_name)
        
    # def read_text_file(self, filename):
    #     file_path = os.path.join(os.path.dirname(__file__), filename)
    #     with open(file_path, 'r') as file:
    #         return file.read()

agent = PrimeAgent()

# %%
chat = agent.start_chat(history=[])
response = chat.send_message('Hello, how are you?')    

# %%
response.text