<template>
  <div>
    <div class = "container-client-space">
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container-has-text-centered">
          <h2 class="title">Register</h2>
          <p class="subtitle error-msg">{{ errorMsg }}</p>
        </div>
      </div>
    </section>
    <form class="section">
      <div class="container">
        <div class="field">
          <label for="username">Username:</label>
          <div class="control">
            <input type="username" id="username" v-model="username">
          </div>
        </div>
        <div class="field">
          <label for="email">Email:</label>
          <div class="control">
            <input type="email" id="email" v-model="email">
          </div>
        </div>
        <div class="field">
          <label for="password">Password:</label>
          <div class="control">
            <input type="password" id="password" v-model="password">
          </div>
          <label for="password">Repeat password:</label>
          <div class="control">
            <input type="password" id="password" v-model="passwordr">
          </div>
        </div>

        <div class="container">
          <button class="button-user" @click="register">Register</button>
          <router-link to="/login"><button class="button-user" @click="helloworld">Already have an account? Log in</button></router-link>
        </div>

      </div>
    </form>
    </div>
  </div>
</template>

<style>
</style>

<script>
import { EventBus } from '@/utils';

export default {
  data() {
    return {
      errorMsg: "",
      username: "",
      email: "",
      password: "",
      passwordr:""
    };
  },
  methods: {
    register () {
      if (this.password==this.passwordr){
        this.$store.dispatch('register', {username: this.username, email: this.email, password: this.password })
          .then(() => this.$router.push('/'))
      }
      else{
        this.errorMsg="Input passwords don't match."
      }
    },
    helloworld () {
      this.$store.dispatch('helloworld', { email: this.email, password: this.password })
    },
  },
  mounted () {
    EventBus.$on('failedRegistering', (msg) => {
      this.errorMsg = msg
    })
    EventBus.$on('failedAuthentication', (msg) => {
      this.errorMsg = msg
    })
  },
  beforeDestroy () {
    EventBus.$off('failedRegistering')
    EventBus.$off('failedAuthentication')
  }
}
</script>


