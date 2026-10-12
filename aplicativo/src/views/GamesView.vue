<template>
  <section class="games-view">
    <header class="games-header">
      <div>
        <h1>Meus jogos</h1>
        <p>Suas personalizações faciais salvas.</p>
      </div>

      <span class="games-count">
        {{ filteredFaces.length }}
      </span>
    </header>

    <!-- Busca por jogo -->
    <div class="search-box">
      <i class="bi bi-search"></i>

      <input
        v-model="search"
        type="search"
        placeholder="Buscar jogo..."
        aria-label="Buscar jogo pelo nome"
      />

      <button
        v-if="search"
        class="clear-search"
        type="button"
        aria-label="Limpar busca"
        @click="search = ''"
      >
        <i class="bi bi-x-lg"></i>
      </button>
    </div>

    <!-- Lista de rostos salvos -->
    <div v-if="filteredFaces.length" class="faces-list">
      <article
        v-for="face in filteredFaces"
        :key="face.id"
        class="face-card"
        :style="{ '--banner-color': face.color }"
      >
        <div class="face-banner">
          <div class="banner-decoration">
            <i class="bi bi-controller"></i>
          </div>

          <span class="saved-badge">
            <i class="bi bi-check-circle-fill"></i>
            Salvo
          </span>

          <div class="banner-content">
            <span class="banner-label">JOGO</span>
            <h2>{{ face.game }}</h2>
          </div>
        </div>

        <div class="face-info">
          <div class="face-avatar">
            <i class="bi bi-person-circle"></i>
          </div>

          <div class="face-details">
            <span class="face-subtitle">Nome salvo</span>
            <h3>{{ face.name }}</h3>
          </div>

          <button
            class="face-action"
            type="button"
            :aria-label="'Abrir ' + face.name"
            @click="openFace(face)"
          >
            <i class="bi bi-chevron-right"></i>
          </button>
        </div>
      </article>
    </div>

    <!-- Nenhum resultado -->
    <div v-else class="empty-state">
      <i class="bi bi-controller"></i>

      <h2>Nenhum jogo encontrado</h2>

      <p>
        {{ search
          ? 'Tente buscar por outro nome.'
          : 'Suas personalizações salvas aparecerão aqui.'
        }}
      </p>

      <button
        v-if="search"
        type="button"
        @click="search = ''"
      >
        Limpar busca
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

interface SavedFace {
  id: number
  game: string
  name: string
  color: string
}

const search = ref('')

// Dados de exemplo para desenvolver a interface.
// Depois, substitua por dados do Supabase.
const savedFaces = ref<SavedFace[]>([
  {
    id: 1,
    game: 'GTA V',
    name: 'Meu personagem',
    color: '#493c75'
  },
  {
    id: 2,
    game: 'GTA V',
    name: 'Personagem masculino',
    color: '#355b68'
  },
  {
    id: 3,
    game: 'GTA V',
    name: 'Personagem feminino',
    color: '#75465f'
  },
  {
    id: 4,
    game: 'Hogwarts Legacy',
    name: 'Meu bruxo',
    color: '#665333'
  },
  {
    id: 5,
    game: 'Monster Hunter Wilds',
    name: 'Meu caçador',
    color: '#46614b'
  }
])

const filteredFaces = computed(() => {
  const term = search.value.trim().toLocaleLowerCase('pt-BR')

  if (!term) return savedFaces.value

  return savedFaces.value.filter(face =>
    face.game.toLocaleLowerCase('pt-BR').includes(term)
  )
})

function openFace(face: SavedFace) {
  console.log('Personalização selecionada:', face)

  // Futuramente, abrir a tela de detalhes
  // ou o tutorial da personalização selecionada.
}
</script>

<style scoped>
.games-view {
  padding: 24px 18px 100px;
  min-height: 100%;
  color: #f4f4f5;
}

.games-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 22px;
}

.games-header h1 {
  margin: 0 0 6px;
  font-size: 1.65rem;
  font-weight: 750;
  letter-spacing: -0.6px;
}

.games-header p {
  margin: 0;
  color: #9699a3;
  font-size: 0.9rem;
}

.games-count {
  display: grid;
  place-items: center;
  min-width: 36px;
  height: 36px;
  padding: 0 10px;
  border: 1px solid #343741;
  border-radius: 12px;
  background: #1c1e25;
  color: #d5d6dc;
  font-size: 0.85rem;
  font-weight: 700;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 12px;
  height: 50px;
  padding: 0 15px;
  margin-bottom: 22px;
  border: 1px solid #30333d;
  border-radius: 14px;
  background: #191b22;
  color: #a4a7b2;
}

.search-box:focus-within {
  border-color: #8b7cf6;
  box-shadow: 0 0 0 3px #8b7cf61a;
}

.search-box > i {
  font-size: 1.05rem;
}

.search-box input {
  width: 100%;
  min-width: 0;
  border: 0;
  outline: 0;
  background: transparent;
  color: #f4f4f5;
  font: inherit;
  font-size: 0.95rem;
}

.search-box input::placeholder {
  color: #777b87;
}

.clear-search {
  display: grid;
  place-items: center;
  width: 30px;
  height: 30px;
  flex-shrink: 0;
  border: 0;
  background: transparent;
  color: #b4b6c0;
}

.faces-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.face-card {
  overflow: hidden;
  border: 1px solid #30333d;
  border-radius: 18px;
  background: #1a1c23;
  transition: border-color 0.2s ease;
}

.face-card:active {
  border-color: #8b7cf6;
}

.face-banner {
  position: relative;
  display: flex;
  align-items: flex-end;
  min-height: 145px;
  padding: 18px;
  overflow: hidden;
  background:
    linear-gradient(
      90deg,
      color-mix(in srgb, var(--banner-color) 95%, #101116),
      color-mix(in srgb, var(--banner-color) 60%, #171820)
    );
}

.face-banner::after {
  position: absolute;
  inset: 0;
  content: '';
  background: linear-gradient(
    0deg,
    #101116a8,
    transparent 75%
  );
  pointer-events: none;
}

.banner-decoration {
  position: absolute;
  top: -30px;
  right: 5px;
  color: #ffffff12;
  transform: rotate(-14deg);
}

.banner-decoration i {
  font-size: 150px;
}

.saved-badge {
  position: absolute;
  top: 14px;
  left: 15px;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border: 1px solid #ffffff24;
  border-radius: 20px;
  background: #15151b75;
  color: #f4f4f5;
  font-size: 0.72rem;
  backdrop-filter: blur(8px);
}

.saved-badge i {
  color: #9de5b2;
}

.banner-content {
  position: relative;
  z-index: 1;
}

.banner-label {
  color: #ffffffa8;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 2px;
}

.banner-content h2 {
  margin: 4px 0 0;
  color: #fff;
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: -0.5px;
}

.face-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
}

.face-avatar {
  display: grid;
  place-items: center;
  width: 46px;
  height: 46px;
  flex-shrink: 0;
  border: 1px solid #373a45;
  border-radius: 14px;
  background: #242630;
  color: #c0b8ff;
  font-size: 1.65rem;
}

.face-details {
  flex: 1;
  min-width: 0;
}

.face-subtitle {
  display: block;
  margin-bottom: 4px;
  color: #9699a3;
  font-size: 0.75rem;
}

.face-details h3 {
  overflow: hidden;
  margin: 0;
  color: #f4f4f5;
  font-size: 0.95rem;
  font-weight: 650;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.face-action {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  border: 1px solid #343741;
  border-radius: 11px;
  background: #22242c;
  color: #c3c5cf;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-state > i {
  margin-bottom: 18px;
  color: #77718f;
  font-size: 3rem;
}

.empty-state h2 {
  margin-bottom: 8px;
  font-size: 1.1rem;
}

.empty-state p {
  max-width: 260px;
  color: #9699a3;
  font-size: 0.9rem;
}

.empty-state button {
  padding: 10px 16px;
  border: 1px solid #51458d;
  border-radius: 12px;
  background: #29243d;
  color: #d9d2ff;
}

@media (min-width: 700px) {
  .games-view {
    max-width: 900px;
    margin: 0 auto;
  }

  .faces-list {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    align-items: start;
  }
}
</style>