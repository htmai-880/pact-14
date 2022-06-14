<template>
    <div style="text-align:center" class="content">
    <div v-if="isAuthenticated">
    <p>Hi, {{username}}</p>
    <FridgeComponent :data="gridData" :columns="gridColumns" v-on:refresh="forceRerender"></FridgeComponent>
    <IngredientAdder v-on:refresh="forceRerender"/>
    <button @click="printGrid">Print fridge</button>
    </div>
    <div v-else>
      Not authenticated! Please log in
    </div>
    </div>
</template>

<style>
     @import '../assets/styles/styles.css';

  
</style>

<script>
import FridgeComponent from '../components/FridgeComponent.vue';
import IngredientAdder from '../components/IngredientAdder.vue';
export default {
  name: 'app',
    data() {
      return {
        gridData: this.$store.getters.myfridge,
        gridColumns: ['name', 'quantity', 'label'],
        componentKey: 0 //Force render
      }
  },
  components: {
    FridgeComponent, IngredientAdder
  },
  methods: {/*
    async profile(){
      var a = await this.$store.dispatch('myprofile', this.$store.getters.email)
      console.log(a)
      return a
    }*/ //Code réutilisable
    forceRerender() {
      this.gridData = this.$store.getters.allstate.user.fridge
      this.componentKey += 1
      console.log("Refreshing grid. componentKey = ", this.componentKey)
      console.log("gridData = ", this.gridData)
    },
    printGrid() {
      console.log("myfridge getter ", this.$store.getters.myfridge)
      console.log("allstate getter ", this.$store.getters.allstate.user.fridge)
    }
  },
  computed: {
    isAuthenticated () {
      return this.$store.getters.isAuthenticated
    },
    email() {
      return this.$store.getters.email
    },
    username(){
      return this.$store.getters.username
    }
  }
}
</script>