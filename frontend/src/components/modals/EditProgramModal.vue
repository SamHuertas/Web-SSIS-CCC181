<script setup>
  import { watch, reactive, ref, onMounted } from 'vue';
  import { X, CircleCheckBig } from 'lucide-vue-next';
  import axios from 'axios';
  import ProgramValidator from '@/utils/programValidator.js';
  import { useToast } from 'vue-toastification';

  // Props
  const props = defineProps({
    isVisible: {
      type: Boolean,
      default: false
    },
    program: {
      type: Object,
      default: null
    }
  });

  // Emits
  const emit = defineEmits(['close', 'refreshTable']);

  const closeModal = () => {
    // Clear error message and reset form when closing
    errorMessage.value = '';
    form.program_code = '';
    form.program_name = '';
    form.college_code = '';
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

  const form = reactive({
    program_code: '',
    program_name: '',
    college_code: ''
  });

  const errorMessage = ref('');
  const isLoading = ref(false);

  const populateForm = () => {
    if (props.program) {
      form.program_code = props.program.program_code;
      form.program_name = props.program.program_name;
      form.college_code = props.program.college_code;
    } else {
      form.college_code = '';
      form.college_name = '';
      form.college_code = '';
    }
  };

  // Watch for program prop changes to populate form
  watch(() => props.college, (newProgram) => {
    populateForm();
  });

  // Also populate form when modal becomes visible
  watch(() => props.isVisible, (isVisible) => {
    if (isVisible) {
      populateForm();
      errorMessage.value = ''; 
    }
  });

  const toast = useToast();

  const submitProgram = async () => {
    errorMessage.value = '';
    isLoading.value = true;

    try {
      const validation = ProgramValidator.validateAndFormatProgram(form);
      
      if (!validation.isValid) {
        errorMessage.value = validation.error;
        isLoading.value = false;
        return;
      }

      // Send formatted data to backend for duplicate checking and DB operations
      const response = await axios.put(`/programs/${props.program.program_code}`, validation.formattedData);
      console.log("Program updated successfully:", response.data);
      
      // Success - refresh table and close modal
      emit('refreshTable');
      form.program_code = '';
      form.program_name = '';
      form.college_code = '';
      closeModal();

      // Show success toast notification
      toast.success("Program updated successfully!", {
        timeout: 3000,
        position: "bottom-right", 
        closeOnClick: false,
        hideProgressBar: false, 
        icon: CircleCheckBig,
        bodyClassName: "font-sans font-medium"
      });
      
    } catch (err) {
      console.error("Error updating program:", err);
      
      // Handle backend errors (duplicate validation, server errors)
      errorMessage.value = err.response?.data?.error || 'An error occurred while adding the program.';
    } finally {
      isLoading.value = false;
    }
  };

  const colleges = ref([]);
  const fetchColleges = async () => {
  try {
    const { data } = await axios.get("/colleges-list");
    colleges.value = data;
  } catch (err) {
    console.error("Error fetching colleges:", err);
  }
};
  
  onMounted(fetchColleges);
</script>

<template>
  <!-- Modal with transition built-in -->
  <Transition name="dialog">
    <div 
      v-if="isVisible" 
      class="fixed inset-0 z-50 bg-black/80"
      @click="closeOnBackdrop"
    >
      <div class="fixed left-1/2 top-1/2 z-50 grid w-full max-w-2xl -translate-x-1/2 -translate-y-1/2 gap-4 border bg-white p-6 shadow-lg duration-200 sm:rounded-lg">
        <!-- Close button -->
         <div>
            <div class="flex items-center justify-between mb-6">
                <h3 class="text-lg font-semibold text-gray-900">
                Edit College - {{ program?.program_code }}
                </h3>
                <button
                @click="closeModal"
                class="text-gray-400 hover:text-gray-600 focus:outline-none"
                >
                    <X class="h-5 w-5" />
                </button>
            </div>
            
            <div v-if="errorMessage" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p class="text-sm text-red-600">{{ errorMessage }}</p>
            </div>

            <form @submit.prevent="submitProgram" class="space-y-4">
                <div class="grid grid-cols-1 gap-4">
                    <div>
                        <label for="programcode" class="block text-sm font-medium text-gray-900 mb-1">Program Code</label>
                        <input
                        v-model="form.program_code"
                        id="programcode"
                        type="text"
                        required
                        :disabled="isLoading"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 sm:text-sm disabled:bg-gray-100 disabled:cursor-not-allowed"
                        placeholder="e.g. BSCS"
                        />
                    </div>
                </div>
                <div>
                    <div>
                        <label for="programname" class="block text-sm font-medium text-gray-900 mb-1">Program Name</label>
                        <input
                        v-model="form.program_name"
                        id="programname"
                        type="text"
                        required
                        :disabled="isLoading"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 sm:text-sm disabled:bg-gray-100 disabled:cursor-not-allowed"
                        placeholder="e.g. Bachelor of Science in Computer Science"
                        />
                    </div>
                </div>
                <div>
                    <label for="collegecode" class="block text-sm font-medium text-gray-900 mb-1">College</label>
                    <select
                        id="collegecode"
                        v-model="form.college_code"
                        required
                        :disabled="isLoading"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 sm:text-sm"
                    >
                        <option value="" disabled selected>Select a college</option>
                        <option v-for="college in colleges" :key="college.college_code" :value="college.college_code">
                        {{ college.college_code }} - {{ college.college_name }}
                        </option>
                    </select>
                </div>

                <div class="flex justify-end space-x-3 pt-6 border-gray-200">
                    <button
                        type="button"
                        @click="closeModal"
                        :disabled="isLoading"
                        class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-900 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors disabled:bg-gray-100 disabled:cursor-not-allowed"
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        :disabled="isLoading"
                        class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors disabled:bg-green-400 disabled:cursor-not-allowed"
                    >
                        <span v-if="isLoading">Updating...</span>
                        <span v-else>Update College</span>
                    </button>
                </div>
            </form>
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

/* Focus ring offset background utility */
.ring-offset-background {
  --tw-ring-offset-color: #ffffff;
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