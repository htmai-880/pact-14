import requests

BASE = "http://127.0.0.1:5000/"

'''
REGISTER_DATA = [
    {'username': 'Rion', 'email': 'somecheesyemail@gmail.com', 'password': 'butthurtaf'},
    {'username': 'John', 'email': 'somesupercheesyemail@gmail.com', 'password': 'verybutthurt'}
    #{'username': 'John', 'email': 'foo@gmail.com', 'password': 'verybutthurt'}, #Username already used
    #{'username': 'bar', 'email': 'somesupercheesyemail@gmail.com', 'password': 'verybutthurt'} #Email already used
]

for data in REGISTER_DATA:
    response = requests.post(BASE+"register", json=data)
    print(response.json())
'''
'''
LOGIN_DATA = [
    {'email': 'somecheesyemail@gmail.com', 'password': 'butthurtaf'},
    {'email': 'somesupercheesyemail@gmail.com', 'password': 'verybutthurt'},
    {'email': 'someseriousemail@gmail.com', 'password': 'veryhurt'}
]

for data in LOGIN_DATA:
    response = requests.get(BASE+"login", json=data)
    print(response.json())

'''


while True:
    email = input("Email: ")
    if email == "QUIT":
        break
    password = input("Password :")

    data = {'email': email, 'password': password}
    response = requests.get(BASE+"login", json=data)
    print(response.json())




