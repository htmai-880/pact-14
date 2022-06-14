<template>
<div>
    <form @submit.prevent="rate" class=user-rating>
        Insert your rating.<br>
        <p v-if="this.errorMessage" class="error-message">{{errorMessage}}</p>
        <b-form-rating v-model="userRating"></b-form-rating> <br />
        <textarea rows="5" cols="60" name="text" placeholder="Write your comment here." v-model="userComment"></textarea>
        <br/>
        <input type="submit" value="Submit"/>
    </form>
</div>
</template>

<style scoped>

.error-message{
    color: red
}

textarea{
    width: 100%;
    height: 100px;
    vertical-align: baseline;
}
</style>


<script>
export default {
    props: {
        id: Number
    },
    data(){
        return {
            userRating: null,
            userComment: "",
            errorMessage: null
        }
    },
    methods: {
        rate(){
            console.log("Hi! I'm a placeholder for the rating function. This makes a POST method to the backend.")
            console.log("userRating : ", this.userRating)
            console.log("userComment : ", this.userComment)
            if (this.userRating==null||this.userComment==""){
                this.errorMessage = "Please give this recipe a rating and a comment for others to know what you thought of this recipe."
                console.log("Please give this recipe a rating and a comment for others to know what you thought of this recipe.")
            }
            else {
                console.log("Everything ok! o/")
                console.log("Rating grade: ", this.userRating)
                const rating = {
                    recipe_id: this.id,
                    email: this.$store.getters.email,
                    rating_grade: this.userRating,
                    rating_comment: this.userComment
                }
                var result = this.$store.dispatch("postrating", rating)
                console.log("Post recipe result: ", result)
                this.userComment=""
                this.errorMessage=null
            }
        }
    },
}
</script>

