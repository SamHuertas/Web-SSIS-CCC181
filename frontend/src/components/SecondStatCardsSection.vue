<script setup>
 import { TrendingUp, Building2 } from 'lucide-vue-next';
</script>

<template>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!--Students per College-->
        <div class="bg-white border border-gray-200 rounded-lg shadow-sm">
            <div class="p-6 pb-4">
                <h3 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
                <Building2 class="h-5 w-5 text-blue-500" />
                Students per College
                </h3>
            </div>

            <div class="px-6 pb-6">
                <div class="space-y-4">
                <!-- div with loopable data -->
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-3">
                        <div>
                            <div class="font-medium text-gray-900">College of Computer Studies</div>
                            <div class="text-sm text-gray-500">CCS</div>
                            </div>
                        </div>
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            12 students
                        </span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Top Courses by Enrollment-->
        <div class="bg-white border border-gray-200 rounded-lg shadow-sm">
            <div class="p-6 pb-4">
                <h3 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
                <TrendingUp class="h-5 w-5 text-green-500" />
                Top Courses by Enrollment
                </h3>
            </div>

            <div class="px-6 pb-6">
                <div class="space-y-4">
                <!-- div with loopable data -->
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-3">
                        <div class="flex items-center justify-center w-6 h-6 rounded-full bg-green-100 text-green-800 text-xs font-bold">
                            1
                        </div>
                        <div>
                            <div class="font-medium text-gray-900">Bachelor of Science in Computer Science</div>
                            <div class="text-sm text-gray-500">BSCS</div>
                            </div>
                        </div>
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            12 students
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
