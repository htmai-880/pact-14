<template>
    <div class="content">
        <div style="text-align:center">
            <h1>Find here your ingredients.</h1>
            <input type="food" placeholder="Search for ingredients." v-model="name" v-on:keyup.enter="searchIngredient"/>
            <SearchResults :data="gridData" :columns="gridColumns"></SearchResults>

        </div>
    </div>
</template>

<style>
    @import '../assets/styles/styles.css';
</style>

<script>
import SearchResults from '../components/SearchResults.vue';
export default {
     data() {
    return {
      errorMsg: "",
      name: "",
      gridData: [],
      gridColumns: ["name"]
    };
  },
  components: {
    SearchResults
  },
  methods: {
    async searchIngredient () {
        console.log("Hi! I'm a placeholder for the ingredient search. The input is " + this.name)
        const results = await this.$store.dispatch("searchingredient", this.name)
        console.log("Search results in Ingredients.vue are :", results)
        this.gridData=results
    }
  },
  computed:{
  }
}
</script>