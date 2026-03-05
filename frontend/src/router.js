import { createRouter, createWebHistory } from 'vue-router'
import MiceView from './views/MiceView.vue'
import CompareView from './views/CompareView.vue'

const routes = [
  { path: '/', redirect: '/mice' }, // אם נכנסים לדף הראשי, קפוץ אוטומטית ל-Mice
  { path: '/mice', component: MiceView },
  { path: '/compare', component: CompareView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router