<template>
  <h1>Home page</h1>
  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>
</template>

<script>
import QuizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  
  data() {
    return {registeredScores: []};
  },
  async created() {
    var QuizInfoApiResult = await QuizApiService.getQuizInfo();
    console.log(QuizInfoApiResult)
    this.registeredScores = QuizInfoApiResult.data.scores;
		console.log("Composant Home page 'created'");

    
  }
};
</script>

