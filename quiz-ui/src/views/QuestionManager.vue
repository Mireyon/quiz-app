<template>
  <QuestionDisplay v-bind:question="currentQuestion" v-bind:currentQuestionPosition="currentQuestionPosition" v-bind:totalNumberOfQuestion="totalNumberOfQuestion" @answer-selected="answerClickedHandler" />
</template>
  
<script>
  import participationStorageService from "@/services/ParticipationStorageService";
  import QuizApiService from "@/services/QuizApiService";
  import QuestionDisplay from '@/components/QuestionDisplay.vue';
  
  export default {
    name: 'QuestionManager',
    components: {
      QuestionDisplay
    },
    data() {
      return {
        totalNumberOfQuestion: 0,
        currentQuestion: {},
        currentQuestionPosition: 1,
        answers: []
      }
    },
    async created() {
      var QuizInfoApiResult = await QuizApiService.getQuizInfo()
      await this.loadQuestionByPosition(this.currentQuestionPosition);
      this.totalNumberOfQuestion = QuizInfoApiResult.data.size;
    },
    methods: {
      async loadQuestionByPosition(position) {
        var response = await QuizApiService.getQuestion(position);
        this.currentQuestion = response.data;
      },

      async answerClickedHandler(answerIndex){
        this.answers.push(answerIndex);

        if(this.currentQuestionPosition>=this.totalNumberOfQuestion){
          this.endQuiz();
          return;
        }
        await this.loadQuestionByPosition(this.currentQuestionPosition+1);
        this.currentQuestionPosition ++;
      },

      async endQuiz() {
        var SendParticipantResult = await QuizApiService.sendParticipation({"playerName":participationStorageService.getPlayerName(), "answers": this.answers});
        participationStorageService.saveParticipationScore(SendParticipantResult.data.score);
        this.$router.push({ path: '/score-page' });
      }
    }
  };
</script>