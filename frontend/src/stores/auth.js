import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import axios from 'axios'

export function useAuth() {
  const router = useRouter()
  const toast = useToast()
  
  const isAuthenticated = ref(!!localStorage.getItem('token'))
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const signup = async (username, email, password) => {
    try {
      const { data } = await axios.post("/auth/register", {
        username, email, password
      })

      toast.success('Account created successfully! Please log in.')
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || 'Network error' 
      }
    }
  }

  const login = async (email, password) => {
    try {
      const { data } = await axios.post("/auth/login", {
        email, password
      })

      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      isAuthenticated.value = true
      user.value = data.user

      toast.success('Login successful!')
      router.push('/home')
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.error || 'Login failed' 
      }
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    isAuthenticated.value = false
    user.value = null
    toast.info('Logged out successfully')
    router.push('/login')
  }

  const verifyToken = async () => {
    const token = localStorage.getItem('token')
    if (!token) return false

    try {
      await axios.get("/auth/verify")
      return true
    } catch {
      logout()
      return false
    }
  }

  return { 
    isAuthenticated, 
    user, 
    signup, 
    login, 
    logout, 
    verifyToken 
  }
}