<template>
  <div class="relative">
    <!-- Filter Button -->
    <button 
      @click="toggleDropdown"
      class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
    >
      <Filter class="h-4 w-4 mr-2" />
      Filter
      <span v-if="activeFilterCount > 0" class="ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
        {{ activeFilterCount }}
      </span>
    </button>

    <!-- Dropdown Panel -->
    <transition
      enter-active-class="transition ease-out duration-100"
      enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100"
      leave-active-class="transition ease-in duration-75"
      leave-from-class="transform opacity-100 scale-100"
      leave-to-class="transform opacity-0 scale-95"
    >
      <div 
        v-if="isOpen"
        class="absolute right-0 mt-2 w-80 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50"
      >
        <div class="p-4">
          <!-- Header -->
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-sm font-semibold text-gray-900">Filter Students</h3>
            <button 
              v-if="hasActiveFilters"
              @click="clearFilters"
              class="text-xs text-green-600 hover:text-green-700 font-medium"
            >
              Clear All
            </button>
          </div>

          <!-- Filter Options -->
          <div class="space-y-4">
            <!-- Gender Filter -->
            <div>
              <label for="gender" class="block text-xs font-medium text-gray-700 mb-1">
                Gender
              </label>
              <select 
                id="gender" 
                v-model="filters.gender"
                @change="applyFilters"
                class="w-full px-3 py-2 text-sm border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
              >
                <option value="">All Genders</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Prefer not to say">Prefer not to say</option>
                <option value="Others">Others</option>
              </select>
            </div>

            <!-- Year Level Filter -->
            <div>
              <label for="year-level" class="block text-xs font-medium text-gray-700 mb-1">
                Year Level
              </label>
              <select 
                id="year-level" 
                v-model="filters.year_level"
                @change="applyFilters"
                class="w-full px-3 py-2 text-sm border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
              >
                <option value="">All Levels</option>
                <option value="1st">1st</option>
                <option value="2nd">2nd</option>
                <option value="3rd">3rd</option>
                <option value="4th">4th</option>
                <option value="4th+">4th+</option>
              </select>
            </div>

            <!-- Program Filter -->
            <div>
              <label for="program" class="block text-xs font-medium text-gray-700 mb-1">
                Program
              </label>
              <select 
                id="program" 
                v-model="filters.program_code"
                @change="applyFilters"
                class="w-full px-3 py-2 text-sm border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
              >
                <option value="">All Programs</option>
                <option 
                  v-for="program in programs" 
                  :key="program.program_code" 
                  :value="program.program_code"
                >
                  {{ program.program_name }}
                </option>
              </select>
            </div>
          </div>

          <!-- Active Filters -->
          <div v-if="hasActiveFilters" class="mt-4 pt-4 border-t border-gray-200">
            <p class="text-xs font-medium text-gray-700 mb-2">Active Filters:</p>
            <div class="flex flex-wrap gap-2">
              <span 
                v-if="filters.gender" 
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
              >
                Gender: {{ filters.gender }}
                <button 
                  @click="removeFilter('gender')"
                  class="ml-1.5 inline-flex items-center justify-center w-4 h-4 rounded-full hover:bg-green-200 focus:outline-none"
                >
                  <X class="h-3 w-3" />
                </button>
              </span>
              
              <span 
                v-if="filters.year_level" 
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
              >
                Year: {{ filters.year_level }}
                <button 
                  @click="removeFilter('year_level')"
                  class="ml-1.5 inline-flex items-center justify-center w-4 h-4 rounded-full hover:bg-blue-200 focus:outline-none"
                >
                  <X class="h-3 w-3" />
                </button>
              </span>
              
              <span 
                v-if="filters.program_code" 
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800"
              >
                Program: {{ getProgramName(filters.program_code) }}
                <button 
                  @click="removeFilter('program_code')"
                  class="ml-1.5 inline-flex items-center justify-center w-4 h-4 rounded-full hover:bg-purple-200 focus:outline-none"
                >
                  <X class="h-3 w-3" />
                </button>
              </span>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Backdrop -->
    <div 
      v-if="isOpen"
      @click="closeDropdown"
      class="fixed inset-0 z-40"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Filter, X } from 'lucide-vue-next'
import axios from 'axios'

const emit = defineEmits(['filter-change'])

const isOpen = ref(false)
const filters = ref({
  gender: '',
  year_level: '',
  program_code: ''
})

const programs = ref([])

// Fetch programs on mount
onMounted(async () => {
  try {
    const response = await axios.get('/students/programs/list')
    if (response.data) {
      programs.value = response.data
    }
  } catch (error) {
    console.error('Failed to load programs:', error)
  }
})

// Computed properties
const hasActiveFilters = computed(() => {
  return filters.value.gender !== '' ||
         filters.value.year_level !== '' ||
         filters.value.program_code !== ''
})

const activeFilterCount = computed(() => {
  let count = 0
  if (filters.value.gender) count++
  if (filters.value.year_level) count++
  if (filters.value.program_code) count++
  return count
})

// Methods
const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const closeDropdown = () => {
  isOpen.value = false
}

const applyFilters = () => {
  const filterParams = {}
  
  if (filters.value.gender) {
    filterParams.gender = filters.value.gender
  }
  
  if (filters.value.year_level) {
    filterParams.year_level = filters.value.year_level
  }
  
  if (filters.value.program_code) {
    filterParams.program_code = filters.value.program_code
  }
  
  emit('filter-change', filterParams)
}

const clearFilters = () => {
  filters.value = {
    gender: '',
    year_level: '',
    program_code: ''
  }
  emit('filter-change', {})
}

const removeFilter = (filterName) => {
  filters.value[filterName] = ''
  applyFilters()
}

const getProgramName = (programCode) => {
  const program = programs.value.find(p => p.program_code === programCode)
  return program ? program.program_name : programCode
}
</script>