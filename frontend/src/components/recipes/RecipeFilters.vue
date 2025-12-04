<template>
  <div class="filters">
    <div style="display:flex; flex-wrap:wrap; gap:24px; align-items:flex-end;">
      <div style="display:flex; flex-direction:column; min-width:220px;">
        <label>Názov receptu:
          <input 
            :value="filters.name" 
            @input="updateFilter('name', $event.target.value)"
            placeholder="e.g., pizza, chicken..." 
            style="margin-bottom:8px;" 
          />
        </label>
        
        <label style="margin-top:8px;">⏱️Čas prípravy (minút)
          <div style="display:flex;align-items:center;gap:8px;">
            <span>0</span>
            <input 
              type="range" 
              min="0" 
              max="240" 
              :value="filters.maxMinutes" 
              @input="updateFilter('maxMinutes', Number($event.target.value))" 
              style="flex:1;" 
            />
            <span style="min-width:32px;text-align:right;">{{ filters.maxMinutes }}</span>
          </div>
        </label>
        
        <label style="margin-top:8px;">🛒 Množstvo ingrediencií
          <div style="display:flex;align-items:center;gap:8px;">
            <span>1</span>
            <input 
              type="range" 
              min="1" 
              max="50" 
              :value="filters.maxIngredients" 
              @input="updateFilter('maxIngredients', Number($event.target.value))" 
              style="flex:1;" 
            />
            <span style="min-width:32px;text-align:right;">{{ filters.maxIngredients }}</span>
          </div>
        </label>
        
        <label style="margin-top:8px;">🔥 Kalórie
          <div style="display:flex;align-items:center;gap:8px;">
            <span>0</span>
            <input 
              type="range" 
              min="0" 
              max="2000" 
              :value="filters.maxCalories" 
              @input="updateFilter('maxCalories', Number($event.target.value))" 
              style="flex:1;" 
            />
            <span style="min-width:32px;text-align:right;">{{ filters.maxCalories }}</span>
          </div>
        </label>
      </div>
      
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; width: 100%;">
        <div style="display: flex; flex-wrap: wrap; gap: 16px;">
          <label>
            Typ jedla:
            <select 
              :value="filters.mealTypes" 
              @change="updateMultiSelect('mealTypes', $event.target)" 
              multiple 
              style="min-width:180px; height:90px;"
            >
              <option v-for="(tags, label) in filtersData.mealType" :key="label" :value="label">{{ label }}</option>
            </select>
          </label>
          <label>
            Kuchyňa:
            <select 
              :value="filters.cuisines" 
              @change="updateMultiSelect('cuisines', $event.target)" 
              multiple 
              style="min-width:180px; height:90px;"
            >
              <option v-for="(tags, label) in filtersData.cuisine" :key="label" :value="label">{{ label }}</option>
            </select>
          </label>
          <label>
            Strava:
            <select 
              :value="filters.diets" 
              @change="updateMultiSelect('diets', $event.target)" 
              multiple 
              style="min-width:180px; height:90px;"
            >
              <option v-for="(tags, label) in filtersData.healthy" :key="label" :value="label">{{ label }}</option>
            </select>
          </label>
          <label>
            Spôsob prípravy:
            <select 
              :value="filters.methods" 
              @change="updateMultiSelect('methods', $event.target)" 
              multiple 
              style="min-width:180px; height:90px;"
            >
              <option v-for="(tags, label) in filtersData.cookingMethod" :key="label" :value="label">{{ label }}</option>
            </select>
          </label>
          <label>
            Sviatky:
            <select 
              :value="filters.occasions" 
              @change="updateMultiSelect('occasions', $event.target)" 
              multiple 
              style="min-width:180px; height:90px;"
            >
              <option v-for="(tags, label) in filtersData.holidays" :key="label" :value="label">{{ label }}</option>
            </select>
          </label>
          <label>
            Sezóna:
            <select 
              :value="filters.seasons" 
              @change="updateMultiSelect('seasons', $event.target)" 
              multiple 
              style="min-width:180px; height:90px;"
            >
              <option v-for="(tags, label) in filtersData.seasonal" :key="label" :value="label">{{ label }}</option>
            </select>
          </label>
          <label>
            Zložitosť:
            <select 
              :value="filters.difficulties" 
              @change="updateMultiSelect('difficulties', $event.target)" 
              multiple 
              style="min-width:180px; height:90px;"
            >
              <option v-for="(tags, label) in filtersData.difficulty" :key="label" :value="label">{{ label }}</option>
            </select>
          </label>
        </div>

        <div style="display: flex; flex-wrap: wrap; gap: 16px;">
          <label>
            Zložky:
            <select 
              :value="filters.ingredients" 
              @change="updateMultiSelect('ingredients', $event.target)" 
              multiple 
              style="min-width:180px; height:90px;"
            >
              <option v-for="(tags, label) in filtersData.ingredients" :key="label" :value="label">{{ label }}</option>
            </select>
          </label>
          <label>
            Dezerty:
            <select 
              :value="filters.dessertsSweets" 
              @change="updateMultiSelect('dessertsSweets', $event.target)" 
              multiple 
              style="min-width:180px; height:90px;"
            >
              <option v-for="(tags, label) in filtersData.dessertsSweets" :key="label" :value="label">{{ label }}</option>
            </select>
          </label>
          <label>
            Nápoje:
            <select 
              :value="filters.beverages" 
              @change="updateMultiSelect('beverages', $event.target)" 
              multiple 
              style="min-width:180px; height:90px;"
            >
              <option v-for="(tags, label) in filtersData.beverages" :key="label" :value="label">{{ label }}</option>
            </select>
          </label>
          <label>
            Mäso a morské plody:
            <select 
              :value="filters.meatSeafood" 
              @change="updateMultiSelect('meatSeafood', $event.target)" 
              multiple 
              style="min-width:180px; height:90px;"
            >
              <option v-for="(tags, label) in filtersData.meatSeafood" :key="label" :value="label">{{ label }}</option>
            </select>
          </label>
          
          <label>
            Čas prípravy:
            <select 
              :value="filters.timePreparation" 
              @change="updateMultiSelect('timePreparation', $event.target)" 
              multiple 
              style="min-width:180px; height:90px;"
            >
              <option v-for="(tags, label) in filtersData.timePreparation" :key="label" :value="label">{{ label }}</option>
            </select>
          </label>
          <label>
            Diétne obmedzenia:
            <select 
              :value="filters.dietaryRestrictions" 
              @change="updateMultiSelect('dietaryRestrictions', $event.target)" 
              multiple 
              style="min-width:180px; height:90px;"
            >
              <option v-for="(tags, label) in filtersData.dietaryRestrictions" :key="label" :value="label">{{ label }}</option>
            </select>
          </label>
          <label>
            Chlieb a pečivo:
            <select 
              :value="filters.breadsBaking" 
              @change="updateMultiSelect('breadsBaking', $event.target)" 
              multiple 
              style="min-width:180px; height:90px;"
            >
              <option v-for="(tags, label) in filtersData.breadsBaking" :key="label" :value="label">{{ label }}</option>
            </select>
          </label>
          <label>
            Osobitné prípady:
            <select 
              :value="filters.specialOccasions" 
              @change="updateMultiSelect('specialOccasions', $event.target)" 
              multiple 
              style="min-width:180px; height:90px;"
            >
              <option v-for="(tags, label) in filtersData.specialOccasions" :key="label" :value="label">{{ label }}</option>
            </select>
          </label>
        </div>
      </div>
      
      <div v-if="hasActiveFilters" class="selected-filters">
        <h4>🎯 Aktívne filtre:</h4>
        <div class="selected-filters-list">
          <span v-if="filters.maxMinutes < 240" class="selected-filter-item">
            ⏱️ Do {{ filters.maxMinutes }} min
            <button @click="clearFilter('maxMinutes')" class="filter-remove">×</button>
          </span>
          <span v-if="filters.maxIngredients < 50" class="selected-filter-item">
            🛒 Do {{ filters.maxIngredients }} ingrediencie
            <button @click="clearFilter('maxIngredients')" class="filter-remove">×</button>
          </span>
          <span v-if="filters.maxCalories < 2000" class="selected-filter-item">
            🔥 Do {{ filters.maxCalories }} kalórií
            <button @click="clearFilter('maxCalories')" class="filter-remove">×</button>
          </span>
          
          <span v-for="category in activeCategoryFilters" :key="category.key" class="selected-filter-item">
            {{ getCategoryLabel(category.key) }}: {{ category.selected.join(', ') }}
            <button @click="clearCategoryFilter(category.key)" class="filter-remove">×</button>
          </span>
          
          <span v-if="filters.onlyNoName" class="selected-filter-item">
            📝 Len bez názvu
            <button @click="clearFilter('onlyNoName')" class="filter-remove">×</button>
          </span>
        </div>
        
        <button @click="clearAllFilters" class="clear-all-filters-btn">
          ✕ Vymazať všetky filtre
        </button>
      </div>
      
      <div style="display:flex;align-items:center;gap:16px;margin-top:16px;width:100%;flex-wrap:wrap;">
        <div style="display:flex;align-items:center;gap:8px;">
          <input 
            type="checkbox" 
            :checked="filters.onlyNoName" 
            @change="updateFilter('onlyNoName', $event.target.checked)" 
            id="onlyNoName" 
          />
          <label for="onlyNoName" style="cursor:pointer;">Zobraziť len bez názvu</label>
        </div>
        <div style="display:flex;align-items:center;gap:8px;">
          <span style="color:#666;font-size:0.9em;">Zobraziť podľa:</span>
          <select 
            :value="pageSize" 
            @change="changePageSize($event.target.value)" 
            style="height:32px;"
          >
            <option v-for="size in pageSizes" :key="size" :value="size">{{ size }}</option>
          </select>
        </div>
        <span style="color:#666;font-size:0.9em;">Nájdených receptov: {{ totalRecipes }}</span>
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
</template>

<script>
import Pagination from '../common/Pagination.vue';

export default {
  name: 'RecipeFilters',
  components: {
    Pagination
  },
  props: {
    filters: Object,
    filtersData: Object,
    hasActiveFilters: Boolean,
    activeCategoryFilters: Array,
    pageSizes: Array,
    pageSize: Number,
    currentPage: Number,
    totalPages: Number,
    totalRecipes: Number
  },
  emits: [
    'fetch-recipes',
    'change-page-size',
    'go-to-page',
    'clear-filter',
    'clear-category-filter',
    'clear-all-filters',
    'debounced-fetch',
    'update-filter',
    'update-multi-select'
  ],
  methods: {
    fetchRecipes() {
      this.$emit('fetch-recipes');
    },
    
    changePageSize(size) {
      this.$emit('change-page-size', Number(size));
    },
    
    goToPage(page) {
      this.$emit('go-to-page', page);
    },
    
    clearFilter(filterKey) {
      this.$emit('clear-filter', filterKey);
    },
    
    clearCategoryFilter(categoryKey) {
      this.$emit('clear-category-filter', categoryKey);
    },
    
    clearAllFilters() {
      this.$emit('clear-all-filters');
    },
    
    debouncedFetch() {
      this.$emit('debounced-fetch');
    },
    
    updateFilter(key, value) {
      this.$emit('update-filter', { key, value });
      if (key === 'name') {
        this.debouncedFetch();
      } else {
        this.fetchRecipes();
      }
    },
    
    updateMultiSelect(key, selectElement) {
      const selectedOptions = Array.from(selectElement.selectedOptions)
        .map(option => option.value);
      this.$emit('update-multi-select', { key, value: selectedOptions });
      this.fetchRecipes();
    },
    
    getCategoryLabel(key) {
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
  }
}
</script>