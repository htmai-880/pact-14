<template>
    <div class="content">
        <input placeholder="Enter ingredient..."
        class="ingredient"
        v-model="ingredient.name"
        ></input>
        <input v-model="ingredient.quantity" placeholder="Enter quantity (ex: 2, 1.2, 5/4)"/>
        <select v-model="ingredient.unit">
        <option v-for="myOption in myOptions" :value="myOption.value">{{ myOption.text }}</option>
        </select>
        <button @click="addingredientforuser">Add ingredient</button>
    </div>
</template>

<script>

export default {
    data() {
        return {
            ingredient: {
                name: '',
                quantity: null,
                unit: ''
            },
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
        async addingredientforuser() {
            const ingredient = await this.$store.dispatch('ingredient', this.ingredient.name)// search ingredient and get its id
            console.log(ingredient)
            const ingredient_id = ingredient.id
            const input = {
                ingredient_id: ingredient_id,
                amount: parseInt(this.ingredient.quantity),
                unit: this.ingredient.unit,
                email: this.$store.getters.email
            }
            const result = await this.$store.dispatch('addingredientforuser', input)
            console.log("Add ingredient in fridge: ", result)
            await this.$store.dispatch('myfridge', this.$store.getters.username)
            this.$emit('refresh')
        }
    }
}
</script>
