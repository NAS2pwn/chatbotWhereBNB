<script setup>
import Chat from './components/Chat.vue'
</script>

<template>
  <header>
    <img src="./assets/logo.png" alt="Logo" class="logo" />
  </header>
  <main>
    <Chat/>
  </main>
  <footer>
    <div class="footer-content">
    © Nassim Bennouar - 2024
    <a href="URL_DU_PROJET_GITHUB" class="footer-link">Github du projet</a>
    <a href="URL_DE_LA_NEWSLETTER" class="footer-link">Newsletter KaleidoTech</a>
    </div>
  </footer>
</template>

<style scoped>
  header {
      /*background-color: #0f0f0f; /* Gris très légèrement plus clair */
      text-align: center;
      padding: 16px;
  }

  .logo {
      width: 120px;
      height: auto;
  }

main {
  flex: 1; /* Cela permet au main de s'étendre et d'occuper tout l'espace disponible */
  display: flex;
  justify-content: center;
  align-items: center;
}

footer {
  background-color: #0f0f0f;
  color: white;
  text-align: center;
  padding: 16px;
}

.footer-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px; /* Espace entre les éléments */
}

.footer-link {
  color: #fe6950; /* Couleur de lien pour correspondre au style de votre site */
  text-decoration: none; /* Supprime le soulignement par défaut */
  margin: 0 10px; /* Marges horizontales pour l'espacement */
}

.footer-link:hover {
  text-decoration: underline; /* Style de survol pour les liens */
}
</style>
