<script setup>
import { LayoutDashboard, UserRound, GraduationCap, Building2, PanelRight, PanelLeft, LogOut } from "lucide-vue-next";
import { RouterLink, useRoute } from 'vue-router'
import { ref, computed } from 'vue';
import { useAuth } from '@/stores/auth.js';

const route = useRoute();
const { user, logout } = useAuth();

const isActiveLink = (routePath) => {
  return route.path === routePath;
}

const isCollapsed = ref(false);

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
}

// Get user initials for avatar
const userInitials = computed(() => {
  if (!user.value) return 'U';
  return user.value.username?.substring(0, 2).toUpperCase() || 'U';
});
</script>

<template>
  <aside :class="[
    'bg-white border-r border-gray-200 flex flex-col h-screen transition-all duration-300 ease-in-out relative',
    isCollapsed ? 'w-20' : 'w-64'
  ]">
    <!-- Header with Toggle Button -->
    <div class="p-4 border-b border-gray-200 flex items-center justify-between overflow-hidden">
      <div 
        :class="[
          'transition-all duration-300 ease-in-out flex-1 min-w-0', 
          isCollapsed ? 'opacity-0 w-0 -ml-4' : 'opacity-100 w-auto ml-0'
        ]"
      >
        <h1 class="font-bold text-normal text-gray-900 truncate whitespace-nowrap">
          Student Information System
        </h1>
      </div>
      
      <button 
        @click="toggleSidebar"
        :class="[
          'p-2 rounded-lg hover:bg-gray-100 transition-all duration-200 flex-shrink-0',
          isCollapsed ? 'mx-auto' : 'ml-2'
        ]"
        :title="isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
      >
        <PanelRight v-if="isCollapsed" class="w-5 h-5 text-gray-700" />
        <PanelLeft v-else class="w-5 h-5 text-gray-700" />
      </button>
    </div>

    <!-- Navigation Menu -->
    <nav class="flex-1 p-3 overflow-y-auto overflow-x-hidden">
      <ul class="space-y-2">
        <li>
          <RouterLink 
            to="/home" 
            :class="[
              'group relative flex items-center rounded-lg transition-all duration-300 h-12',
              isActiveLink('/home') 
                ? 'bg-green-600 hover:bg-green-700 text-white shadow-sm' 
                : 'text-gray-700 hover:bg-gray-100'
            ]"
          >
            <div class="absolute left-4 flex items-center justify-center">
              <LayoutDashboard class="w-6 h-6" />
            </div>
            <span 
              :class="[
                'font-medium text-normal whitespace-nowrap transition-all duration-300 overflow-hidden absolute left-14',
                isCollapsed ? 'opacity-0 w-0' : 'opacity-100 w-auto'
              ]"
            >
              Dashboard
            </span>
          </RouterLink>
        </li>
        
        <li>
          <RouterLink 
            to="/students" 
            :class="[
              'group relative flex items-center rounded-lg transition-all duration-300 h-12',
              isActiveLink('/students') 
                ? 'bg-green-600 hover:bg-green-700 text-white shadow-sm' 
                : 'text-gray-700 hover:bg-gray-100'
            ]"
          >
            <div class="absolute left-4 flex items-center justify-center">
              <UserRound class="w-6 h-6" />
            </div>
            <span 
              :class="[
                'font-medium text-normal whitespace-nowrap transition-all duration-300 overflow-hidden absolute left-14',
                isCollapsed ? 'opacity-0 w-0' : 'opacity-100 w-auto'
              ]"
            >
              Students
            </span>
          </RouterLink>
        </li>
        
        <li>
          <RouterLink 
            to="/programs" 
            :class="[
              'group relative flex items-center rounded-lg transition-all duration-300 h-12',
              isActiveLink('/programs') 
                ? 'bg-green-600 hover:bg-green-700 text-white shadow-sm' 
                : 'text-gray-700 hover:bg-gray-100'
            ]"
          >
            <div class="absolute left-4 flex items-center justify-center">
              <GraduationCap class="w-6 h-6" />
            </div>
            <span 
              :class="[
                'font-medium text-normal whitespace-nowrap transition-all duration-300 overflow-hidden absolute left-14',
                isCollapsed ? 'opacity-0 w-0' : 'opacity-100 w-auto'
              ]"
            >
              Programs
            </span>
          </RouterLink>
        </li>
        
        <li>
          <RouterLink 
            to="/colleges" 
            :class="[
              'group relative flex items-center rounded-lg transition-all duration-300 h-12',
              isActiveLink('/colleges') 
                ? 'bg-green-600 hover:bg-green-700 text-white shadow-sm' 
                : 'text-gray-700 hover:bg-gray-100'
            ]"
          >
            <div class="absolute left-4 flex items-center justify-center">
              <Building2 class="w-6 h-6" />
            </div>
            <span 
              :class="[
                'font-medium text-normal whitespace-nowrap transition-all duration-300 overflow-hidden absolute left-14',
                isCollapsed ? 'opacity-0 w-0' : 'opacity-100 w-auto'
              ]"
            >
              Colleges
            </span>
          </RouterLink>
        </li>
      </ul>
    </nav>

    <!-- Footer with User Info and Logout -->
    <div class="p-3 border-t border-gray-200 overflow-hidden">
      <div class="relative flex items-center mb-2 h-12">
        <div class="absolute left-2 flex items-center justify-center">
          <div class="rounded-full bg-gradient-to-br from-green-500 to-green-600 text-white font-bold flex items-center justify-center w-10 h-10 text-sm">
            {{ userInitials }}
          </div>
        </div>
        <div 
          v-if="user"
          :class="[
            'font-medium text-normal whitespace-nowrap transition-all duration-300 overflow-hidden absolute left-14',
            isCollapsed ? 'opacity-0 w-0' : 'opacity-100 w-auto'
          ]"
        >
          <p class="text-gray-900 truncate text-sm">{{ user.username }}</p>
          <p class="text-xs text-gray-500 truncate max-w-[180px]">{{ user.email }}</p>
        </div>
      </div>
      
      <!-- Logout Button -->
      <div class="relative flex items-center h-12">
        <button 
          @click="logout"
          class="group relative flex items-center w-full rounded-lg transition-all duration-300 h-12 text-red-600 hover:bg-red-50"
          :title="isCollapsed ? 'Logout' : ''"
        >
          <div class="absolute left-4 flex items-center justify-center">
            <LogOut class="w-4 h-4 flex-shrink-0" />
          </div>
          <span 
            :class="[
              'font-medium text-normal whitespace-nowrap transition-all duration-300 overflow-hidden absolute left-14',
              isCollapsed ? 'opacity-0 w-0' : 'opacity-100 w-auto'
            ]"
          >
            Logout
          </span>
        </button>
      </div>
    </div>
  </aside>
</template>