<template>
  <div class="content">
    <div class="container-recipe-display">
    
    <h2>{{title}}</h2>
    <h2> Ingredients: </h2>
    <b-form-rating v-model="avgRating" readonly inline></b-form-rating>
    <li v-for="ingredient in ingredients" :key="ingredient.id">
      {{ingredient.name}} (Qtt : {{ingredient.properties.quantity_numerator/ingredient.properties.quantity_denominator}} {{ingredient.properties.unit && ""}})
    </li>
    <h2>Instructions</h2>
    <li v-for="instruction in instructions" :key="instruction">
      {{instruction}}
    </li>
    </div>
    <div class="comment-section">
      <h2> Ratings </h2>
    <p @click="ratingShowHide"> {{showOrHide}} ratings </p>
    <div v-if="viewingRating">
    <li v-for="rating in ratings" :key="rating.username">
      <b-form-rating v-model="rating.grade" readonly inline></b-form-rating>
      {{rating.username}}, {{rating.date}} : <br>
      {{rating.comment}}
    </li>
    </div>
    <RatingForm v-if="isAuthenticated" :id="id"/> <br />
    </div>
  </div>
</template>

<style scoped>
.container-recipe-display{
  font-size: 12px;
}
.comment-section{
  position: relative;
  float: right;
  border: 3px solid #73AD21;
  background-color:#333;
  color: #f2f2f2;
  padding: 10px;
  width: 100%;
}
</style>

<script>
import RatingForm from '@/components/RatingForm.vue';
export default {
  props:{
    id: Number,
    title: String,
    provenance: String,
    ingredients: Array,
    instructions: Array,
  },
  data(){
    return {
      avgRating: 2,
      viewingRating: false,
      ratings: [] // TODO: Only handle top 10 comments.
    }
  },
  methods: {
    async ratingShowHide() {
      if (this.viewingRating) {
        this.ratings = []
        this.viewingRating = false
      }
      else {
        this.viewingRating = true
        console.log("this.id = ", this.id)
        const ratings = await this.$store.dispatch('getrating', this.id)
        this.ratings = ratings
        console.log("Ratings in RecipeDisplay are: ", ratings)
      }
    }
  },
  computed: {
    isAuthenticated () {
      return this.$store.getters.isAuthenticated
    },
    showOrHide () {
      if (this.viewingRating) {
        return "Hide"
      }
      else{
        return "Show"
      } 
    }
  },
  components: { RatingForm }
}
</script>