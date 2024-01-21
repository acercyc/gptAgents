# %% 
import json


def get_google_api_key():
    # Open the JSON file
    with open('config.json', 'r') as f:
        # Load JSON data from file
        data = json.load(f)

    # extract the value of GOOGLE_API_KEY
    GOOGLE_API_KEY = data[0]['GOOGLE_API_KEY']
    
    return GOOGLE_API_KEY


