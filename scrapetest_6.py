import json
from urllib.request import urlopen

def getCountry(ipAdress):
    response = urlopen("http://freegeoip.net/json/"+ipAdress).read().decode('utf-8')
    responseJson = json.loads(response)
    return "Courty Code is: "+responseJson.get("country_code")

print(getCountry("50.78.253.58"))
