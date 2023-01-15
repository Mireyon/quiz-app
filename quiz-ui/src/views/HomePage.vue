<template>
  <div class="home-page">
    <div class="homepage-image">
      <img class="square-image rounded-borders" src="/src/assets/mythology_quiz.png" />
    </div>

    <div class="homepage-start">
      <p class="homepage-title">Bienvenue sur Mythology Quiz</p>
      <p>Les règles sont simples:</p>
      <li>Vous avez 30 secondes pour répondre à chaque question</li>
      <li>Une seule réponse est correcte pour chaque question</li>
      <li>Une bonne réponse rapporte un point</li>
      <li>Une mauvaise réponse ne fait pas perdre de point</li>
      <li>A la fin du décompte, si vous n'avez toujours pas choisi de réponse, la réponse vous est affichée et la question est passée</li>
      <br>
      <button type="button" class="btn btn-outline-info center" @click="this.$router.push({ path: '/start-new-quiz-page' });">Démarrer le quiz</button>
      <br>
    </div>

      <p class="score-title">10 Meilleurs scores</p>
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
            <td>{{ scoreEntry.playerName }}</td>
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

export default {
  name: "HomePage",
  
  data() {
    return {registeredScores: [],
            progress: 0,
            nbrQuestions: 0,};
  },
  async created() {
    var QuizInfoApiResult = await QuizApiService.getQuizInfo();
    this.registeredScores = QuizInfoApiResult.data.scores;
    this.registeredScores.forEach(scoreEntry => {
        scoreEntry.progress = ((scoreEntry.score / this.nbrQuestions) * 100).toFixed(0);
      });
    this.nbrQuestions = QuizInfoApiResult.data.size;
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