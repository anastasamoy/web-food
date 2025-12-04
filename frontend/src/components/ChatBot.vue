<template>
  <div class="chat-widget">
    <!-- Кнопка открытия чата -->
    <button class="chat-toggle-btn" @click="isOpen = !isOpen">
      {{ isOpen ? '❌ Zatvoriť' : '🤖 AI-Kuchár' }}
    </button>

    <!-- Окно чата -->
    <div v-if="isOpen" class="chat-window">
      <div class="chat-header">
        <h3>Asistent</h3>
      </div>
      
      <div class="chat-messages" ref="messagesContainer">
        <div 
          v-for="(msg, index) in messages" 
          :key="index" 
          :class="['message', msg.isUser ? 'user-message' : 'bot-message']"
        >
          {{ msg.text }}
        </div>
        <div v-if="isLoading" class="message bot-message">
          Thinking...
        </div>
      </div>

      <div class="chat-input">
        <input 
          v-model="newMessage" 
          @keyup.enter="sendMessage"
          placeholder="Opýtaj sa na recept..." 
          type="text"
        />
        <button @click="sendMessage" :disabled="isLoading || !newMessage.trim()">➤</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, nextTick } from 'vue';

export default {
  name: 'ChatBot',
  setup() {
    const isOpen = ref(false);
    const newMessage = ref('');
    const messages = ref([
      { text: 'Ahoj! Som kuchár s umelou inteligenciou. Čo mám uvariť?', isUser: false }
    ]);
    const isLoading = ref(false);
    const messagesContainer = ref(null);

    const scrollToBottom = async () => {
      await nextTick();
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
      }
    };

    const sendMessage = async () => {
      if (!newMessage.value.trim()) return;

      const userText = newMessage.value;
      messages.value.push({ text: userText, isUser: true });
      newMessage.value = '';
      isLoading.value = true;
      await scrollToBottom();

      try {
        // Запрос к вашему Python серверу
        const response = await fetch('http://127.0.0.1:5000/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: userText })
        });

        const data = await response.json();
        
        if (data.reply) {
          messages.value.push({ text: data.reply, isUser: false });
        } else {
          messages.value.push({ text: 'Chyba servera', isUser: false });
        }
      } catch (error) {
        messages.value.push({ text: 'Nepodarilo sa spojiť s botom.', isUser: false });
        console.error(error);
      } finally {
        isLoading.value = false;
        await scrollToBottom();
      }
    };

    return {
      isOpen,
      newMessage,
      messages,
      isLoading,
      sendMessage,
      messagesContainer
    };
  }
}
</script>

<style scoped>
.chat-widget {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  font-family: sans-serif;
}

.chat-toggle-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 30px;
  cursor: pointer;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.chat-toggle-btn:hover {
  transform: scale(1.05);
}

.chat-window {
  position: absolute;
  bottom: 60px;
  right: 0;
  width: 320px;
  height: 450px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid #eee;
}

.chat-header {
  background: #4CAF50;
  color: white;
  padding: 10px 15px;
  font-size: 16px;
}

.chat-messages {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  background: #f9f9f9;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.message {
  max-width: 80%;
  padding: 8px 12px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.4;
}

.user-message {
  align-self: flex-end;
  background: #4CAF50;
  color: white;
  border-bottom-right-radius: 2px;
}

.bot-message {
  align-self: flex-start;
  background: #e0e0e0;
  color: #333;
  border-bottom-left-radius: 2px;
}

.chat-input {
  padding: 10px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 5px;
  background: white;
}

.chat-input input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 20px;
  outline: none;
}

.chat-input button {
  background: #4CAF50;
  color: white;
  border: none;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-input button:disabled {
  background: #ccc;
}
</style>