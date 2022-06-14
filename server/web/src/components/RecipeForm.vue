<template>
<div>
<h1>Recipe Form</h1>
<p>NOTE TO USER: This only works if you input the exact name of the ingredients. A dropdown search will be added.</p>
<input v-model="title" placeholder="Enter title..."/>
<div class="ingredients" v-for="(input,k) in inputs" :key="k">
    <input placeholder="Enter ingredient..."
      class="ingredient"
      v-model="input.name"
      ></input>
    <input v-model="input.quantity" placeholder="Enter quantity (ex: 2, 1.2, 5/4)"/>
    <select v-model="input.unit">
    <option v-for="myOption in myOptions" :value="myOption.value">{{ myOption.text }}</option>
    </select>
    <b-form-textarea placeholder="Enter ingredient preparation (optional)..."
      rows="1"
      max-rows="1"
      class="ingredient"
      v-model="input.prep"
      ></b-form-textarea>
      	<p>
    Selected Unit = {{ (input.unit||"None") }}<br>
	</p>
    <span>
        <button class="circle minus" @click="remove_ingredient(k)" v-show="k || ( !k && inputs.length > 1)"></button>
        <button class="circle plus" @click="add_ingredient(k)" v-show="k == inputs.length-1"></button>
    </span>
</div>
<div class="instructions" v-for="(instruction,k) in instructions" :key="k">
    <b-form-textarea placeholder="Enter instruction..."
      rows="3"
      max-rows="6"
      class="instruction"
      v-model="instruction.desc"
      ></b-form-textarea>
    <span>
        <button class="circle minus" @click="remove_instruction(k)" v-show="k || ( !k && instructions.length > 1)"></button>
        <button class="circle plus" @click="add_instruction(k)" v-show="k == instructions.length-1"></button>
    </span>
</div>
<button @click="generate">Post recipe</button>
</div>
    
</template>

<style scoped>
.ingredients{
    background-color: rgb(189, 189, 189);
    padding: 10px;
}
.ingredient{
    width:70%;
    display: inline-block
}
.instructions{
    background-color: rgb(236, 217, 213);
    padding: 10px;
}
.instruction{
    width:90%;
    display: inline-block
}
.circle{
    border: 1px solid #aaa;
    box-shadow: inset 1px 1px 3px #fff;
    width: 22px;
    height: 22px;
    border-radius: 100%;
    position: relative;
    margin: 4px;
    display: inline-block;
    vertical-align: middle;
    background: #aaaaaa4f;
    display: inline-block
}
.circle:hover{
    background: #6363634f;
}
.circle:active{
    background: radial-gradient(#aaa, #fff);
}
.circle:before,
.circle:after{
    content:'';position:absolute;top:0;left:0;right:0;bottom:0;
}
/* PLUS */
.circle.plus:before,
.circle.plus:after {
    background:green;
    box-shadow: 1px 1px 1px #ffffff9e;
}
.circle.plus:before{
    width: 2px;
    margin: 3px auto;
}
.circle.plus:after{
    margin: auto 3px;
    height: 2px;
    box-shadow: none;
}
/* MINUS */
.circle.minus:before{
    background: #cc0000;
    margin: auto 3px;
    height: 2px;
    box-shadow: 0px 1px 1px #ffffff9e;
}
/* CROSS */
.circle.cross:after,
.circle.cross:before{
    background: #000;
    margin: auto 4px;
    height: 2px;
    transform:rotateZ(45deg);
    box-shadow: 0px 1px 1px #ffffff9e;
}
.circle.cross:after{
    transform:rotateZ(-45deg);
}

</style>

<script>

import {stringToFraction} from "@/utils"

export default {
    data() {
        return {
            title: null,
            inputs: [{name: '', quantity: '', unit: '', prep: ''}],
            instructions : [{desc: ''}],
            provenance : null,
            myModel:{},
            myOptions: [
                { value: '', text: 'unit(s)' },
                { value: 'kg', text: 'kg' },
                { value: '', text: 'gr' },
                { value: 'lb', text: 'lb' },
                { value: 'L', text: 'L' },
                { value: 'mL', text: 'mL' }
            ]
        }
    },
    methods: {
        generate() {
            console.log(stringToFraction("5.2"), this.title, this.inputs, this.instructions)
            var ingredients_list = []
            for (const ingredient of this.inputs){
                var fraction = stringToFraction(ingredient.quantity)
                var numerator = fraction[0]
                var denominator = fraction[1]
                ingredients_list.push(
                    {
                        name: ingredient.name,
                        properties: {
                            quantity_numerator: numerator, 
                            quantity_denominator: denominator, 
                            unit: ingredient.unit,
                            prep: (ingredient.prep||'')
                        }
                    }
                )
            }
            var instructions_list = []
            for (const instruction of this.instructions){
                instructions_list.push(instruction.desc)
            }
            const recipe = {
                email: this.$store.getters.email,
                title: this.title,
                ingredients: ingredients_list,
                provenance: '',
                instructions: instructions_list
            }
            console.log("Recipe = ", recipe)

            var r = this.$store.dispatch("postrecipe", recipe)
            console.log("Response", r)

            return recipe
        },
        add_ingredient(index) {
            this.inputs.push({ name: '' });
        },
        remove_ingredient(index) {
            this.inputs.splice(index, 1);
        },
        add_instruction(index) {
            this.instructions.push({ name: '' });
        },
        remove_instruction(index) {
            this.instructions.splice(index, 1);
        }
    },
    computed: {
        dropdownContent() {
            return null
        }
    }
}
</script>
