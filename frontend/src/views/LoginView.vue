<script setup>
import { ref } from 'vue'
import { useAuth } from '@/stores/auth.js'
import { LogIn, Mail, Lock } from 'lucide-vue-next'
import { RouterLink } from 'vue-router'

const { login } = useAuth()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  error.value = ''
  
  if (!email.value || !password.value) {
    error.value = 'Please fill in all fields'
    return
  }

  loading.value = true
  
  const result = await login(email.value, password.value)
  
  if (!result.success) {
    error.value = result.error || 'Login failed'
  }
  
  loading.value = false
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-green-100 p-4">
    <div class="max-w-md w-full">
      <!-- Card -->
      <div class="bg-white rounded-2xl shadow-xl p-8">
        <!-- Header -->
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-100 mb-4">
            <LogIn class="w-8 h-8 text-green-600" />
          </div>
          <h1 class="text-3xl font-bold text-gray-900">Welcome Back</h1>
          <p class="text-gray-600 mt-2">Sign in to your account</p>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-sm text-red-600">{{ error }}</p>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleLogin" class="space-y-6">
          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Mail class="h-5 w-5 text-gray-400" />
              </div>
              <input
                v-model="email"
                type="email"
                id="email"
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                placeholder="Enter your email"
                :disabled="loading"
              />
            </div>
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Lock class="h-5 w-5 text-gray-400" />
              </div>
              <input
                v-model="password"
                type="password"
                id="password"
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                placeholder="Enter your password"
                :disabled="loading"
              />
            </div>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            class="w-full py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-semibold flex justify-center items-center transition-colors duration-200"
            :disabled="loading"
            :class="loading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-green-700'"
          >
            <span v-if="!loading">Sign In</span>
            <span v-else>Signing in...</span>
          </button>

          <!-- Don't have account -->
          <p class="text-center text-sm text-gray-600 mt-4">
            Don't have an account?
            <RouterLink to="/signup" class="text-green-600 hover:underline font-medium">Sign up</RouterLink>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>