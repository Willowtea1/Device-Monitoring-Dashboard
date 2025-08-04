// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import DeviceManagement from '../views/DeviceManagement.vue'
import Analytics from '../views/Analytics.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/devices', name: 'Device Management', component: DeviceManagement },
  { path: '/analytics', name: 'Analytics', component: Analytics },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
