<template>
  <div class="mb-8">
    <h1 class="text-3xl font-bold text-gray-900">{{ title }}</h1>
    <p class="text-gray-600 mt-1">{{ subtitle }}</p>
  </div>
</template>

<script>
export default {
  name: 'DashboardHeader',
  props: {
    title: {
      type: String,
      default: 'Dashboard'
    },
    subtitle: {
      type: String,
      default: 'Overview of your student information system'
    }
  }
}
</script>