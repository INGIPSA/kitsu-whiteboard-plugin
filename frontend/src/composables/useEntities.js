import { ref } from 'vue'

export function useEntities() {
  const shots = ref([])
  const assets = ref([])
  const loading = ref(false)

  async function loadEntities(projectId) {
    if (!projectId) return
    loading.value = true
    try {
      const [shotRes, assetRes] = await Promise.all([
        fetch(`/api/data/projects/${projectId}/shots`).then((r) => r.json()),
        fetch(`/api/data/projects/${projectId}/assets`).then((r) => r.json())
      ])
      shots.value = shotRes || []
      assets.value = assetRes || []
    } catch (e) {
      console.error('Failed to load entities:', e)
    }
    loading.value = false
  }

  return { shots, assets, loading, loadEntities }
}
