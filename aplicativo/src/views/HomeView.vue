<template>
  <main class="home-page">
    <section class="home-card">
      <form class="home-form" @submit.prevent="processImage">
        <!-- Foto do rosto -->
        <section class="image-section">
          <h1 class="section-label">
            Adicione uma foto do rosto
          </h1>

          <button type="button" class="image-box" aria-label="Adicionar ou alterar foto do rosto"
            @click="openImageModal">
            <img v-if="selectedPhoto" :src="selectedPhoto" alt="Foto do rosto selecionada" />

            <span v-else class="add-image" aria-hidden="true">
              +
            </span>
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

          <!-- Resultados da pesquisa -->
          <div v-if="
            showGameResults &&
            search.trim() &&
            filteredGames.length
          " class="game-results">
            <button v-for="game in filteredGames" :key="game" type="button" :class="{ selected: selectedGame === game }"
              @click="selectGame(game)">
              {{ game }}
            </button>
          </div>

          <!-- Nenhum jogo encontrado -->
          <p v-if="
            showGameResults &&
            search.trim() &&
            !filteredGames.length
          " class="no-results">
            Nenhum jogo encontrado.
          </p>
        </section>

        <!-- Processamento da imagem -->
        <button type="submit" class="process-button"> <!-- :disabled="!selectedPhoto || !selectedGame" -->

          Processar imagem
        </button>
      </form>
    </section>

    <!-- Modal para selecionar uma foto -->
    <ImageModal v-if="showImageModal" @close="closeImageModal" @image-selected="handleImageSelected" />

    <!-- Modal de análise facial em tela cheia -->
    <FaceAnalysisModal v-if="showAnalysisModal" :game="selectedGame" :photo="selectedPhoto"
      @close="showAnalysisModal = false" @save="openSaveModal" />

    <!-- Mini modal para nomear a personalização -->
    <SaveFaceModal v-if="showSaveModal" @close="showSaveModal = false" @confirm="saveCustomization" />
  </main>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'

import ImageModal from '../components/modals/ImageModal.vue'
import FaceAnalysisModal from '../components/modals/FaceAnalysisModal.vue'
import SaveFaceModal from '../components/modals/SaveFaceModal.vue'

import '../assets/styles/home.css'

/* =========================================
   TIPOS
========================================= */

interface SavedCustomization {
  id: string
  name: string
  game: string
  photo: string
  createdAt: string
}

/* =========================================
   ESTADOS DOS MODAIS
========================================= */

const showImageModal = ref(false)
const showAnalysisModal = ref(false)
const showSaveModal = ref(false)

/* =========================================
   FOTO SELECIONADA
========================================= */

const selectedPhoto = ref<string | null>(null)

/* =========================================
   PESQUISA E SELEÇÃO DO JOGO
========================================= */

const search = ref('')
const selectedGame = ref<string | null>(null)
const showGameResults = ref(false)

/* Jogos disponíveis para pesquisa */
const games = [
  'Free Fire',
  'Minecraft',
  'Fortnite',
  'GTA V',
  'Roblox',
  'League of Legends'
]

/* Filtra os jogos conforme o texto pesquisado */
const filteredGames = computed(() => {
  const value = search.value.trim().toLowerCase()

  if (!value) return []

  return games.filter((game) =>
    game.toLowerCase().includes(value)
  )
})

/*
 * Se a pesquisa for alterada manualmente,
 * o jogo anteriormente selecionado deixa de ser válido.
 */
watch(search, (value) => {
  if (selectedGame.value && value !== selectedGame.value) {
    selectedGame.value = null
  }
})

/* =========================================
   MODAL DE IMAGEM
========================================= */

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

/* Cria uma URL temporária para exibir a imagem */
function setPhoto(file: File) {
  releasePhotoUrl()
  selectedPhoto.value = URL.createObjectURL(file)
}

/* Libera a URL temporária da imagem */
function releasePhotoUrl() {
  if (selectedPhoto.value) {
    URL.revokeObjectURL(selectedPhoto.value)
    selectedPhoto.value = null
  }
}

/* Remove a foto selecionada */
function removePhoto() {
  releasePhotoUrl()
}

/* =========================================
   SELEÇÃO DO JOGO
========================================= */

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

/* =========================================
   PROCESSAMENTO DA IMAGEM
========================================= */

function processImage() {
  console.log('FaceCraft: iniciar processamento', {
    game: selectedGame.value,
    photo: selectedPhoto.value
  })

  // Abre o modal de análise facial para testes.
  showAnalysisModal.value = true
}

/* =========================================
   MINI MODAL DE SALVAMENTO
========================================= */

function openSaveModal() {
  showSaveModal.value = true
}

/* =========================================
   SALVAR PERSONALIZAÇÃO
========================================= */

const STORAGE_KEY = 'facecraft_saved_faces'

async function saveCustomization(name: string) {
  const trimmedName = name.trim()

  if (
    !trimmedName ||
    !selectedGame.value ||
    !selectedPhoto.value
  ) {
    return
  }

  try {
    /*
     * Converte a foto temporária para Data URL,
     * permitindo persistir a imagem no armazenamento.
     */
    const response = await fetch(selectedPhoto.value)
    const blob = await response.blob()

    const photo = await new Promise<string>(
      (resolve, reject) => {
        const reader = new FileReader()

        reader.onload = () => {
          if (typeof reader.result === 'string') {
            resolve(reader.result)
          } else {
            reject(
              new Error('Não foi possível converter a foto.')
            )
          }
        }

        reader.onerror = () => {
          reject(new Error('Erro ao ler a foto.'))
        }

        reader.readAsDataURL(blob)
      }
    )

    /*
     * Recupera as personalizações existentes.
     */
    const storedData = localStorage.getItem(STORAGE_KEY)

    const existing: SavedCustomization[] = storedData
      ? JSON.parse(storedData)
      : []

    /*
     * Cria o registro da nova personalização.
     */
    const customization: SavedCustomization = {
      id: crypto.randomUUID(),
      name: trimmedName,
      game: selectedGame.value,
      photo,
      createdAt: new Date().toISOString()
    }

    existing.push(customization)

    /*
     * Persiste os dados localmente.
     */
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(existing)
    )

    console.log(
      'FaceCraft: personalização salva',
      customization
    )

    /* Fecha os modais após salvar */
    showSaveModal.value = false
    showAnalysisModal.value = false
  } catch (error) {
    console.error(
      'FaceCraft: erro ao salvar personalização',
      error
    )
  }
}

/* =========================================
   LIMPEZA
========================================= */

onBeforeUnmount(() => {
  releasePhotoUrl()
})
</script>