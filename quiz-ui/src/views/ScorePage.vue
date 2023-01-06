<template>
  <h1>Score table</h1>
  <br>
  <div class="table-container">
    <table class="score-table">
      <tr class="score-table-header">
        <th>Player</th>
        <th>Score</th>
      </tr>
      <tr class="score-table-row" v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
        <td v-if="scoreEntry.playerName==this.playerName && scoreEntry.score==this.score"  class="red">{{ scoreEntry.playerName }}</td>
        <td v-else>{{ scoreEntry.playerName }}</td>
        <td v-if="scoreEntry.playerName==this.playerName && scoreEntry.score==this.score"  class="red">{{ scoreEntry.score }}</td>
        <td v-else>{{ scoreEntry.score }}</td>
      </tr>
    </table>
  </div>
</template>

<script>
  import QuizApiService from "@/services/QuizApiService";
  import participationStorageService from "@/services/ParticipationStorageService";

  export default {
    name: "HomePage",
    
    data() {
      return {registeredScores: [],
              playerName: "",
              score: 0};
    },
    async created() {
      var QuizInfoApiResult = await QuizApiService.getQuizInfo();
      this.registeredScores = QuizInfoApiResult.data.scores;
      this.playerName = participationStorageService.getPlayerName();
      this.score = participationStorageService.getParticipationScore();
      console.log(this.playerName, this.score);
    }
  };
</script>