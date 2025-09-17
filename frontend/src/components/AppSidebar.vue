<script setup>
import { LayoutDashboard, UserRound, GraduationCap, Building2 } from "lucide-vue-next";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarFooter,
} from "@/components/ui/sidebar"
import SidebarHeader from "./ui/sidebar/SidebarHeader.vue";

// Menu items.
</script>

<template>
  <div class="flex justify-center items-center min-h-screen">
    <Sidebar collapsible="none" class="w-64 border-r">
      <SidebarHeader class="text-center font-semibold text-l p-4 border-b"> 
        Student Information System 
      </SidebarHeader>
      <SidebarContent class="flex-1">
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu class="space-y-1">
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a to="/home" class="flex items-center gap-3 px-5 py-5 rounded-md hover:bg-gray-100 transition-colors">
                    <LayoutDashboard class="w-5 h-5" />
                    <span class="font-semibold">Dashboard</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
              
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a to="/profile" class="flex items-center gap-3 px-4 py-5 rounded-md hover:bg-gray-100 transition-colors">
                    <UserRound class="w-5 h-5" />
                    <span class="font-semibold">Students</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
              
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a to="/courses" class="flex items-center gap-3 px-4 py-5 rounded-md hover:bg-gray-100 transition-colors">
                    <GraduationCap class="w-5 h-5" />
                    <span class="font-semibold">Courses</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
              
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a to="/institutions" class="flex items-center gap-3 px-4 py-5 rounded-md hover:bg-gray-100 transition-colors">
                    <Building2 class="w-5 h-5" />
                    <span class="font-semibold">Colleges</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter class="text-center text-sm text-gray-600 p-4 border-t"> 
        Made by Sam Huertas 
      </SidebarFooter>
    </Sidebar>
  </div>
</template>