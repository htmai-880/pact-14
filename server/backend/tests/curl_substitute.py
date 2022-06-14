import requests

BASE = "http://127.0.0.1:5000/"

r = ""

while r!="QUIT":
    r = input(BASE)
    method = input("Method : ")
    if r!="QUIT":
        if method == 'GET':
            response = requests.get(BASE+r)
            print(response.json())
        elif method == 'POST':
            response = requests.post(BASE+r)
            print(response.json())
        elif method == 'DELETE':
            response = requests.delete(BASE+r)
            print(response.json())
        else:
            print("Invalid method.\n")
print("END")