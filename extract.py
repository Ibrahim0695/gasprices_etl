import http.client
import json

def extract_prices():
    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        'content-type': "application/json",
        'authorization': "apikey 5hqygBScH1ifb1p6OdZodL:6uYLDoWQxkYaI5r4oHoxvr"
        }

    conn.request("GET", "/gasPrice/stateUsaPrice?state=WA", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    data_string = data.decode("utf-8")
    data_list = json.loads(data_string)


    return data_list