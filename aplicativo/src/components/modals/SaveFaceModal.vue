<template>
    <Teleport to="body">
        <div class="save-face-overlay" @click.self="closeModal">
            <section class="save-face-modal" role="dialog" aria-modal="true" aria-labelledby="save-face-title"
                aria-describedby="save-face-description">
                <!-- Cabeçalho -->
                <header class="save-face-header">
                    <div class="save-face-icon" aria-hidden="true">
                        <i class="bi bi-bookmark-plus"></i>
                    </div>

                    <button type="button" class="save-face-close" aria-label="Fechar janela" @click="closeModal">
                        <i class="bi bi-x-lg"></i>
                    </button>
                </header>

                <!-- Título e descrição -->
                <div class="save-face-heading">
                    <h2 id="save-face-title">
                        Salvar personalização
                    </h2>

                    <p id="save-face-description">
                        Escolha um nome para identificar esta
                        personalização facial na sua coleção de jogos.
                    </p>
                </div>

                <!-- Formulário -->
                <form class="save-face-form" @submit.prevent="confirmSave">
                    <label for="save-face-name">
                        Nome da personalização
                    </label>

                    <input id="save-face-name" ref="nameInput" v-model="name" type="text"
                        placeholder="Ex.: Meu personagem" autocomplete="off" maxlength="60" required
                        :aria-invalid="!!errorMessage" :aria-describedby="errorMessage ? 'save-face-error' : undefined
                            " @input="errorMessage = ''" />

                    <p v-if="errorMessage" id="save-face-error" class="save-face-error" role="alert">
                        {{ errorMessage }}
                    </p>

                    <p class="save-face-hint">
                        Você poderá salvar várias personalizações
                        para o mesmo jogo.
                    </p>

                    <!-- Ações -->
                    <div class="save-face-actions">
                        <button type="button" class="save-face-cancel" @click="closeModal">
                            Cancelar
                        </button>

                        <button type="submit" class="save-face-confirm" :disabled="!name.trim()">
                            <i class="bi bi-check2" aria-hidden="true"></i>
                            Salvar
                        </button>
                    </div>
                </form>
            </section>
        </div>
    </Teleport>
</template>

<script setup lang="ts">
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import '../../assets/styles/save-face-modal.css'

/* =========================================
   EVENTOS
========================================= */

const emit = defineEmits<{
    close: []
    confirm: [name: string]
}>()

/* =========================================
   ESTADO DO FORMULÁRIO
========================================= */

const name = ref('')
const errorMessage = ref('')
const nameInput = ref<HTMLInputElement | null>(null)

/* =========================================
   FECHAR MODAL
========================================= */

function closeModal() {
    emit('close')
}

/* =========================================
   CONFIRMAR SALVAMENTO
========================================= */

function confirmSave() {
    const trimmedName = name.value.trim()

    if (!trimmedName) {
        errorMessage.value = 'Digite um nome para continuar.'
        return
    }

    if (trimmedName.length > 60) {
        errorMessage.value = 'O nome deve ter até 60 caracteres.'
        return
    }

    emit('confirm', trimmedName)
}

/* =========================================
   TECLA ESC
========================================= */

function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
        closeModal()
    }
}

/* =========================================
   INICIALIZAÇÃO E LIMPEZA
========================================= */

onMounted(async () => {
    document.addEventListener('keydown', handleKeydown)

    await nextTick()
    nameInput.value?.focus()
})

onBeforeUnmount(() => {
    document.removeEventListener('keydown', handleKeydown)
})
</script>