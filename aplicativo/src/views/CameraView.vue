<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { requestCamera } from '../services/camera/camera'

const video = ref<HTMLVideoElement | null>(null)
const error = ref('')

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

    <p v-if="error">
      {{ error }}
    </p>
  </main>
</template>