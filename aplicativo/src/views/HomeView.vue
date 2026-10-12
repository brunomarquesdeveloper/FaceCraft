<template>
  <main class="home-page">
    <section class="home-card">
      <form class="home-form" @submit.prevent="processImage">
        <!-- Foto do rosto -->
        <section class="image-section">
          <h1 class="section-label">Adicione uma foto do rosto</h1>

          <button type="button" class="image-box" aria-label="Adicionar ou alterar foto do rosto"
            @click="openImageModal">
            <img v-if="selectedPhoto" :src="selectedPhoto" alt="Foto do rosto selecionada" />

            <span v-else class="add-image" aria-hidden="true">+</span>
          </button>

          <div v-if="selectedPhoto" class="image-actions">
            <button type="button" class="secondary-button" @click="openImageModal">
              Mudar imagem
            </button>

            <button type="button" class="danger-button" @click="removePhoto">
              Excluir
            </button>
          </div>
        </section>

        <!-- Escolha do jogo -->
        <section class="game-section">
          <label for="game-search" class="section-label">
            Escolha um jogo
          </label>

          <input id="game-search" v-model="search" type="search" placeholder="Pesquisar jogo..." autocomplete="off"
            @focus="showGameResults = true" @keydown.esc="showGameResults = false" />

          <div v-if="showGameResults && search.trim() && filteredGames.length" class="game-results">
            <button v-for="game in filteredGames" :key="game" type="button" :class="{ selected: selectedGame === game }"
              @click="selectGame(game)">
              {{ game }}
            </button>
          </div>

          <p v-if="showGameResults && search.trim() && !filteredGames.length" class="no-results">
            Nenhum jogo encontrado.
          </p>
        </section>

        <!-- Processamento -->
        <button type="submit" class="process-button" :disabled="!selectedPhoto || !selectedGame">
          Processar imagem
        </button>
      </form>
    </section>

    <ImageModal v-if="showImageModal" @close="closeImageModal" @image-selected="handleImageSelected" />
  </main>
</template>


<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import ImageModal from '../components/ImageModal.vue'
import '../assets/styles/home.css'

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

  if (!value) return []

  return games.filter(game =>
    game.toLowerCase().includes(value)
  )
})

// Se o usuário editar a pesquisa manualmente,
// o jogo anterior deixa de ser considerado selecionado.
watch(search, (value) => {
  if (selectedGame.value && value !== selectedGame.value) {
    selectedGame.value = null
  }
})

function openImageModal() {
  showImageModal.value = true
}

function closeImageModal() {
  showImageModal.value = false
}

function handleImageSelected(file: File) {
  if (!(file instanceof File)) return
  if (!file.type.startsWith('image/')) return

  setPhoto(file)
  closeImageModal()
}

function setPhoto(file: File) {
  releasePhotoUrl()
  selectedPhoto.value = URL.createObjectURL(file)
}

function releasePhotoUrl() {
  if (selectedPhoto.value) {
    URL.revokeObjectURL(selectedPhoto.value)
    selectedPhoto.value = null
  }
}

function removePhoto() {
  releasePhotoUrl()
}

function selectGame(game: string) {
  selectedGame.value = game
  search.value = game
  showGameResults.value = false
}

function clearSelectedGame() {
  selectedGame.value = null
  search.value = ''
  showGameResults.value = true
}

function processImage() {
  if (!selectedPhoto.value || !selectedGame.value) return

  console.log('FaceCraft: iniciar processamento', {
    game: selectedGame.value,
    photo: selectedPhoto.value
  })

  // Próxima etapa: integrar com o serviço de análise facial.
}

onBeforeUnmount(() => {
  releasePhotoUrl()
})
</script>