<template>
  <div class="whiteboard-app" :class="{ dark: isDark }">
    <router-view />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isDark = computed(() => route.query.dark_theme === 'true')
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.whiteboard-app {
  background: #ffffff;
  font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    sans-serif;
  min-height: 100vh;
}

.whiteboard-app.dark {
  background: #1e1e2e;
  color: #eee;
}
</style>
