<template>
  <nav class="bottom-nav">
    <div class="bottom-nav-content">

      <RouterLink
        v-for="item in items"
        :key="item.path"
        :to="item.path"
        class="bottom-nav-item"
        :class="{ active: isActive(item.path) }"
      >
        <component :is="item.icon" :size="22" />

        <span>{{ item.label }}</span>
      </RouterLink>

    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  House,
  Gamepad2,
  Settings
} from 'lucide-vue-next'

const route = useRoute()

const items = [
  {
    label: 'Início',
    icon: House,
    path: '/'
  },
  {
    label: 'Jogos',
    icon: Gamepad2,
    path: '/jogos'
  },
  {
    label: 'Config.',
    icon: Settings,
    path: '/configuracoes'
  }
]

const currentPath = computed(() => route.path)

function isActive(path: string) {
  return currentPath.value === path
}
</script>

<style scoped>
.bottom-nav {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 100;

  background: #0f1115;
  border-top: 1px solid #24272d;
}

.bottom-nav-content {
  width: 100%;
  max-width: 480px;
  height: 68px;
  margin: 0 auto;

  display: flex;
  align-items: stretch;
  justify-content: space-around;
}

.bottom-nav-item {
  flex: 1;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;

  color: #777;
  text-decoration: none;

  font-size: 12px;
  font-weight: 500;

  transition:
    color 0.2s ease,
    background 0.2s ease;
}

.bottom-nav-item:hover {
  color: #aaa;
}

.bottom-nav-item.active {
  color: #42b883;
}

.bottom-nav-item.active svg {
  stroke-width: 2.5;
}

.bottom-nav-item span {
  line-height: 1;
}
</style>