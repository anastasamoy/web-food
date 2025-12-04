<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <h2>Регистрация</h2>
      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label>Имя:</label>
          <input 
            v-model="userData.displayName" 
            type="text" 
            placeholder="Введите ваше имя" 
            required
          >
        </div>

        <div class="form-group">
          <label>Email:</label>
          <input 
            v-model="userData.email" 
            type="email" 
            placeholder="Введите ваш email" 
            required
          >
        </div>
        
        <div class="form-group">
          <label>Пароль:</label>
          <input 
            v-model="userData.password" 
            type="password" 
            placeholder="Введите пароль (минимум 6 символов)" 
            required
            minlength="6"
          >
        </div>

        <button type="submit" :disabled="loading" class="auth-button register">
          {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </button>

        <div class="auth-links">
          <p>Už máte účet? 
            <a href="#" @click.prevent="switchToLogin">Prihlásiť sa</a>
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
  name: 'RegisterForm',
  emits: ['success', 'close', 'switch-to-login'],
  
  setup(props, { emit }) {
    const userData = ref({
      displayName: '',
      email: '',
      password: ''
    });
    const loading = ref(false);

    const handleRegister = async () => {
      if (userData.value.password.length < 6) {
        alert('Пароль должен содержать минимум 6 символов');
        return;
      }

      loading.value = true;
      try {
        await AuthService.register(
          userData.value.email, 
          userData.value.password, 
          userData.value.displayName
        );
        emit('success');
      } catch (error) {
        alert(`Ошибка регистрации: ${error.message}`);
      } finally {
        loading.value = false;
      }
    };

    const switchToLogin = () => {
      emit('switch-to-login');
    };

    return {
      userData,
      loading,
      handleRegister,
      switchToLogin
    };
  }
};
</script>

<style scoped src="../../styles/auth.css"></style>