<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { ContactRound, GraduationCap, School, TrendingUp, Building2, University } from 'lucide-vue-next';
import axios from 'axios';

// State
const colleges = ref([]);
const programs = ref([]);
const students = ref([]);
const studentsPerCollege = ref([]);
const studentsPerProgram = ref([]);
const collegeStats = ref([]);
const loading = ref(true);
const hasFetched = ref(false); // Prevent multiple fetches

// Single API call for all dashboard data
const fetchDashboardData = async () => {
  // Prevent multiple calls
  if (hasFetched.value && studentsPerCollege.value.length > 0) {
    console.log("⚠️ Dashboard data already fetched, skipping...");
    return;
  }
  
  try {
    console.log("🔄 FETCHING DASHBOARD DATA...");
    loading.value = true;
    
    // Get all dashboard data in one call
    const { data } = await axios.get("/dashboard/summary");
    
    console.log("✅ Data received. Counts:", {
      students_per_college: data.students_per_college?.length || 0,
      top_programs: data.top_programs?.length || 0,
      college_stats: data.college_stats?.length || 0
    });
    
    // RESET arrays first to prevent accumulation
    colleges.value = [];
    programs.value = [];
    students.value = [];
    studentsPerCollege.value = [];
    studentsPerProgram.value = [];
    collegeStats.value = [];
    
    // Use setTimeout to ensure reactive updates are batched
    setTimeout(() => {
      // Map data to original structure - using objects with proper counts
      colleges.value = Array.from({ length: data.total_colleges || 0 }, (_, i) => ({ id: i }));
      programs.value = Array.from({ length: data.total_programs || 0 }, (_, i) => ({ id: i }));
      students.value = Array.from({ length: data.total_students || 0 }, (_, i) => ({ id: i }));
      
      // IMPORTANT: Use slice() to create new arrays and prevent reference issues
      studentsPerCollege.value = [...(data.students_per_college || [])];
      studentsPerProgram.value = [...(data.top_programs || [])];
      collegeStats.value = [...(data.college_stats || [])];
      
      console.log("🎯 Final counts after setting:", {
        studentsPerCollege: studentsPerCollege.value.length,
        studentsPerProgram: studentsPerProgram.value.length,
        collegeStats: collegeStats.value.length
      });
      
      hasFetched.value = true;
      loading.value = false;
    }, 0);
    
  } catch (err) {
    console.error("❌ Error fetching dashboard data:", err);
    // Reset everything on error
    colleges.value = [];
    programs.value = [];
    students.value = [];
    studentsPerCollege.value = [];
    studentsPerProgram.value = [];
    collegeStats.value = [];
    loading.value = false;
  }
};

// Load all data on mount - only once
onMounted(() => {
  console.log("🚀 Dashboard mounted");
  fetchDashboardData();
});

// Optional: Clean up on unmount
onUnmounted(() => {
  console.log("🧹 Dashboard unmounted");
  // Reset flag when component is destroyed
  hasFetched.value = false;
});
</script>

<template>
  <div class="flex-1 flex flex-col overflow-hidden">
    <main class="flex-1 overflow-auto p-6">
      <div class="bg-white rounded-lg shadow p-6 w-full flex flex-col">
        <div class="space-y-6 flex-1 flex flex-col">
          <!-- Header -->
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p class="text-gray-600 mt-2">Overview of your student information system</p>
            <div v-if="studentsPerCollege.length > 7" class="text-sm text-red-500 mt-1">
              ⚠️ Warning: Showing {{ studentsPerCollege.length }} colleges (expected max 7)
            </div>
          </div>

          <!-- Stat Cards Section -->
          <div class="grid grid-cols-1 sm:grid-cols-1 lg:grid-cols-3 gap-6">
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm border-l-4 border-l-blue-500">
              <div class="flex flex-row items-center justify-between space-y-0 pb-2 p-6">
                <h3 class="text-sm font-medium text-gray-600">Students</h3>
                <ContactRound class="h-4 w-4 text-blue-500" />
              </div>
              <div class="px-6 pb-4">
                <div v-if="loading" class="text-2xl font-bold text-gray-900 animate-pulse">...</div>
                <div v-else class="text-2xl font-bold text-gray-900">{{ students.length }}</div>
              </div>
            </div>

            <div class="bg-white border border-gray-200 rounded-lg shadow-sm border-l-4 border-l-green-500">
              <div class="flex flex-row items-center justify-between space-y-0 pb-2 p-6">
                <h3 class="text-sm font-medium text-gray-600">Programs</h3>
                <GraduationCap class="h-4 w-4 text-green-500" />
              </div>
              <div class="px-6 pb-4">
                <div v-if="loading" class="text-2xl font-bold text-gray-900 animate-pulse">...</div>
                <div v-else class="text-2xl font-bold text-gray-900">{{ programs.length }}</div>
              </div>
            </div>

            <div class="bg-white border border-gray-200 rounded-lg shadow-sm border-l-4 border-l-purple-500">
              <div class="flex flex-row items-center justify-between space-y-0 pb-2 p-6">
                <h3 class="text-sm font-medium text-gray-600">Colleges</h3>
                <School class="h-4 w-4 text-purple-500" />
              </div>
              <div class="px-6 pb-4">
                <div v-if="loading" class="text-2xl font-bold text-gray-900 animate-pulse">...</div>
                <div v-else class="text-2xl font-bold text-gray-900">{{ colleges.length }}</div>
              </div>
            </div>
          </div>

          <!-- Second Section: Students per College & Top Programs -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Students per College - FIXED -->
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm">
              <div class="p-6 pb-4">
                <h3 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
                  <Building2 class="h-5 w-5 text-blue-500" />
                  Students per College 
                </h3>
              </div>
              <div class="px-6 pb-6">
                <div v-if="loading" class="text-center py-8 text-gray-500">
                  Loading...
                </div>
                <div v-else-if="studentsPerCollege.length === 0" class="text-center py-8 text-gray-500">
                  No data available
                </div>
                <div v-else>
                  <!-- Simple, clean rendering without extra wrappers -->
                  <div 
                    v-for="(college, index) in studentsPerCollege" 
                    :key="`college-${college.college_code}-${index}`"
                    class="flex items-center justify-between py-3 border-b border-gray-100 last:border-0"
                  >
                    <div class="flex items-center gap-3">
                      <div class="w-6 text-center text-sm text-gray-500">
                        {{ index + 1 }}
                      </div>
                      <div>
                        <div class="font-medium text-gray-900">{{ college.college_name }}</div>
                        <div class="text-sm text-gray-500">{{ college.college_code }}</div>
                      </div>
                    </div>
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {{ college.student_count }} students
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Top Programs by Enrollment - FIXED -->
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm">
              <div class="p-6 pb-4">
                <h3 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
                  <TrendingUp class="h-5 w-5 text-green-500" />
                  Top Programs by Enrollment
                </h3>
              </div>
              <div class="px-6 pb-6">
                <div v-if="loading" class="text-center py-8 text-gray-500">
                  Loading...
                </div>
                <div v-else-if="studentsPerProgram.length === 0" class="text-center py-8 text-gray-500">
                  No data available
                </div>
                <div v-else>
                  <div 
                    v-for="(program, index) in studentsPerProgram" 
                    :key="`program-${program.program_code}-${index}`"
                    class="flex items-center justify-between py-3 border-b border-gray-100 last:border-0"
                  >
                    <div class="flex items-center gap-3">
                      <div class="flex items-center justify-center w-6 h-6 rounded-full bg-green-100 text-green-800 text-xs font-bold">
                        {{ index + 1 }}
                      </div>
                      <div>
                        <div class="font-medium text-gray-900">{{ program.program_name }}</div>
                        <div class="text-sm text-gray-500">{{ program.program_code }}</div>
                      </div>
                    </div>
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      {{ program.student_count }} students
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- College Statistics Table -->
          <div class="grid grid-cols-1 lg:grid-cols-1 gap-6">
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm">
              <div class="p-6 pb-4">
                <h3 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
                  <University class="h-5 w-5 text-purple-500" />
                  College Statistics
                  <span class="text-sm font-normal text-gray-500">
                    ({{ collegeStats.length }})
                  </span>
                </h3>
              </div>
              <div class="px-6 pb-6">
                <div v-if="loading" class="text-center py-8 text-gray-500">
                  Loading...
                </div>
                <div v-else-if="collegeStats.length === 0" class="text-center py-8 text-gray-500">
                  No college statistics available
                </div>
                <div v-else class="overflow-x-auto">
                  <table class="w-full">
                    <thead>
                      <tr class="border-b border-gray-200">
                        <th class="text-left py-3 px-4 font-medium text-gray-600">#</th>
                        <th class="text-left py-3 px-4 font-medium text-gray-600">College</th>
                        <th class="text-left py-3 px-4 font-medium text-gray-600">Code</th>
                        <th class="text-center py-3 px-4 font-medium text-gray-600">Programs</th>
                        <th class="text-center py-3 px-4 font-medium text-gray-600">Students</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr 
                        v-for="(college, index) in collegeStats" 
                        :key="`stat-${college.college_code}-${index}`"
                        class="border-b border-gray-100 hover:bg-gray-50"
                      >
                        <td class="py-3 px-4 text-gray-500">{{ index + 1 }}</td>
                        <td class="py-3 px-4 font-medium text-gray-900">{{ college.college_name }}</td>
                        <td class="py-3 px-4 text-gray-600">{{ college.college_code }}</td>
                        <td class="py-3 px-4 text-center">
                          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 border border-gray-300">
                            {{ college.program_count }}
                          </span>
                        </td>
                        <td class="py-3 px-4 text-center">
                          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 border border-gray-300">
                            {{ college.student_count }}
                          </span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>