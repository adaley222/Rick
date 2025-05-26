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
              <button @click="handleUndo" class="rick-btn rick-btn-undo">
                <Undo class="rick-btn-icon text-rickred" /> Undo
              </button>
              <button
                @click="toggleMic"
                :class="['rick-btn rick-btn-mic', isListening ? 'listening' : '']"
              >
                <Mic class="rick-btn-icon" />
                {{ isListening ? 'Listening...' : 'Start Listening' }}
              </button>
              <button @click="handleClear" class="rick-btn rick-btn-clear">
                <Trash2 class="rick-btn-icon" /> Clear Chat
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
</style>