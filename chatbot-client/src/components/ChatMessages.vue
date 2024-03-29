<!-- components/ChatMessages.vue -->
<script setup>
import { inject } from 'vue';

const messages = inject('messages');
</script>

<template>
  <div class="chat-messages">
    <div v-for="(message, index) in messages" :key="index" class="message" :class="`message-${message.type}`" style="white-space: pre-wrap">{{ message.content }}</div>
  </div>
</template>

<style scoped>
.chat-messages {
  display: flex;
  flex-direction: column;
  padding: 1em;
  overflow-y: auto; /* Pour le défilement si les messages débordent de l'espace disponible */
}

.message {
  display: flex;
  margin-bottom: 12px;
  padding: 8px 12px;
  border-radius: 18px;
  max-width: 80%;
}

.message-user {
  background-color: #ff4646;
  margin-left: auto; /* Aligner à droite */
  justify-content: flex-end;
}

.message-bot {
  background-color: #28272c;
  margin-right: auto; /* Aligner à gauche */
  justify-content: flex-start;
}
</style>
