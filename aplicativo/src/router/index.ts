import { createRouter, createWebHistory } from 'vue-router'

import DefaultLayout from '../layouts/DefaultLayout.vue'

import HomeView from '../views/HomeView.vue'
import CameraView from '../views/CameraView.vue'
import GamesView from '../views/GamesView.vue'
import SettingsView from '../views/SettingsView.vue'

const router = createRouter({
  history: createWebHistory(),

  routes: [
    {
      path: '/',
      component: DefaultLayout,

      children: [
        {
          path: '',
          name: 'home',
          component: HomeView
        },
        {
          path: 'jogos',
          name: 'games',
          component: GamesView
        },
        {
          path: 'configuracoes',
          name: 'settings',
          component: SettingsView
        }
      ]
    },

    {
      path: '/camera',
      name: 'camera',
      component: CameraView
    }
  ]
})

export default router