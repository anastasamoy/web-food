<template>
  <div>
    <header class="header">
      <h1>🍳 Кулинарная книга</h1>
      <p>Просмотр таблиц: рецепты, пользователи, взаимодействия, PP-рецепты</p>
    </header>
    
    <!-- Навигация по вкладкам -->
    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab"
        @click="switchTab(tab)"
        :class="{ active: currentTab === tab }"
      >
        {{ tab }}
      </button>
    </div>

    <div v-if="currentTab === 'Рецепты'" class="tab-content">
      <div class="filters">
        <div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-end;">
          <div style="display:flex; flex-direction:column; min-width:220px;">
            <label>Название рецепта:
              <input v-model="filters.name" @input="fetchRecipes" placeholder="e.g., pizza, chicken..." style="margin-bottom:8px;" />
            </label>
            <label style="margin-top:8px;">⏱️ Время приготовления (минут)
              <div style="display:flex;align-items:center;gap:8px;">
                <input type="range" min="0" max="240" v-model.number="filters.minMinutes" @input="fetchRecipes" style="flex:1;" />
                <span style="min-width:32px;text-align:right;">{{ filters.minMinutes }}</span>
              </div>
            </label>
            <label style="margin-top:8px;">🛒 Количество ингредиентов
              <div style="display:flex;align-items:center;gap:8px;">
                <input type="range" min="1" max="50" v-model.number="filters.minIngredients" @input="fetchRecipes" style="flex:1;" />
                <span style="min-width:32px;text-align:right;">{{ filters.minIngredients }}</span>
              </div>
            </label>
            <label style="margin-top:8px;">🔥 Калории
              <div style="display:flex;align-items:center;gap:8px;">
                <input type="range" min="0" max="2000" v-model.number="filters.minCalories" @input="fetchRecipes" style="flex:1;" />
                <span style="min-width:32px;text-align:right;">{{ filters.minCalories }}</span>
              </div>
            </label>
          </div>
          
          <!-- ФИЛЬТРЫ В ДВУХ КОЛОНКАХ -->
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; width: 100%;">
            <!-- ЛЕВАЯ КОЛОНКА -->
            <div style="display: flex; flex-wrap: wrap; gap: 16px;">
              <!-- Основные категории -->
              <label>
                Тип блюда:
                <select v-model="filters.mealTypes" @change="fetchRecipes" multiple style="min-width:180px; height:90px;">
                  <option v-for="(tags, label) in filtersData.mealType" :key="label" :value="label">{{ label }}</option>
                </select>
              </label>
              <label>
                Кухня:
                <select v-model="filters.cuisines" @change="fetchRecipes" multiple style="min-width:180px; height:90px;">
                  <option v-for="(tags, label) in filtersData.cuisine" :key="label" :value="label">{{ label }}</option>
                </select>
              </label>
              <label>
                Диета:
                <select v-model="filters.diets" @change="fetchRecipes" multiple style="min-width:180px; height:90px;">
                  <option v-for="(tags, label) in filtersData.healthy" :key="label" :value="label">{{ label }}</option>
                </select>
              </label>
              <label>
                Метод приготовления:
                <select v-model="filters.methods" @change="fetchRecipes" multiple style="min-width:180px; height:90px;">
                  <option v-for="(tags, label) in filtersData.cookingMethod" :key="label" :value="label">{{ label }}</option>
                </select>
              </label>
              <label>
                Праздники:
                <select v-model="filters.occasions" @change="fetchRecipes" multiple style="min-width:180px; height:90px;">
                  <option v-for="(tags, label) in filtersData.holidays" :key="label" :value="label">{{ label }}</option>
                </select>
              </label>
              <label>
                Сезон:
                <select v-model="filters.seasons" @change="fetchRecipes" multiple style="min-width:180px; height:90px;">
                  <option v-for="(tags, label) in filtersData.seasonal" :key="label" :value="label">{{ label }}</option>
                </select>
              </label>
              <label>
                Сложность:
                <select v-model="filters.difficulties" @change="fetchRecipes" multiple style="min-width:180px; height:90px;">
                  <option v-for="(tags, label) in filtersData.difficulty" :key="label" :value="label">{{ label }}</option>
                </select>
              </label>
            </div>

            <!-- ПРАВАЯ КОЛОНКА -->
            <div style="display: flex; flex-wrap: wrap; gap: 16px;">
              <!-- Дополнительные категории -->
              <label>
                Ингредиенты:
                <select v-model="filters.ingredients" @change="fetchRecipes" multiple style="min-width:180px; height:90px;">
                  <option v-for="(tags, label) in filtersData.ingredients" :key="label" :value="label">{{ label }}</option>
                </select>
              </label>
              <label>
                Десерты:
                <select v-model="filters.dessertsSweets" @change="fetchRecipes" multiple style="min-width:180px; height:90px;">
                  <option v-for="(tags, label) in filtersData.dessertsSweets" :key="label" :value="label">{{ label }}</option>
                </select>
              </label>
              <label>
                Напитки:
                <select v-model="filters.beverages" @change="fetchRecipes" multiple style="min-width:180px; height:90px;">
                  <option v-for="(tags, label) in filtersData.beverages" :key="label" :value="label">{{ label }}</option>
                </select>
              </label>
              <label>
                Мясо и морепродукты:
                <select v-model="filters.meatSeafood" @change="fetchRecipes" multiple style="min-width:180px; height:90px;">
                  <option v-for="(tags, label) in filtersData.meatSeafood" :key="label" :value="label">{{ label }}</option>
                </select>
              </label>
              
              <!-- НОВЫЕ КАТЕГОРИИ -->
              <label>
                Время приготовления:
                <select v-model="filters.timePreparation" @change="fetchRecipes" multiple style="min-width:180px; height:90px;">
                  <option v-for="(tags, label) in filtersData.timePreparation" :key="label" :value="label">{{ label }}</option>
                </select>
              </label>
              <label>
                Диетические ограничения:
                <select v-model="filters.dietaryRestrictions" @change="fetchRecipes" multiple style="min-width:180px; height:90px;">
                  <option v-for="(tags, label) in filtersData.dietaryRestrictions" :key="label" :value="label">{{ label }}</option>
                </select>
              </label>
              <label>
                Хлеб и выпечка:
                <select v-model="filters.breadsBaking" @change="fetchRecipes" multiple style="min-width:180px; height:90px;">
                  <option v-for="(tags, label) in filtersData.breadsBaking" :key="label" :value="label">{{ label }}</option>
                </select>
              </label>
              <label>
                Особые случаи:
                <select v-model="filters.specialOccasions" @change="fetchRecipes" multiple style="min-width:180px; height:90px;">
                  <option v-for="(tags, label) in filtersData.specialOccasions" :key="label" :value="label">{{ label }}</option>
                </select>
              </label>
            </div>
          </div>
          
          <!-- КНОПКИ ФИЛЬТРОВ, ПАГИНАЦИЯ -->
          <div style="display:flex;align-items:center;gap:16px;margin-top:16px;width:100%;flex-wrap:wrap;">
            <div style="display:flex;align-items:center;gap:8px;">
              <input type="checkbox" v-model="filters.onlyNoName" @change="fetchRecipes" id="onlyNoName" />
              <label for="onlyNoName" style="cursor:pointer;">Показать только без названия</label>
            </div>
            <button @click="clearFilters" style="height:32px;">Сбросить фильтры</button>
            <div style="display:flex;align-items:center;gap:8px;">
              <span style="color:#666;font-size:0.9em;">Показывать по:</span>
              <select v-model="pageSize" @change="changePageSize(Number($event.target.value))" style="height:32px;">
                <option v-for="size in pageSizes" :key="size" :value="size">{{ size }}</option>
              </select>
            </div>
            <span style="color:#666;font-size:0.9em;">Найдено рецептов: {{ totalRecipes }}</span>
            <div v-if="totalPages > 1 || totalRecipes > pageSize" style="display:flex;align-items:center;gap:4px;">
              <button :disabled="currentPage === 1" @click="goToPage(currentPage-1)">&lt;</button>
              <span v-for="page in getPageList()" :key="page">
                <button v-if="page !== '...'" :class="{active: currentPage === page}" @click="goToPage(page)">{{ page }}</button>
                <span v-else style="padding:0 4px;">...</span>
              </span>
              <button :disabled="currentPage === totalPages" @click="goToPage(currentPage+1)">&gt;</button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="loading" class="loading">Загрузка...</div>
      
      <div class="recipes-grid">
        <div v-for="recipe in recipes" :key="recipe.id" class="recipe-card" @click="openRecipe(recipe)">
          <h3>{{ getRecipeName(recipe.name) }}</h3>
          <div class="meta">
            <span>⏱️ {{ recipe.minutes }} мин</span>
            <span>🛒 {{ recipe.n_ingredients }} ингредиентов</span>
          </div>
          <div class="desc">{{ recipe.description?.slice(0, 80) }}...</div>
        </div>
      </div>

      <!-- Модальное окно подробного рецепта -->
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
          <button class="modal-close" @click="closeModal">×</button>
          <h2>{{ getRecipeName(selectedRecipe.name) }}</h2>
          <div class="meta">
            <span>⏱️ {{ selectedRecipe.minutes }} мин</span>
            <span>🛒 {{ selectedRecipe.n_ingredients }} ингредиентов</span>
          </div>
          <div class="desc">{{ selectedRecipe.description }}</div>
          <div v-if="selectedRecipe.ingredients">
            <h4>Ингредиенты:</h4>
            <ul>
              <li v-for="(ing, idx) in parseTags(selectedRecipe.ingredients)" :key="idx">{{ ing }}</li>
            </ul>
          </div>
          <div v-if="selectedRecipe.tags">
            <h4>Категории/теги:</h4>
            <div class="tags">
              <span v-for="tag in parseTags(selectedRecipe.tags)" :key="tag" class="tag">{{ tag }}</span>
            </div>
          </div>
          <div v-if="selectedRecipe.steps">
            <h4>Как готовить:</h4>
            <ol>
              <li v-for="(step, idx) in parseTags(selectedRecipe.steps)" :key="idx">{{ step }}</li>
            </ol>
          </div>
          <div v-if="selectedRecipe.nutrition">
            <h4>Пищевая ценность:</h4>
            <ul style="padding-left:18px;">
              <li v-for="(nutr, idx) in parseTags(selectedRecipe.nutrition)" :key="idx">
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
    </div>  

    <!-- Другие вкладки -->
    <div v-if="currentTab !== 'Рецепты'" class="tab-content">
      <p>Вкладка "{{ currentTab }}" в разработке</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { api } from './api.js';
import * as filtersData from './filters.js';

// Вкладки
const tabs = ['Рецепты', 'Пользователи', 'PP-рецепты', 'Взаимодействия'];
const currentTab = ref('Рецепты');

// Состояния
const loading = ref(false);
const recipes = ref([]);
const totalRecipes = ref(0);
const pageSizes = [4, 8, 16, 32, 64, 128];
const pageSize = ref(8);
const currentPage = ref(1);
const totalPages = ref(1);

// Модальное окно для подробного рецепта
const showModal = ref(false);
const selectedRecipe = ref({});

function openRecipe(recipe) {
  selectedRecipe.value = recipe;
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
  selectedRecipe.value = {};
}

function getRecipeName(name) {
  if (!name || /^-+$/.test(name.trim())) {
    return 'Без названия';
  }
  return name;
}

// Подписи для nutrition
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

// Фильтры
const filters = reactive({
  name: '',
  minMinutes: '',
  minIngredients: '',
  minCalories: '',
  mealTypes: [],
  cuisines: [],
  diets: [],
  methods: [],
  occasions: [],
  seasons: [],
  difficulties: [],
  ingredients: [],
  dessertsSweets: [],
  beverages: [],
  meatSeafood: [],
  timePreparation: [],
  dietaryRestrictions: [],
  breadsBaking: [],
  specialOccasions: [],
  onlyNoName: false
});

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

function collectTags(selected, dict) {
  const tags = selected.flatMap(key => dict[key] || []);
  return Array.from(new Set(tags));
}

async function fetchRecipes() {
  loading.value = true;
  const params = {};
  if (filters.name) params.name = filters.name;
  // Время приготовления
  if (filters.minMinutes !== '' && filters.minMinutes !== undefined) params.min_minutes = 0;
  if (filters.minMinutes !== '' && filters.minMinutes !== undefined && filters.minMinutes < 240) params.max_minutes = filters.minMinutes;
  // Количество ингредиентов
  if (filters.minIngredients !== '' && filters.minIngredients !== undefined) params.min_ingredients = 1;
  if (filters.minIngredients !== '' && filters.minIngredients !== undefined && filters.minIngredients < 50) params.max_ingredients = filters.minIngredients;
  // Калории
  if (filters.minCalories !== '' && filters.minCalories !== undefined) params.min_calories = 0;
  if (filters.minCalories !== '' && filters.minCalories !== undefined && filters.minCalories < 2000) params.max_calories = filters.minCalories;
  // Пагинация
  params.limit = pageSize.value;
  params.offset = (currentPage.value - 1) * pageSize.value;
  // Все фильтры по тегам
  const tagFilters = [
    { key: 'mealTypes', dict: filtersData.mealType, param: 'meal_types' },
    { key: 'cuisines', dict: filtersData.cuisine, param: 'cuisines' },
    { key: 'diets', dict: filtersData.healthy, param: 'diets' },
    { key: 'methods', dict: filtersData.cookingMethod, param: 'methods' },
    { key: 'occasions', dict: filtersData.holidays, param: 'occasions' },
    { key: 'seasons', dict: filtersData.seasonal, param: 'seasons' },
    { key: 'difficulties', dict: filtersData.difficulty, param: 'difficulties' },
    { key: 'ingredients', dict: filtersData.ingredients, param: 'ingredients' },
    { key: 'dessertsSweets', dict: filtersData.dessertsSweets, param: 'desserts_sweets' },
    { key: 'beverages', dict: filtersData.beverages, param: 'beverages' },
    { key: 'meatSeafood', dict: filtersData.meatSeafood, param: 'meat_seafood' },
    { key: 'timePreparation', dict: filtersData.timePreparation, param: 'time_preparation' },
    { key: 'dietaryRestrictions', dict: filtersData.dietaryRestrictions, param: 'dietary_restrictions' },
    { key: 'breadsBaking', dict: filtersData.breadsBaking, param: 'breads_baking' },
    { key: 'specialOccasions', dict: filtersData.specialOccasions, param: 'special_occasions' },
  ];
  tagFilters.forEach(({ key, dict, param }) => {
    const tags = collectTags(filters[key], dict);
    if (tags.length) params[param] = tags.join(',');
  });
  try {
    const data = await api.getRecipes(params);
    let result = data.recipes || data || [];
    totalRecipes.value = data.total || result.length;
    totalPages.value = Math.max(1, Math.ceil(totalRecipes.value / pageSize.value));
    if (filters.onlyNoName) {
      result = result.filter(r => !r.name || /^-+$/.test(r.name.trim()));
    }
    recipes.value = result;
  } catch (e) {
    console.error('Error fetching recipes:', e);
    recipes.value = [];
    totalRecipes.value = 0;
    totalPages.value = 1;
  }
  loading.value = false;
}

function changePageSize(size) {
  pageSize.value = size;
  currentPage.value = 1;
  fetchRecipes();
}

function goToPage(page) {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
  fetchRecipes();
}

function clearFilters() {
  Object.keys(filters).forEach(key => {
    if (Array.isArray(filters[key])) {
      filters[key] = [];
    } else {
      filters[key] = '';
    }
  });
  currentPage.value = 1;
  fetchRecipes();
}

function switchTab(tab) {
  currentPage.value = 1;
  currentTab.value = tab;
  if(tab === 'Рецепты') {
    fetchRecipes();
  }
}

function getPageList() {
  const pages = [];
  if (totalPages.value <= 9) {
    for (let i = 1; i <= totalPages.value; i++) pages.push(i);
  } else {
    if (currentPage.value <= 5) {
      pages.push(1,2,3,4,5,6,'...',totalPages.value);
    } else if (currentPage.value >= totalPages.value - 4) {
      pages.push(1,'...',totalPages.value-5,totalPages.value-4,totalPages.value-3,totalPages.value-2,totalPages.value-1,totalPages.value);
    } else {
      pages.push(1,'...',currentPage.value-1,currentPage.value,currentPage.value+1,'...',totalPages.value);
    }
  }
  return pages;
}

// Загрузка рецептов при монтировании
onMounted(() => {
  fetchRecipes();
});
</script>

<style scoped>
/* Стили остаются без изменений */
.tabs {
  margin: 20px 0;
}

.tabs button {
  padding: 10px 20px;
  margin-right: 10px;
  border: 1px solid #ccc;
  background: white;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.tabs button.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.tabs button:hover {
  background: #f8f9fa;
}

.tabs button.active:hover {
  background: #0056b3;
}

.loading {
  text-align: center;
  padding: 20px;
  font-size: 1.2em;
  color: #666;
}

.recipes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.recipe-card {
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.recipe-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  border-color: #007bff;
}

.meta {
  display: flex;
  justify-content: space-between;
  margin: 10px 0;
  font-size: 0.9em;
  color: #666;
}

.desc {
  color: #555;
  line-height: 1.4;
}

/* Стили для модального окна */
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
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 30px;
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.modal-close {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s ease;
}

.modal-close:hover {
  background: #f0f0f0;
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
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85em;
  color: #495057;
}

@media (max-width: 768px) {
  .modal-content {
    padding: 20px;
    width: 95%;
  }
}
</style>