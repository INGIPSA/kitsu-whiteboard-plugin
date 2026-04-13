import { createRouter, createWebHashHistory } from 'vue-router'
import WhiteboardApp from './components/WhiteboardApp.vue'

const routes = [
  {
    path: '/',
    name: 'whiteboard',
    component: WhiteboardApp
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// Transfer Kitsu URL query params into hash-based route
let queryTransferred = false
router.beforeEach((to, from, next) => {
  if (!queryTransferred) {
    queryTransferred = true
    const realParams = new URLSearchParams(window.location.search)
    if (realParams.toString()) {
      const query = {}
      realParams.forEach((value, key) => {
        query[key] = value
      })
      next({ path: to.path, query })
      return
    }
  }
  next()
})

export default router
