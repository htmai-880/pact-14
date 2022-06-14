<template>
  <div>
    <div class = "container-contact">
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container-has-text-centered">
          <h1 class="title">Contact us</h1>
                <p> Send us a message anytime. We'll be happy to answer.</p>
          <p class="subtitle error-msg">{{ errorMsg }}</p>
        </div>
      </div>
    </section>
    <form class="section">
      <div class="container">
        <div class="username">
          <label for="name">Name:</label>
          <div class="control">
            <input type="email" id="email" v-model="name" required>
          </div>
        </div>
        <div class="field">
          <label for="email">Email:</label>
          <div class="control">
            <input type="email" id="email" v-model="email" required>
          </div>
        </div>
        <div class="field">
          <label for="contact-message">Message:</label>
          <div class="control">
            <input type="contact-message" id="contact-message" v-model="contactMessage" required>
          </div>
        </div>
        <div class="container">
            <button class="button-user">Send</button>
        </div>

      </div>
    </form>
    </div>
  </div>
</template>

<style>
  @import "../assets/styles/styles.css";
  
  .error-msg {
  color: red
}
</style>

<script>

export default {
  data() {
    return {
      errorMsg: "",
      email: "",
      password: ""
    };
  }
}