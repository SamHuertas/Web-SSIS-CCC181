<script setup>
  import { SidebarProvider, SidebarTrigger } from './components/ui/sidebar';
  import AppSidebar from './components/AppSidebar.vue';
  import DashboardView from './views/DashboardView.vue';
</script>

<template>
  <SidebarProvider class="flex h-screen">
    <AppSidebar />
    <main class="flex-1 flex flex-col">
      <SidebarTrigger />
      <DashboardView />
    </main>
  </SidebarProvider>
</template>