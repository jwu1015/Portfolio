import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import api from '../services/api'

export const useAuthStore = create(
  persist(
    (set) => ({
      token: null,
      user: null,
      isAuthenticated: false,
      
      login: async (email, password) => {
        try {
          const response = await api.post('/auth/login', { email, password })
          const { token, user } = response.data
          
          set({ token, user, isAuthenticated: true })
          api.defaults.headers.common['Authorization'] = `Bearer ${token}`
          
          return { success: true }
        } catch (error) {
          return {
            success: false,
            error: error.response?.data?.error || 'Login failed',
          }
        }
      },
      
      logout: () => {
        set({ token: null, user: null, isAuthenticated: false })
        delete api.defaults.headers.common['Authorization']
      },
      
      init: () => {
        const state = useAuthStore.getState()
        if (state.token) {
          api.defaults.headers.common['Authorization'] = `Bearer ${state.token}`
        }
      },
    }),
    {
      name: 'hope-services-auth',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)

// Initialize auth on load
if (typeof window !== 'undefined') {
  useAuthStore.getState().init()
}

