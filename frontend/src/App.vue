<template>
  <div class="app-container">
    <LoadingScreen v-if="isLoading" @complete="onLoadingComplete" />
    <template v-else>
      <NavBar />
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
      <Footer />
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import LoadingScreen from './components/common/LoadingScreen.vue'
import NavBar from './components/common/NavBar.vue'
import Footer from './components/common/Footer.vue'

const isLoading = ref(true)

onMounted(() => {
  const hasVisited = sessionStorage.getItem('hasVisited')
  if (hasVisited) {
    isLoading.value = false
  }
})

const onLoadingComplete = () => {
  sessionStorage.setItem('hasVisited', 'true')
  isLoading.value = false
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
