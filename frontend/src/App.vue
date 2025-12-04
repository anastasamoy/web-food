<template>
  <div>
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

    <AppTabs
      :tabs="tabs"
      :current-tab="currentTab"
      @tab-change="switchTab"
    />

    <component :is="currentView" />

    <ChatBot v-if="isAuthenticated" />

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

import AppHeader from './components/layout/AppHeader.vue';
import AppTabs from './components/layout/AppTabs.vue';
import ChatBot from './components/ChatBot.vue';

import LoginForm from './components/auth/LoginForm.vue';
import RegisterForm from './components/auth/RegisterForm.vue';

import RecipesView from './views/RecipesView.vue';
import UsersView from './views/UsersView.vue';
import PPRecipesView from './views/PPRecipesView.vue';
import InteractionsView from './views/InteractionsView.vue';

export default {
  name: 'App',
  components: {
    AppHeader,
    AppTabs,
    ChatBot,
    LoginForm,
    RegisterForm,
    RecipesView,
    UsersView,
    PPRecipesView,
    InteractionsView
  },
  setup() {
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

    const tabs = ['Recepty', 'Používatelia', 'PP recepty', 'Interakcie'];
    const currentTab = ref('Recepty');

    const currentView = computed(() => {
      const views = {
        'Recepty': RecipesView, // Изменил строки на компоненты
        'Používatelia': UsersView,
        'PP recepty': PPRecipesView,
        'Interakcie': InteractionsView
      };
      return views[currentTab.value] || RecipesView;
    });

    const switchTab = (tab) => {
      currentTab.value = tab;
    };

    return {
      isAuthenticated,
      user,
      isAdmin,
      showLogin,
      showRegister,
      handleLogout,
      switchToAdmin,
      switchToRegister,
      switchToLogin,
      tabs,
      currentTab,
      currentView,
      switchTab
    };
  }
}
</script>

<style scoped>
/* Стили можно добавить здесь, если они короткие */
</style>

<style>
/* Глобальные стили */
@import './styles/app.css';
@import './styles/auth.css';
</style>