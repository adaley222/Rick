<template>
  <div class="min-h-screen bg-gray-100 p-4 flex flex-col items-center">
    <div class="w-full max-w-2xl space-y-4">
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold">Rick 🎙️</h1>
        <button @click="openSettings" class="p-2 hover:bg-gray-200 rounded">
          <Settings class="w-5 h-5" />
        </button>
      </div>

      <div class="h-96 overflow-y-auto p-4 space-y-4 bg-white rounded shadow">
        <div v-if="chatHistory.length === 0" class="text-gray-400">No chat history yet.</div>
        <div v-else v-for="(entry, idx) in chatHistory" :key="idx" class="mb-2">
          <p><strong>User:</strong> {{ entry.user }}</p>
          <p><strong>Rick:</strong> {{ entry.rick }}</p>
        </div>
      </div>

      <div class="flex justify-between items-center">
        <button @click="handleUndo" class="bg-gray-200 px-4 py-2 rounded hover:bg-gray-300">
          <Undo class="inline w-4 h-4 mr-1" /> Undo
        </button>

        <button
          @click="toggleMic"
          :class="['px-4 py-2 rounded text-white flex items-center', isListening ? 'bg-red-500 hover:bg-red-600' : 'bg-blue-500 hover:bg-blue-600']"
        >
          <Mic class="inline w-4 h-4 mr-1" />
          {{ isListening ? 'Listening...' : 'Start Listening' }}
        </button>

        <button @click="handleClear" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded">
          <Trash2 class="inline w-4 h-4 mr-1" /> Clear Chat
        </button>
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
</style>