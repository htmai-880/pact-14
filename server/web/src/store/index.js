import Vue from 'vue'
import Vuex from 'vuex'

// imports of AJAX functions will go here
import { authenticate, register, helloworld, myprofile, myfridge, searchingredient, searchrecipe, recipe, 
  powersearchrecipe, postrecipe, ingredient, addingredientforuser, deleteingredientforuser} from '@/api'
import { getrating, postrating } from '@/api'
import { isValidJwt, userEmailFromJwt, userNameFromJwt, EventBus, formatFridge } from '@/utils'

Vue.use(Vuex)

const state = {
  // single source of data
  user: {},
  jwt: ''
}

const actions = {
  // asynchronous operations
  login (context, userData) {
    context.commit('setUserData', { userData })
    return authenticate(userData)
      .then(response => {
        context.commit('setJwtToken', { jwt: response.data });
        console.log("state = ", state);
      })
      .catch(error => {
        console.log('Error Authenticating: ', error)
        EventBus.$emit('failedAuthentication', error)
      })
  },
  register (context, userData) {
    context.commit('setUserData', { userData })
    return register(userData)
      .catch(error => {
        console.log('Error Registering: ', error)
        EventBus.$emit('failedRegistering: ', error)
      })
  },
  logout (context) {
    context.commit('removeUserData')
  },
  helloworld(context, userData) {
    context.commit('setUserData', { userData })
    return helloworld(userData)
      .then(response => {console.log("response to hello world= ", response)})
      .catch(error => {
        console.log('Error Hello World: ', error)
        EventBus.$emit('failedHelloWorld: ', error)
      })
  },
  /*async myprofile(context, email){
    console.log('My profile')
    const a = await myprofile(email)
    console.log(a.data.user)
    return a.data.user
  }*/ //Code réutilisable
  myfridge(context, username){
    console.log('My Fridge (username : ' + username + ')')
    return myfridge(username)
    .then(response => {
      context.commit('setFridge', { fridge: response.data });
      console.log("state = ", state);
    })
    .catch(error => {
      console.log('Error getting your fridge: ', error)
      EventBus.$emit('Failed obtaining fridge', error)
    })
  },
  postrecipe(context, recipe){
    return postrecipe(recipe)
    .catch(error => {
      console.log('Error posting recipe: ', error)
      EventBus.$emit('Failed posting recipe', error)
    })
  },
  async searchingredient(context, name){
    console.log('Search ingredient (name : ' + name + ')')
    const results = await searchingredient(name)
    console.log("Search results are : ", results.data)
    return results.data.ingredients
  },
  async ingredient(context, name){
    console.log('Search ingredient (name : ' + name + ')')
    const results = await ingredient(name)
    console.log("Search results are : ", results.data)
    return results.data.ingredient
  },
  async searchrecipe(context, title){
    console.log('Search recipe (title : ' + title + ')')
    const results = await searchrecipe(title)
    console.log("Search results are : ", results.data)
    return results.data.recipes
  },
  async powersearchrecipe(context, email){
    console.log('Power search recipe (email: ' + email + ')')
    const results = await powersearchrecipe(email)
    console.log("Search results are : ", results.data)
    return results.data.recipes_id
  },
  async recipe(context, id){
    console.log('Search recipe by id (id : ' + id + ')')
    const results = await recipe(id)
    console.log("Search results are : ", results.data)
    return results.data.recipe
  },
  async getrating(context, id){
    console.log('Getting ratings of recipe (id : ' + id + ')')
    const ratings = await getrating(id)
    console.log("Ratings are : ", ratings.data)
    return ratings.data.ratings
  },
  postrating(context, rating){
    console.log('Posting rating of recipe (id : ' + rating.id + ')')
    return postrating(rating)
    .catch(error => {
      console.log('Error posting rating: ', error)
      EventBus.$emit('Failed posting rating', error)
    })
  },
  addingredientforuser(context, input){
    console.log('Input is : ', input)
    const expiration_date = new Date (Date.now() + 1000*60*60*24*7) //In one week
    console.log("Complete expiration datetime is = ", expiration_date)
    console.log('Expiration date is : ', expiration_date.toISOString().split('T')[0])
    return addingredientforuser(input.ingredient_id, input.amount, input.unit, input.email, expiration_date.toISOString().split('T')[0])
  },
  deleteingredientforuser(context, input){
    console.log('Removing ingredient for user : ', input)
    return deleteingredientforuser(input.own_id, input.email)
    .catch(error => {
      console.log('Error deleting ingredient: ', error)
      EventBus.$emit('Failed deleting ingredient: ', error)
    })
  }
}

const mutations = {
  // isolated data mutations
  setUserData (state, payload) {
    console.log('setUserData payload = ', payload)
    state.userData = payload.userData
  },
  setJwtToken (state, payload) {
    console.log('setJwtToken payload = ', payload)
    localStorage.token = payload.jwt.token
    state.jwt = payload.jwt
    state.user = {}
    state.user.email = userEmailFromJwt(payload.jwt)
    state.user.username = userNameFromJwt(payload.jwt)
    isValidJwt(state.jwt)
  },
  removeUserData(state){
    console.log('removeUserData (logging out)')
    state.user= {}
    state.jwt= ''
  },
  setFridge(state, payload){
    console.log('setFridge ingredients =', payload)
    state.user.fridge = formatFridge(payload.fridge.ingredients)
    console.log('Fridge in store = ', state.user.fridge)
  }
}

const getters = {
  // reusable data accessors
  isAuthenticated (state) {
    return isValidJwt(state.jwt)
  },
  email(state){
    return state.user.email
  },
  username(state){
    return state.user.username
  },
  myfridge(state){
    return state.user.fridge
  },
  allstate(state){
    return state
  }
}

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters
})

export default store