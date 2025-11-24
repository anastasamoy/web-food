import { reactive, computed } from 'vue';
import * as filtersData from '../filters.js';

export function useFilters() {
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
  const getCategoryLabel = (key) => {
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
  };

  const clearFilter = (filterKey, fetchFunction) => {
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
    fetchFunction();
  };

  const clearCategoryFilter = (categoryKey, fetchFunction) => {
    filters[categoryKey] = [];
    fetchFunction();
  };

  const clearAllFilters = (fetchFunction) => {
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
    fetchFunction();
  };

  const collectTags = (selected, dict) => {
    const tags = selected.flatMap(key => dict[key] || []);
    return Array.from(new Set(tags));
  };

  const buildApiParams = (currentPage, pageSize) => {
    const params = {};
    if (filters.name) params.name = filters.name;
    
    if (filters.maxMinutes < 240) {
      params.max_minutes = filters.maxMinutes;
    }
    
    if (filters.maxIngredients < 50) {
      params.max_ingredients = filters.maxIngredients;
    }
    
    if (filters.maxCalories < 2000) {
      params.max_calories = filters.maxCalories;
    }
    
    // Пагинация
    params.limit = pageSize;
    params.offset = (currentPage - 1) * pageSize;
    
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

    return params;
  };

  return {
    filters,
    filtersData,
    hasActiveFilters,
    activeCategoryFilters,
    getCategoryLabel,
    clearFilter,
    clearCategoryFilter,
    clearAllFilters,
    buildApiParams
  };
}