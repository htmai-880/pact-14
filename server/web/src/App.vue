<template>
  <div id="app">
    <Header></Header>
    <transition name=moveIn>
      <router-view/>
    </transition>
      <b-modal id="modal-login" size="lg" hide-footer>
    <LoginFormModal/>
  </b-modal>
        <b-modal id="modal-register" size="lg" hide-footer>
    <RegisterFormModal/>
  </b-modal>
  </div>
</template>

<style>
  @import "./assets/styles/styles.css";

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
.moveIn-enter-active{
  animation: fadeIn .5s ease-in;
}
@keyframes fadeIn{
  0%{
    opacity: 0;
    transform: translateY(20);
  }
  50%{
    opacity: 0.5;
    transform: translateY(10px);
  }
  100%{
    opacity: 1;
    transform: translateY(0px);
  }
}
</style>

<script>
import LoginFormModal from "@/components/LoginFormModal"
import RegisterFormModal from "@/components/RegisterFormModal"
import Header from '@/components/Header'
export default {
  name: 'App',
  components: { Header, LoginFormModal, RegisterFormModal }
}
</script>
