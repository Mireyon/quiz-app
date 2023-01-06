<template>
  <h1>List of best players</h1>
  <button type="button" class="btn btn-outline-info center" @click="this.$router.push({ path: '/start-new-quiz-page' });">Start Quiz</button>
  <br>
  <div class="table-container">
    <table class="score-table">
      <tr class="score-table-header">
        <th>Player</th>
        <th>Score</th>
      </tr>
      <tr class="score-table-row" v-for="scoreEntry in registeredScores.slice(0,8)" v-bind:key="scoreEntry.date">
        <td>{{ scoreEntry.playerName }}</td>
        <td>{{ scoreEntry.score }}</td>
      </tr>
    </table>
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
    this.registeredScores = QuizInfoApiResult.data.scores;
  }
};
</script>