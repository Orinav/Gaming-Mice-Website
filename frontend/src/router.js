import { createRouter, createWebHistory } from 'vue-router'
import MiceView from './views/MiceView.vue'
import CompareView from './views/CompareView.vue'

const routes = [
  { path: '/', redirect: '/mice' },
  { path: '/mice', component: MiceView },
  { path: '/compare', component: CompareView }
]

const router = createRouter({
  history: createWebHistory(), // history determines how the URLs will look like, and createWebHistory() makes it look like normal URL (without # characters and etc).
  routes
})

export default router