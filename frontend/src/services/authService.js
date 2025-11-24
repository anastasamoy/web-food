import { 
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  updateProfile
} from 'firebase/auth';
import { auth } from '../firebase/config.js';

class AuthService {
  // Регистрация
  async register(email, password, displayName) {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    if (displayName) {
      await updateProfile(userCredential.user, { displayName });
    }
    return userCredential;
  }

  // Вход
  async login(email, password) {
    return await signInWithEmailAndPassword(auth, email, password);
  }

  // Выход
  async logout() {
    return await signOut(auth);
  }

  // Слушатель изменения состояния аутентификации
  onAuthChange(callback) {
    return onAuthStateChanged(auth, callback);
  }

  // Текущий пользователь
  getCurrentUser() {
    return auth.currentUser;
  }
}

export default new AuthService();