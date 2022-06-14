<template>
<div class="content">
  <span class="encadrer">
<h1>
  As students in first year at Telecom Paris, we are involved in a mandatory scientific project called "PACT".
  <br>
  It is based on the theme :  "Digital technology at the service of humans" 
  <br>


 Here is a quick summary of our application :
 </h1>
 <br>
 <br>
 <h3>
Currently existing cooking applications that provide recipes almost systematically require one to purchase
additional ingredients. Thus, they can become impractical for cooking “on the go” and encourage users to
overconsume and to waste.
<br>
We thereby offer a recipe recommendation application named S2R, SuppliesToRecipe. The logo designed for both the website and the application 
is the next one :
<br>
<img src="@/assets/logo_s2r.png" alt="Logo de S2R">
<br>
<br>

The distinctive feature of our product is its ability to prioritize the use of ingredients near their expiry
date by generating new recipes using ONLY the user’s ingredients.
<br>
<br>

We also attribute great importance to the user friendliness of our app, mainly by speeding up ingredient input.
<br>
<br>
Accordingly to the theme of the PACT project, “digital technology at the service of humans”, S2R will serve waste prevention and user experience.
</h3>
</span>


<div>
  <b-button v-b-modal.modal-login>Launch demo modal</b-button>
  <button @click="helloworld">Sanity Test Button</button>
</div>

</div>
  
</template>

<style >
.em {
  font-style:italic;
}
.h1 {

  text-align:justify;
  border : 1px solid black ;
  margin: auto;
  border-radius: 15px / 15px; 
  padding: 50;
  margin-bottom: 20px;
  background-color:#307954; 

}



.h3 {
  text-align:justify;
  border : 1px solid black ;
  margin: auto;
  border-radius: 15px / 15px; 
  padding: 50;
  margin-bottom: 20px;
  background-color:#243a79; 

}
.encadrer {
   padding-right: 10 px;
   padding-left: 10 px;
}
img {
  margin-left: auto;
  margin-right: auto;
}

</style>

<script>

export default {
  methods: {
        helloworld () {
      this.$store.dispatch('helloworld', {data: "dummydata"})
      console.log("All state = ", this.$store.getters.allstate)
      console.log("Fridge = ", this.$store.getters.myfridge)
    }
  }
}
</script>
