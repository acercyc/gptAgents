"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

from pathlib import Path
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 1024,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Validate that an image is present
if not (img := Path("image0.jpeg")).exists():
  raise FileNotFoundError(f"Could not find image: {img}")

image_parts = [
  {
    "mime_type": "image/jpeg",
    "data": Path("image0.jpeg").read_bytes()
  },
  {
    "mime_type": "image/jpeg",
    "data": Path("image1.jpeg").read_bytes()
  },
  {
    "mime_type": "image/jpeg",
    "data": Path("image2.jpeg").read_bytes()
  },
]

prompt_parts = [
  "Extract the objects in the provided image and output them in a list in alphabetical order",
  "Image: ",
  image_parts[0],
  "List of Objects: - airplane\n- coffee cup\n- eiffel tower\n- globe\n- keyboard\n- mouse\n- money\n- notebook\n- passport\n- pen\n- sunglasses\n- shopping cart\n- tablet",
  "Image: ",
  image_parts[1],
  "List of Objects: - gardening gloves\n- rake\n- shovel\n- plants\n- pots\n- watering can",
  "Image: ",
  image_parts[2],
  "List of Objects: ",
]

response = model.generate_content(prompt_parts)
print(response.text)