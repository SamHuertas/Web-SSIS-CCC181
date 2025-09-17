<script setup>
  import { SidebarProvider, SidebarTrigger } from './components/ui/sidebar';
  import AppSidebar from './components/AppSidebar.vue';
</script>

<template>
  <SidebarProvider>
    <AppSidebar />
    <main>
      <SidebarTrigger />
      <slot />
    </main>
  </SidebarProvider>
</template>