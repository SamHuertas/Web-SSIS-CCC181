<script setup>
  import { SidebarProvider, SidebarTrigger } from './components/ui/sidebar';
  import AppSidebar from './components/AppSidebar.vue';
  import DashboardView from './views/DashboardView.vue';
  import StudentManagementView from './views/StudentManagementView.vue';
  import ProgramManagementView from './views/ProgramManagementView.vue';
  import CollegeManagementView from './views/CollegeManagementView.vue';
  import { RouterView } from 'vue-router';
</script>

<template>
  <SidebarProvider class="flex h-screen">
    <AppSidebar />
    <main class="flex-1 flex flex-col">
      <SidebarTrigger />
      <RouterView />
    </main>
  </SidebarProvider>
</template>