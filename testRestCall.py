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
    #response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
    #print(response.status_code)
    #jprint(response.json())
    #https://gorest.co.in/public-api/users?_format=json&access-token=EK7sSevkyefDnTnim4rI2II_XupiP6UJ9OV5
    url = 'https://www.w3schools.com/python/demopage.php'
    myobj = {'somekey': 'somevalue'}

    x = requests.post(url, data=myobj)
    print(x.status_code)
    print(x.text)
