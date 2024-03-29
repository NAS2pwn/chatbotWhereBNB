<script setup>
import { ref, provide, onMounted, onUnmounted } from 'vue';
import ChatMessages from './ChatMessages.vue'
import ChatInput from './ChatInput.vue'

const messages = ref([
    {
        'type' : 'bot',
        'content' : 'Bonjour ! Je suis nassnass, votre assistant de voyage, que puis-je faire pour vous ?',
    }
]);
const ws = ref(null);

const sendMessage = (message) => {
    if (ws.value && message.trim() !== '') {
        ws.value.send(message);
    }
    messages.value.push({ type : 'user', content: message });
}

const updateOrAddBotMessage = (chunk) => {
    const lastMessage = messages.value[messages.value.length - 1];
    if (lastMessage && lastMessage.type === 'bot') {
        // Concaténer le nouveau chunk au dernier message du bot
        lastMessage.content += chunk;
        // Pour déclencher la réactivité sur les objets imbriqués
        messages.value[messages.value.length - 1] = { ...lastMessage };
    } else {
        // Sinon, ajouter un nouveau message bot
        messages.value.push({ type: 'bot', content: chunk });
    }
}

onMounted(() => {
    ws.value = new WebSocket('ws://localhost:8000/ws/chat');
    ws.value.onmessage = (event) => {
        updateOrAddBotMessage(event.data);
    };
});

onUnmounted(() => {
    if (ws.value) ws.value.close();
});

provide('messages', messages);
provide('sendMessage', sendMessage);
</script>

<!-- components/Chat.vue -->
<template>
    <div class="chat-container">
        <ChatMessages />
        <ChatInput />
    </div>
</template>

<style scoped>
    .chat-container {
        font-family: 'TwCenMT', sans-serif;
        font-size: 1.1em;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border-radius: 20px;
        border: 4px solid transparent;
        background: linear-gradient(#0e0f0f, #151313) padding-box,
            linear-gradient(to right, #fe6950, #c50017) border-box;
        width: 80%;
        height: 500px;
        overflow: hidden; /* Pour empêcher le contenu de déborder */
        margin-bottom: 20px;
    }

    .chat-messages { /*div principale de ChatMessages*/
        flex: 1; /* Cela permet aux messages de chat de remplir l'espace restant */
        overflow-y: auto; /* Permet de faire défiler les messages si nécessaire */
    }
</style>
