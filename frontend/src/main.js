import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'
import router from './router'
import 'vue-toastification/dist/index.css';
import Toast from 'vue-toastification';
import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:8000";

axios.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const isAuthEndpoint = error.config?.url?.includes('/auth/login') || 
                             error.config?.url?.includes('/auth/register');
      
      if (!isAuthEndpoint) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

const app = createApp(App)
app.use(router)
app.use(Toast)
app.mount('#app')
