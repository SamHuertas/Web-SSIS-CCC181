<script setup>
  import Header from '@/components/Header.vue';
  import StudentManagement from '@/components/StudentManagement.vue';
  import Keyboard from './components/Keyboard.vue';
  import Phone from './components/Phone.vue';
</script>

<template> 
<body class="bg-blue-100">
  <Header />
  <StudentManagement />
    <Phone/>
    <Keyboard/>
    <Phone/>
  </body>
</template>