import { defineStore } from 'pinia'
import { ref } from 'vue'
import { docsAPI } from '@/services/api'

export const useDocsStore = defineStore('docs', () => {
  const documents = ref([])
  const currentDoc = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchAllDocs = async () => {
    loading.value = true
    error.value = null
    try {
      documents.value = await docsAPI.getAll()
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  const fetchDocBySlug = async (slug) => {
    loading.value = true
    error.value = null
    try {
      currentDoc.value = await docsAPI.getBySlug(slug)
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  const createDoc = async (data) => {
    try {
      const newDoc = await docsAPI.create(data)
      documents.value.push(newDoc)
      return { success: true }
    } catch (e) {
      return { success: false, error: e.message }
    }
  }

  const updateDoc = async (id, data) => {
    try {
      const updated = await docsAPI.update(id, data)
      const index = documents.value.findIndex(d => d.id === id)
      if (index !== -1) {
        documents.value[index] = updated
      }
      if (currentDoc.value?.id === id) {
        currentDoc.value = updated
      }
      return { success: true }
    } catch (e) {
      return { success: false, error: e.message }
    }
  }

  const deleteDoc = async (id) => {
    try {
      await docsAPI.delete(id)
      documents.value = documents.value.filter(d => d.id !== id)
      if (currentDoc.value?.id === id) {
        currentDoc.value = null
      }
      return { success: true }
    } catch (e) {
      return { success: false, error: e.message }
    }
  }

  return {
    documents,
    currentDoc,
    loading,
    error,
    fetchAllDocs,
    fetchDocBySlug,
    createDoc,
    updateDoc,
    deleteDoc
  }
})
