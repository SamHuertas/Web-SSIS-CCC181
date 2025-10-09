import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'
import StudentManagementView from '@/views/StudentManagementView.vue'
import ProgramManagementView from '@/views/ProgramManagementView.vue'
import CollegeManagementView from '@/views/CollegeManagementView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
    routes : [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresGuest: true }
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupView,
    meta: { requiresGuest: true }
  },
  {
    path: '/home',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/students',
    name: 'students',
    component: StudentManagementView,
    meta: { requiresAuth: true }
  },
  {
    path: '/programs',
    name: 'programs',
    component: ProgramManagementView,
    meta: { requiresAuth: true }
  },
  {
    path: '/colleges',
    name: 'colleges',
    component: CollegeManagementView,
    meta: { requiresAuth: true }
  }
]
});

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const isAuthenticated = !!token

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && isAuthenticated) {
    next('/home')
  } else {
    next()
  }
})

export default router 