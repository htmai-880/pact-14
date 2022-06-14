<template>
  <div>
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container-has-text-centered">
          <h2 class="title">Log in</h2>
          <p class="subtitle error-msg">{{ errorMsg }}</p>
        </div>
      </div>
    </section>
    <form @submit.prevent="authenticate" class="section">
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
          <button class="button-user" @click="authenticate">Log in</button>
          <button class="button-user" @click="goToRegister">Don't have an account yet? Register</button>
        </div>

      </div>
    </form>
  </div>
</template>

<style>
  @import "../assets/styles/styles.css";
  
  .error-msg {
  color: red
}

</style>


<script>
import { EventBus } from '@/utils';

export default {
  data() {
    return {
      errorMsg: "",
      email: "",
      password: ""
    };
  },
  methods: {
    goToRegister(){
        this.$bvModal.show('modal-register')
        this.$bvModal.hide('modal-login')
    },
    authenticate () {
      this.$store.dispatch('login', { email: this.email, password: this.password })
        .then(() => this.$store.dispatch('myfridge', this.$store.getters.username))
        .then(()=> this.$bvModal.hide('modal-login'))
        .then(() => this.$router.push('/'))
    }

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