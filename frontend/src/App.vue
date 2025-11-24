<template>
  <div>
    <!-- Хедер с аутентификацией -->
    <AppHeader
      :is-authenticated="isAuthenticated"
      :user="user"
      :is-admin="isAdmin"
      :show-login="showLogin"
      :show-register="showRegister"
      @logout="handleLogout"
      @switch-to-admin="switchToAdmin"
      @show-login="showLogin = true"
      @show-register="showRegister = true"
    />

    <!-- Навигация по вкладкам -->
    <AppTabs
      :tabs="tabs"
      :current-tab="currentTab"
      @tab-change="switchTab"
    />

    <!-- Основной контент -->
    <component :is="currentView" />

    <!-- Модальные окна аутентификации -->
    <LoginForm 
      v-if="showLogin"
      @success="showLogin = false"
      @close="showLogin = false"
      @switch-to-register="switchToRegister"
    />
    <RegisterForm 
      v-if="showRegister"
      @success="showRegister = false"
      @close="showRegister = false"
      @switch-to-login="switchToLogin"
    />
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useAuth } from './composables/useAuth.js';

// Layout Components
import AppHeader from './components/layout/AppHeader.vue';
import AppTabs from './components/layout/AppTabs.vue';

// Auth Components
import LoginForm from './components/auth/LoginForm.vue';
import RegisterForm from './components/auth/RegisterForm.vue';

// Views
import RecipesView from './views/RecipesView.vue';
import UsersView from './views/UsersView.vue';
import PPRecipesView from './views/PPRecipesView.vue';
import InteractionsView from './views/InteractionsView.vue';

export default {
  name: 'App',
  components: {
    AppHeader,
    AppTabs,
    LoginForm,
    RegisterForm,
    RecipesView,
    UsersView,
    PPRecipesView,
    InteractionsView
  },
  setup() {
    // Аутентификация
    const {
      isAuthenticated,
      user,
      isAdmin,
      showLogin,
      showRegister,
      handleLogout,
      switchToAdmin,
      switchToRegister,
      switchToLogin
    } = useAuth();

    // Вкладки
    const tabs = ['Рецепты', 'Пользователи', 'PP-рецепты', 'Взаимодействия'];
    const currentTab = ref('Рецепты');

    // Вычисляем текущий view компонент
    const currentView = computed(() => {
      const views = {
        'Рецепты': 'RecipesView',
        'Пользователи': 'UsersView',
        'PP-рецепты': 'PPRecipesView',
        'Взаимодействия': 'InteractionsView'
      };
      return views[currentTab.value] || 'RecipesView';
    });

    const switchTab = (tab) => {
      currentTab.value = tab;
    };

    return {
      // Аутентификация
      isAuthenticated,
      user,
      isAdmin,
      showLogin,
      showRegister,
      handleLogout,
      switchToAdmin,
      switchToRegister,
      switchToLogin,

      // Вкладки
      tabs,
      currentTab,
      currentView,
      switchTab
    };
  }
}
</script>

<style scoped src="./styles/app.css"></style>
<style src="./styles/auth.css"></style>