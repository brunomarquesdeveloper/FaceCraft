<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { requestCamera } from "../../services/camera/camera";
import { selectPhoto } from "../../services/camera/gallery";
import { analyzeFace, loadModels } from "../../services/faceApi";

const video = ref<HTMLVideoElement | null>(null)
const error = ref('')
const loading = ref(false)

const selectedPhoto = ref<string | null>(null)
const selectedFile = ref<File | null>(null)
const facialData = ref<FaceAnalysisResult | null>(null)

async function handleSelectPhoto() {
  const file = await selectPhoto()
  if (!file) return

  selectedFile.value = file
  selectedPhoto.value = URL.createObjectURL(file)
  facialData.value = null
}

async function handleAnalyze() {
  if (!selectedFile.value) return

  loading.value = true
  error.value = ''

  try {
    facialData.value = await analyzeFace(selectedFile.value)
  } catch (err: any) {
    console.error('Erro na análise:', err)
    error.value = err.message || 'Falha ao analisar a imagem.'
  } finally {
    loading.value = false
  }
}

let stream: MediaStream | null = null

onMounted(async () => {
  try {
    const [streamResult] = await Promise.all([
      requestCamera(),
      loadModels('/models')
    ])
    
    stream = streamResult
    if (video.value) {
      video.value.srcObject = stream
    }
  } catch (err) {
    console.error('Erro na inicialização:', err)
    error.value = 'Não foi possível acessar a câmera ou carregar os modelos de IA.'
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
  <main class="camera-view">
    <h1>FaceCraft - Câmera</h1>

    <div class="video-wrapper">
      <video ref="video" autoplay playsinline muted />
    </div>

    <div class="actions">
      <button type="button" @click="handleSelectPhoto">
        Selecionar foto da galeria
      </button>

      <button 
        type="button" 
        v-if="selectedFile" 
        @click="handleAnalyze" 
        :disabled="loading"
      >
        {{ loading ? 'Analisando...' : 'Analisar Rosto' }}
      </button>
    </div>

    <div v-if="selectedPhoto" class="preview-container">
      <h3>Foto Selecionada:</h3>
      <img :src="selectedPhoto" alt="Preview" class="preview-img" />
    </div>

    <p v-if="loading" class="loading-text">Processando dados faciais localmente...</p>

    <!-- Exibição simples temporária dos dados analisados -->
    <div v-if="facialData" class="results-box">
      <h3>Resultado da Análise:</h3>
      <p>Rosto detectado com sucesso!</p>
      <p>Confiança: {{ (facialData.detection.score * 100).toFixed(1) }}%</p>
    </div>

    <p v-if="error" class="error-msg">
      {{ error }}
    </p>
  </main>
</template>

<style scoped>
.camera-view {
  padding: 1rem;
  max-width: 600px;
  margin: 0 auto;
}
video, .preview-img {
  width: 100%;
  max-height: 250px;
  object-fit: cover;
  border-radius: 8px;
  margin-top: 0.5rem;
}
.actions {
  display: flex;
  gap: 10px;
  margin-top: 1rem;
}
button {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  border: none;
  background: #2563eb;
  color: white;
  cursor: pointer;
}
button:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}
.loading-text {
  color: #2563eb;
  margin-top: 1rem;
}
.error-msg {
  color: #dc2626;
  margin-top: 1rem;
}
.results-box {
  margin-top: 1rem;
  padding: 1rem;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
  color: #166534;
}
</style>