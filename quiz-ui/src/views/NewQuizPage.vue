<template>
  <div class="form-container">
    <form @submit.prevent="launchNewQuiz">
      <p class="form-row"><label for="playerName">Nom du joueur&nbsp;:</label></p>
      <p class="form-row"><input type="text" id="playerName" placeholder="Username" v-model="username" required/></p>
      <p class="form-row"><button type="submit" class="color-shift-button">Démarrer</button></p>
    </form>
  </div>
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
          this.$router.push({ path: '/questions' });
      }
    } 
}
</script>