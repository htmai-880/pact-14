<template>
    <div class=content>
        <div class="container">
          <div class="container" style="float:left">
              </div>
                <img src= "@/assets/logo_s2r.png">
              <div class="container" style ="float:right;text-align:center; width: 400px;height:400px">
                <div class="container">
                    <h1><strong>Welcome to the S2R web application.</strong></h1>
                        <button  v-if="!isAuthenticated" v-b-modal.modal-login class="button-home">
                          Log in
                        </button>
                    
                        <button  v-if="!isAuthenticated" v-b-modal.modal-register class="button-home">
                          Register
                        </button>
                </div>
          </div>
      </div>
    </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'Home',
  computed: {
    isAuthenticated () {
      return this.$store.getters.isAuthenticated
    }
  }

}
</script>
