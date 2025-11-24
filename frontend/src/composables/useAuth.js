import { ref, onMounted } from 'vue';
import AuthService from '../services/authService.js';

export function useAuth() {
  const isAuthenticated = ref(false);
  const user = ref(null);
  const isAdmin = ref(false);
  const showLogin = ref(false);
  const showRegister = ref(false);

  const handleLogout = async () => {
    try {
      await AuthService.logout();
      isAuthenticated.value = false;
      user.value = null;
      isAdmin.value = false;
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const switchToAdmin = () => {
    alert('Админ-панель в разработке');
  };

  const switchToRegister = () => {
    showLogin.value = false;
    showRegister.value = true;
  };

  const switchToLogin = () => {
    showRegister.value = false;
    showLogin.value = true;
  };

  // Проверка аутентификации при загрузке
  onMounted(() => {
    AuthService.onAuthChange((currentUser) => {
      isAuthenticated.value = !!currentUser;
      user.value = currentUser;
      isAdmin.value = currentUser?.email === 'admin@webfood.com';
    });
  });

  return {
    isAuthenticated,
    user,
    isAdmin,
    showLogin,
    showRegister,
    handleLogout,
    switchToAdmin,
    switchToRegister,
    switchToLogin
  };
}