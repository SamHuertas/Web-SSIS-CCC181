<script setup>
  import { watch, reactive } from 'vue';
  import { X } from 'lucide-vue-next';
  import axios from 'axios';

  // Props
  const props = defineProps({
    isVisible: {
      type: Boolean,
      default: false
    }
  });

  // Emits
  const emit = defineEmits(['close', 'refreshTable']);

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

  const form = reactive({
    college_code: '',
    college_name: ''
  });

  const submitCollege = async () => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/colleges", form)
    console.log("College added:", response.data)
    emit('refreshTable');
  } catch (err) {
    console.error("Error adding college:", err)
  } finally {
    form.college_code = ''
    form.college_name = ''
    closeModal();
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
      <div class="fixed left-1/2 top-1/2 z-50 grid w-full max-w-2xl -translate-x-1/2 -translate-y-1/2 gap-4 border bg-white p-6 shadow-lg duration-200 sm:rounded-lg">
        <!-- Close button -->
         <div>
            <div class="flex items-center justify-between mb-6">
                <h3 class="text-lg font-semibold text-gray-900">
                Add New College
                </h3>
                <button
                @click="closeModal"
                class="text-gray-400 hover:text-gray-600 focus:outline-none"
                >
                    <X class="h-5 w-5" />
                </button>
            </div>

            <form @submit.prevent="submitCollege" class="space-y-4">
                <div class="grid grid-cols-1 gap-4">
                    <div>
                        <label for="collegecode" class="block text-sm font-medium text-gray-900 mb-1">College Code</label>
                        <input
                        v-model="form.college_code"
                        id="collegecode"
                        type="text"
                        required
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 sm:text-sm"
                        placeholder="e.g. CCS"
                        />
                    </div>
                </div>
                <div>
                    <div>
                        <label for="collegename" class="block text-sm font-medium text-gray-900 mb-1">College Name</label>
                        <input
                        v-model="form.college_name"
                        id="collegename"
                        type="text"
                        required
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 sm:text-sm"
                        placeholder="e.g. College of Computer Studies"
                        />
                    </div>
                </div>

                <div class="flex justify-end space-x-3 pt-6 border-gray-200">
                    <button
                        type="button"
                        @click="closeModal"
                        class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-900 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors"
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors"
                    >
                        Add College
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