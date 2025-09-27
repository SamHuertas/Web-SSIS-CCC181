<script setup>
    import { School, Search, Plus } from 'lucide-vue-next';
    import EditButton from '@/components/EditButton.vue';
    import DeleteButton from '@/components/DeleteButton.vue';
    import { defineProps, onMounted, reactive, ref } from 'vue';
    import AddCollegeModal from '@/components/modals/AddCollegeModal.vue';
    import EditCollegeModal from '@/components/modals/EditCollegeModal.vue';


    // modal state
    const isAddModalVisible = ref(false);
    const isEditModalVisible = ref(false);
    const selectedCollege = ref(null);
    
    // Modal functions
    const openAddModal = () => {
        isAddModalVisible.value = true;
    };
    
    const closeAddModal = () => {
        isAddModalVisible.value = false;
    };

    const openEditModal = (college) => {
        selectedCollege.value = { ...college };
        isEditModalVisible.value = true;
    };
    
    const closeEditModal = () => {
        selectedCollege.value = null;
        isEditModalVisible.value = false;
    };

    const colleges = ref([]);
    const loading = ref(true);
    const searchTerm = ref('');
    const currentPage = ref(1);
    const totalPages = ref(1);

    const fetchColleges = async () => {
        try{
            const res = await fetch("http://127.0.0.1:8000/colleges");
            const data = await res.json();
            colleges.value = data;
            console.log(colleges)
        } catch (err) {
            console.error("Error fetching colleges:", err);
        } finally {
            loading.value = false;
        }
    }

    onMounted(fetchColleges);

    const forceRefresh = () => {
        fetchColleges();
    }

</script>

<template>
    <div class="flex-1 flex flex-col overflow-hidden">
        <main class="flex-1 overflow-auto p-6">
            <div class="bg-white rounded-lg shadow h-full p-6 space-y-6 w-full">
                <div class="space-y-6">
                    <div class="flex items-center justify-between">
                        <div>
                            <h1 class="text-3xl font-bold text-gray-900 flex items-center gap-2">
                            <School class="h-8 w-8 text-purple-500" />
                            Colleges
                            </h1>
                            <p class="text-gray-600 mt-2">Manage college departments</p>
                        </div>
                        <button @click="openAddModal" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                            <Plus class="mr-2 h-4 w-4" />
                            Add College
                        </button>
                    </div>

                    <div class="bg-white border border-gray-200 rounded-lg shadow-sm">
                        <div class="p-6 pb-4">
                            <div class="flex items-center justify-between mb-4">
                                <h3 class="text-lg font-semibold text-gray-900">College Departments ({{ colleges.length }})</h3>
                                <div class="flex items-center space-x-4">
                                    <div class="relative">
                                    <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                                    <input
                                        v-model="searchTerm"
                                        type="text"
                                        placeholder="Search by code or name..."
                                        class="pl-10 w-64 px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"/>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="px-6 pb-6">
                            <div v-if="loading" class="text-center py-8 text-gray-500">
                                Loading colleges...
                            </div>
                            <div v-else-if="colleges.length === 0" class="text-center py-8 text-gray-500">
                                No colleges found. Add your first college!
                            </div>
                            <div v-else class="overflow-x-auto">
                                <table class="w-full">
                                    <thead>
                                        <tr class="border-b border-gray-200">
                                            <th class="text-left py-3 px-4 font-medium text-gray-600 cursor-pointer hover:bg-gray-50">
                                                Code 
                                            </th>
                                            <th class="text-left py-3 px-4 font-medium text-gray-600 cursor-pointer hover:bg-gray-50">
                                                College Name 
                                            </th>
                                            <th class="text-center py-3 px-4 font-medium text-gray-600">Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <!--loopable for dynamic data or modified for pagination-->
                                        <tr
                                        v-for="college in colleges"
                                        :key="college.code"
                                         class="border-b border-gray-100 hover:bg-gray-50">
                                            <td class="py-3 px-4 font-mono font-medium text-purple-600">{{college.college_code}}</td>
                                            <td class="py-3 px-4 font-medium text-gray-900">{{college.college_name}}</td>
                                            <td class="py-3 px-4">
                                            <div class="flex items-center justify-center space-x-2">
                                                <EditButton @click="openEditModal(college)"/>
                                                <DeleteButton/>
                                            </div>
                                        </td>
                                        </tr>
                                    </tbody>
                                </table>
                                <!-- if no data searched 
                                <div v-if="paginatedStudents.length === 0" class="text-center py-8 text-gray-500">
                                    No programs found matching your search.
                                </div> -->
                            </div>
                        </div>

                         <!--Pagination-->
                         <div class="border-t border-gray-200">
                            <div class="flex items-center justify-between px-6 py-4">
                                <div class="flex items-center text-sm text-gray-700">
                                    <span>
                                    Showing 1 to 10 of 100 results
                                    </span>
                                </div>
                                
                                <div class="flex items-center space-x-4">
                                <div class="flex items-center space-x-2">
                                    <label for="itemsPerPage" class="text-sm text-gray-700">Show:</label>
                                    <select class="px-3 py-1.5 text-sm border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 bg-white"
                                    >
                                        <option :value="5">5</option>
                                        <option :value="10">10</option>
                                        <option :value="25">25</option>
                                        <option :value="50">50</option>
                                    </select>
                                </div>

                                <div class="flex items-center space-x-1">
                                    <button
                                        @click="currentPage = currentPage - 1"
                                        :disabled="currentPage === 1"
                                        :class="[
                                        'px-3 py-1.5 text-sm font-medium rounded-md border transition-colors',
                                        currentPage === 1
                                            ? 'text-gray-400 bg-gray-50 border-gray-200 cursor-not-allowed'
                                            : 'text-gray-700 bg-white border-gray-300 hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500'
                                        ]"
                                    >
                                        Previous
                                    </button>
                                    
                                    <div>
                                        <button
                                        class="
                                            px-3 py-1.5 text-sm font-medium rounded-md border transition-colors text-white bg-green-600 border-green-600 shadow-sm"
                                        >
                                        1
                                        </button>
                                        <span class="px-2 py-1.5 text-sm text-gray-500">...</span>
                                    </div>

                                    <button
                                        @click="currentPage = currentPage + 1"
                                        :disabled="currentPage === totalPages"
                                        :class="[
                                        'px-3 py-1.5 text-sm font-medium rounded-md border transition-colors',
                                        currentPage === totalPages
                                            ? 'text-gray-400 bg-gray-50 border-gray-200 cursor-not-allowed'
                                            : 'text-gray-700 bg-white border-gray-300 hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500'
                                        ]"
                                    >
                                        Next
                                    </button>
                                </div>
                            </div>
                            </div>
                         </div>
                    </div>
                </div>
            </div>
            <AddCollegeModal :is-visible="isAddModalVisible" @close="closeAddModal" @refreshTable="forceRefresh"/> 
            <EditCollegeModal :is-visible="isEditModalVisible" :college="selectedCollege" @close="closeEditModal" @refreshTable="forceRefresh" />
        </main>
    </div>
</template>