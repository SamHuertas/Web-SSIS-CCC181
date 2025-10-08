<script setup>
    import { ContactRound, Plus, Search } from 'lucide-vue-next';
    import { ref, onMounted, computed } from 'vue'; 
    import EditButton from '@/components/ui/EditButton.vue';
    import DeleteButton from '@/components/ui/DeleteButton.vue';
    import AddStudentModal from '@/components/modals/AddStudentModal.vue';
    import EditStudentModal from '@/components/modals/EditStudentModal.vue';
    import DeleteStudentModal from '@/components/modals/DeleteStudentModal.vue';
    import axios from 'axios';

    // modal state
    const isAddModalVisible = ref(false);
    const isEditModalVisible = ref(false);
    const isDeleteModalVisible = ref(false);
    const selectedStudent = ref(null);
    
    // Modal functions
    const openAddModal = () => {
        isAddModalVisible.value = true;
    };
    
    const closeAddModal = () => {
        isAddModalVisible.value = false;
    };

    const openEditModal = (student) => {
        selectedStudent.value = { ...student };
        isEditModalVisible.value = true;
    };

    const closeEditModal = () => {
        selectedStudent.value = null;
        isEditModalVisible.value = false;
    };

    const openDeleteModal = (student) => {
        selectedStudent.value = { ...student };
        isDeleteModalVisible.value = true;
    };

    const closeDeleteModal = () => {
        selectedStudent.value = null;
        isDeleteModalVisible.value = false;
    };

    const students = ref([]);
    const loading = ref(true);
    const searchTerm = ref('');

    // Pagination state
    const currentPage = ref(1);
    const itemsPerPage = ref(5);

    // Sorting state
    const sortField = ref('id_number')
    const sortDirection = ref('asc')

    const handleSort = (field) => {
        if (sortField.value === field) {
            sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
        } else {
            sortField.value = field
            sortDirection.value = 'asc'
        }
        // Reset to first page when sorting
        currentPage.value = 1;
    }

    const fetchStudents = async () => {
        try {
            const { data } = await axios.get("/students");
            students.value = data;
            console.log(students.value);
        } catch (err) {
            console.error("Error fetching students:", err);
        } finally {
            loading.value = false;
        }
    };

    onMounted(fetchStudents);

    const forceRefresh = () => {
        fetchStudents();
        currentPage.value = 1; // Reset to first page on refresh
    }

    //sorted and filtered students
    const filteredAndSortedStudents = computed(() => {
        let filtered = students.value;

        //Apply search filter
        if(searchTerm.value){
            const term = searchTerm.value.toLowerCase();
            filtered = filtered.filter(student => 
                student.id_number.toLowerCase().includes(term) ||
                student.first_name.toLowerCase().includes(term) ||
                student.last_name.toLowerCase().includes(term) ||
                (student.program_code && student.program_code.toLowerCase().includes(term)) ||
                (student.year_level && student.year_level.toString().includes(term))
        );
    }

    // Apply sorting
        return [...filtered].sort((a, b) => {
            const aValue = a[sortField.value];
            const bValue = b[sortField.value];
            
            if (sortDirection.value === 'asc') {
                return aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
            } else {
                return aValue > bValue ? -1 : aValue < bValue ? 1 : 0;
            }
        });
    });

    // Pagination
    const totalPages = computed(() => {
        return Math.ceil(filteredAndSortedStudents.value.length / itemsPerPage.value);
    });

    const paginatedStudents = computed(() => {
        const startIndex = (currentPage.value - 1) * itemsPerPage.value;
        const endIndex = startIndex + itemsPerPage.value;
        return filteredAndSortedStudents.value.slice(startIndex, endIndex);
    });

    const startItem = computed(() => {
        return (currentPage.value - 1) * itemsPerPage.value + 1;
    });

    const endItem = computed(() => {
        const end = currentPage.value * itemsPerPage.value;
        return end > filteredAndSortedStudents.value.length ? filteredAndSortedStudents.value.length : end;
    });

    // Pagination functions
    const goToPage = (page) => {
        if (page >= 1 && page <= totalPages.value) {
            currentPage.value = page;
        }
    };

    const nextPage = () => {
        if (currentPage.value < totalPages.value) {
            currentPage.value++;
        }
    };

    const prevPage = () => {
        if (currentPage.value > 1) {
            currentPage.value--;
        }
    };
    
     // Generate page numbers for pagination buttons
    const pageNumbers = computed(() => {
        const pages = [];
        const total = totalPages.value;
        const current = currentPage.value;
        
        if (total <= 7) {
            // Show all pages if total pages is small
            for (let i = 1; i <= total; i++) {
                pages.push(i);
            }
        } else {
            // Show pages with ellipsis for larger sets
            if (current <= 4) {
                for (let i = 1; i <= 5; i++) pages.push(i);
                pages.push('...');
                pages.push(total);
            } else if (current >= total - 3) {
                pages.push(1);
                pages.push('...');
                for (let i = total - 4; i <= total; i++) pages.push(i);
            } else {
                pages.push(1);
                pages.push('...');
                for (let i = current - 1; i <= current + 1; i++) pages.push(i);
                pages.push('...');
                pages.push(total);
            }
        }
        return pages;
    });

    // Reset to first page when search term changes
    const handleSearch = () => {
        currentPage.value = 1;
    };
</script>

<template>
    <div class="flex-1 flex flex-col overflow-hidden">
      <main class="flex-1 overflow-auto p-6">
        <!-- Main white container that always fills screen but extends when needed -->
        <div class="bg-white rounded-lg shadow p-6 w-full  flex flex-col">
            <div class="space-y-6 flex-1 flex flex-col">

                <!-- Header Section -->
                <div class="flex items-center justify-between flex-shrink-0">
                    <div>
                        <h1 class="text-3xl font-bold text-gray-900 flex items-center gap-2">
                        <ContactRound class="h-8 w-8 text-blue-500"/>
                        Students
                        </h1>
                        <p class="text-gray-600 mt-2">Manage student records</p>
                    </div>
                    
                    <button @click="openAddModal"
                        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                        <Plus class="mr-2 h-4 w-4"/>
                        Add Student
                    </button>
                </div>
            
            <!-- Table Container - This will expand to fill space -->
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm flex-1 flex flex-col">

                <!-- Search Section -->
                <div class="p-6 pb-4 flex-shrink-0">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-gray-900">Student Records ({{filteredAndSortedStudents.length}})</h3>
                        <div class="flex items-center space-x-2">
                            <div class="relative">
                                <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4"/>
                                <input
                                    v-model="searchTerm"
                                    @input="handleSearch"
                                    type="text"
                                    placeholder="Search students..."
                                    class="pl-10 w-64 px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"/>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Table Section - Scrollable area -->
                <div class="px-6 pb-4 flex-1 overflow-hidden">
                    <div v-if="loading" class="text-center py-8 text-gray-500 h-full flex items-center justify-center">
                                Loading students...
                            </div>
                            <div v-else-if="students.length === 0" class="text-center py-8 text-gray-500 h-full flex items-center justify-center">
                                No students found. Add your first student!
                            </div>
                            <div v-else class="h-full flex flex-col">
                                <!-- Scrollable table container --> 
                                <div class="overflow-x-auto flex-1">
                                    <table class="w-full">
                                        <colgroup>
                                            <col class="w-1/12"> 
                                            <col class="w-1/6">
                                            <col class="w-1/4">
                                            <col class="w-1/12">
                                            <col class="w-1/12">
                                            <col class="w-1/6">
                                            <col class="w-1/6">
                                        </colgroup>

                                        <thead>
                                            <tr class="border-b border-gray-200">
                                                <th 
                                                    @click="handleSort('id_number')"
                                                    class="text-left py-3 px-4 font-medium text-gray-600 cursor-pointer hover:bg-gray-50 whitespace-nowrap"
                                                    >
                                                    Student ID
                                                        <span v-if="sortField === 'id_number'">
                                                        {{ sortDirection === 'asc' ? '↑' : '↓' }}
                                                        </span>
                                                </th>
                                                <th 
                                                    @click="handleSort('first_name')"
                                                    class="text-left py-3 px-4 font-medium text-gray-600 cursor-pointer hover:bg-gray-50 whitespace-nowrap"
                                                    >
                                                    First Name
                                                        <span v-if="sortField === 'first_name'">
                                                        {{ sortDirection === 'asc' ? '↑' : '↓' }}
                                                        </span>
                                                </th>
                                                <th 
                                                    @click="handleSort('last_name')"
                                                    class="text-left py-3 px-4 font-medium text-gray-600 cursor-pointer hover:bg-gray-50 whitespace-nowrap"
                                                    >
                                                    Last Name
                                                        <span v-if="sortField === 'last_name'">
                                                        {{ sortDirection === 'asc' ? '↑' : '↓' }}
                                                        </span>
                                                </th>
                                                <th 
                                                    @click="handleSort('program_code')"
                                                    class="text-left py-3 px-4 font-medium text-gray-600 cursor-pointer hover:bg-gray-50 whitespace-nowrap"
                                                    >
                                                    Course
                                                        <span v-if="sortField === 'program_code'">
                                                        {{ sortDirection === 'asc' ? '↑' : '↓' }}
                                                        </span>
                                                </th>
                                                <th 
                                                    @click="handleSort('year_level')"
                                                    class="text-center py-3 px-4 font-medium text-gray-600 cursor-pointer hover:bg-gray-50 whitespace-nowrap"
                                                    >
                                                    Year
                                                        <span v-if="sortField === 'year_level'">
                                                        {{ sortDirection === 'asc' ? '↑' : '↓' }}
                                                        </span>
                                                </th>
                                                <th 
                                                    @click="handleSort('gender')"
                                                    class="text-center py-3 px-4 font-medium text-gray-600 cursor-pointer hover:bg-gray-50 whitespace-nowrap"
                                                    >
                                                    Gender
                                                        <span v-if="sortField === 'gender'">
                                                        {{ sortDirection === 'asc' ? '↑' : '↓' }}
                                                        </span>
                                                </th>
                                                <th class="text-center py-3 px-4 font-medium text-gray-600 whitespace-nowrap">Actions</th>
                                            </tr>
                                        </thead>

                                        <tbody>
                                            <!--loopable for dynamic data or modified for pagination-->
                                            <tr 
                                            v-for="student in paginatedStudents"
                                            :key="student.id"
                                            class="border-b border-gray-100 hover:bg-gray-50"
                                            >
                                                <td class="py-3 px-4 font-mono text-sm">{{student.id_number}}</td>
                                                <td class="py-3 px-4 font-medium text-gray-900">{{student.first_name}}</td>
                                                <td class="py-3 px-4 font-medium text-gray-900">{{student.last_name}}</td>
                                                <td :class="['font-medium py-3 px-4', !student.program_code ? 'text-red-500' : 'text-gray-900']">{{student.program_code || 'NULL' }}</td>
                                                <td class="py-3 px-4 text-center">
                                                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 border border-gray-300">
                                                        {{student.year_level}}
                                                    </span>
                                                </td>
                                                <td class="py-3 px-4 text-center">
                                                    <span :class="[
                                                        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                                                        student.gender === 'Male' ? 'bg-blue-100 text-blue-800' :
                                                        student.gender === 'Female' ? 'bg-pink-100 text-pink-800' :
                                                        student.gender === 'Prefer not to say' ? 'bg-purple-100 text-purple-800' :
                                                        student.gender === 'Others' ? 'bg-yellow-100 text-yellow-800' :
                                                        'bg-gray-100 text-gray-800'
                                                    ]">
                                                        {{ student.gender }}
                                                    </span>
                                                </td>
                                                <td class="py-3 px-4">
                                                    <div class="flex items-center justify-center space-x-2">
                                                        <EditButton @click="openEditModal(student)" />
                                                        <DeleteButton @click="openDeleteModal(student)" />
                                                    </div>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            <div v-if="filteredAndSortedStudents.length === 0 && students.length > 0" class="text-center py-8 text-gray-500">
                                No students found matching your search.
                            </div>  
                        </div>
                    </div>

                    <!--Pagination-->
                    <div class="border-t border-gray-200">
                        <div class="flex items-center justify-between px-6 py-4">
                            <div class="flex items-center text-sm text-gray-700">
                                <span>
                                Showing {{startItem}} to {{endItem}} of {{filteredAndSortedStudents.length}} results
                                </span>
                            </div>

                            <div class="flex items-center space-x-4">
                                <div class="flex items-center space-x-2">
                                    <label for="itemsPerPage" class="text-sm text-gray-700">Show:</label>
                                    <select 
                                        v-model="itemsPerPage"
                                        @change="currentPage = 1"
                                        class="px-3 py-1.5 text-sm border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 bg-white"
                                    >
                                        <option :value="5">5</option>
                                        <option :value="10">10</option>
                                        <option :value="25">25</option>
                                        <option :value="50">50</option>
                                    </select>
                                </div>

                            <div class="flex items-center space-x-1">
                                    <button
                                        @click="prevPage"
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
                                    
                                    <button
                                        v-for="page in pageNumbers"
                                        :key="page"
                                        @click="page !== '...' && goToPage(page)"
                                        :class="[
                                        'px-3 py-1.5 text-sm font-medium rounded-md border transition-colors',
                                        page === '...'
                                            ? 'text-gray-500 bg-white border-gray-300 cursor-default'
                                            : page === currentPage
                                            ? 'text-white bg-green-600 border-green-600 shadow-sm'
                                            : 'text-gray-700 bg-white border-gray-300 hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500'
                                        ]"
                                        :disabled="page === '...'"
                                    >
                                        {{ page }}
                                    </button>

                                    <button
                                        @click="nextPage"
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
        <AddStudentModal :is-visible="isAddModalVisible"  @close="closeAddModal" @refreshTable="forceRefresh" /> 
        <EditStudentModal :is-visible="isEditModalVisible" :student="selectedStudent" @close="closeEditModal" @refreshTable="forceRefresh" />
        <DeleteStudentModal :is-visible="isDeleteModalVisible" :student="selectedStudent" @close="closeDeleteModal" @refreshTable="forceRefresh" />
    </main>
    </div>
</template>
