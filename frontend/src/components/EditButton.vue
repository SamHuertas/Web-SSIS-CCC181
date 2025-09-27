<script setup>
    import { SquarePen } from 'lucide-vue-next';
    defineEmits(['click']);
</script>

<template>
    <button @click="$emit('click')" class="inline-flex items-center px-2 py-1 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
        <square-pen class="h-4 w-4"/>
    </button>
</template>