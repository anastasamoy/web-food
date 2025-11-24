<template>
  <div class="tabs">
    <button 
      v-for="tab in tabs" 
      :key="tab"
      @click="$emit('tab-change', tab)"
      :class="{ active: currentTab === tab }"
    >
      {{ tab }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'AppTabs',
  props: {
    tabs: Array,
    currentTab: String
  },
  emits: ['tab-change']
}
</script>

<style scoped>
.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 0.5rem;
}

.tabs button {
  padding: 0.75rem 1.5rem;
  border: none;
  background: none;
  cursor: pointer;
  border-radius: 4px 4px 0 0;
  transition: all 0.3s;
  font-weight: 500;
}

.tabs button:hover {
  background: #f5f5f5;
}

.tabs button.active {
  background: #3498db;
  color: white;
}
</style>