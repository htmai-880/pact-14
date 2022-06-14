<template>
        <!-- Navigation bar -->
    <div id="nav">
      <router-link to="/">Home</router-link>
      <router-link to="/recipes">Recipes</router-link>
      <router-link to="/ingredients">Ingredients</router-link>
      <router-link to="/contact">Contact</router-link>
      <router-link to="/about">About</router-link>
      <router-link to="/myfridge" v-if="isAuthenticated">My fridge</router-link>
      <a v-if="isAuthenticated" @click="logout">Log out</a>
      <a v-if="!isAuthenticated" v-b-modal.modal-login>Log in</a>
      <a v-if="!isAuthenticated" v-b-modal.modal-register>Register</a>
      <input type="text" placeholder="Search for recipes or ingredients" style="width: 400px; height: 50px; margin-left: 5%"/>
    </div>
</template>

<style scoped>
#nav {
  margin-right:0px;
  margin-left:0px;
  padding:30px 0px;
  overflow: hidden;
  background-color: #333;
  width: 100%;
  text-align: center;
}

#nav a {
  font-weight: bold;
  background-color:#333;
  color: #f2f2f2;
  text-align: center;
  padding: 30px 30px;
  width: 8%;
  text-decoration: none;
  font-size: 20px;
  margin: 8px 8px;
}

#nav a:hover{
  background-color: #FF0000;
  color: black;
}


#nav a.router-link-exact-active {
  color: #42b983;
}

</style>

<script>
export default {
  methods:{
      logout () {
      this.$router.push('/')
      this.$store.dispatch('logout')
    }
  },
  computed: {
    isAuthenticated () {
      return this.$store.getters.isAuthenticated
    }
  }
}
</script>