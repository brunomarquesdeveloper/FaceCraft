<template>
  <section class="games-view">
    <header class="games-header">
      <div>
        <h1>Meus jogos</h1>
        <p>Suas personalizações faciais salvas.</p>
      </div>

      <span class="games-count">
        {{ filteredFaces.length }}
      </span>
    </header>

    <!-- Busca por jogo -->
    <div class="search-box">
      <i class="bi bi-search" aria-hidden="true"></i>

      <input v-model="search" type="search" placeholder="Buscar jogo..." aria-label="Buscar jogo pelo nome" />

      <button v-if="search" class="clear-search" type="button" aria-label="Limpar busca" @click="search = ''">
        <i class="bi bi-x-lg" aria-hidden="true"></i>
      </button>
    </div>

    <!-- Lista de personalizações salvas -->
    <div v-if="filteredFaces.length" class="faces-list">
      <article v-for="face in filteredFaces" :key="face.id" class="face-card" :style="{ '--banner-color': face.color }">
        <div class="face-banner">
          <div class="banner-decoration" aria-hidden="true">
            <i class="bi bi-controller"></i>
          </div>

          <span class="saved-badge">
            <i class="bi bi-check-circle-fill" aria-hidden="true"></i>
            Salvo
          </span>

          <div class="banner-content">
            <span class="banner-label">JOGO</span>
            <h2>{{ face.game }}</h2>
          </div>
        </div>

        <div class="face-info">
          <div class="face-avatar" aria-hidden="true">
            <i class="bi bi-person-circle"></i>
          </div>

          <div class="face-details">
            <span class="face-subtitle">Nome salvo</span>
            <h3>{{ face.name }}</h3>
          </div>

          <button class="face-action" type="button" :aria-label="'Abrir ' + face.name" @click="openFace(face)">
            <i class="bi bi-chevron-right" aria-hidden="true"></i>
          </button>
        </div>
      </article>
    </div>

    <!-- Estado vazio -->
    <div v-else class="empty-state">
      <i class="bi bi-controller" aria-hidden="true"></i>

      <h2>
        {{ search.trim()
          ? 'Nenhum jogo encontrado'
          : 'Nenhuma personalização salva'
        }}
      </h2>

      <p>
        {{ search.trim()
          ? 'Tente buscar por outro nome.'
          : 'Suas personalizações salvas aparecerão aqui.'
        }}
      </p>

      <button v-if="search" type="button" @click="search = ''">
        Limpar busca
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import '../assets/styles/games.css'

interface SavedFace {
  id: number
  game: string
  name: string
  color: string
}

const search = ref('')

// Dados temporários para desenvolvimento da interface.
// Posteriormente, substituir pela fonte real das personalizações.
const savedFaces = ref<SavedFace[]>([
  {
    id: 1,
    game: 'GTA V',
    name: 'Meu personagem',
    color: '#493c75'
  },
  {
    id: 2,
    game: 'GTA V',
    name: 'Personagem masculino',
    color: '#355b68'
  },
  {
    id: 3,
    game: 'GTA V',
    name: 'Personagem feminino',
    color: '#75465f'
  },
  {
    id: 4,
    game: 'Hogwarts Legacy',
    name: 'Meu bruxo',
    color: '#665333'
  },
  {
    id: 5,
    game: 'Monster Hunter Wilds',
    name: 'Meu caçador',
    color: '#46614b'
  }
])

const filteredFaces = computed(() => {
  const term = search.value.trim().toLocaleLowerCase('pt-BR')

  if (!term) {
    return savedFaces.value
  }

  return savedFaces.value.filter(face =>
    face.game.toLocaleLowerCase('pt-BR').includes(term)
  )
})

function openFace(face: SavedFace) {
  console.log('Personalização selecionada:', face)

  // Futuramente, navegar para os detalhes
  // ou para o tutorial dessa personalização.
}
</script>