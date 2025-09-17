<script setup>
    import { defineProps } from 'vue';
    import * as LucideIcons from 'lucide-vue-next';

    const stats = defineProps({
        title: {
            type: String,
            required: true
        },
        value: {
            type: [String, Number],
            required: true
        },
        color: {
            type: String,
            default: 'blue'
        },
        icon: {
            type: String,
            default: 'user'
        }
    });
    const IconComponent = LucideIcons[stats.icon.charAt(0).toUpperCase() + stats.icon.slice(1).replace(/-([a-z])/g, (g) => g[1].toUpperCase())] || LucideIcons.User;
    const colorClasses = {
      blue: {
        border: 'border-l-blue-500',
        text: 'text-blue-500'
      },
      green: {
        border: 'border-l-green-500',
        text: 'text-green-500'
      },
      purple: {
        border: 'border-l-purple-500',
        text: 'text-purple-500'
      }
    }
</script>

<template>
    <div class="bg-white border border-gray-200 rounded-lg shadow-sm border-l-4" :class="colorClasses[stats.color]?.border">
        <div class="flex flex-row items-center justify-between space-y-0 pb-2 p-6">
          <h3 class="text-sm font-medium text-gray-600">{{ stats.title }}</h3>

          <component
            :is="IconComponent"
            class="h-4 w-4" :class="colorClasses[stats.color]?.text"
          />
        </div>
        <div class="px-6 pb-4">
          <div class="text-2xl font-bold text-gray-900">{{ stats.value }}</div>
        </div>
      </div>
</template>