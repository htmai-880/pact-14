<template>
  <div>
    <div class = "container-client-space">
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container-has-text-centered">
          <h2 class="title">Hello World Sanity Test</h2>
          <p class="subtitle error-msg">{{ errorMsg }}</p>
        </div>
      </div>
    </section>
    <form class="section">
      <div class="container">
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
        </div>

        <div class="container">
          <button class="button-user" @click="helloworld">Log in</button>
          <router-link to="/register"><button class="button-user" @click="helloworld">Don't have an account yet? Register</button></router-link>
        </div>

      </div>
    </form>
    </div>
  </div>
</template>




<script>
import { EventBus } from '@/utils';

export default {
  name: 'HelloWorld',
    data() {
    return {
      errorMsg: "",
      email: "",
      password: ""
    };
  },
  methods:{
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
