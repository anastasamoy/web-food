const API_BASE = import.meta.env.VITE_API_URL + '/api'

export const api = {
  async getRecipes() {
    const response = await fetch(`${API_BASE}/recipes`)
    return response.json()
  },
  async register(userData) {
    const response = await fetch(`${API_BASE}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    })
    return response.json()
  }
}
