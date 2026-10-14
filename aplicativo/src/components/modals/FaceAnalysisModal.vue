<template>
  <Teleport to="body">
    <div
      class="face-analysis-overlay"
      @click.self="closeModal"
    >
      <section
        class="face-analysis-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="face-analysis-title"
      >
        <!-- Cabeçalho -->
        <header class="face-analysis-header">
          <button
            type="button"
            class="face-analysis-close"
            aria-label="Fechar análise"
            @click="closeModal"
          >
            &times;
          </button>

          <div class="face-analysis-heading">
            <span class="face-analysis-eyebrow">
              FACECRAFT
            </span>

            <h1 id="face-analysis-title">
              Análise facial
            </h1>

            <p class="face-analysis-game">
              {{ game || 'Nenhum jogo selecionado' }}
            </p>
          </div>

          <span class="face-analysis-icon" aria-hidden="true">
            ◎
          </span>
        </header>

        <!-- Conteúdo com rolagem -->
        <div class="face-analysis-content">
          <!-- Foto selecionada -->
          <section class="face-analysis-preview">
            <div class="face-analysis-photo">
              <img
                v-if="photo"
                :src="photo"
                alt="Foto utilizada na análise facial"
              />

              <span v-else class="face-analysis-no-photo">
                Foto indisponível
              </span>
            </div>

            <div class="face-analysis-photo-info">
              <h2>Seu rosto</h2>
              <p>Imagem selecionada para personalização</p>
            </div>
          </section>

          <!-- Lista de características -->
          <section class="face-analysis-results">
            <div class="face-analysis-section-heading">
              <div>
                <h2>Características faciais</h2>
                <p>Prévia dos parâmetros de personalização</p>
              </div>

              <span class="face-analysis-count">
                {{ characteristics.length }}
              </span>
            </div>

            <!--
              Valores demonstrativos.
              Substituir pelos resultados do serviço de
              análise facial quando a integração estiver pronta.
            -->
            <ul class="face-analysis-list">
              <li
                v-for="item in characteristics"
                :key="item.id"
                class="face-analysis-item"
              >
                <span
                  class="face-analysis-item-icon"
                  aria-hidden="true"
                >
                  {{ item.icon }}
                </span>

                <div class="face-analysis-item-info">
                  <span class="face-analysis-item-label">
                    {{ item.label }}
                  </span>

                  <span class="face-analysis-item-value">
                    {{ item.value }}
                  </span>
                </div>

                <span
                  class="face-analysis-item-status"
                  aria-label="Valor demonstrativo"
                >
                  •
                </span>
              </li>
            </ul>

            <p class="face-analysis-notice">
              Os valores exibidos são exemplos de interface,
              não resultados reais da análise facial.
            </p>
          </section>
        </div>

        <!-- Rodapé fixo -->
        <footer class="face-analysis-footer">
          <button
            type="button"
            class="face-analysis-save"
            @click="saveAnalysis"
          >
            <span aria-hidden="true">↧</span>
            Salvar personalização
          </button>

          <p>
            Você poderá identificar esta personalização
            pelo nome escolhido.
          </p>
        </footer>
      </section>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted } from 'vue'
import '../../assets/styles/face-analysis-modal.css'

/* =========================================
   PROPRIEDADES RECEBIDAS DA HOME
========================================= */

defineProps<{
  game: string | null
  photo: string | null
}>()

/* =========================================
   EVENTOS ENVIADOS PARA A HOME
========================================= */

const emit = defineEmits<{
  close: []
  save: []
}>()

/* =========================================
   CARACTERÍSTICAS FACIAIS
========================================= */

/*
 * Dados temporários para construir a interface.
 * A integração com o detector facial será responsável
 * por fornecer os valores reais posteriormente.
 */

const characteristics = [
  {
    id: 'face',
    icon: '◇',
    label: 'Formato do rosto',
    value: 'Não analisado'
  },
  {
    id: 'eyes',
    icon: '◎',
    label: 'Olhos',
    value: 'Não analisado'
  },
  {
    id: 'nose',
    icon: '⌁',
    label: 'Nariz',
    value: 'Não analisado'
  },
  {
    id: 'cheeks',
    icon: '◉',
    label: 'Bochechas',
    value: 'Não analisado'
  },
  {
    id: 'jaw',
    icon: '⬡',
    label: 'Mandíbula',
    value: 'Não analisado'
  },
  {
    id: 'chin',
    icon: '▽',
    label: 'Queixo',
    value: 'Não analisado'
  }
]

/* =========================================
   AÇÕES DO MODAL
========================================= */

function closeModal() {
  emit('close')
}

function saveAnalysis() {
  emit('save')
}

/* =========================================
   TECLA ESC
========================================= */

function handleKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape') {
    closeModal()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>