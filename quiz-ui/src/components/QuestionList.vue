<template>
  <button type="button" class="btn btn-outline-success create-question center" @click="createQuestion">+</button>
  <h1>Liste des questions</h1>
  <div v-for="(question,index) in questions">
    <button class="btn btn-primary btn-questions center" type="button" @click="emitQuestion(question)">{{ question.title }} : {{ question.text }}</button>
  </div>
</template>

<script>
  import QuizApiService from "@/services/QuizApiService";

  export default {
    name: 'QuestionList',
    emits: ["question-selected", 'question-creation'],
    data() {
      return {
        questions: [],
      }
    },

    async created() {
      var response = await QuizApiService.getQuestion("all");
      this.questions = response.data;
    },

    methods: {
      emitQuestion(question){
        this.$emit('question-selected', question);
      },
      createQuestion(){
        this.$emit('question-creation');
      }

    }
}
</script>