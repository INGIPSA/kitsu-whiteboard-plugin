<template>
  <div class="whiteboard-page">
    <!-- Board List -->
    <div class="board-list-view" v-if="!store.currentBoard">
      <div class="board-header">
        <h2>Boards</h2>
        <button class="btn" @click="createBoard">+ New Board</button>
      </div>
      <div class="board-grid" v-if="store.boards.length">
        <div class="board-card" :key="b.id" @click="store.openBoard(b)" v-for="b in store.boards">
          <div class="board-card-preview">
            <img :src="b.thumbnail" v-if="b.thumbnail" />
            <span v-else>Board</span>
          </div>
          <div class="board-card-info">
            <div class="board-card-top">
              <span class="board-card-name">{{ b.name }}</span>
              <div class="card-actions">
                <button
                  class="card-action-btn"
                  :title="b.visibility || 'private'"
                  @click.stop="cycleVisibility(b)"
                >
                  <lock-icon :size="12" v-if="!b.visibility || b.visibility === 'private'" />
                  <users-icon :size="12" v-else-if="b.visibility === 'team'" />
                  <globe-icon :size="12" v-else />
                </button>
                <button
                  class="card-action-btn"
                  :class="{ disabled: !b.visibility || b.visibility === 'private' }"
                  title="Copy link"
                  @click.stop="copyLink(b)"
                >
                  <link-icon :size="12" />
                </button>
                <button
                  class="card-action-btn card-delete"
                  title="Delete"
                  @click.stop="confirmDelete(b)"
                >
                  <trash2-icon :size="12" />
                </button>
              </div>
            </div>
            <span class="board-card-date">{{ formatDate(b.updated_at) }}</span>
          </div>
        </div>
      </div>
      <div class="empty" v-else>
        <p>No boards yet.</p>
        <button class="btn" @click="createBoard">+ New Board</button>
      </div>
    </div>

    <!-- Board Editor -->
    <div class="board-editor" v-else>
      <div class="editor-header">
        <button class="btn-back" @click="goBack">&larr; Boards</button>
        <span class="board-name">{{ store.currentBoard.name }}</span>
        <button class="btn" @click="saveBoard">Save</button>
        <button class="btn" @click="exportPNG">Export PNG</button>
      </div>
      <div class="editor-body">
        <board-canvas
          ref="canvasRef"
          :board="store.currentBoard"
          @canvas-changed="onCanvasChanged"
        />
        <board-entity-sidebar :shots="entities.shots.value" :assets="entities.assets.value" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { GlobeIcon, LinkIcon, LockIcon, Trash2Icon, UsersIcon } from 'lucide-vue-next'
import { useBoardsStore } from '../stores/boards'
import { useEntities } from '../composables/useEntities'
import BoardCanvas from './BoardCanvas.vue'
import BoardEntitySidebar from './BoardEntitySidebar.vue'

const route = useRoute()
const store = useBoardsStore()
const entities = useEntities()
const canvasRef = ref(null)
let pendingData = null
let saveTimer = null

const projectId = () => route.query.production_id

onMounted(() => {
  const pid = projectId()
  if (pid) {
    store.loadBoards(pid)
    entities.loadEntities(pid)
  }
})

async function createBoard() {
  const board = await store.createBoard(projectId())
  store.openBoard(board)
}

function goBack() {
  if (pendingData) saveBoard()
  store.closeBoard()
}

function onCanvasChanged({ data, thumbnail }) {
  pendingData = { data, thumbnail }
  if (saveTimer) clearTimeout(saveTimer)
  saveTimer = setTimeout(() => saveBoard(), 2000)
}

async function saveBoard() {
  if (!store.currentBoard || !pendingData) return
  await store.saveBoard({
    ...store.currentBoard,
    canvas_data: pendingData.data,
    thumbnail: pendingData.thumbnail
  })
  pendingData = null
}

async function cycleVisibility(board) {
  const cycle = { private: 'team', team: 'public', public: 'private' }
  const next = cycle[board.visibility || 'private']
  await store.saveBoard({ ...board, visibility: next })
}

function copyLink(board) {
  if (!board.visibility || board.visibility === 'private') return
  const url = window.location.href.split('#')[0] + '#/?board_id=' + board.id
  navigator.clipboard.writeText(url).catch(() => {})
}

async function confirmDelete(board) {
  if (confirm(`Delete "${board.name}"?`)) {
    await store.deleteBoard(board.id)
  }
}

function exportPNG() {
  canvasRef.value?.exportAsPNG()
}

function formatDate(d) {
  if (!d) return ''
  return new Date(d).toLocaleString()
}
</script>

<style scoped>
.whiteboard-page { display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
.board-list-view { padding: 20px; }
.board-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.board-header h2 { margin: 0; color: #eee; }
.btn { padding: 6px 14px; border: 1px solid #555; border-radius: 4px; background: transparent; color: #eee; cursor: pointer; font-size: 13px; }
.btn:hover { background: #333; }
.btn-back { padding: 4px 10px; border: 1px solid #555; border-radius: 4px; background: transparent; color: #ccc; cursor: pointer; font-size: 13px; }
.board-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
.board-card { border: 1px solid #444; border-radius: 8px; overflow: hidden; cursor: pointer; background: #2a2a2a; }
.board-card:hover { border-color: #3b82f6; }
.board-card-preview { height: 140px; display: flex; align-items: center; justify-content: center; background: #1e1e1e; color: #666; overflow: hidden; }
.board-card-preview img { width: 100%; height: 100%; object-fit: cover; }
.board-card-info { padding: 10px 12px; }
.board-card-top { display: flex; align-items: center; justify-content: space-between; }
.board-card-name { font-size: 14px; font-weight: 500; color: #fff; }
.card-actions { display: flex; gap: 2px; }
.card-action-btn { width: 22px; height: 22px; border: none; background: transparent; color: #999; border-radius: 3px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.card-action-btn:hover { background: rgba(255,255,255,0.1); color: #fff; }
.card-action-btn.disabled { opacity: 0.3; pointer-events: none; }
.card-delete:hover { background: rgba(255,0,0,0.15); color: #e53e3e; }
.board-card-date { font-size: 11px; color: #888; }
.empty { text-align: center; padding: 60px 20px; color: #888; }
.editor-header { display: flex; align-items: center; gap: 12px; padding: 8px 16px; border-bottom: 1px solid #333; background: #2a2a2a; }
.board-name { font-size: 16px; font-weight: 500; color: #fff; flex: 1; }
.editor-body { display: flex; flex: 1; overflow: hidden; }
</style>
