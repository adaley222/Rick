<template>
  <div class="rick-ui">    <div class="rick-card">
      <div class="rick-layout">
        <!-- Left column: Text and buttons -->
        <div class="rick-left-column">
          <div class="rick-content">
            <h1 class="rick-title">Rick 🎙️</h1>
            <div class="rick-settings-row">
              <button @click="openSettings" class="rick-settings-btn">
                <Settings class="w-5 h-5 text-rickred" />
              </button>
            </div>
            <div class="rick-chat-area">
              <div v-if="chatHistory.length === 0" class="rick-chat-empty">No chat history yet.</div>
              <div v-else v-for="(entry, idx) in chatHistory" :key="idx" class="rick-chat-entry">
                <p><strong class="rick-chat-label">User:</strong> {{ entry.user }}</p>
                <p><strong class="rick-chat-label">Rick:</strong> {{ entry.rick }}</p>
              </div>
            </div>
            <div class="rick-buttons-row">
              <button @click="handleUndo" class="rick-btn rick-btn-undo" title="Undo">
                <Undo class="rick-btn-icon text-rickred" />
              </button>
              <button
                @click="toggleMic"
                :class="['rick-btn rick-btn-mic', isListening ? 'listening' : '']"
                :title="isListening ? 'Stop Listening' : 'Start Listening'"
              >
                <Mic class="rick-btn-icon" />
              </button>
              <button @click="handleClear" class="rick-btn rick-btn-clear" title="Clear Chat">
                <Trash2 class="rick-btn-icon" />
              </button>
            </div>
          </div>
        </div>
        
        <!-- Right column: Rick image -->
        <div class="rick-right-column">
          <img
            src="/Rick_pic.jpeg"
            alt="Rick"
            class="rick-image"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Mic, Undo, Settings, Trash2 } from 'lucide-vue-next';

const chatHistory = ref([
  { user: 'Play the last take', rick: 'Playing last take.' },
  { user: 'Mute drums', rick: 'Drums muted.' },
]);

const isListening = ref(false);

function handleUndo() {
  chatHistory.value.pop();
}

function handleClear() {
  chatHistory.value = [];
}

function toggleMic() {
  isListening.value = !isListening.value;
}

function openSettings() {
  alert('Settings modal coming soon!');
}
</script>

<style scoped>
.text-rickred {
  color: #C1272D;
}

.rick-ui {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(145deg, #1a1a1a, #2a2a2a);
  color: #e0e0e0;
}

.rick-card {
  background: linear-gradient(145deg, #2d2d2d, #232323);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  padding: 1.5rem;
  margin: 1rem;
  max-width: 725px;
  width: 100%;
  border: 1px solid rgba(255, 255, 255, 0.1);
  height: 500px;
}

.rick-layout {
  display: grid;
  grid-template-columns: 1fr 200px;
  gap: 1rem;
  height: 100%;
}

.rick-left-column {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.rick-right-column {
  display: flex;
  align-items: center;
}

.rick-image {
  width: 100%;
  height: 200px;
  border-radius: 8px;
  object-fit: cover;
}

.rick-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.rick-title {
  color: #ffffff;
  margin: 0 0 0.75rem 0;
  font-size: 1.5rem;
}

.rick-chat-area {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 0.75rem;
  margin: 0.5rem 0;
  flex: 1;
  overflow-y: auto;
  min-height: 0;
  font-size: 0.9rem;
}

.rick-chat-empty {
  color: #888888;
}

.rick-chat-entry {
  margin-bottom: 0.75rem;
  padding: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.rick-chat-label {
  color: #C1272D;
}

.rick-buttons-row {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.75rem;
  justify-content: center;
}

.rick-btn {
  width: 36px;
  height: 36px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #333333;
  color: #e0e0e0;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.rick-btn-icon {
  width: 18px;
  height: 18px;
}

.rick-btn:hover {
  background: #444444;
  border-color: rgba(255, 255, 255, 0.2);
}

.rick-btn.listening {
  background: #C1272D;
  color: white;
}

.rick-settings-row {
  position: absolute;
  top: 1rem;
  right: 1rem;
}

.rick-settings-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
}
</style>