import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Dashboard from './components/Dashboard.vue'
import VehicleDetail from './components/VehicleDetail.vue'
import './assets/main.css'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/vehicle/:id', name: 'VehicleDetail', component: VehicleDetail, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

createApp(App).use(router).mount('#app')
