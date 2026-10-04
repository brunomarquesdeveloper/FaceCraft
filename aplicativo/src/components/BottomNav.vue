<script setup lang="ts">
import { RouterLink } from 'vue-router'
import {
  House,
  Gamepad2,
  Settings
} from 'lucide-vue-next'
</script>

<template>
  <nav class="bottom-nav">
    <div class="bottom-nav-content">

      <RouterLink
        to="/"
        class="bottom-nav-item"
      >
        <House :size="22" />
        <span>Início</span>
      </RouterLink>

      <RouterLink
        to="/jogos"
        class="bottom-nav-item"
      >
        <Gamepad2 :size="22" />
        <span>Jogos</span>
      </RouterLink>

      <RouterLink
        to="/configuracoes"
        class="bottom-nav-item"
      >
        <Settings :size="22" />
        <span>Config.</span>
      </RouterLink>

    </div>
  </nav>
</template>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1000;

  background: var(--bs-body-bg);
  border-top: 1px solid var(--bs-border-color);

  padding-bottom: env(safe-area-inset-bottom);
}

.bottom-nav-content {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;

  display: flex;
  align-items: center;
  justify-content: space-around;
}

.bottom-nav-item {
  flex: 1;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  gap: 4px;

  padding: 10px 8px;

  color: var(--bs-secondary-color);
  text-decoration: none;

  font-size: 0.75rem;
}

.bottom-nav-item.router-link-active {
  color: var(--bs-primary);
}

.bottom-nav-item:hover {
  color: var(--bs-primary);
}
</style>