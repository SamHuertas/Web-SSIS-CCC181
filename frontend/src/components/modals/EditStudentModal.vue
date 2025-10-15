<script setup>
    import { watch, reactive, ref, onMounted, computed } from 'vue';
    import { X, CircleCheckBig } from 'lucide-vue-next';
    import axios from 'axios';
    import StudentValidator from '@/utils/studentValidator.js';
    import { useToast } from 'vue-toastification';

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
    const emit = defineEmits(['close', 'refreshTable']);

    const closeModal = () => {
        emit('close');
        errorMessage.value = '';
        form.id_number = '';
        form.first_name = '';
        form.last_name = '';
        form.year_level = '';
        form.gender = '';
        form.program_code = '';
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
        id_number: '',
        first_name: '',
        last_name: '',
        year_level: '',
        gender: '',
        program_code: ''
    });

    const errorMessage = ref('');
    const isLoading = ref(false);

    const populateForm = () => {
        if (props.student) {
            form.id_number = props.student.id_number;
            form.first_name = props.student.first_name;
            form.last_name = props.student.last_name;
            form.year_level = props.student.year_level;
            form.gender = props.student.gender;
            form.program_code = props.student.program_code;
        } else {
            form.id_number = '';
            form.first_name = '';
            form.last_name = '';
            form.year_level = '';
            form.gender = '';
            form.program_code = '';
        }
    };

    // Watch for student prop changes to populate form
    watch(() => props.student, (newStudent) => {
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
    const submitStudent = async () => {
        errorMessage.value = '';
        isLoading.value = true;

        try {
        const validation = StudentValidator.validateAndFormatStudent(form);

        if (!validation.isValid) {
            errorMessage.value = validation.error;
            isLoading.value = false;
            return;
        }

        // Send formatted data to backend for duplicate checking and DB operations
        const response = await axios.put(`/students/${props.student.id_number}`, validation.formattedData);
        console.log("Student updated successfully:", response.data);

        // Success - refresh table and close modal
        emit('refreshTable');
        form.id_number = '';
        form.first_name = '';
        form.last_name = '';
        form.year_level = '';
        form.gender = '';
        form.program_code = '';
        closeModal();
        
        // Show success toast notification
      toast.success("Student updated successfully!", {
        timeout: 3000,
        position: "bottom-right", 
        closeOnClick: false,
        hideProgressBar: false, 
        icon: CircleCheckBig,
        bodyClassName: "font-sans font-medium"
      });

        } catch (err) {
        console.error("Error updating student:", err);

        // Handle backend errors (duplicate validation, server errors)
        errorMessage.value = err.response?.data?.error || 'An error occurred while adding the student.';
        } finally {
        isLoading.value = false;
        }
    };

    const programs = ref([]);
    const fetchPrograms = async () => {
  try {
    const { data } = await axios.get("/programs");
    programs.value = data;
  } catch (err) {
    console.error("Error fetching programs:", err);
  }
};
    
    onMounted(fetchPrograms);

const sortedPrograms = computed(() => {
  if (!programs.value) return [];
  return [...programs.value].sort((a, b) => 
    a.program_code.localeCompare(b.program_code)
  );
});
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
                Edit Student - {{ student ? student.first_name + ' ' + student.last_name : '' }}
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

            <form @submit.prevent="submitStudent" class="space-y-4">
                <div>
                    <label for="idnumber" class="block text-sm font-medium text-gray-900 mb-1">ID Number</label>
                    <input
                    v-model="form.id_number"
                    id="idnumber"
                    type="text"
                    required
                    :disabled="isLoading"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 sm:text-sm"
                    placeholder="Enter ID number"
                    />
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label for="firstname" class="block text-sm font-medium text-gray-900 mb-1">First Name</label>
                        <input
                        v-model="form.first_name"
                        id="firstname"
                        type="text"
                        required
                        :disabled="isLoading"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 sm:text-sm"
                        placeholder="Enter first name"
                        />
                    </div>
                    <div>
                        <label for="lastname" class="block text-sm font-medium text-gray-900 mb-1">Last Name</label>
                        <input
                        v-model="form.last_name"
                        id="lastname"
                        type="text"
                        required
                        :disabled="isLoading"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 sm:text-sm"
                        placeholder="Enter last name"
                        />
                    </div>
                </div>
                <div>
                    <label for="program" class="block text-sm font-medium text-gray-900 mb-1">Program</label>
                    <select
                        v-model="form.program_code"
                        id="program"
                        required
                        :disabled="isLoading"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 sm:text-sm"
                    >
                        <option value="" disabled selected>Select a program</option>
                        <option v-for="program in sortedPrograms" :key="program.program_code" :value="program.program_code">
                        {{ program.program_code }}
                        </option>
                    </select>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label for="year" class="block text-sm font-medium text-gray-900 mb-1">Year Level</label>
                        <select
                        v-model="form.year_level"
                        id="year"
                        required
                        :disabled="isLoading"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 sm:text-sm"
                        >
                        <option value="" disabled selected>Select a year level</option>
                        <option :value="'1st'">1st Year</option>
                        <option :value="'2nd'">2nd Year</option>
                        <option :value="'3rd'">3rd Year</option>
                        <option :value="'4th'">4th Year</option>
                        <option :value="'4th+'">4th+ Year</option>
                        </select>
                    </div>
                    
                    <div>
                        <label for="gender" class="block text-sm font-medium text-gray-900 mb-1">Gender</label>
                        <select
                        v-model="form.gender"
                        id="gender"
                        required
                        :disabled="isLoading"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 sm:text-sm"
                        >
                        <option value="" disabled selected>Select a gender</option>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Others">Others</option>
                        <option value="Prefer not to say">Prefer not to say</option>
                        </select>
                    </div>
                </div>

                <div class="flex justify-end space-x-3 pt-6 border-gray-200">
                    <button
                        type="button"
                        @click="closeModal"
                        :disabled="isLoading"
                        class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-900 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors"
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        :disabled="isLoading"
                        class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors"
                    >
                        <span v-if="isLoading">Updating...</span>
                        <span v-else>Update Student</span>
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