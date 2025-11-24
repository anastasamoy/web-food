import { ref, onMounted } from 'vue';
import { api } from '../api.js';

export function useRecipes() {
  const loading = ref(false);
  const recipes = ref([]);
  const totalRecipes = ref(0);
  const pageSizes = [4, 8, 16, 32, 64, 128];
  const pageSize = ref(8);
  const currentPage = ref(1);
  const totalPages = ref(1);
  const showModal = ref(false);
  const selectedRecipe = ref({});

  // Debounce функция для поиска
  let debounceTimer = null;
  const debouncedFetchRecipes = (fetchFunction) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      fetchFunction();
    }, 300);
  };

  const openRecipe = (recipe) => {
    selectedRecipe.value = recipe;
    showModal.value = true;
  };

  const closeModal = () => {
    showModal.value = false;
    selectedRecipe.value = {};
  };

  const changePageSize = (size, fetchFunction) => {
    pageSize.value = size;
    currentPage.value = 1;
    fetchFunction();
  };

  const goToPage = (page, fetchFunction) => {
    if (page < 1 || page > totalPages.value) return;
    currentPage.value = page;
    fetchFunction();
  };

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
    debouncedFetchRecipes,
    openRecipe,
    closeModal,
    changePageSize,
    goToPage
  };
}