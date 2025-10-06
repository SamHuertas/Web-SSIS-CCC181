<script setup>
  import AppSidebar from './components/ui/AppSidebar.vue';
  import { RouterView } from 'vue-router';
</script>

<template>
  <div class="flex h-screen">
    <AppSidebar />
      <main class="flex-1 flex flex-col overflow-hidden">
      <RouterView />
    </main>
  </div>
</template>