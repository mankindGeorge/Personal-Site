import { ref, onMounted, onUnmounted } from 'vue'

export function useSSE(url, options = {}) {
  const data = ref(null)
  const error = ref(null)
  const status = ref('disconnected')
  let eventSource = null

  const connect = () => {
    if (eventSource) {
      eventSource.close()
    }

    status.value = 'connecting'
    eventSource = new EventSource(url)

    eventSource.onopen = () => {
      status.value = 'connected'
      error.value = null
    }

    eventSource.onmessage = (event) => {
      try {
        data.value = JSON.parse(event.data)
      } catch {
        data.value = event.data
      }
    }

    eventSource.onerror = () => {
      status.value = 'error'
      error.value = '连接失败，正在重试...'
      
      if (options.autoReconnect !== false) {
        setTimeout(() => {
          connect()
        }, 3000)
      }
    }
  }

  const disconnect = () => {
    if (eventSource) {
      eventSource.close()
      eventSource = null
      status.value = 'disconnected'
    }
  }

  onMounted(() => {
    if (options.autoConnect !== false) {
      connect()
    }
  })

  onUnmounted(() => {
    disconnect()
  })

  return {
    data,
    error,
    status,
    connect,
    disconnect
  }
}
