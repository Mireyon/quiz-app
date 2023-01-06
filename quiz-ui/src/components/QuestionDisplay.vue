<template>
  <div id="question-template">
    <div v-if="totalNumberOfQuestion!=0"><h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1></div>
    <div class="container"><img class="center square-image rounded-borders" v-if="question.image" :src="question.image" /></div>
    <h2>{{ question.title }}</h2>
    <h3>{{ question.text }}</h3>
      <div class="wrapper">
        <button class="btn btn-primary" type="button" v-for="(answer,index) in question.possibleAnswers" @click="emitAnswer(index+1)">{{ answer.text }}</button>
      </div>
  </div>
</template>
  
<script>
  export default {
    name: 'QuestionDisplay',
    props: {
      question: {
        type: Object,
        required: true
      },
      currentQuestionPosition:{
        required: true
      },
      totalNumberOfQuestion:{
        required: true
      },
    },
    emits: ["answer-selected"],
    methods: {
      emitAnswer(index){
        this.$emit('answer-selected', index)
      }
    }
  }
</script>