<script setup>
    import StatCardsSection from '@/components/StatCardsSection.vue';
    import SecondStatCardsSection from '@/components/SecondStatCardsSection.vue';
    import ThirdStatCardsSection from '@/components/ThirdStatCardsSection.vue';
</script>

<template>
    <div class="flex-1 flex flex-col overflow-hidden">
      <main class="flex-1 overflow-auto p-6">
        <div class="bg-white rounded-lg shadow h-full p-6 space-y-6 w-full">
                <div>
                <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
                <p class="text-gray-600 mt-2">Overview of your student information system</p>
                </div>

               <!-- stat card Components -->
                <StatCardsSection />
                <SecondStatCardsSection />
                <ThirdStatCardsSection />
        </div>
      </main>
    </div>
</template>