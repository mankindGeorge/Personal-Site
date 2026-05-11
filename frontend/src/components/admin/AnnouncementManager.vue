<template>
  <div class="announcement-manager">
    <div class="manager-header">
      <h2 class="manager-title">公告列表</h2>
      <button @click="openEditor()" class="add-btn">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/>
          <line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        新建公告
      </button>
    </div>

    <div class="announcement-list">
      <div 
        v-for="ann in announcements" 
        :key="ann.id"
        class="announcement-item"
      >
        <div class="ann-left">
          <span class="ann-type" :class="ann.type">{{ ann.type }}</span>
        </div>
        <div class="ann-info">
          <h3 class="ann-title">{{ ann.title }}</h3>
          <p class="ann-content">{{ ann.content }}</p>
          <span class="ann-date">{{ formatDate(ann.created_at) }}</span>
        </div>
        <div class="ann-actions">
          <button @click="openEditor(ann)" class="action-btn edit">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </button>
          <button @click="deleteAnn(ann.id)" class="action-btn delete">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
          </button>
        </div>
      </div>

      <div v-if="announcements.length === 0" class="empty-state">
        <p>暂无公告</p>
      </div>
    </div>

    <div v-if="editorOpen" class="modal-overlay" @click.self="closeEditor">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ currentAnn ? '编辑公告' : '新建公告' }}</h3>
          <button @click="closeEditor" class="close-btn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <form @submit.prevent="handleSave" class="modal-form">
          <div class="form-group">
            <label>标题</label>
            <input v-model="formData.title" type="text" required />
          </div>

          <div class="form-group">
            <label>内容</label>
            <textarea v-model="formData.content" rows="4" required></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>类型</label>
              <select v-model="formData.type">
                <option value="info">信息</option>
                <option value="success">成功</option>
                <option value="warning">警告</option>
              </select>
            </div>
            <div class="form-group">
              <label>优先级</label>
              <input v-model.number="formData.priority" type="number" min="0" />
            </div>
          </div>

          <div class="form-group">
            <label>
              <input v-model="formData.is_published" type="checkbox" />
              立即发布
            </label>
          </div>

          <div class="form-actions">
            <button type="button" @click="closeEditor" class="cancel-btn">取消</button>
            <button type="submit" class="save-btn">保存</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { announcementsAPI } from '@/services/api'

const announcements = ref([])
const editorOpen = ref(false)
const currentAnn = ref(null)
const formData = ref({
  title: '',
  content: '',
  type: 'info',
  priority: 0,
  is_published: true
})

const fetchAnnouncements = async () => {
  try {
    announcements.value = await announcementsAPI.getAll()
  } catch (error) {
    console.error('获取公告失败:', error)
  }
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const openEditor = (ann = null) => {
  if (ann) {
    currentAnn.value = ann
    formData.value = { ...ann }
  } else {
    currentAnn.value = null
    formData.value = {
      title: '',
      content: '',
      type: 'info',
      priority: 0,
      is_published: true
    }
  }
  editorOpen.value = true
}

const closeEditor = () => {
  editorOpen.value = false
  currentAnn.value = null
}

const handleSave = async () => {
  try {
    if (currentAnn.value) {
      await announcementsAPI.update(currentAnn.value.id, formData.value)
    } else {
      await announcementsAPI.create(formData.value)
    }
    await fetchAnnouncements()
    closeEditor()
  } catch (error) {
    console.error('保存失败:', error)
  }
}

const deleteAnn = async (id) => {
  if (confirm('确定要删除这条公告吗？')) {
    try {
      await announcementsAPI.delete(id)
      await fetchAnnouncements()
    } catch (error) {
      console.error('删除失败:', error)
    }
  }
}

onMounted(() => {
  fetchAnnouncements()
})
</script>

<style scoped>
.announcement-manager {
  max-width: 900px;
}

.manager-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.manager-title {
  font-family: 'Fira Code', monospace;
  font-size: 1.25rem;
  color: #E6EDF3;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: linear-gradient(135deg, #00FFCC, #00CC99);
  border: none;
  border-radius: 8px;
  color: #0A0A0A;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 255, 204, 0.3);
}

.announcement-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.announcement-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.25rem;
  background: linear-gradient(145deg, rgba(13, 17, 23, 0.8), rgba(10, 10, 10, 0.9));
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.announcement-item:hover {
  border-color: rgba(0, 255, 204, 0.3);
}

.ann-left {
  flex-shrink: 0;
}

.ann-type {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.625rem;
  font-weight: 600;
  text-transform: uppercase;
}

.ann-type.info {
  background: rgba(176, 38, 255, 0.1);
  color: #B026FF;
  border: 1px solid rgba(176, 38, 255, 0.2);
}

.ann-type.success {
  background: rgba(0, 255, 204, 0.1);
  color: #00FFCC;
  border: 1px solid rgba(0, 255, 204, 0.2);
}

.ann-type.warning {
  background: rgba(255, 184, 0, 0.1);
  color: #FFB800;
  border: 1px solid rgba(255, 184, 0, 0.2);
}

.ann-info {
  flex: 1;
}

.ann-title {
  font-family: 'Fira Code', monospace;
  font-size: 1rem;
  color: #E6EDF3;
  margin-bottom: 0.5rem;
}

.ann-content {
  color: #8B949E;
  font-size: 0.875rem;
  line-height: 1.6;
  margin-bottom: 0.5rem;
}

.ann-date {
  color: #8B949E;
  font-size: 0.75rem;
}

.ann-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 8px;
  color: #8B949E;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn.edit:hover {
  color: #00FFCC;
  border-color: #00FFCC;
}

.action-btn.delete:hover {
  color: #FF4757;
  border-color: #FF4757;
}

.empty-state {
  padding: 3rem;
  text-align: center;
  color: #8B949E;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
}

.modal-content {
  width: 100%;
  max-width: 500px;
  background: #0D1117;
  border: 1px solid rgba(0, 255, 204, 0.2);
  border-radius: 16px;
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(0, 255, 204, 0.1);
}

.modal-header h3 {
  font-family: 'Fira Code', monospace;
  color: #E6EDF3;
}

.close-btn {
  background: none;
  border: none;
  color: #8B949E;
  cursor: pointer;
  padding: 0.25rem;
  transition: color 0.3s ease;
}

.close-btn:hover {
  color: #E6EDF3;
}

.modal-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #8B949E;
  font-size: 0.875rem;
}

.form-group input[type="text"],
.form-group input[type="number"],
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(0, 255, 204, 0.05);
  border: 1px solid rgba(0, 255, 204, 0.1);
  border-radius: 8px;
  color: #E6EDF3;
  font-size: 0.9375rem;
  outline: none;
}

.form-group textarea {
  resize: vertical;
  font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  border-color: #00FFCC;
}

.form-group input[type="checkbox"] {
  margin-right: 0.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.cancel-btn,
.save-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn {
  background: transparent;
  border: 1px solid rgba(0, 255, 204, 0.2);
  color: #8B949E;
}

.cancel-btn:hover {
  border-color: #E6EDF3;
  color: #E6EDF3;
}

.save-btn {
  background: linear-gradient(135deg, #00FFCC, #00CC99);
  border: none;
  color: #0A0A0A;
}

.save-btn:hover {
  box-shadow: 0 4px 15px rgba(0, 255, 204, 0.3);
}
</style>
