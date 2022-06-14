import requests


BASE = input("BASE URL: ") #"http://pact15.r2.enst.fr/api/backend/"


USERS = [
    {'username': 'Rion', 'email': 'rion@example.com', 'password': 'badpassword0'},
    {'username': 'John', 'email': 'john@example.com', 'password': 'badpassword1'},
    {'username': 'Arthur', 'email': 'arthur@example.com', 'password': 'badpassword2'},
    {'username': 'Noelle', 'email': 'noelle@example.com', 'password': 'badpassword3'},
    {'username': 'Mayu', 'email': 'mayu@example.com', 'password': 'badpassword2'},
    {'username': 'Noel', 'email': 'noel@example.com', 'password': 'badpassword3'}
]

'''
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
'''
for user in USERS:
    email = user["email"]
    data = {'email':email}
    argument=email.replace("@", "%40")
    print(argument)
    response = requests.get(BASE+"userfromemail?email="+argument)
    print(response.json())
'''
while True:
    email = input("Email: ")
    if email == "QUIT":
        break
    password = input("Password :")

    data = {'email': email, 'password': password}
    response = requests.post(BASE+"login", json=data)
    print(response.json())




