<template>
  <div class="recipe-card" @click="$emit('click')">
    <h3>{{ getRecipeName(recipe.name) }}</h3>
    <div class="meta">
      <span>⏱️ {{ recipe.minutes }} мин</span>
      <span>🛒 {{ recipe.n_ingredients }} ингредиентов</span>
    </div>
    <div class="desc">{{ recipe.description?.slice(0, 80) }}...</div>
  </div>
</template>

<script setup>
defineProps({
  recipe: {
    type: Object,
    required: true
  }
});

defineEmits(['click']);

function getRecipeName(name) {
  if (!name || /^-+$/.test(name.trim())) {
    return 'Без названия';
  }
  return name;
}
</script>

<style scoped>
.recipe-card {
  border: 1px solid #e9ecef;
  padding: 20px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.recipe-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
  border-color: #667eea;
}

.recipe-card h3 {
  margin: 0 0 12px 0;
  color: #333;
  font-size: 1.3em;
  line-height: 1.3;
}

.meta {
  display: flex;
  justify-content: space-between;
  margin: 12px 0;
  font-size: 0.9em;
  color: #666;
}

.desc {
  color: #555;
  line-height: 1.5;
  font-size: 0.95em;
}
</style>