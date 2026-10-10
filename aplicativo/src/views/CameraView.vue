<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

import { requestCamera } from '../services/camera/camera'
import { selectPhoto } from '../services/camera/gallery'

import {
  analyzeFace,
  loadModels,
  mapToGame,
  EXAMPLE_PROFILE,
  type FaceAnalysis,
  type FaceWarning,
  type TraitKey,
} from '../services/faceApi'

type AnalysisSource = 'photo' | 'camera'

const TRAIT_LABELS: Record<TraitKey, string> = {
  faceLength: 'Comprimento do rosto',
  jawWidth: 'Largura da mandíbula',
  chinPointiness: 'Queixo pontudo',
  eyeSpacing: 'Distância entre os olhos',
  eyeSize: 'Tamanho dos olhos',
  eyeOpenness: 'Abertura dos olhos',
  noseWidth: 'Largura do nariz',
  noseLength: 'Comprimento do nariz',
  mouthWidth: 'Largura da boca',
  lipFullness: 'Volume dos lábios',
}

const FACE_SHAPE_LABELS: Record<string, string> = {
  oval: 'Oval',
  round: 'Redondo',
  square: 'Quadrado',
  heart: 'Coração',
  oblong: 'Alongado',
}

const WARNING_LABELS: Record<FaceWarning, string> = {
  MULTIPLE_FACES: 'Há mais de um rosto na imagem; foi usado o maior.',
  FACE_TOO_SMALL: 'O rosto está pequeno na imagem. Aproxime-se da câmera.',
  FACE_CUT_OFF: 'O rosto está cortado nas bordas da imagem.',
  LOW_CONFIDENCE: 'Baixa confiança na detecção. Use uma foto mais nítida.',
  HEAD_TILTED: 'A cabeça está inclinada. Mantenha-a reta.',
  HEAD_TURNED: 'O rosto não está de frente. Olhe direto para a câmera.',
  TOO_DARK: 'A imagem está escura. Procure um local mais iluminado.',
  OVEREXPOSED: 'A imagem está muito clara/estourada.',
}

const video = ref<HTMLVideoElement | null>(null)

const error = ref('')
const loading = ref(false)
const cameraReady = ref(false)

const selectedPhoto = ref<string | null>(null)
const selectedFile = ref<File | null>(null)

const analysis = ref<FaceAnalysis | null>(null)

const gameParams = computed(() =>
  analysis.value ? mapToGame(analysis.value, EXAMPLE_PROFILE) : null,
)

const traitRows = computed(() =>
  analysis.value
    ? (Object.keys(TRAIT_LABELS) as TraitKey[]).map((key) => ({
        key,
        label: TRAIT_LABELS[key],
        percent: Math.round(analysis.value!.traits[key] * 100),
      }))
    : [],
)

let stream: MediaStream | null = null
let currentObjectUrl: string | null = null
let isUnmounted = false

function releaseObjectUrl() {
  if (currentObjectUrl) {
    URL.revokeObjectURL(currentObjectUrl)
    currentObjectUrl = null
  }
}

function stopCamera() {
  stream?.getTracks().forEach((track) => track.stop())
  stream = null

  if (video.value) {
    video.value.srcObject = null
  }
}

function errorMessage(err: unknown, fallback: string): string {
  return err instanceof Error ? err.message : fallback
}

async function handleSelectPhoto() {
  error.value = ''

  try {
    const file = await selectPhoto()

    if (!file) return

    if (!file.type.startsWith('image/')) {
      error.value = 'Selecione um arquivo de imagem válido.'
      return
    }

    releaseObjectUrl()
    currentObjectUrl = URL.createObjectURL(file)

    selectedFile.value = file
    selectedPhoto.value = currentObjectUrl
    analysis.value = null
  } catch (err: unknown) {
    console.error('Erro ao selecionar a foto:', err)
    error.value = errorMessage(err, 'Não foi possível selecionar a foto.')
  }
}

function clearSelectedPhoto() {
  releaseObjectUrl()

  selectedPhoto.value = null
  selectedFile.value = null
  analysis.value = null
  error.value = ''
}

async function handleAnalyze(source: AnalysisSource) {
  if (loading.value) return

  let input: File | HTMLVideoElement | null = null

  if (source === 'photo') {
    input = selectedFile.value
  } else if (video.value && video.value.readyState >= 2) {
    input = video.value
  } else {
    error.value = 'A câmera ainda não está pronta.'
    return
  }

  if (!input) return

  loading.value = true
  error.value = ''
  analysis.value = null

  try {
    analysis.value = await analyzeFace(input)
  } catch (err: unknown) {
    console.error('Erro na análise facial:', err)
    error.value = errorMessage(err, 'Não foi possível analisar a imagem.')
  } finally {
    loading.value = false
  }
}

async function initializeCamera() {
  // Câmera e modelos são independentes: se um falhar, o outro continua útil
  // (ex.: sem permissão de câmera, ainda dá para analisar fotos da galeria).
  const [cameraResult, modelsResult] = await Promise.allSettled([
    requestCamera(),
    loadModels('/models'),
  ])

  // Se o usuário saiu da tela antes de terminar, libera a câmera na hora.
  if (isUnmounted) {
    if (cameraResult.status === 'fulfilled') {
      cameraResult.value.getTracks().forEach((track) => track.stop())
    }
    return
  }

  if (modelsResult.status === 'rejected') {
    console.error('Erro ao carregar modelos:', modelsResult.reason)
    error.value = errorMessage(
      modelsResult.reason,
      'Não foi possível carregar os modelos de IA.',
    )
  }

  if (cameraResult.status === 'rejected') {
    console.error('Erro ao acessar a câmera:', cameraResult.reason)
    error.value = errorMessage(
      cameraResult.reason,
      'Não foi possível acessar a câmera.',
    )
    return
  }

  stream = cameraResult.value

  if (video.value) {
    video.value.srcObject = stream

    try {
      await video.value.play()
    } catch (playError) {
      // Alguns navegadores iniciam a reprodução após interação do usuário.
      console.warn('A reprodução da câmera aguarda interação:', playError)
    }
  }

  cameraReady.value = modelsResult.status === 'fulfilled'
}

onMounted(() => {
  void initializeCamera()
})

onBeforeUnmount(() => {
  isUnmounted = true
  stopCamera()
  releaseObjectUrl()
})
</script>

<template>
  <main class="camera-view">
    <header class="page-header">
      <h1>FaceCraft</h1>
      <p>Análise facial para criação de personagens</p>
    </header>

    <section class="camera-section">
      <h2>Câmera</h2>

      <div class="video-wrapper">
        <video
          ref="video"
          autoplay
          playsinline
          muted
        />

        <p v-if="!cameraReady" class="camera-status">
          Inicializando câmera e modelos faciais...
        </p>
      </div>

      <div class="actions">
        <button
          type="button"
          class="primary-button"
          :disabled="loading || !cameraReady"
          @click="handleAnalyze('camera')"
        >
          {{ loading ? 'Analisando...' : 'Analisar pela câmera' }}
        </button>
      </div>
    </section>

    <section class="photo-section">
      <h2>Foto para análise</h2>

      <div v-if="selectedPhoto" class="preview-container">
        <img
          :src="selectedPhoto"
          alt="Foto selecionada para análise facial"
          class="preview-img"
        />

        <button
          type="button"
          class="secondary-button"
          :disabled="loading"
          @click="clearSelectedPhoto"
        >
          Remover foto
        </button>
      </div>

      <p v-else class="empty-state">
        Selecione uma foto da galeria para começar a análise.
      </p>

      <div class="actions">
        <button
          type="button"
          class="primary-button"
          :disabled="loading"
          @click="handleSelectPhoto"
        >
          Selecionar foto da galeria
        </button>

        <button
          v-if="selectedFile"
          type="button"
          class="primary-button"
          :disabled="loading"
          @click="handleAnalyze('photo')"
        >
          {{ loading ? 'Analisando...' : 'Analisar rosto' }}
        </button>
      </div>
    </section>

    <p v-if="loading" class="loading-text" role="status">
      Analisando os pontos e as proporções faciais...
    </p>

    <p v-if="error" class="error-msg" role="alert">
      {{ error }}
    </p>

    <section v-if="analysis" class="results-box">
      <h2>Resultado da análise</h2>

      <ul v-if="analysis.warnings.length" class="warning-list" role="status">
        <li v-for="warning in analysis.warnings" :key="warning">
          {{ WARNING_LABELS[warning] }}
        </li>
      </ul>

      <div class="metric-group">
        <h3>Resumo</h3>

        <ul>
          <li>
            <strong>Formato do rosto:</strong>
            {{ FACE_SHAPE_LABELS[analysis.faceShape] }}
          </li>

          <li v-if="analysis.skin">
            <strong>Tom de pele (aproximado):</strong>
            <span
              class="swatch"
              :style="{ background: analysis.skin.hex }"
              aria-hidden="true"
            />
            {{ analysis.skin.hex }}
          </li>

          <li>
            <strong>Confiança da detecção:</strong>
            {{ (analysis.score * 100).toFixed(1) }}%
          </li>
        </ul>
      </div>

      <div class="metric-group">
        <h3>Traços faciais</h3>

        <ul class="trait-list">
          <li v-for="row in traitRows" :key="row.key">
            <div class="trait-head">
              <span>{{ row.label }}</span>
              <span>{{ row.percent }}%</span>
            </div>
            <div class="bar" role="presentation">
              <div class="fill" :style="{ width: row.percent + '%' }" />
            </div>
          </li>
        </ul>
      </div>

      <details class="metric-group">
        <summary>Valores brutos (para calibração)</summary>

        <ul>
          <li v-for="row in traitRows" :key="row.key">
            {{ row.key }}: {{ analysis.ratios[row.key] }}
          </li>
          <li>
            Imagem: {{ analysis.image.width }} × {{ analysis.image.height }} px |
            rosto: {{ analysis.box.width }} px de largura
          </li>
        </ul>
      </details>

      <div v-if="gameParams" class="metric-group">
        <h3>Prévia: {{ EXAMPLE_PROFILE.name }}</h3>

        <ul>
          <li v-if="gameParams.facePreset">
            <strong>Preset de rosto:</strong> {{ gameParams.facePreset }}
          </li>

          <li v-for="(value, id) in gameParams.sliders" :key="id">
            <strong>{{ id }}:</strong> {{ value }}
          </li>
        </ul>
      </div>

      <p class="results-note">
        Os valores são estimativas baseadas nos pontos faciais detectados e
        dependem da pose, da expressão e da iluminação da foto. A confiança
        indica a certeza do detector, não a precisão da reconstrução facial.
        A imagem é processada no seu dispositivo.
      </p>
    </section>
  </main>
</template>

<style scoped>
.camera-view {
  width: 100%;
  max-width: 680px;
  margin: 0 auto;
  padding: 1rem;
  padding-bottom: 2rem;
  color: #e5e7eb;
}

.page-header {
  margin-bottom: 1.5rem;
}

.page-header h1 {
  margin: 0;
  font-size: 1.6rem;
}

.page-header p {
  margin: 0.25rem 0 0;
  color: #9ca3af;
}

.camera-section,
.photo-section {
  margin-bottom: 1.5rem;
}

.camera-view h2 {
  margin: 0 0 0.75rem;
  font-size: 1.15rem;
}

.video-wrapper {
  position: relative;
  overflow: hidden;
  min-height: 180px;
  background: #111827;
  border: 1px solid #374151;
  border-radius: 12px;
}

video,
.preview-img {
  display: block;
  width: 100%;
  max-height: 360px;
  object-fit: contain;
  border-radius: 12px;
}

video {
  min-height: 180px;
}

.preview-container {
  display: grid;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.preview-img {
  background: #111827;
}

.camera-status,
.empty-state {
  color: #9ca3af;
  font-size: 0.9rem;
}

.camera-status {
  padding: 0.75rem;
}

.empty-state {
  padding: 1rem;
  border: 1px dashed #4b5563;
  border-radius: 10px;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1rem;
}

button {
  min-height: 44px;
  padding: 0.7rem 1rem;
  border: 0;
  border-radius: 8px;
  font: inherit;
  font-weight: 600;
  cursor: pointer;
}

.primary-button {
  flex: 1 1 180px;
  background: #2563eb;
  color: #fff;
}

.secondary-button {
  background: #374151;
  color: #fff;
}

button:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.loading-text {
  margin-top: 1rem;
  color: #93c5fd;
}

.error-msg {
  margin-top: 1rem;
  padding: 0.75rem;
  color: #fecaca;
  background: #7f1d1d;
  border: 1px solid #b91c1c;
  border-radius: 8px;
  overflow-wrap: anywhere;
}

.results-box {
  margin-top: 1.5rem;
  padding: 1rem;
  color: #e5e7eb;
  background: #17231d;
  border: 1px solid #365b43;
  border-radius: 12px;
}

.results-box > h2 {
  margin-top: 0;
  font-size: 1.25rem;
}

.warning-list {
  margin: 0 0 1rem;
  padding: 0.75rem 0.75rem 0.75rem 1.75rem;
  color: #fde68a;
  background: #422006;
  border: 1px solid #a16207;
  border-radius: 8px;
  font-size: 0.9rem;
}

.metric-group {
  margin-top: 1.25rem;
}

.metric-group h3 {
  margin: 0 0 0.5rem;
  color: #86efac;
  font-size: 1rem;
}

.metric-group ul {
  margin: 0;
  padding-left: 1.25rem;
}

.metric-group li {
  margin-bottom: 0.5rem;
  line-height: 1.5;
  overflow-wrap: anywhere;
}

.trait-list {
  padding-left: 0;
  list-style: none;
}

.trait-head {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
}

.bar {
  height: 6px;
  margin-top: 0.25rem;
  overflow: hidden;
  background: #1f3a2a;
  border-radius: 999px;
}

.fill {
  height: 100%;
  background: #4ade80;
  border-radius: 999px;
}

.swatch {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  margin: 0 0.25rem;
  vertical-align: middle;
  border: 1px solid #6b7280;
  border-radius: 4px;
}

.results-note {
  margin: 1.25rem 0 0;
  padding-top: 0.75rem;
  color: #a7f3d0;
  border-top: 1px solid #365b43;
  font-size: 0.85rem;
  line-height: 1.5;
}

@media (max-width: 420px) {
  .camera-view {
    padding: 0.75rem;
  }

  .actions {
    flex-direction: column;
  }

  .primary-button {
    width: 100%;
  }
}
</style>
