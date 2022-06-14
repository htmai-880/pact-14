import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component : Home
  },
  {
    path: '/recipes',
    name: 'Recipes',
    component: () => import(/* webpackChunkName: "recipes" */ '../views/Recipes.vue')
  },
  {
    path: '/ingredients',
    name: 'Ingredients',
    component: () => import(/* webpackChunkName: "Ingredients" */ '../views/Ingredients.vue')
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import(/* webpackChunkName: "contact" */ '../views/Contact.vue')
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/myfridge',
    name: 'MyFridge',
    component: () => import(/* webpackChunkName: "myfridge" */ '../views/MyFridge.vue')
  },

 {
  path: '/recipes/newrecipe',
  name: 'NewRecipe',
  component: () => import(/* webpackChunkName: "about" */ '../views/NewRecipe.vue')
},
{
  path : '/profile',
  name :'Profile',
  component : () => import (/* webpackChunkName: "about" */ '../views/Profile.vue')

}


]

const router = new VueRouter({
  routes
})

export default router
