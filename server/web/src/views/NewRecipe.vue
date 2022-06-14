<template>
<div>
    <div class="content">
    <RecipeForm v-if="isAuthenticated"/>
    <p v-else v-b-modal.modal-login>Not authenticated! Please log in by clicking here.</p>
    </div>
</div>
</template>

<style>
    @import '../assets/styles/styles.css';
</style>

<script>
import RecipeForm from "@/components/RecipeForm";

export default {
    components: { RecipeForm },
    computed: {
        isAuthenticated () {
            return this.$store.getters.isAuthenticated
        }
    }
}
</script>