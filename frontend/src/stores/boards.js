import { defineStore } from 'pinia'
import { ref } from 'vue'

const API_BASE = '/api/plugins/whiteboard'

async function api(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options
  })
  if (res.status === 204) return null
  return res.json()
}

export const useBoardsStore = defineStore('boards', () => {
  const boards = ref([])
  const currentBoard = ref(null)
  const loading = ref(false)

  async function loadBoards(projectId) {
    loading.value = true
    boards.value = await api(`/boards?project_id=${projectId}`)
    loading.value = false
  }

  async function createBoard(projectId, name = 'New Board') {
    const board = await api('/boards', {
      method: 'POST',
      body: JSON.stringify({ project_id: projectId, name })
    })
    boards.value.unshift(board)
    return board
  }

  async function saveBoard(board) {
    const updated = await api(`/boards/${board.id}`, {
      method: 'PUT',
      body: JSON.stringify(board)
    })
    const idx = boards.value.findIndex((b) => b.id === board.id)
    if (idx >= 0) boards.value[idx] = updated
    if (currentBoard.value?.id === board.id) currentBoard.value = updated
    return updated
  }

  async function deleteBoard(boardId) {
    await api(`/boards/${boardId}`, { method: 'DELETE' })
    boards.value = boards.value.filter((b) => b.id !== boardId)
    if (currentBoard.value?.id === boardId) currentBoard.value = null
  }

  function openBoard(board) {
    currentBoard.value = board
  }

  function closeBoard() {
    currentBoard.value = null
  }

  return {
    boards,
    currentBoard,
    loading,
    loadBoards,
    createBoard,
    saveBoard,
    deleteBoard,
    openBoard,
    closeBoard
  }
})
