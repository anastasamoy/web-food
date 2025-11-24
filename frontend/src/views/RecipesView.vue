<template>
  <div class="tab-content">
    <RecipeFilters
        :filters="filters"
        :filters-data="filtersData"
        :has-active-filters="hasActiveFilters"
        :active-category-filters="activeCategoryFilters"
        :page-sizes="pageSizes"
        :page-size="pageSize"
        :current-page="currentPage"
        :total-pages="totalPages"
        :total-recipes="totalRecipes"
        @fetch-recipes="fetchRecipes"
        @change-page-size="changePageSize"
        @go-to-page="goToPage"
        @clear-filter="clearFilter"
        @clear-category-filter="clearCategoryFilter"
        @clear-all-filters="clearAllFilters"
        @debounced-fetch="debouncedFetchRecipes"
        @update-filter="updateFilter"
        @update-multi-select="updateMultiSelect"
    />

    <RecipeGrid
      :loading="loading"
      :recipes="recipes"
      @recipe-click="openRecipe"
    />

    <RecipeModal 
      v-if="showModal"
      :recipe="selectedRecipe"
      @close="closeModal"
    />
  </div>
</template>

<script>
import { onMounted } from 'vue';
import { api } from '../api.js';
import { useRecipes } from '../composables/useRecipes.js';
import { useFilters } from '../composables/useFilters.js';
import RecipeFilters from '../components/recipes/RecipeFilters.vue';
import RecipeGrid from '../components/recipes/RecipeGrid.vue';
import RecipeModal from '../components/common/RecipeModal.vue';

export default {
  name: 'RecipesView',
  components: {
    RecipeFilters,
    RecipeGrid,
    RecipeModal
  },
  setup() {
    const {
      loading,
      recipes,
      totalRecipes,
      pageSizes,
      pageSize,
      currentPage,
      totalPages,
      showModal,
      selectedRecipe,
      debouncedFetchRecipes: debouncedFetch,
      openRecipe,
      closeModal,
      changePageSize: changePageSizeBase,
      goToPage: goToPageBase
    } = useRecipes();

    const {
      filters,
      filtersData,
      hasActiveFilters,
      activeCategoryFilters,
      getCategoryLabel,
      clearFilter: clearFilterBase,
      clearCategoryFilter: clearCategoryFilterBase,
      clearAllFilters: clearAllFiltersBase,
      buildApiParams
    } = useFilters();

    const fetchRecipes = async () => {
      loading.value = true;
      const params = buildApiParams(currentPage.value, pageSize.value);
      
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
    };

    const changePageSize = (size) => {
      changePageSizeBase(size, fetchRecipes);
    };

    const goToPage = (page) => {
      goToPageBase(page, fetchRecipes);
    };

    const clearFilter = (filterKey) => {
      clearFilterBase(filterKey, fetchRecipes);
    };

    const clearCategoryFilter = (categoryKey) => {
      clearCategoryFilterBase(categoryKey, fetchRecipes);
    };

    const clearAllFilters = () => {
      currentPage.value = 1;
      clearAllFiltersBase(fetchRecipes);
    };

    const debouncedFetchRecipes = () => {
      debouncedFetch(fetchRecipes);
    };
    const updateFilter = ({ key, value }) => {
    filters[key] = value;
    };

    const updateMultiSelect = ({ key, value }) => {
    filters[key] = value;
    };


    onMounted(() => {
      fetchRecipes();
    });

    return {
      loading,
      recipes,
      totalRecipes,
      pageSizes,
      pageSize,
      currentPage,
      totalPages,
      showModal,
      selectedRecipe,
      filters,
      filtersData,
      hasActiveFilters,
      activeCategoryFilters,
      fetchRecipes,
      changePageSize,
      goToPage,
      clearFilter,
      clearCategoryFilter,
      clearAllFilters,
      debouncedFetchRecipes,
      openRecipe,
      closeModal,
      getCategoryLabel,
      updateFilter,
      updateMultiSelect,
    };
  }
}
</script>