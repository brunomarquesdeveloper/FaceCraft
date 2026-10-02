<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { requestCamera } from '../services/camera/camera'
import { selectPhoto } from '../services/camera/gallery'

const video = ref<HTMLVideoElement | null>(null)
const error = ref('')

const selectedPhoto = ref<string | null>(null)

async function handleSelectPhoto() {
  const file = await selectPhoto()

  if (!file) return

  selectedPhoto.value = URL.createObjectURL(file)
}

let stream: MediaStream | null = null

onMounted(async () => {
  try {
    stream = await requestCamera()

    if (video.value) {
      video.value.srcObject = stream
    }
  } catch (err) {
    console.error('Erro ao acessar a câmera:', err)
    error.value = 'Não foi possível acessar a câmera.'
  }
})

onBeforeUnmount(() => {
  stream?.getTracks().forEach(track => track.stop())

  if (selectedPhoto.value) {
    URL.revokeObjectURL(selectedPhoto.value)
  }
})
</script>

<template>
  <main>
    <h1>Câmera</h1>

    <video
      ref="video"
      autoplay
      playsinline
      muted
    />

    <button type="button" @click="handleSelectPhoto">
      Selecionar foto da galeria
    </button>

    <img
      v-if="selectedPhoto"
      :src="selectedPhoto"
      alt="Foto selecionada"
    />

    <p v-if="error">
      {{ error }}
    </p>
  </main>
</template>