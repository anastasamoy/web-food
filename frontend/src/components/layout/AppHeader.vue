<template>
  <header class="auth-header">
    <div class="header-content">
      <h1>🍳 Кулинарная книга</h1>
      <div class="auth-buttons">
        <!-- Используем emits вместо прямого изменения props -->
        <button v-if="!isAuthenticated" @click="$emit('show-login')" class="auth-btn">Войти</button>
        <button v-if="!isAuthenticated" @click="$emit('show-register')" class="auth-btn register">Регистрация</button>
        <div v-if="isAuthenticated" class="user-menu">
          <span class="user-greeting">Привет, {{ user?.displayName || user?.email }}!</span>
          <button v-if="isAdmin" @click="switchToAdmin" class="auth-btn admin">Админка</button>
          <button @click="handleLogout" class="auth-btn logout">Выйти</button>
        </div>
      </div>
    </div>
  </header>

  <header class="header">
    <p>Просмотр таблиц: рецепты, пользователи, взаимодействия, PP-рецепты</p>
  </header>
</template>

<script>
export default {
  name: 'AppHeader',
  props: {
    isAuthenticated: Boolean,
    user: Object,
    isAdmin: Boolean,
    showLogin: Boolean,
    showRegister: Boolean
  },
  emits: ['logout', 'switch-to-admin', 'show-login', 'show-register'],
  methods: {
    handleLogout() {
      this.$emit('logout');
    },
    switchToAdmin() {
      this.$emit('switch-to-admin');
    }
  }
}
</script>

<style scoped src="../../styles/auth.css"></style>