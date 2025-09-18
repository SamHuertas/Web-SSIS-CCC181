<script setup>
    import { GraduationCap, Plus, Search } from 'lucide-vue-next';
    import EditButton from '@/components/EditButton.vue';
    import DeleteButton from '@/components/DeleteButton.vue';
</script>

<template>
    <div class="flex-1 flex flex-col overflow-hidden">
      <main class="flex-1 overflow-auto p-6">
        <div class="bg-white rounded-lg shadow h-full p-6 space-y-6 w-full">
            <div class="space-y-6">
                <div class="flex items-center justify-between">
                    <div>
                        <h1 class="text-3xl font-bold text-gray-900 flex items-center gap-2">
                        <graduation-cap class="h-8 w-8 text-green-500"/>
                        Programs
                        </h1>
                        <p class="text-gray-600 mt-2">Manage academic programs</p>
                    </div>
                
                    <button
                        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                        <Plus class="mr-2 h-4 w-4"/>
                        Add Program
                    </button>
                </div>

                <div class="bg-white border border-gray-200 rounded-lg shadow-sm">
                    <div class="p-6 pb-4">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-lg font-semibold text-gray-900">Academic Programs (4)</h3>
                            <div class="flex items-center space-x-2">
                                <div class="relative">
                                    <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4"/>
                                    <input
                                        v-model="searchTerm"
                                        type="text"
                                        placeholder="Search programs..."
                                        class="pl-10 w-64 px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                                    />
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="px-6 pb-6">
                        <div class="overflow-x-auto">
                            <table class="w-full">
                                <thead>
                                    <tr class="border-b border-gray-200">
                                        <th class="text-left py-3 px-4 font-medium text-gray-600 cursor-pointer hover:bg-gray-50"> Code </th>
                                        <th class="text-left py-3 px-4 font-medium text-gray-600 cursor-pointer hover:bg-gray-50"> Program Name </th>
                                        <th class="text-left py-3 px-4 font-medium text-gray-600 cursor-pointer hover:bg-gray-50"> College </th>
                                        <th class="text-center py-3 px-4 font-medium text-gray-600">Actions</th>
                                    </tr>
                                </thead>

                                <tbody>
                                    <!--loopable for dynamic data or modified for pagination-->
                                    <tr class="border-b border-gray-100 hover:bg-gray-50">
                                        <td class="py-3 px-4 font-mono font-medium text-green-600">BSCS</td>
                                        <td class="py-3 px-4 font-medium text-gray-900">Bachelor of Science in Computer Science</td>
                                        <td class="py-3 px-4">
                                            <div>
                                                <div class="font-medium">CCS</div>
                                                <div class="text-sm text-gray-500">College of Computer Studies</div>
                                            </div>
                                        </td>
                                        <td class="py-3 px-4">
                                            <div class="flex items-center justify-center space-x-2">
                                                <EditButton/>
                                                <DeleteButton/>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
    </div>
</template>