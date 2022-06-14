<template>
  <div>
    <div class = "container-contact">
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container-has-text-centered">
          <h1 class="title">Check and update your profile</h1>
                <p> Here are your informations.</p>
                <p> /
                </p>
                    
          <p class="subtitle error-msg">{{ errorMsg }}</p>
        </div>
      </div>
    </section>

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

    };
  }
}
</script>
