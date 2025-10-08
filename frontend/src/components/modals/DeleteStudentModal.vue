<script setup>
  import { watch, reactive, ref } from 'vue';
  import { TriangleAlert, CircleCheckBig } from 'lucide-vue-next';
  import axios from 'axios';
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
    // Clear error message and reset form when closing
    errorMessage.value = '';
    form.id_number = '';
    form.first_name = '';
    form.last_name = '';
    form.year_level = '';
    form.gender = '';
    form.program_code = '';
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
    id_number: '',
    first_name: '',
    last_name: '',
    year_level: '',
    gender: '',
    program_code: ''
  });

  const errorMessage = ref('');
  const isLoading = ref(false);
  const toast = useToast();

  const deleteStudent = async () => {
    isLoading.value = true;
    errorMessage.value = '';
    try{
        const response = await axios.delete(`/students/${props.student.id_number}`);
        console.log("Student deleted successfully:", response.data);
        emit('refreshTable');
        closeModal();

        // Show success toast notification
      toast.success("Student deleted successfully!", {
        timeout: 3000,
        position: "bottom-right", 
        closeOnClick: false,
        hideProgressBar: false, 
        icon: CircleCheckBig,
        bodyClassName: "font-sans font-medium"
      });

    } catch (err) {
      console.error("Error deleting student:", err);
    } finally {
      isLoading.value = false;
    }
  } 

</script>

<template>
  <!-- Modal with transition built-in -->
  <Transition name="dialog">
    <div 
      v-if="isVisible" 
      class="fixed inset-0 z-50 bg-black/80"
      @click="closeOnBackdrop"
    >
      <div class="fixed left-1/2 top-1/2 z-50 items-center grid w-full max-w-2xl -translate-x-1/2 -translate-y-1/2 gap-4 border bg-white p-6 shadow-lg duration-200 sm:rounded-lg">
         <div class="mt-3">
          <div class="flex items-center justify-center w-12 h-12 mx-auto bg-red-100 rounded-full mb-4">
                <TriangleAlert class="w-8 h-8 text-red-600 " />
            </div>

            <h3 class="text-lg font-semibold text-gray-900 text-center mb-2">
            Delete Program
            </h3>
            <p class="text-sm text-gray-500 text-center mb-2">
            Are you sure you want to delete the student {{student.id_number}} - {{student.first_name}} {{student.last_name}}?
            </p>
            <p class="text-sm text-gray-500 text-center mb-2">
            This action cannot be undone.
            </p>
            <div class="flex justify-end space-x-3 border-gray-200">
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
                        @click="deleteStudent"
                        :disabled="isLoading"
                        class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors disabled:bg-red-400 disabled:cursor-not-allowed"
                    >
                    Delete
                    </button>
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