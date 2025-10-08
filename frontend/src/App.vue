<script setup>
import AppSidebar from './components/ui/AppSidebar.vue';
import { RouterView, useRoute } from 'vue-router';
import { computed } from 'vue';

const route = useRoute();

// Hide sidebar on login and signup pages
const showSidebar = computed(() => {
  return route.path !== '/login' && route.path !== '/signup';
});
</script>

<template>
  <div class="flex h-screen">
    <AppSidebar v-if="showSidebar" />
    <main class="flex-1 flex flex-col overflow-hidden">
      <RouterView />
    </main>
  </div>
</template>