import openai
import os
from dotenv import load_dotenv
import requests
import json
load_dotenv()

openai.api_key = os.getenv("OPEN_AI_KEY")
messages1 = [
        {"role":"system", "content":"You give very short answers"},
        {"role":"user", "content":"can you describe the degree in bangalore?"},
    ]
function_description = [{
  'name': 'getWeather',
  'description': 'Get the current weather of a city',
  'parameters': {
    'type': 'object',
    'properties': {
      'city': {
        'type': 'string',
        'description': 'The City'
      }
    },
    'required': ['city']
  },
}]


response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = messages1,
    functions = function_description,
    function_call = "auto"
)
output = (response.choices[0].message).to_dict()
messages1.append(output)
print("----------------------FIRST REQUEST -------------------")
print(output)


def getWeather(city):
    base_url = f"https://api.weatherapi.com/v1/current.json"
    
    # Set up the parameters for the API request
    params = {
        "key": "",
        "q": "bengaluru"
    }

    try:
        # Make the API request
        response1 = requests.get(base_url, params=params, verify=False)
        data = response1.json()

        # Check if the request was successful
        if response1.status_code == 200:
            return data
        else:
            # Print an error message if the request was unsuccessful
            print(f"Error: {data['error']['message']}")

    except Exception as e:
        print(f"An error occurred: {e}")

if output['function_call']['name'] == 'getWeather':
    cityName = json.loads(output['function_call']['arguments'])['city']
    weather = str(getWeather(cityName));
    print(type(weather))
    # weather={'name': 'Bangalore', 'region': 'Karnataka','country': 'India','lat': 12.98,'lon': 77.58 }
    print("----------------------SECOND REQUEST -------")
    messages1.append({"role":"function", "name":output['function_call']['name'], "content":weather},)
    print(messages1)

    
# call the GPT and give it a weather data
    response2 = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages1,
        functions = function_description,
        function_call = "auto"
    )
print("----------------------FINAL REQUEST -------")
output1 = response2.choices[0].message.content
# messages1.append(output)
print(output1)