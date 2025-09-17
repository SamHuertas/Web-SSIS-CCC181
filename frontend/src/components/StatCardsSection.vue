<script setup>
  import StatCard from '@/components/StatCard.vue';
</script>

<template>
  <div class="grid grid-cols-1 sm:grid-cols-1 lg:grid-cols-3 gap-6">
    <StatCard title="Students" value="1,234" color="blue" icon="contact-round" />
    <StatCard title="Courses" value="8" color="green" icon="graduation-cap" />
    <StatCard title="Colleges" value="13" color="purple" icon="school" />
  </div>
</template>