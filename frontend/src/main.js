import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // הייבוא של הראוטר שיצרנו

const app = createApp(App)
app.use(router) // חיבור הראוטר לאפליקציה
app.mount('#app')