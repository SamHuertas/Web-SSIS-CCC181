<script setup>
import { LayoutDashboard, UserRound, GraduationCap, Building2, PanelRight, PanelLeft } from "lucide-vue-next";
import { RouterLink, useRoute } from 'vue-router'
import { ref } from 'vue';

const route = useRoute();
const isActiveLink = (routePath) => {
  return route.path === routePath;
}

const isCollapsed = ref(false);

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
}
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
            to="/" 
            :class="[
              'group relative flex items-center rounded-lg transition-all duration-300 h-12',
              isActiveLink('/') 
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

    <!-- Footer -->
    <div class="p-4 border-t border-gray-200 overflow-hidden">
      <div class="relative flex items-center h-10">
        <div class="absolute left-0 rounded-full bg-gradient-to-br from-green-500 to-green-600 text-white font-bold flex items-center justify-center w-10 h-10 text-sm flex-shrink-0">
          SH
        </div>
        <div 
          :class="[
            'transition-all duration-300 overflow-hidden absolute left-14',
            isCollapsed ? 'opacity-0 w-0' : 'opacity-100 w-auto'
          ]"
        >
          <p class="text-sm font-medium text-gray-900 truncate whitespace-nowrap">Sam Huertas</p>
          <p class="text-xs text-gray-500 truncate whitespace-nowrap">Developer</p>
        </div>
      </div>
    </div>
  </aside>
</template>