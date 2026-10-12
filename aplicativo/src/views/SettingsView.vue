
<template>
  <section class="settings-view">
    <header class="settings-header">
      <h1>Configurações</h1>
      <p>Gerencie as preferências do FaceCraft.</p>
    </header>

    <!-- PERMISSÕES -->
    <section class="settings-section">
      <h2 class="section-title">Permissões</h2>

      <div class="settings-card">
        <div class="setting-item">
          <div class="setting-icon camera-icon">
            <Camera :size="21" />
          </div>

          <div class="setting-content">
            <h3>Câmera</h3>
            <p>{{ cameraDescription }}</p>

            <span class="permission-status" :class="cameraStatus">
              <span class="status-dot"></span>
              {{ cameraStatusLabel }}
            </span>
          </div>

          <button
            class="setting-action"
            type="button"
            :disabled="cameraLoading"
            @click="requestCamera"
          >
            {{ cameraLoading ? 'Aguarde...' : cameraButtonLabel }}
          </button>
        </div>

        <div class="setting-divider"></div>

        <div class="setting-item">
          <div class="setting-icon files-icon">
            <Images :size="21" />
          </div>

          <div class="setting-content">
            <h3>Fotos e arquivos</h3>
            <p>Selecione imagens do seu dispositivo.</p>
            <span class="permission-status neutral">
              <span class="status-dot"></span>
              Acesso sob demanda
            </span>
          </div>

          <button
            class="setting-action"
            type="button"
            @click="openFilePicker"
          >
            Abrir
          </button>

          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            hidden
            @change="handleFileSelection"
          />
        </div>

        <p
          v-if="permissionMessage"
          class="feedback-message"
          role="status"
        >
          {{ permissionMessage }}
        </p>
      </div>
    </section>

    <!-- DADOS LOCAIS -->
    <section class="settings-section">
      <div class="section-heading">
        <h2 class="section-title">Dados do aplicativo</h2>
        <span class="local-badge">
          <HardDrive :size="13" />
          Local
        </span>
      </div>

      <div class="settings-card">
        <div class="storage-summary">
          <div class="storage-icon">
            <Database :size="24" />
          </div>

          <div>
            <span class="storage-label">Armazenamento utilizado</span>
            <div class="storage-number">
              {{ formattedStorage }}
            </div>
            <p class="storage-description">
              Estimativa dos dados FaceCraft salvos neste navegador.
            </p>
          </div>
        </div>

        <div class="storage-meter">
          <div
            class="storage-meter-fill"
            :style="{ width: storageMeterWidth }"
          ></div>
        </div>

        <p class="storage-footnote">
          O indicador é visual e não representa o limite total do dispositivo.
        </p>

        <div class="setting-divider"></div>

        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-icon">
              <Gamepad2 :size="19" />
            </div>
            <span class="stat-value">{{ savedGamesCount }}</span>
            <span class="stat-label">Jogos salvos</span>
          </div>

          <div class="stat-item">
            <div class="stat-icon">
              <ScanFace :size="19" />
            </div>
            <span class="stat-value">{{ savedFacesCount }}</span>
            <span class="stat-label">Rostos salvos</span>
          </div>
        </div>

        <div class="setting-divider"></div>

        <button
          class="link-item"
          type="button"
          @click="goToGames"
        >
          <div class="setting-icon app-icon">
            <Gamepad2 :size="21" />
          </div>

          <div class="setting-content">
            <h3>Gerenciar jogos</h3>
            <p>Consultar suas personalizações salvas.</p>
          </div>

          <ChevronRight :size="19" class="chevron" />
        </button>

        <div class="setting-divider"></div>

        <div class="delete-area">
          <div class="delete-copy">
            <h3>Excluir todos os dados</h3>
            <p>
              Remove os jogos e rostos salvos localmente pelo FaceCraft.
            </p>
          </div>

          <button
            class="delete-button"
            type="button"
            :disabled="!hasSavedData"
            @click="showDeleteConfirmation = true"
          >
            <Trash2 :size="17" />
            Excluir tudo
          </button>
        </div>

        <p
          v-if="storageMessage"
          class="feedback-message"
          role="status"
        >
          {{ storageMessage }}
        </p>
      </div>
    </section>

    <!-- APLICATIVO -->
    <section class="settings-section">
      <h2 class="section-title">Sobre o aplicativo</h2>

      <div class="settings-card">
        <div class="setting-item">
          <div class="setting-icon app-icon">
            <Smartphone :size="21" />
          </div>

          <div class="setting-content">
            <h3>FaceCraft</h3>
            <p>Transforme seu rosto em um personagem.</p>
          </div>
        </div>

        <div class="setting-divider"></div>

        <div class="info-row">
          <span>Versão</span>
          <span class="info-value">{{ appVersion }}</span>
        </div>
      </div>
    </section>

    <!-- SUPORTE -->
    <section class="settings-section">
      <h2 class="section-title">Suporte</h2>

      <div class="settings-card">
        <button
          class="link-item"
          type="button"
          @click="showSupport = !showSupport"
        >
          <div class="setting-icon support-icon">
            <CircleHelp :size="21" />
          </div>

          <div class="setting-content">
            <h3>Ajuda e suporte</h3>
            <p>Orientações para usar o aplicativo.</p>
          </div>

          <ChevronRight
            :size="19"
            class="chevron"
            :class="{ rotated: showSupport }"
          />
        </button>

        <div v-if="showSupport" class="support-details">
          <p>
            <strong>Problemas com a câmera?</strong>
            Verifique a permissão do navegador e acesse o aplicativo por
            HTTPS ou localhost.
          </p>

          <p>
            <strong>Onde ficam meus dados?</strong>
            Esta seção contabiliza os dados FaceCraft armazenados no
            localStorage deste navegador.
          </p>

          <p>
            <strong>Precisa relatar um erro?</strong>
            Registre a mensagem apresentada e as etapas para reproduzi-lo.
          </p>
        </div>
      </div>
    </section>

    <!-- CRIADOR -->
    <section class="settings-section">
      <h2 class="section-title">Criador</h2>

      <div class="creator-card">
        <div class="creator-logo">
          <ScanFace :size="32" />
        </div>

        <div class="creator-info">
          <h3>FaceCraft</h3>
          <p>Personalização facial para seus jogos favoritos.</p>
          <span>Desenvolvido por Bruno Marques</span>
        </div>
      </div>

      <p class="footer-note">
        FaceCraft · v{{ appVersion }}
      </p>
    </section>

    <!-- CONFIRMAÇÃO DE EXCLUSÃO -->
    <Teleport to="body">
      <div
        v-if="showDeleteConfirmation"
        class="confirmation-backdrop"
        @click.self="showDeleteConfirmation = false"
        @keydown.esc="showDeleteConfirmation = false"
      >
        <section
          class="confirmation-dialog"
          role="alertdialog"
          aria-modal="true"
          aria-labelledby="delete-title"
          aria-describedby="delete-description"
        >
          <div class="confirmation-icon">
            <AlertTriangle :size="28" />
          </div>

          <h2 id="delete-title">Excluir todos os dados?</h2>

          <p id="delete-description">
            Você perderá os {{ savedFacesCount }} rostos salvos e os
            registros locais associados. Esta ação não pode ser desfeita.
          </p>

          <div class="confirmation-actions">
            <button
              class="cancel-button"
              type="button"
              @click="showDeleteConfirmation = false"
            >
              Cancelar
            </button>

            <button
              class="confirm-delete-button"
              type="button"
              @click="deleteAllData"
            >
              <Trash2 :size="17" />
              Excluir dados
            </button>
          </div>
        </section>
      </div>
    </Teleport>
  </section>
</template>

<script setup lang="ts">
import '../assets/styles/settings.css'
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  Camera,
  Images,
  Smartphone,
  CircleHelp,
  ChevronRight,
  Gamepad2,
  ScanFace,
  HardDrive,
  Database,
  Trash2,
  AlertTriangle
} from 'lucide-vue-next'

const router = useRouter()

const appVersion = '1.0.0'
const STORAGE_PREFIX = 'facecraft_'
const SAVED_FACES_KEY = 'facecraft_saved_faces'

interface SavedFace {
  id?: string | number
  game?: string
  gameId?: string | number
  game_id?: string | number
  name?: string
  [key: string]: unknown
}

const fileInput = ref<HTMLInputElement | null>(null)
const cameraPermission = ref<PermissionState | 'unknown'>('unknown')
const cameraLoading = ref(false)
const permissionMessage = ref('')
const storageMessage = ref('')
const showSupport = ref(false)
const showDeleteConfirmation = ref(false)

const savedFaces = ref<SavedFace[]>([])
const storageBytes = ref(0)
const showStorageMeter = ref(false)

let permissionStatus: PermissionStatus | null = null

const savedFacesCount = computed(() => savedFaces.value.length)

const savedGamesCount = computed(() => {
  const gameKeys = new Set(
    savedFaces.value.map(face => {
      const gameId = face.gameId ?? face.game_id

      if (gameId !== undefined && gameId !== null) {
        return String(gameId).trim().toLocaleLowerCase('pt-BR')
      }

      return (face.game ?? '').trim().toLocaleLowerCase('pt-BR')
    }).filter(Boolean)
  )

  return gameKeys.size
})

const hasSavedData = computed(() => {
  try {
    return Object.keys(localStorage).some(key =>
      key.startsWith(STORAGE_PREFIX)
    )
  } catch {
    return false
  }
})

const formattedStorage = computed(() => {
  if (storageBytes.value < 1024) {
    return `${storageBytes.value} B`
  }

  if (storageBytes.value < 1024 * 1024) {
    return `${(storageBytes.value / 1024).toFixed(1)} KB`
  }

  return `${(storageBytes.value / (1024 * 1024)).toFixed(2)} MB`
})

const storageMeterWidth = computed(() => {
  if (storageBytes.value === 0) return '0%'
  if (storageBytes.value < 1024) return '4%'
  if (storageBytes.value < 10 * 1024) return '12%'
  if (storageBytes.value < 100 * 1024) return '28%'
  if (storageBytes.value < 1024 * 1024) return '50%'
  return '75%'
})

const cameraStatus = computed(() => {
  if (cameraPermission.value === 'granted') return 'granted'
  if (cameraPermission.value === 'denied') return 'denied'
  if (cameraPermission.value === 'prompt') return 'pending'
  return 'neutral'
})

const cameraStatusLabel = computed(() => {
  if (cameraPermission.value === 'granted') return 'Permissão concedida'
  if (cameraPermission.value === 'denied') return 'Permissão bloqueada'
  if (cameraPermission.value === 'prompt') return 'Permissão necessária'
  return 'Ainda não verificada'
})

const cameraDescription = computed(() => {
  if (cameraPermission.value === 'granted') {
    return 'O navegador permite o acesso à câmera.'
  }

  if (cameraPermission.value === 'denied') {
    return 'Verifique as configurações de permissão do navegador.'
  }

  return 'Necessária para capturar fotos diretamente.'
})

const cameraButtonLabel = computed(() =>
  cameraPermission.value === 'granted' ? 'Verificar' : 'Permitir'
)

function readSavedFaces(): SavedFace[] {
  try {
    const raw = localStorage.getItem(SAVED_FACES_KEY)

    if (!raw) return []

    const parsed: unknown = JSON.parse(raw)

    return Array.isArray(parsed) ? parsed as SavedFace[] : []
  } catch {
    return []
  }
}

function refreshStorageData() {
  try {
    savedFaces.value = readSavedFaces()

    let bytes = 0

    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i)

      if (key?.startsWith(STORAGE_PREFIX)) {
        const value = localStorage.getItem(key) ?? ''
        bytes += new Blob([key + value]).size
      }
    }

    storageBytes.value = bytes
    showStorageMeter.value = true
  } catch {
    storageMessage.value =
      'Não foi possível consultar os dados locais deste navegador.'
  }
}

function handleStorageChange(event: StorageEvent) {
  if (!event.key || event.key.startsWith(STORAGE_PREFIX)) {
    refreshStorageData()
  }
}

async function refreshCameraPermission() {
  if (!navigator.permissions?.query) return

  try {
    permissionStatus = await navigator.permissions.query({
      name: 'camera' as PermissionName
    })

    cameraPermission.value = permissionStatus.state

    permissionStatus.onchange = () => {
      cameraPermission.value = permissionStatus?.state ?? 'unknown'
    }
  } catch {
    // Nem todos os navegadores permitem consultar esse estado.
  }
}

async function requestCamera() {
  permissionMessage.value = ''

  if (!navigator.mediaDevices?.getUserMedia) {
    permissionMessage.value =
      'Câmera indisponível. Verifique se está usando HTTPS ou localhost.'
    return
  }

  cameraLoading.value = true

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: false
    })

    stream.getTracks().forEach(track => track.stop())

    cameraPermission.value = 'granted'
    permissionMessage.value = 'Acesso à câmera verificado com sucesso.'
  } catch (error) {
    const err = error as DOMException

    if (err.name === 'NotAllowedError' || err.name === 'SecurityError') {
      permissionMessage.value =
        'Acesso negado. Verifique as permissões do navegador.'
    } else if (err.name === 'NotFoundError') {
      permissionMessage.value = 'Nenhuma câmera encontrada.'
    } else {
      permissionMessage.value =
        'Não foi possível acessar a câmera. Tente novamente.'
    }
  } finally {
    cameraLoading.value = false
    await refreshCameraPermission()
  }
}

function openFilePicker() {
  permissionMessage.value = ''
  fileInput.value?.click()
}

function handleFileSelection(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]

  if (file) {
    permissionMessage.value =
      `Arquivo selecionado: ${file.name}. Nenhum dado foi salvo por esta tela.`
  }

  input.value = ''
}

function goToGames() {
  router.push('/jogos')
}

function deleteAllData() {
  try {
    const keysToDelete: string[] = []

    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i)

      if (key?.startsWith(STORAGE_PREFIX)) {
        keysToDelete.push(key)
      }
    }

    keysToDelete.forEach(key => localStorage.removeItem(key))

    savedFaces.value = []
    storageBytes.value = 0
    storageMessage.value = 'Os dados locais do FaceCraft foram excluídos.'
    showDeleteConfirmation.value = false
  } catch {
    storageMessage.value =
      'Não foi possível excluir os dados. Verifique o armazenamento do navegador.'
    showDeleteConfirmation.value = false
    refreshStorageData()
  }
}

onMounted(() => {
  refreshStorageData()
  refreshCameraPermission()
  window.addEventListener('storage', handleStorageChange)
})

onUnmounted(() => {
  window.removeEventListener('storage', handleStorageChange)

  if (permissionStatus) {
    permissionStatus.onchange = null
  }
})
</script>