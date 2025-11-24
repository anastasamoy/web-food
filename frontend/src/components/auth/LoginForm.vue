<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <h2>Вход в систему</h2>
      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label>Email:</label>
          <input 
            v-model="credentials.email" 
            type="email" 
            placeholder="Введите ваш email" 
            required
          >
        </div>
        
        <div class="form-group">
          <label>Пароль:</label>
          <input 
            v-model="credentials.password" 
            type="password" 
            placeholder="Введите пароль" 
            required
          >
        </div>

        <button type="submit" :disabled="loading" class="auth-button">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>

        <div class="auth-links">
          <p>Нет аккаунта? 
            <a href="#" @click.prevent="switchToRegister">Зарегистрироваться</a>
          </p>
        </div>
      </form>

      <button class="close-button" @click="$emit('close')">×</button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import AuthService from '../../services/authService.js';

export default {
  name: 'LoginForm',
  emits: ['success', 'close', 'switch-to-register'],
  
  setup(props, { emit }) {
    const credentials = ref({
      email: '',
      password: ''
    });
    const loading = ref(false);

    const handleLogin = async () => {
      loading.value = true;
      try {
        await AuthService.login(credentials.value.email, credentials.value.password);
        emit('success');
      } catch (error) {
        alert(`Ошибка входа: ${error.message}`);
      } finally {
        loading.value = false;
      }
    };

    const switchToRegister = () => {
      emit('switch-to-register');
    };

    return {
      credentials,
      loading,
      handleLogin,
      switchToRegister
    };
  }
};
</script>

<style scoped src="../../styles/auth.css"></style>