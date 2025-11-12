<script setup>
import { watch, computed } from 'vue';
import { X, User, Mail, Calendar, BookOpen, GraduationCap, Users } from 'lucide-vue-next';

// Props
const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false
  },
  student: {
    type: Object,
    default: null
  }
});

// Emits
const emit = defineEmits(['close']);

const closeModal = () => {
  emit('close');
};

// Close modal on Escape key
const handleKeydown = (event) => {
  if (event.key === 'Escape') {
    closeModal();
  }
};

// Close modal when clicking outside
const closeOnBackdrop = (event) => {
  if (event.target === event.currentTarget) {
    closeModal();
  }
};

// Add/remove event listener for Escape key
const setupKeyListener = () => {
  if (props.isVisible) {
    document.addEventListener('keydown', handleKeydown);
  } else {
    document.removeEventListener('keydown', handleKeydown);
  }
};

// Watch for visibility changes to manage event listener
watch(() => props.isVisible, setupKeyListener);

// Helper function to add cache-busting timestamp to image URLs
const getCacheBustedImageUrl = (url) => {
  if (!url) return null;
  const separator = url.includes('?') ? '&' : '?';
  return `${url}${separator}t=${Date.now()}`;
};

// Get gender badge color
const getGenderBadgeClass = computed(() => {
  if (!props.student) return 'bg-gray-100 text-gray-800';
  
  switch (props.student.gender) {
    case 'Male':
      return 'bg-blue-100 text-blue-800';
    case 'Female':
      return 'bg-pink-100 text-pink-800';
    case 'Prefer not to say':
      return 'bg-purple-100 text-purple-800';
    case 'Others':
      return 'bg-yellow-100 text-yellow-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
});
</script>

<template>
  <!-- Modal with transition built-in -->
  <Transition name="dialog">
    <div 
      v-if="isVisible && student" 
      class="fixed inset-0 z-50 bg-black/80"
      @click="closeOnBackdrop"
    >
      <div class="fixed left-1/2 top-1/2 z-50 grid w-full max-w-2xl -translate-x-1/2 -translate-y-1/2 gap-4 border bg-white p-6 shadow-lg duration-200 sm:rounded-lg">
        <!-- Close button -->
        <div>
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-gray-900">
              Student Details
            </h3>
            <button
              @click="closeModal"
              class="text-gray-400 hover:text-gray-600 focus:outline-none"
            >
              <X class="h-5 w-5" />
            </button>
          </div>

          <!-- Student Details Content -->
          <div class="space-y-6">
            <!-- Profile Picture and Basic Info Section -->
            <div class="flex items-start space-x-6 pb-6 border-b border-gray-200">
              <!-- Profile Picture -->
              <div class="flex-shrink-0">
                <div v-if="student.picture" class="w-32 h-32 rounded-lg overflow-hidden border-2 border-gray-200 shadow-md">
                  <img 
                    :src="getCacheBustedImageUrl(student.picture)" 
                    :key="student.picture + '-' + student.id_number"
                    :alt="`${student.first_name} ${student.last_name}`"
                    class="w-full h-full object-cover"
                  />
                </div>
                <div v-else class="w-32 h-32 rounded-lg bg-gray-200 flex items-center justify-center border-2 border-gray-300">
                  <User class="w-16 h-16 text-gray-500" />
                </div>
              </div>

              <!-- Name and ID -->
              <div class="flex-1">
                <h2 class="text-2xl font-bold text-gray-900 mb-2">
                  {{ student.first_name }} {{ student.last_name }}
                </h2>
                <p class="text-sm text-gray-600 font-mono mb-3">
                  ID: {{ student.id_number }}
                </p>
                <div class="flex items-center space-x-2">
                  <span :class="['inline-flex items-center px-3 py-1 rounded-full text-sm font-medium', getGenderBadgeClass]">
                    {{ student.gender }}
                  </span>
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-800 border border-gray-300">
                    {{ student.year_level }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Detailed Information Grid -->
            <div class="grid grid-cols-1 gap-4">
              <!-- Program -->
              <div class="flex items-start space-x-3 p-4 bg-gray-50 rounded-lg">
                <div class="flex-shrink-0">
                  <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                    <BookOpen class="w-5 h-5 text-green-600" />
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-500">Program</p>
                  <p :class="['text-base font-semibold mt-1', !student.program_code ? 'text-red-500' : 'text-gray-900']">
                    {{ student.program_code || 'Not Assigned' }}
                  </p>
                </div>
              </div>

              <!-- Year Level -->
              <div class="flex items-start space-x-3 p-4 bg-gray-50 rounded-lg">
                <div class="flex-shrink-0">
                  <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                    <GraduationCap class="w-5 h-5 text-blue-600" />
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-500">Year Level</p>
                  <p class="text-base font-semibold text-gray-900 mt-1">
                    {{ student.year_level }}
                  </p>
                </div>
              </div>

              <!-- Gender -->
              <div class="flex items-start space-x-3 p-4 bg-gray-50 rounded-lg">
                <div class="flex-shrink-0">
                  <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                    <Users class="w-5 h-5 text-purple-600" />
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-500">Gender</p>
                  <p class="text-base font-semibold text-gray-900 mt-1">
                    {{ student.gender }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Footer Actions -->
            <div class="flex justify-end pt-4 border-t border-gray-200">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-900 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
/* shadcn/ui inspired dialog transitions */
.dialog-enter-active,
.dialog-leave-active {
  transition: all 200ms ease-in-out;
}

/* Backdrop transitions */
.dialog-enter-from,
.dialog-leave-to {
  opacity: 0;
}

.dialog-enter-to,
.dialog-leave-from {
  opacity: 1;
}

/* Content transitions - combining fade, zoom, and slide */
.dialog-enter-active .bg-white,
.dialog-leave-active .bg-white {
  transition: all 200ms ease-in-out;
}

.dialog-enter-from .bg-white {
  opacity: 0;
  transform: translate(-50%, -52%) scale(0.95);
}

.dialog-leave-to .bg-white {
  opacity: 0;
  transform: translate(-50%, -48%) scale(0.95);
}

.dialog-enter-to .bg-white,
.dialog-leave-from .bg-white {
  opacity: 1;
  transform: translate(-50%, -50%) scale(1);
}

/* Screen reader only utility */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>