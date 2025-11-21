<template>
  <div v-if="totalPages > 1" class="pagination">
    <button :disabled="currentPage === 1" @click="$emit('page-change', currentPage - 1)" class="pagination-btn">
      &lt;
    </button>
    
    <button 
      v-for="page in visiblePages" 
      :key="page"
      :class="{ active: currentPage === page }" 
      @click="$emit('page-change', page)" 
      class="pagination-btn"
    >
      {{ page }}
    </button>
    
    <button :disabled="currentPage === totalPages" @click="$emit('page-change', currentPage + 1)" class="pagination-btn">
      &gt;
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  totalPages: {
    type: Number,
    required: true
  },
  totalRecipes: {
    type: Number,
    required: true
  },
  pageSize: {
    type: Number,
    required: true
  }
});

defineEmits(['page-change']);

// Простая пагинация - показываем только 5 страниц вокруг текущей
const visiblePages = computed(() => {
  const pages = [];
  const start = Math.max(1, props.currentPage - 2);
  const end = Math.min(props.totalPages, props.currentPage + 2);
  
  for (let i = start; i <= end; i++) {
    pages.push(i);
  }
  return pages;
});
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  gap: 4px;
}

.pagination-btn {
  padding: 8px 12px;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease;
  min-width: 40px;
}

.pagination-btn:hover:not(:disabled) {
  background: #f8f9fa;
  border-color: #667eea;
}

.pagination-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>