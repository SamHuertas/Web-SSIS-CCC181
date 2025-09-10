<template>
  <div class="bg-white rounded-lg shadow-sm mx-auto my-6 max-w-7xl">
    <div class="p-6 border-b border-gray-200">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 class="text-xl font-semibold text-gray-900">Student Management</h2>
          <p class="text-sm text-gray-600 mt-1">
            Manage student records with ID format YYYY-NNNN. Add, edit, delete, and search through student information.
          </p>
        </div>
        <div class="mt-4 sm:mt-0">
          <button class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-gray-800 hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            Add Student
          </button>
        </div>
      </div>
    </div>

    <div class="p-6">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
        <h3 class="text-lg font-medium text-gray-900">Student Management</h3>
        <div class="mt-4 sm:mt-0 relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
          <input
            type="text"
            placeholder="Search students..."
            class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
        </div>
      </div>

      <StudentTable />
    </div>
  </div>
</template>

<script>
import StudentTable from './StudentTable.vue'

export default {
  name: 'StudentManagement',
  components: {
    StudentTable
  }
}
</script>