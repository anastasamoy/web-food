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
              <input v-model="filters.name" @input="debouncedFetchRecipes" placeholder="e.g., pizza, chicken..." style="margin-bottom:8px;" />
            </label>
            
            <!-- ⏱️ ФИЛЬТРЫ ПО ВРЕМЕНИ ПРИГОТОВЛЕНИЯ -->
            <label style="margin-top:8px;">⏱️ Время приготовления (минут)
              <div style="display:flex;align-items:center;gap:8px;">
                <span>0</span>
                <input type="range" min="0" max="240" v-model.number="filters.maxMinutes" @input="fetchRecipes" style="flex:1;" />
                <span style="min-width:32px;text-align:right;">{{ filters.maxMinutes }}</span>
              </div>
            </label>
            
            <!-- 🛒 ФИЛЬТРЫ ПО КОЛИЧЕСТВУ ИНГРЕДИЕНТОВ -->
            <label style="margin-top:8px;">🛒 Количество ингредиентов
              <div style="display:flex;align-items:center;gap:8px;">
                <span>1</span>
                <input type="range" min="1" max="50" v-model.number="filters.maxIngredients" @input="fetchRecipes" style="flex:1;" />
                <span style="min-width:32px;text-align:right;">{{ filters.maxIngredients }}</span>
              </div>
            </label>
            
            <!-- 🔥 ФИЛЬТРЫ ПО КАЛОРИЯМ -->
            <label style="margin-top:8px;">🔥 Калории
              <div style="display:flex;align-items:center;gap:8px;">
                <span>0</span>
                <input type="range" min="0" max="2000" v-model.number="filters.maxCalories" @input="fetchRecipes" style="flex:1;" />
                <span style="min-width:32px;text-align:right;">{{ filters.maxCalories }}</span>
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
          
          <!-- ВЫБРАННЫЕ ФИЛЬТРЫ -->
          <div v-if="hasActiveFilters" class="selected-filters">
            <h4>🎯 Активные фильтры:</h4>
            <div class="selected-filters-list">
              <!-- Фильтры по диапазонам -->
              <span v-if="filters.maxMinutes < 240" class="selected-filter-item">
                ⏱️ До {{ filters.maxMinutes }} мин
                <button @click="clearFilter('maxMinutes')" class="filter-remove">×</button>
              </span>
              <span v-if="filters.maxIngredients < 50" class="selected-filter-item">
                🛒 До {{ filters.maxIngredients }} ингредиентов
                <button @click="clearFilter('maxIngredients')" class="filter-remove">×</button>
              </span>
              <span v-if="filters.maxCalories < 2000" class="selected-filter-item">
                🔥 До {{ filters.maxCalories }} калорий
                <button @click="clearFilter('maxCalories')" class="filter-remove">×</button>
              </span>
              
              <!-- Фильтры по категориям -->
              <span v-for="category in activeCategoryFilters" :key="category.key" class="selected-filter-item">
                {{ getCategoryLabel(category.key) }}: {{ category.selected.join(', ') }}
                <button @click="clearCategoryFilter(category.key)" class="filter-remove">×</button>
              </span>
              
              <!-- Фильтр "только без названия" -->
              <span v-if="filters.onlyNoName" class="selected-filter-item">
                📝 Только без названия
                <button @click="clearFilter('onlyNoName')" class="filter-remove">×</button>
              </span>
            </div>
            
            <!-- КНОПКА ОЧИСТКИ ВСЕХ ФИЛЬТРОВ -->
            <button @click="clearAllFilters" class="clear-all-filters-btn">
              ✕ Очистить все фильтры
            </button>
          </div>
          
          <!-- КНОПКИ ФИЛЬТРОВ, ПАГИНАЦИЯ -->
          <div style="display:flex;align-items:center;gap:16px;margin-top:16px;width:100%;flex-wrap:wrap;">
            <div style="display:flex;align-items:center;gap:8px;">
              <input type="checkbox" v-model="filters.onlyNoName" @change="fetchRecipes" id="onlyNoName" />
              <label for="onlyNoName" style="cursor:pointer;">Показать только без названия</label>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
              <span style="color:#666;font-size:0.9em;">Показывать по:</span>
              <select v-model="pageSize" @change="changePageSize(Number($event.target.value))" style="height:32px;">
                <option v-for="size in pageSizes" :key="size" :value="size">{{ size }}</option>
              </select>
            </div>
            <span style="color:#666;font-size:0.9em;">Найдено рецептов: {{ totalRecipes }}</span>
            <Pagination 
              :current-page="currentPage"
              :total-pages="totalPages"
              :total-recipes="totalRecipes"
              :page-size="pageSize"
              @page-change="goToPage"
            />
          </div>
        </div>
      </div>

      <div v-if="loading" class="loading">Загрузка...</div>
      <div class="recipes-grid">
        <RecipeCard 
          v-for="recipe in recipes" 
          :key="recipe.id" 
          :recipe="recipe"
          @click="openRecipe(recipe)"
        />
      </div>
      <div v-if="!loading && recipes.length === 0" class="no-results">
        <p>😔 Рецепты не найдены</p>
        <p>Попробуйте изменить фильтры поиска</p>
      </div>

      <RecipeModal 
        v-if="showModal"
        :recipe="selectedRecipe"
        @close="closeModal"
      />
        
    </div>  

    <!-- Другие вкладки -->
    <div v-if="currentTab !== 'Рецепты'" class="tab-content">
      <p>Вкладка "{{ currentTab }}" в разработке</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { api } from './api.js';
import * as filtersData from './filters.js';


import Pagination from './components/Pagination.vue';
import RecipeCard from './components/RecipeCard.vue';
import RecipeModal from './components/RecipeModal.vue';

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

// Debounce функция для поиска
let debounceTimer = null;
const debouncedFetchRecipes = () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    fetchRecipes();
  }, 300);
};

function openRecipe(recipe) {
  selectedRecipe.value = recipe;
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
  selectedRecipe.value = {};
}





// Фильтры
const filters = reactive({
  name: '',
  maxMinutes: 240,
  maxIngredients: 50,
  maxCalories: 2000,
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

// Вычисляемые свойства для активных фильтров
const hasActiveFilters = computed(() => {
  return filters.maxMinutes < 240 || 
         filters.maxIngredients < 50 || 
         filters.maxCalories < 2000 ||
         filters.mealTypes.length > 0 ||
         filters.cuisines.length > 0 ||
         filters.diets.length > 0 ||
         filters.methods.length > 0 ||
         filters.occasions.length > 0 ||
         filters.seasons.length > 0 ||
         filters.difficulties.length > 0 ||
         filters.ingredients.length > 0 ||
         filters.dessertsSweets.length > 0 ||
         filters.beverages.length > 0 ||
         filters.meatSeafood.length > 0 ||
         filters.timePreparation.length > 0 ||
         filters.dietaryRestrictions.length > 0 ||
         filters.breadsBaking.length > 0 ||
         filters.specialOccasions.length > 0 ||
         filters.onlyNoName;
});

const activeCategoryFilters = computed(() => {
  const categories = [
    { key: 'mealTypes', label: 'Тип блюда', selected: filters.mealTypes },
    { key: 'cuisines', label: 'Кухня', selected: filters.cuisines },
    { key: 'diets', label: 'Диета', selected: filters.diets },
    { key: 'methods', label: 'Метод приготовления', selected: filters.methods },
    { key: 'occasions', label: 'Праздники', selected: filters.occasions },
    { key: 'seasons', label: 'Сезон', selected: filters.seasons },
    { key: 'difficulties', label: 'Сложность', selected: filters.difficulties },
    { key: 'ingredients', label: 'Ингредиенты', selected: filters.ingredients },
    { key: 'dessertsSweets', label: 'Десерты', selected: filters.dessertsSweets },
    { key: 'beverages', label: 'Напитки', selected: filters.beverages },
    { key: 'meatSeafood', label: 'Мясо и морепродукты', selected: filters.meatSeafood },
    { key: 'timePreparation', label: 'Время приготовления', selected: filters.timePreparation },
    { key: 'dietaryRestrictions', label: 'Диетические ограничения', selected: filters.dietaryRestrictions },
    { key: 'breadsBaking', label: 'Хлеб и выпечка', selected: filters.breadsBaking },
    { key: 'specialOccasions', label: 'Особые случаи', selected: filters.specialOccasions }
  ];
  
  return categories.filter(cat => cat.selected.length > 0);
});

// Функции для работы с фильтрами
function getCategoryLabel(key) {
  const labels = {
    mealTypes: 'Тип блюда',
    cuisines: 'Кухня',
    diets: 'Диета',
    methods: 'Метод приготовления',
    occasions: 'Праздники',
    seasons: 'Сезон',
    difficulties: 'Сложность',
    ingredients: 'Ингредиенты',
    dessertsSweets: 'Десерты',
    beverages: 'Напитки',
    meatSeafood: 'Мясо и морепродукты',
    timePreparation: 'Время приготовления',
    dietaryRestrictions: 'Диетические ограничения',
    breadsBaking: 'Хлеб и выпечка',
    specialOccasions: 'Особые случаи'
  };
  return labels[key] || key;
}

function clearFilter(filterKey) {
  if (filterKey === 'maxMinutes') {
    filters[filterKey] = 240;
  } else if (filterKey === 'maxIngredients') {
    filters[filterKey] = 50;
  } else if (filterKey === 'maxCalories') {
    filters[filterKey] = 2000;
  } else if (filterKey === 'onlyNoName') {
    filters[filterKey] = false;
  } else {
    filters[filterKey] = '';
  }
  fetchRecipes();
}

function clearCategoryFilter(categoryKey) {
  filters[categoryKey] = [];
  fetchRecipes();
}

function clearAllFilters() {
  Object.keys(filters).forEach(key => {
    if (Array.isArray(filters[key])) {
      filters[key] = [];
    } else if (key === 'maxMinutes') {
      filters[key] = 240;
    } else if (key === 'maxIngredients') {
      filters[key] = 50;
    } else if (key === 'maxCalories') {
      filters[key] = 2000;
    } else if (key === 'onlyNoName') {
      filters[key] = false;
    } else {
      filters[key] = '';
    }
  });
  currentPage.value = 1;
  fetchRecipes();
}



function collectTags(selected, dict) {
  const tags = selected.flatMap(key => dict[key] || []);
  return Array.from(new Set(tags));
}

async function fetchRecipes() {
  loading.value = true;
  const params = {};
  if (filters.name) params.name = filters.name;
  
  // ⏱️ ФИЛЬТРЫ ПО ВРЕМЕНИ ПРИГОТОВЛЕНИЯ
  if (filters.maxMinutes < 240) {
    params.max_minutes = filters.maxMinutes;
  }
  
  // 🛒 ФИЛЬТРЫ ПО КОЛИЧЕСТВУ ИНГРЕДИЕНТОВ
  if (filters.maxIngredients < 50) {
    params.max_ingredients = filters.maxIngredients;
  }
  
  // 🔥 ФИЛЬТРЫ ПО КАЛОРИЯМ
  if (filters.maxCalories < 2000) {
    params.max_calories = filters.maxCalories;
  }
  
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

function switchTab(tab) {
  currentPage.value = 1;
  currentTab.value = tab;
  if(tab === 'Рецепты') {
    fetchRecipes();
  }
}

// Загрузка рецептов при монтировании
onMounted(() => {
  fetchRecipes();
});
</script>
<style scoped src="./styles/app.css"></style>