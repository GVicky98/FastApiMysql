import requests
import pandas as pd

# demo for GET method

api_url1 = "https://jsonplaceholder.typicode.com/users"
response = requests.get(api_url1)
a = response.json()
df1 = pd.DataFrame(a)
print(df1)

# demo for POST method

data1 = {
    "id": 11,
    "name": "Vignesh",
    "username": "vicky",
    "email": "vicky@abc.com",
    "address": {
        "street": "pasubathi street",
        "suite": "Apt. 154",
        "city": "Ariyalur",
        "zipcode": "621707",
        "geo": {
            "lat": "-37.3159",
            "lng": "81.1496"
        }
    },
    "phone": "8870110464",
    "website": "vicky.org",
    "company": {
        "name": "Riverstone",
        "catchPhrase": "Multi-layered client-server neural-net",
        "bs": "harness real-time e-markets"
    }
}
response1 = requests.post(api_url1,json=data1)
b = response1.json()
print(b)

# demo for PUT method

api_url2 = "https://httpbin.org/put"
data2 = {
    "id": 1,
    "employee_name": "Vignesh",
    "employee_salary": 13000,
    "employee_age": 25,
    "profile_image": ""
}
response2 = requests.put(api_url2,data = data2)
c = response2.json()
print(c)

# demo for DELETE method

api_url3 = "https://httpbin.org/delete"
response3 = requests.delete(api_url3)
d = response3.json()
print(d)