<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <button class="modal-close" @click="$emit('close')">×</button>
      <h2>{{ getRecipeName(recipe.name) }}</h2>
      <div class="meta">
        <span>⏱️ {{ recipe.minutes }} мин</span>
        <span>🛒 {{ recipe.n_ingredients }} ингредиентов</span>
      </div>
      <div class="desc">{{ recipe.description }}</div>
      
      <div v-if="recipe.ingredients">
        <h4>Ингредиенты:</h4>
        <ul>
          <li v-for="(ing, idx) in parseTags(recipe.ingredients)" :key="idx">{{ ing }}</li>
        </ul>
      </div>
      
      <div v-if="recipe.tags">
        <h4>Категории/теги:</h4>
        <div class="tags">
          <span v-for="tag in parseTags(recipe.tags)" :key="tag" class="tag">{{ tag }}</span>
        </div>
      </div>
      
      <div v-if="recipe.steps">
        <h4>Как готовить:</h4>
        <ol>
          <li v-for="(step, idx) in parseTags(recipe.steps)" :key="idx">{{ step }}</li>
        </ol>
      </div>
      
      <div v-if="recipe.nutrition">
        <h4>Пищевая ценность:</h4>
        <ul class="nutrition-list">
          <li v-for="(nutr, idx) in parseTags(recipe.nutrition)" :key="idx">
            <template v-if="nutritionLabels[idx]">
              <b>{{ nutritionLabels[idx] }}:</b> {{ isNaN(Number(nutr)) ? nutr : Number(nutr).toFixed(2) }}
            </template>
            <template v-else>
              {{ isNaN(Number(nutr)) ? nutr : Number(nutr).toFixed(2) }}
            </template>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  recipe: {
    type: Object,
    required: true
  }
});

defineEmits(['close']);

const nutritionLabels = [
  'Калории (kcal)',
  'Жиры (g)',
  'Насыщенные жиры (g)',
  'Углеводы (g)',
  'Сахар (g)',
  'Белки (g)',
  'Клетчатка (g)',
  'Натрий (mg)',
  'Холестерин (mg)'
];

function getRecipeName(name) {
  if (!name || /^-+$/.test(name.trim())) {
    return 'Без названия';
  }
  return name;
}

function parseTags(tags) {
  if (!tags) return [];
  if (Array.isArray(tags)) return tags.map(cleanText);
  
  try {
    const arr = JSON.parse(tags);
    if (Array.isArray(arr)) return arr.map(cleanText);
  } catch (e) {}
  
  return tags
    .replace(/^[\[]|[\]]$/g, '')
    .split(',')
    .map(t => cleanText(t))
    .filter(Boolean);
}

function cleanText(str) {
  return String(str)
    .replace(/^['"\\[]+|['"\\]]+$/g, '')
    .replace(/^'+|'+$/g, '')
    .replace(/^\s+|\s+$/g, '')
    .replace(/^,+|,+$/g, '')
    .replace(/^-+|-+$/g, '')
    .replace(/^\d+\.\s*/, '')
    .replace(/^'+/, '')
    .replace(/'+$/, '')
    .trim();
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
  backdrop-filter: blur(5px);
}

.modal-content {
  background: white;
  border-radius: 16px;
  padding: 30px;
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  animation: modalAppear 0.3s ease;
}

@keyframes modalAppear {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-close {
  position: absolute;
  top: 15px;
  right: 15px;
  background: #f8f9fa;
  border: none;
  font-size: 24px;
  cursor: pointer;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  color: #666;
}

.modal-close:hover {
  background: #667eea;
  color: white;
  transform: rotate(90deg);
}

.modal-content h2 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 1.8em;
  padding-right: 50px;
}

.modal-content h4 {
  margin: 20px 0 12px 0;
  color: #667eea;
  font-size: 1.2em;
}

.modal-content ul,
.modal-content ol {
  margin: 0;
  padding-left: 20px;
}

.modal-content li {
  margin-bottom: 6px;
  line-height: 1.5;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.tag {
  display: inline-block;
  background: #e9ecef;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85em;
  color: #495057;
  transition: all 0.2s ease;
}

.tag:hover {
  background: #667eea;
  color: white;
  transform: translateY(-1px);
}

.nutrition-list {
  list-style: none;
  padding-left: 0;
}

.nutrition-list li {
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.nutrition-list li:last-child {
  border-bottom: none;
}

@media (max-width: 768px) {
  .modal-content {
    padding: 20px;
    width: 95%;
    border-radius: 12px;
  }
}
</style>