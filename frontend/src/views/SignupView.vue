<script setup>
import { ref } from 'vue'
import { useAuth } from '@/stores/auth.js'
import { UserPlus, User, Mail, Lock } from 'lucide-vue-next'
import { RouterLink, useRouter } from 'vue-router' // Added useRouter

const { signup } = useAuth()
const router = useRouter() // Initialized router

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')

const handleSignup = async () => {
  error.value = ''
  
  if (!username.value || !email.value || !password.value || !confirmPassword.value) {
    error.value = 'Please fill in all fields'
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  if (password.value.length < 8) {
    error.value = 'Password must be at least 8 characters'
    return
  }

  loading.value = true
  
  const result = await signup(username.value, email.value, password.value)
  
  if (result.success) {
    // Redirect to login page after successful registration
    router.push('/login')
  } else {
    error.value = result.error || 'Signup failed'
  }
  
  loading.value = false
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-green-100 p-4">
    <div class="max-w-md w-full">
      <div class="bg-white rounded-2xl shadow-xl p-8">
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-100 mb-4">
            <UserPlus class="w-8 h-8 text-green-600" />
          </div>
          <h1 class="text-3xl font-bold text-gray-900">Create Account</h1>
          <p class="text-gray-600 mt-2">Sign up for a new account</p>
        </div>

        <div v-if="error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-sm text-red-600">{{ error }}</p>
        </div>

        <form @submit.prevent="handleSignup" class="space-y-6">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
              Username
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <User class="h-5 w-5 text-gray-400" />
              </div>
              <input
                v-model="username"
                type="text"
                id="username"
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                placeholder="Choose a username"
                :disabled="loading"
              />
            </div>
          </div>

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
                placeholder="Create a password"
                :disabled="loading"
              />
            </div>
          </div>

          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
              Confirm Password
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Lock class="h-5 w-5 text-gray-400" />
              </div>
              <input
                v-model="confirmPassword"
                type="password"
                id="confirmPassword"
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                placeholder="Confirm your password"
                :disabled="loading"
              />
            </div>
          </div>

          <button
            type="submit"
            class="w-full py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-semibold flex justify-center items-center"
            :disabled="loading"
          >
            <span v-if="!loading">Sign Up</span>
            <span v-else>Signing up...</span>
          </button>

          <p class="text-center text-sm text-gray-600 mt-4">
            Already have an account?
            <RouterLink to="/login" class="text-green-600 hover:underline font-medium">Log in</RouterLink>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>