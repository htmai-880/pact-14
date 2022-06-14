# Module IA

Ce module expose une API Rest (codé en python via Flask Restfull)
qui donne la liste des recettes en fonction des entrées et des recette
connues au moment de la demande dans la base de donné.

```json
{
  "ingredients": [{"name": "TEST1", "amount": 1}, {"name": "TEST2", "amount": 2}]
}
```

```json
{
  "recipes_id": [1, 2, 3, 4]
}
```
