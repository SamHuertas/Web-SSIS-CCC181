import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'
import StudentManagementView from '@/views/StudentManagementView.vue'
import ProgramManagementView from '@/views/ProgramManagementView.vue'
import CollegeManagementView from '@/views/CollegeManagementView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
    routes : [
  {
    path: '/',
    name: 'dashboard',
    component: DashboardView
  },
  {
    path: '/students',
    name: 'students',
    component: StudentManagementView
  },
  {
    path: '/programs',
    name: 'programs',
    component: ProgramManagementView 
  },
  {
    path: '/colleges',
    name: 'colleges',
    component: CollegeManagementView
  }
]
});


export default router