<template>
  <div class="board-entity-sidebar">
    <div class="sidebar-header">
      <h3>Entities</h3>
      <div class="sidebar-tabs">
        <button class="tab-btn" :class="{ active: activeTab === 'shots' }" @click="activeTab = 'shots'">Shots</button>
        <button class="tab-btn" :class="{ active: activeTab === 'assets' }" @click="activeTab = 'assets'">Assets</button>
      </div>
      <input type="text" class="search-input" placeholder="Search..." v-model="searchText" />
    </div>
    <div class="entity-list">
      <div class="entity-item" :key="entity.id" draggable="true" @dragstart="onDragStart(entity, $event)" v-for="entity in filteredEntities">
        <div class="entity-thumbnail">
          <img :src="`/api/pictures/previews/preview-files/${entity.preview_file_id}.png`" v-if="entity.preview_file_id" @error="e => e.target.style.display='none'" />
          <span v-else style="color:#666;font-size:10px">No img</span>
        </div>
        <div class="entity-info">
          <span class="entity-name">{{ entity.name }}</span>
          <span class="entity-type">{{ entity.sequence_name || entity.asset_type_name || '' }}</span>
        </div>
      </div>
      <div class="empty-list" v-if="!filteredEntities.length">No entities</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  shots: { type: Array, default: () => [] },
  assets: { type: Array, default: () => [] }
})

const activeTab = ref('shots')
const searchText = ref('')

const currentEntities = computed(() => activeTab.value === 'shots' ? props.shots : props.assets)
const filteredEntities = computed(() => {
  if (!searchText.value) return currentEntities.value
  const q = searchText.value.toLowerCase()
  return currentEntities.value.filter(e => (e.name || '').toLowerCase().includes(q))
})

function onDragStart(entity, event) {
  event.dataTransfer.setData('application/json', JSON.stringify({
    id: entity.id, name: entity.name, type: activeTab.value === 'shots' ? 'Shot' : 'Asset',
    preview_file_id: entity.preview_file_id
  }))
}
</script>

<style scoped>
.board-entity-sidebar { width: 260px; border-left: 1px solid #333; background: #2a2a2a; display: flex; flex-direction: column; overflow: hidden; }
.sidebar-header { padding: 12px; border-bottom: 1px solid #333; }
.sidebar-header h3 { margin: 0 0 8px; font-size: 14px; color: #eee; }
.sidebar-tabs { display: flex; gap: 4px; margin-bottom: 8px; }
.tab-btn { flex: 1; padding: 4px 8px; font-size: 11px; border: 1px solid #444; border-radius: 4px; background: transparent; color: #ccc; cursor: pointer; }
.tab-btn.active { background: #3b82f6; border-color: #3b82f6; color: #fff; }
.search-input { width: 100%; padding: 6px 8px; border: 1px solid #444; border-radius: 4px; font-size: 12px; background: #1e1e1e; color: #eee; }
.entity-list { flex: 1; overflow-y: auto; padding: 8px; }
.entity-item { display: flex; align-items: center; padding: 6px; border-radius: 4px; cursor: grab; gap: 8px; margin-bottom: 4px; }
.entity-item:hover { background: #333; }
.entity-thumbnail { width: 48px; height: 36px; border-radius: 3px; overflow: hidden; flex-shrink: 0; background: #1e1e1e; display: flex; align-items: center; justify-content: center; }
.entity-thumbnail img { width: 100%; height: 100%; object-fit: cover; }
.entity-info { display: flex; flex-direction: column; min-width: 0; }
.entity-name { font-size: 12px; font-weight: 500; color: #eee; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.entity-type { font-size: 10px; color: #888; }
.empty-list { text-align: center; color: #666; font-size: 12px; padding: 20px; }
</style>
