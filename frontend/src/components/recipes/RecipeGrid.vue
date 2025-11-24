<template>
  <div>
    <div v-if="loading" class="loading">Загрузка...</div>
    <div class="recipes-grid">
      <RecipeCard 
        v-for="recipe in recipes" 
        :key="recipe.id" 
        :recipe="recipe"
        @click="$emit('recipe-click', recipe)"
      />
    </div>
    <div v-if="!loading && recipes.length === 0" class="no-results">
      <p>😔 Рецепты не найдены</p>
      <p>Попробуйте изменить фильтры поиска</p>
    </div>
  </div>
</template>

<script>
import RecipeCard from '../common/RecipeCard.vue';

export default {
  name: 'RecipeGrid',
  components: {
    RecipeCard
  },
  props: {
    loading: Boolean,
    recipes: Array
  },
  emits: ['recipe-click']
}
</script>