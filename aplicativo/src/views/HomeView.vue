<template>
  <main class="home-page">

    <!-- Área da imagem -->
    <section class="image-section">
      <p class="section-label">Adicione uma foto</p>

      <button
        type="button"
        class="image-box"
        @click="openImageModal"
      >
        <img
          v-if="selectedPhoto"
          :src="selectedPhoto"
          alt="Imagem selecionada"
        />

        <span v-else class="add-image">
          +
        </span>
      </button>

      <div v-if="selectedPhoto" class="image-actions">
        <button
          type="button"
          @click="openImageModal"
        >
          Mudar imagem
        </button>

        <button
          type="button"
          class="danger-button"
          @click="removePhoto"
        >
          Excluir
        </button>
      </div>
    </section>

    <!-- Pesquisa do jogo -->
<section class="game-section">
  <p class="section-label">Escolha um jogo</p>

  <input
    id="game-search"
    v-model="search"
    type="search"
    placeholder="🔍 Pesquisar jogo"
    autocomplete="off"
    @focus="showGameResults = true"
  />

  <div
    v-if="showGameResults && search.trim() && filteredGames.length"
    class="game-results"
  >
    <button
      v-for="game in filteredGames"
      :key="game"
      type="button"
      :class="{ selected: selectedGame === game }"
      @click="selectGame(game)"
    >
      {{ game }}
    </button>
  </div>

  <p
    v-if="search.trim() && !filteredGames.length"
    class="no-results"
  >
    Nenhum jogo encontrado.
  </p>
</section>

    <!-- Processar -->
    <button
      type="button"
      class="process-button"
      :disabled="!selectedPhoto || !selectedGame"
      @click="processImage"
    >
      Processar imagem
    </button>

    <!-- Modal -->
    <ImageModal
      v-if="showImageModal"
      @close="closeImageModal"
      @image-selected="handleImageSelected"
    />

  </main>
</template>
<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

import ImageModal from '../components/ImageModal.vue'

import '../layouts/home.css'

const showImageModal = ref(false)

const selectedPhoto = ref<string | null>(null)

const search = ref('')
const selectedGame = ref<string | null>(null)
const showGameResults = ref(false)

const games = [
  'Free Fire',
  'Minecraft',
  'Fortnite',
  'GTA V',
  'Roblox',
  'League of Legends'
]

const filteredGames = computed(() => {
  const value = search.value.trim().toLowerCase()

  if (!value) {
    return []
  }

  return games.filter(game =>
    game.toLowerCase().includes(value)
  )
})

function openImageModal() {
  console.log('abriu modal')

  showImageModal.value = true
}

function closeImageModal() {
  showImageModal.value = false
}

function handleImageSelected(file: File) {
  console.log('📸 IMAGEM CHEGOU NO HOME:', file)

  setPhoto(file)
  
  console.log('🖼️ URL DA IMAGEM:', selectedPhoto.value)

  closeImageModal()
}

function setPhoto(file: File) {
  if (selectedPhoto.value) {
    URL.revokeObjectURL(selectedPhoto.value)
  }

  selectedPhoto.value = URL.createObjectURL(file)
}

function removePhoto() {
  if (selectedPhoto.value) {
    URL.revokeObjectURL(selectedPhoto.value)
  }

  selectedPhoto.value = null
}

function selectGame(game: string) {
  selectedGame.value = game
  search.value = game
  showGameResults.value = false
}


function processImage() {
  console.log('processando imagem')
}

onBeforeUnmount(() => {
  if (selectedPhoto.value) {
    URL.revokeObjectURL(selectedPhoto.value)
  }
})
</script>