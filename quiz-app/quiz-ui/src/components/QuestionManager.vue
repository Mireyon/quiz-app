<template>
    <div class="question-manager">
      <template v-if="currentQuestion">
        <QuestionDisplay v-bind:question="currentQuestion" />
        <button v-for="answer in currentQuestion.answers" v-bind:key="answer.id" v-on:click="answerClickedHandler(answer.id)">
          {{ answer.text }}
        </button>
      </template>
      <template v-else>
        <h1>Quiz terminé !</h1>
        <p>Votre score est de {{ score }} points sur {{ currentPosition }} questions.</p>
        <button v-on:click="restartQuiz">Recommencer le quiz</button>
      </template>
    </div>
  </template>
  
  <script>
  import questionDisplay from './QuestionDisplay';
  import axios from 'axios';
  
  export default {
    name: 'QuestionManager',
    components: {
      questionDisplay
    },
    data() {
      return {
        currentQuestion: null,
        currentPosition: 1,
        score: 0
      }
    },
    created() {
      this.loadQuestionByPosition(this.currentPosition);
    },
    methods: {
      async loadQuestionByPosition(position) {
        try {
            // Need help here pour savoir ou sont les questions
            //Peut etre aussi check avec endQuizz si on a pas fini avec la position
            const response = await QuizApiService.getQuestion(position);
            this.currentQuestion = response.data;
        } catch (error) {
          console.error(error);
          this.endQuizz();
        }
      },
      async answerClickedHandler(answerId) {
        const correctAnswer = this.currentQuestion.answers.find(answer => answer.correct);
        if (answerId === correctAnswer.id) {
          this.score++;
        }
        this.currentPosition++;
        try {
          //Meme probleme ici, cf internet await axios.get pourrait marcher mais je suis pas sur
          const response = await axios.get(`/questions/${this.currentPosition}`);
          this.currentQuestion = response.data;
        } catch (error) {
          console.error(error);
          this.endQuiz();
        }
      },
      async endQuiz() {
        this.currentQuestion = null;
      },
      async restartQuiz() {
        this.currentQuestion = null;
        this.currentPosition = 0;
        this.score = 0;
        this.loadQuestionByPosition(0);
      }
    }
  };
</script>
  
  <style>
  .question-manager {
    text-align: center;
  }
  </style>