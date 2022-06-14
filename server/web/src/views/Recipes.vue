<template>
    <div class="content">
        <b-modal id="modal-recipe-display" size="lg" hide-footer>
            <RecipeDisplay v-if="id>=0" :id="recipe.id" :title="recipe.title" :ingredients="recipe.ingredients" 
            :instructions="recipe.instructions" :provenance="recipe.provenance"/>
        </b-modal>
        <div style="text-align:center">
            <h1 @click="getrecipe">It's time to get souped.
            </h1>
            <input type="food" placeholder="Search for recipes." v-model="title" v-on:keyup.enter="searchRecipe"/>
            <button @click="powerSearch" v-if="isAuthenticated">Power search</button>
            <SearchResults :data="gridData" :columns="gridColumns" v-model="id" v-on:getRecipe="getrecipe"></SearchResults>

        </div>
        <FONT size=50 pt>
        <div>
            <router-link to="/recipes/newrecipe">  Wanna share your awesomeness? Give us a new recipe! </router-link>
            <img src="@/assets/cheftoque.jpg" alt="image chef" align=right>
        </div>
        </FONT>
    </div>
</template>

<style>
    @import '../assets/styles/styles.css';
    .img {
      width:100px;

    }
    
</style>

<script>
import SearchResults from '../components/RecipeSearchResults.vue';
import RecipeDisplay from '../components/RecipeDisplay.vue';
import RecipeForm from  '../components/RecipeForm.vue'
export default {
         data() {
    return {
      errorMsg: "",
      title: "",
      gridData: [],
      gridColumns: ["title", "provenance", "id"],
      id: -1,
      recipe: JSON
    };
  },
  components: {
    SearchResults, RecipeDisplay, RecipeForm
  },
  methods: {
    async searchRecipe () {
        console.log("Hi! I'm a placeholder for the recipe search. The input is " + this.title)
        const results = await this.$store.dispatch("searchrecipe", this.title)
        console.log("Search results in Recipes.vue are :", results)
        this.gridData=results
    },
    async getrecipe () {
        console.log("Id : ", this.id)
        const result = await this.$store.dispatch("recipe", this.id)
        console.log("Recipe is ", result)
        this.recipe = result
        this.$bvModal.show('modal-recipe-display')
    },
    async powerSearch (){
        console.log("Hi! I'm a placeholder for the power search. The current user is " + this.$store.getters.email)
        const ids = await this.$store.dispatch("powersearchrecipe", this.$store.getters.email)
        console.log("Power search results in Recipes.vue are :", ids)
        var recipes = []
        for (const id of ids){
          const temp = await this.$store.dispatch('recipe', id)
          recipes.push({title: temp.title, provenance: temp.provenance, id: temp.id})
        }
        console.log("Displayed recipes in Recipe.vue are : ", recipes)
        this.gridData=recipes
    } 
  },
  computed:{
    isAuthenticated () {
      return this.$store.getters.isAuthenticated
    }
  }
}
</script>