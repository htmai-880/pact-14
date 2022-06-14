import Vue from 'vue'
import Vuex from 'vuex'
// imports of AJAX functions will go here
import { authenticate, register, helloworld} from '@/api'
import { isValidJwt, userEmailFromJwt, EventBus } from '@/utils'
import { getName } from '../api/recipes'

Vue.use(Vuex)

const state = {
  // single source of data
  user: {},
  jwt: ''
}

const actions = {
    getQuantity (context, Datas) {
        context.commit('')
        return authenticate(Datas)
        .then(response)

    },
    getName (context,Datas) {
        context.commit('getNameIngredients', {Datas})
        return getName(datas)
            .then(response=> {
                context.commit()
                console.log()
            })

    },
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
}
const mutations = {

}
const getters = {
    isAuthenticated (state) {
        return isValidJwt(state.jwt)
      }
    }


const store = {

}
export default store 