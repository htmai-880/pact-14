
// api/index.js
import axios from 'axios'


//Environment variable to be imported
const API_URL = "http://pact15.r2.enst.fr/api/backend" //process.env.BACKEND_API_URL
const SEARCH_API_URL = "http://pact15.r2.enst.fr/api/ai" //process.env.AI_API_URL
const allowed_origin = "*"


export function authenticate (userData) {
  return axios.post(`${API_URL}/login`, userData, {
    headers: {"Access-Control-Allow-Origin": allowed_origin}
  })
}

export function register (userData) {
  return axios.post(`${API_URL}/register`, userData, {
    headers: {"Access-Control-Allow-Origin": allowed_origin}
  })
}

export function helloworld (userData) {
  const a = axios.post(`${API_URL}/helloworld`, userData,{
    headers: {"Access-Control-Allow-Origin": allowed_origin}
  })
  return a
}

export function myprofile (email) {
  const r = email.replace("@", "%40")
  return axios.get(`${API_URL}/userfromemail?email=${r}`,{
    headers: {"Access-Control-Allow-Origin": allowed_origin}
  })
}

export function myfridge(username){
  return axios.get(`${API_URL}/useringredients?username=${username}`,{
    headers: {"Access-Control-Allow-Origin": allowed_origin}
  })
}
export function searchingredient(name){
  return axios.get(`${API_URL}/searchingredient?name=${name}`,{
    headers: {"Access-Control-Allow-Origin": allowed_origin}
  })
}
export function ingredient(name){
  return axios.get(`${API_URL}/ingredient?name=${name}`,{
    headers: {"Access-Control-Allow-Origin": allowed_origin}
  })
}

export function searchrecipe(title){
  return axios.get(`${API_URL}/searchrecipe?title=${title}`,{
    headers: {"Access-Control-Allow-Origin": allowed_origin}
  })
}

export function recipe(id){
  return axios.get(`${API_URL}/recipebyid?id=${id}`,{
    headers: {"Access-Control-Allow-Origin": allowed_origin}
  })
}

export function powersearchrecipe(user_email){
  const r = user_email.replace("@", "%40")
  return axios.get(`${SEARCH_API_URL}/?user_email=${r}`,{
    headers: {"Access-Control-Allow-Origin": allowed_origin}
  })
}

export function postrecipe(recipe){
  console.log("Recipe in api :", recipe)
  if (!recipe.email){
    throw('No email to post recipe')
  }
  else{
    return axios.post(`${API_URL}/addrecipe`, recipe, {
      headers: {"Access-Control-Allow-Origin": allowed_origin}
    })
  }
}

export function getrating(recipe_id){
  console.log("Recipe id to get comments of: ", recipe_id)
  if (isNaN(recipe_id)){
    throw("recipe id is not a number!")
  }
  else{
    return axios.get(`${API_URL}/rating?recipe_id=${recipe_id}`,{
      headers: {"Access-Control-Allow-Origin": allowed_origin}
    })
  }
}

export function postrating(rating){
  console.log("Rating of recipe: ", rating)
  // rating contains recipe_id, email, rating_grade, rating_comment
  return axios.post(`${API_URL}/rating`, rating, {
    headers: {"Access-Control-Allow-Origin": allowed_origin}
  })
}

export function addingredientforuser(ingredient_id, amount, unit, email, expiration_date){
  const input = {
    ingredient_id: ingredient_id,
    amount: amount,
    unit: unit,
    user_email: email,
    expiration_date: expiration_date
  }
  console.log("input = ", input)
  return axios.post(`${API_URL}/addingredientforuser`, input,{
    headers: {"Access-Control-Allow-Origin": allowed_origin}
  })
}

export function deleteingredientforuser(own_id, email){
  const input = {
   own_id: own_id,
   user_email: email
  }
  return axios.delete(`${API_URL}/addingredientforuser`, {
    headers: {"Access-Control-Allow-Origin": allowed_origin},
    data: input
  })
}

/*
//Placeholder user data:

var USERS=[{username: "Rion", email: "rion@example.com", password: "foo"},
 {username: "Arthur", email: "arthur@example.com", password: "bar"}
]
const secretKey = "supersecretkey"

export function authenticate(userData){
  console.log(USERS);
  console.log(userData);
  if (USERS.find(user => user.email === userData.email && user.password === userData.password)){
    var jwt = require('jwt-simple');
    var payload = {
      'sub': userData.email,
      'iat': Date.now(),
      'exp': Date.now()+30*1000*60
    }
    var secret = secretKey;
    const a = jwt.encode(payload, secret);
    console.log(a); //Ok until here
    return Promise.resolve({data:decodeURIComponent(escape(a))});
  }
  else{
    console.log("User not found");
  }
}

export function register(userData){
  if (!(USERS.find(user => user.username === userData.username || user.email === userData.email))){
    USERS.push(userData);
    return Promise.resolve(true);
  }
}

export function helloworld(userData){
  console.log(userData);
  console.log("Hello World!");
  return Promise.resolve(true);
}


//decodeURIComponent(escape(s))
*/
