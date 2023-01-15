<template>
  <div class="home-page">
    <p class="score-title">Tableau des scores</p>
    <div class="table-container">
      <table class="score-table">
        <tr class="score-table-header">
          <th>Rang</th>
          <th>Joueur</th>
          <th>Score</th>
          <th>Pourcentage de réussite</th>
        </tr>
        <tr class="score-table-row" v-for="scoreEntry, index in registeredScores.slice(0,10)">
          <td v-if="index+1==1" style="color:gold;">{{ index + 1 }}</td>
          <td v-else-if="index+1==2" style="color:silver;">{{ index + 1 }}</td>
          <td v-else-if="index+1==3" style="color:#B87333;">{{ index + 1 }}</td>
          <td v-else>{{ index + 1 }}</td>
          <td v-if="scoreEntry.playerName==this.playerName && scoreEntry.score==this.score"  class="red">{{ scoreEntry.playerName }}</td>
          <td v-else>{{ scoreEntry.playerName }}</td>
          <td>{{ scoreEntry.score }}</td>
          <td>
            <div class="score-winrate">
              <div class="progress-bar">
                <div class="progress-bar-fill" :style="progressStyle(scoreEntry.score)">{{ getProgress(scoreEntry.score) }}%</div>
              </div>
            </div>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
  import QuizApiService from "@/services/QuizApiService";
  import participationStorageService from "@/services/ParticipationStorageService";

  export default {
    name: "ScorePage",
    
    data() {
      return {registeredScores: [],
              playerName: "",
              score: 0,
              progress: 0,
              nbrQuestions: 0,};
    },
    async created() {
      var QuizInfoApiResult = await QuizApiService.getQuizInfo();
      this.registeredScores = QuizInfoApiResult.data.scores;
      this.nbrQuestions = QuizInfoApiResult.data.size;
      this.playerName = participationStorageService.getPlayerName();
      this.score = participationStorageService.getParticipationScore();
    },
    methods: {
    progressStyle(score) {
      let progress = this.getProgress(score);
      return { width: progress + '%' }
    },
    getProgress(score) {
      return ((score / this.nbrQuestions) * 100).toFixed(0);
    }
  },
  };
</script>