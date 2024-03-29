<script setup>
import { ref, inject, onMounted } from 'vue';
import SendIcon from '../assets/send.svg';

const sendMessage = inject('sendMessage'); // Injection de la fonction sendMessage
const inputMessage = ref('');

const handleKeyDown = (event) => {
  // Vérifier si Entrée est pressée sans la touche Shift
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault(); // Empêcher le comportement par défaut de la touche Entrée (saut de ligne)
    sendMessage(inputMessage.value.trim());
    inputMessage.value = ''; // Réinitialiser le champ après l'envoi
  }
};

const handleSend = () => {
  sendMessage(inputMessage.value);
  inputMessage.value = '';
};

const autoGrow = (element) => {
  element.style.height = '5px'; // Réinitialiser la hauteur pour obtenir la hauteur correcte du contenu
  element.style.height = (element.scrollHeight) + 'px'; // Ajuster la hauteur au contenu
};

onMounted(() => {
  const textarea = document.querySelector('.chat-input');
  textarea.addEventListener('input', () => autoGrow(textarea));
  autoGrow(textarea); // Ajuster au chargement si le textarea n'est pas vide
});
</script>

<template>
  <div class="input-container">
    <textarea v-model="inputMessage" placeholder="Type a message..." class="chat-input" @keydown="handleKeyDown"></textarea>
    <button @click="handleSend" class="send-button">
      <SendIcon class="send-icon" />
    </button>
  </div>
</template>

<style scoped>
.input-container {
  display: flex;
  align-items: flex-end; /* Aligner le bouton et le textarea en bas */
  padding: 1px 13px;
  margin : 1em;
  background: #0b0c0d; /* Fond du conteneur */
  border-radius: 10px; /* Radius du conteneur */
  min-height: 20px;
}

.chat-input {
  font-family: 'TwCenMT', sans-serif;
  font-size: 1.1em;
  flex-grow: 1;
  background: transparent; /* Fond transparent pour le textarea */
  border: none; /* Pas de bordure pour le textarea */
  outline: none; /* Pas d'outline pour le textarea */
  color: #fff; /* Couleur du texte */
  margin-right: 0.5em;
  padding: 0em;
  padding-top: 10px;
  box-sizing: border-box;
  border-radius: 8px; /* Radius du textarea */
  resize: none; /* Empêcher le redimensionnement */
  max-height: 100px; /* Limiter la hauteur maximale */
  overflow-y: auto; /* Permettre le défilement vertical si le contenu dépasse max-height */
}

.send-button {
  /*background: linear-gradient(180deg, rgba(236,71,62,1) 0%, rgba(197,0,23,1) 100%);*/
  background: transparent;
  /*color: #fff;*/
  border: none;
  padding: 5px 7px; /* Ajuster le padding pour équilibrer la hauteur avec le textarea */
  /*border-radius: 10px;*/
  cursor: pointer;
  align-self: center; /* Assurer que le bouton ne change pas de position verticalement */
}

/*.send-button:hover {
  background-color: #c50017;
}*/

.send-icon {
  fill: white;
  height: 20px;
  width: auto;
}

.send-icon:hover {
  fill: #ff4646;
}
</style>
