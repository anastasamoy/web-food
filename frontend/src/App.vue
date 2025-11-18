<template>
  <div>
    <h1>Мои рецепты</h1>
    <div v-for="recipe in recipes" :key="recipe.id">
      {{ recipe.title }}
    </div>
  </div>
</template>

<script>
import { api } from './api'
export default {
  data() {
    return {
      recipes: []
    }
  },
  async mounted() {
    const data = await api.getRecipes()
    this.recipes = data.recipes
  }
}
</script>
