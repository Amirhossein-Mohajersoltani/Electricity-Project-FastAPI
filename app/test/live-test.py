import requests

data = {
    "year": [1401,1402,1403],
    "region_code": [5,12],
    "fidder_code": [1,2,3,4,52,6,9,1,25,74,62]
}
response = requests.post("http://178.236.33.157:8000/long-term", json=data)

print(response.json())

