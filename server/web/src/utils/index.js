/*
    An event bus which I can use to send messages around the application when certain things happen, like failed authentication in the event of a expired JWT
    A function to check a JWT to see if it is still valid or not

*/

import Vue from 'vue'

export const EventBus = new Vue()

export function isValidJwt (jwt) {
  /*console.log("Testing function");
  const token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJleGFtcGxlQG1haWwuY29tIiwiaWF0IjoxNTIyMzI2NzMyLCJleHAiOjE1MjIzMjg1MzJ9.1n9fx0vL9GumDGatwm2vfUqQl3yZ7Kl4t5NWMvW-pgw'
  const tokenParts = token.split('.')
  const body = JSON.parse(atob(tokenParts[1]))
  console.log(body)
  console.log("End test")*/
  console.log("JWT: ", jwt)
  if (!jwt.token || jwt.token.split('.').length < 3) {
    console.log("JWT is not in the right format or is null")
    return false
  }
  const data = JSON.parse(atob(jwt.token.split('.')[1])) //Second element of the jwt contains the data of the expiry time of the JWT.
  const exp = new Date((data.iat + 20*60) * 1000) //Now + 20 minutes
  console.log("JWT expires at: ", exp)
  const now = Date.now()
  console.log("Now is: ", now)
  console.log("JWT is valid: ", now < exp)
  return now < exp //The JWT is valid as long as it hasn't expired. Also this part gives me cancer.
}


export function userEmailFromJwt (jwt) {
  if (!jwt.token || jwt.token.split('.').length < 3) {
    return false
  }
  var a =  JSON.parse(atob(jwt.token.split('.')[1]))
  console.log("Current user = ", a)
  return a.sub
}

export function userNameFromJwt(jwt) {
  if (!jwt.token || jwt.token.split('.').length < 3) {
    return false
  }
  var a =  JSON.parse(atob(jwt.token.split('.')[1]))
  return a.usr
}

export function formatFridge(fridge){
  var ffridge = [] //formatted fridge
  console.log("Formatting fridge ", fridge)
  for (const ingredient of fridge){
    ffridge.push({name:ingredient.name,
      quantity: (ingredient.properties.quantity_numerator/ingredient.properties.quantity_denominator).toString().substring(0,5)
      + " " + ingredient.properties.unit,
      id:ingredient.id,
      label: ingredient.label,
      own_id: ingredient.own_id
    })
  }
  return ffridge
}

export function stringToFraction(string){
  var gcd = function gcd(a,b){
    return b ? gcd(b, a%b) : a;
  };

  const number = string.split('/')
  console.log("Number = ", number)
  if ((string.length==0)||(number.length>2)){
    console.log("Invalid format for number")
  }
  if (number.length==1){
    var x = parseFloat(number[0])
    var y = 1
  }
  if (number.length==2){
    var x = parseFloat(number[0])
    var y = parseFloat(number[1])
  }
  if (x==0) {
    return [0, 1]
  }
  while (!Number.isInteger(x)){
    x *= 10
    y *= 10
  }
  const number_gcd = gcd(x,y);
  return [x/number_gcd, y/number_gcd]
}