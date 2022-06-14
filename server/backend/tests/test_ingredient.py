import requests

BASE = "http://127.0.0.1:5000/"

NAMES = ["Cheese", "Soy sauce"]

for name in NAMES:
    response = requests.post(BASE + "addingredient?name="+name)
    print(response.json())


response = requests.get(BASE + "searchrecipe?title=R")
print(response.json())

response = requests.get(BASE + "searchingredient?name=Chee")
print(response.json())
response = requests.get(BASE + "searchingredient?name=Soy")
print(response.json())

'''
response = requests.get(BASE + "/recipe?title=Recette1_titre")
print(response.json())'''
