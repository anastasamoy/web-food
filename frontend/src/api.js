const API_BASE = import.meta.env.VITE_API_URL + '/api';

export const api = {
  /**
   * Получить рецепты
   * @param {Object} params - параметры (limit, offset)
   * @returns {Promise<Object>}
   */
  async getRecipes(params = {}) {
    const query = new URLSearchParams(params).toString();
    const url = `${API_BASE}/recipes/search${query ? '?' + query : ''}`;
    const response = await fetch(url);
    return response.json();
  },

  /**
   * Получить пользователей
   */
  async getUsers() {
    const response = await fetch(`${API_BASE}/users`);
    return response.json();
  },

  /**
   * Получить PP-рецепты
   */
  async getPPRecipes() {
    const response = await fetch(`${API_BASE}/pp_recipes`);
    return response.json();
  },

  /**
   * Получить взаимодействия
   */
  async getInteractions() {
    const response = await fetch(`${API_BASE}/interactions`);
    return response.json();
  },

  /**
   * Регистрация пользователя
   */
  async register(userData) {
    const response = await fetch(`${API_BASE}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    return response.json();
  }
};