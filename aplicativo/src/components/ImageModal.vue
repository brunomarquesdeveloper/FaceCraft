<template>
  <div class="modal-overlay" @click.self="handleClose">

    <div class="modal">

      <!-- Escolha da origem -->
      <template v-if="!cameraActive">

        <h2>Inserir imagem</h2>

        <div class="modal-options">

          <button
            type="button"
            @click="openCamera"
          >
            📷
            <span>Câmera</span>
          </button>

          <button
            type="button"
            @click="handleFiles"
          >
            📁
            <span>Arquivos</span>
          </button>

          <button
            type="button"
            @click="handleClose"
          >
            ✕
            <span>Cancelar</span>
          </button>

        </div>

      </template>

      <!-- Câmera -->
      <template v-else>

        <h2>Tirar foto</h2>

        <video
          ref="video"
          autoplay
          playsinline
          muted
          class="camera-preview"
        />

        <p v-if="error" class="camera-error">
          {{ error }}
        </p>

        <div class="camera-actions">

          <button
            type="button"
            class="capture-button"
            @click="capturePhoto"
          >
            Capturar
          </button>

          <button
            type="button"
            class="back-button"
            @click="closeCamera"
          >
            Voltar
          </button>

        </div>

      </template>

    </div>

  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, ref } from 'vue'
import { requestCamera } from '../services/camera/camera'
import { selectPhoto } from '../services/camera/gallery'

const emit = defineEmits<{
  close: []
  imageSelected: [file: File]
}>()

const cameraActive = ref(false)
const video = ref<HTMLVideoElement | null>(null)
const error = ref('')

let stream: MediaStream | null = null

async function openCamera() {
  cameraActive.value = true
  error.value = ''

  try {
    stream = await requestCamera()

    if (video.value) {
      video.value.srcObject = stream
    }
  } catch (err) {
    console.error('Erro ao acessar a câmera:', err)

    error.value = 'Não foi possível acessar a câmera.'
  }
}

function closeCamera() {
  stopCamera()

  cameraActive.value = false
  error.value = ''
}

function stopCamera() {
  stream?.getTracks().forEach(track => track.stop())
  stream = null
}

function capturePhoto() {
  if (!video.value) return

  const canvas = document.createElement('canvas')

  canvas.width = video.value.videoWidth
  canvas.height = video.value.videoHeight

  const context = canvas.getContext('2d')

  if (!context) return

  context.drawImage(
    video.value,
    0,
    0,
    canvas.width,
    canvas.height
  )

  canvas.toBlob(blob => {
    if (!blob) return

    const file = new File(
      [blob],
      'facecraft-photo.jpg',
      {
        type: 'image/jpeg'
      }
    )

    stopCamera()

    emit('imageSelected', file)
  }, 'image/jpeg', 0.9)
}

async function handleFiles() {
  const file = await selectPhoto()

  if (!file) return

  emit('imageSelected', file)
}

function handleClose() {
  stopCamera()
  emit('close')
}

onBeforeUnmount(() => {
  stopCamera()
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 20px;

  background: rgba(0, 0, 0, 0.65);
}

.modal {
  width: 100%;
  max-width: 360px;

  padding: 24px;

  border-radius: 18px;

  background: #181b20;

  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}

.modal h2 {
  margin: 0 0 20px;

  text-align: center;

  font-size: 20px;
}

.modal-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);

  gap: 10px;
}

.modal-options button {
  min-height: 90px;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  gap: 8px;

  border: 0;
  border-radius: 12px;

  background: #242830;
  color: #fff;

  cursor: pointer;
}

.modal-options button:first-child {
  background: #20382f;
}

.modal-options span {
  font-size: 13px;
}

.camera-preview {
  width: 100%;
  aspect-ratio: 1 / 1;

  display: block;

  border-radius: 14px;

  object-fit: cover;

  background: #000;
}

.camera-error {
  margin: 12px 0;

  color: #ff6b6b;

  text-align: center;

  font-size: 14px;
}

.camera-actions {
  display: flex;
  flex-direction: column;

  gap: 10px;

  margin-top: 16px;
}

.capture-button,
.back-button {
  width: 100%;

  padding: 13px;

  border: 0;
  border-radius: 10px;

  color: #fff;

  font-size: 15px;

  cursor: pointer;
}

.capture-button {
  background: #42b883;
}

.back-button {
  background: #242830;
}
</style>