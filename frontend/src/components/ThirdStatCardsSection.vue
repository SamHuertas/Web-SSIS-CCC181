<script setup>
    import { University } from 'lucide-vue-next';
</script>

<template>
    <div class="grid grid-cols-1 lg:grid-cols-1 gap-6">
        <div class="bg-white border border-gray-200 rounded-lg shadow-sm">
            <div class="p-6 pb-4">
                <h3 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
                    <University class="h-5 w-5 text-purple-500" />
                    College Statistics
                </h3>
            </div>
            <div class="px-6 pb-6">
                <div class="overflow-x-auto">
                    <table class="w-full">
                        <thead>
                            <tr class="border-b border-gray-200">
                            <th class="text-left py-3 px-4 font-medium text-gray-600">College</th>
                            <th class="text-left py-3 px-4 font-medium text-gray-600">Code</th>
                            <th class="text-center py-3 px-4 font-medium text-gray-600">Programs</th>
                            <th class="text-center py-3 px-4 font-medium text-gray-600">Students</th>
                            </Tr>
                        </thead>
                        <tbody>
                            <!-- loopable rows for dynamic data-->
                            <tr class="border-b border-gray-100 hover:bg-gray-50">
                            <td class="py-3 px-4 font-medium text-gray-900">College of Computer Studies</td>
                            <td class="py-3 px-4 text-gray-600">CCS</td>
                            <td class="py-3 px-4 text-center">
                                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 border border-gray-300">
                                    10
                                </span>
                            </td>
                            <td class="py-3 px-4 text-center">
                                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 border border-gray-300">
                                    1000
                                </span>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>