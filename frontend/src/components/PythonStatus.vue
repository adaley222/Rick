<template>
  <div class="python-status">
    <h2>Python Backend Status</h2>
    <p>Status: {{ status }}</p>
    <button @click="checkStatus" :disabled="loading">
      {{ loading ? 'Checking...' : 'Check Status' }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const status = ref('Not checked')
const loading = ref(false)

async function checkStatus() {
  loading.value = true
  try {
    const response = await fetch('http://127.0.0.1:8000/api/status')
    const data = await response.json()
    status.value = data.status
  } catch (error) {
    console.error('Error:', error)
    status.value = 'Error connecting to backend'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.python-status {
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin: 20px;
}

button {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style> 