Pour les modules de front-end (Android, Web):

Ce module expose une API Rest (codé en python via Flask Restful). Par défaut, elle sera lancée à l'adresse http://127.0.0.1:5000/.

Endpoints:

".../helloworld", méthode POST: prend un objet JSON quelconque et renvoie `{'hello': 'world'}`. Cette URL permet de tester la cohérence de l'API.

".../login", méthode POST: prend un objet JSON de la forme `{"email": ..., "password": ...}` et renvoie:
- {"message": ...}; 400 si l'authentification échoue
- Un jeton JWT encodé si l'anthentification marche avec succès. Les trois données contenues dans le corps du jeton sont (email de l'utilisateur).(date de création du jeton).(date d'expiration du jeton)


".../register", méthode POST: prend un objet JSON de la forme `{"username": ..., "email": ..., "password": ...}` et renvoie:
- {"message": ...}, 400 si l'inscription de l'utilisateur échoue pour quelconque raison mentionnée dans le message
- {"message": ...}, 200 si l'inscription se fait avec succès.


".../searchuser", méthode GET: prend en argument `username` le nom de l'utililisateur recherché dans l'URL (par exemple, ".../searchuser?username=Rio") et renvoie `{"users": users}` où users est une liste d'objets JSON contenant les informations sur les utilisateurs dont le pseudo contient le `username` renseigné, sous la forme: `{"username": ..., "email": ..., "api_key": ...}` (exemple: `{users: {"username": "Rion", "email": "rion@example.com, "api_key": "a4815d5db6d38ee14e7971b9b2b64eb560de572c"}}`).


".../profile", méthode GET: prend en argument `username` le nom de l'utilisateur recherché (complet) dans l'URL (par exemple, ".../searchuser?username=Rion") et renvoie `{"users": users}` où users est un objet JSON contenant les informations sur l'utilisateur dont le pseudo est exactement le `username` renseigné, sous la forme: `{"username": ..., "email": ..., "api_key": ...}` (exemple: `{user: {"username": "Rion", "email": "rion@example.com, "api_key": "a4815d5db6d38ee14e7971b9b2b64eb560de572c"}}`).
Note: on pourra considérer d'ajouter plus d'informations, par exemple un chemin vers la photo de profil pour la fetch ou les recettes crées par l'utilisateur.

".../searchrecipe", méthode GET: prend en argument `title` le nom de l'utilisateur recherché dans l'URL (par exemple, ".../searchuser?title=Rio") et renvoie `{"users": users}` où users est une liste d'objets JSON contenant les informations sur les utilisateurs dont le pseudo contient le `username` renseigné, sous la forme: `{"username": ..., "email": ..., "api_key": ...}` (exemple: `{users: {"username": "Rion", "email": "rion@example.com, "api_key": "a4815d5db6d38ee14e7971b9b2b64eb560de572c"}}`).

