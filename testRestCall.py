import requests
import json

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)



if __name__ == '__main__':
    parameters = {
        "lat": 40.71,
        "lon": -74
    }
    #response = requests.get("http://api.open-notify.org/astros.json")
    response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
    print(response.status_code)
    jprint(response.json())