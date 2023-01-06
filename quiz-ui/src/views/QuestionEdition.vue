<template>
  <div class="center margin-top form-container">
    <button type="button" class="btn btn-outline-danger margin-element" @click="goBack">Back</button>
    <button type="button" class="btn btn-outline-success margin-element" @click="editQuestion">Edit</button>
    <button type="button" class="btn btn-outline-danger margin-element" @click="deleteQuestion(question.id)">Delete</button>
  </div>

  <div id="question-template">
    <div class="container"><img class="center square-image rounded-borders margin-top" v-if="question.image" :src="question.image" /></div>
    <h2>{{ question.title }}</h2>
    <h3>{{ question.text }}</h3>
      <div class="wrapper">
        <button class="btn" type="button" v-for="(answer,index) in question.possibleAnswers" :class="buttonClass(answer)">
          {{ answer.text }}
        </button>
      </div>
  </div>
</template>

<script>
  export default {
    name: 'QuestionEdition',
    emits: ["question-deleted","question-edit","go-back"],
    props: {
      question: {
        type: Object,
        required: true
      },
    },
    methods:{
      deleteQuestion(id){
        this.$emit('question-deleted', id);
      },
      editQuestion(){
        this.$emit('question-edit', this.question);
      },
      buttonClass(answer) {
        return {
          'btn-success': answer.isCorrect,
          'btn-primary': !answer.isCorrect,
        }
      },
      goBack(){
        this.$emit("go-back", null);
      }
    }

  }
</script>