<template>
    <form @submit.prevent="launchNewQuiz">
      <p><label for="playerName">Nom du joueur&nbsp;:</label></p>
      <p><input type="text" id="playerName" placeholder="Username" v-model="username" /></p>
      <p><button type="submit">Soumettre</button></p>

    </form>
</template>
  <script>
  import participationStorageService from "@/services/ParticipationStorageService";

  export default {
    data() {
      return {username: ''}
    },
    methods: {
        launchNewQuiz() {
            participationStorageService.savePlayerName(this.username)
            // const playerName = participationStorageService.getPlayerName()
            this.$router.push({ path: '/questions' });
            return
             // Code à exécuter lorsque le bouton est cliqué
    }

    // Autres propriétés et méthodes du composant vue.js
    } 
}
  </script>
  
  