import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/styles/main.css'

console.log('🚀 FaceCraft PWA: configuração carregada')

createApp(App)
  .use(router)
  .mount('#app')