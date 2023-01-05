<template>
    <div class="question-display">
      <h1>{{ question.text }}</h1>
      <a @click="$emit('answer-selected', 2)">La réponse D</a>
    </div>
  </template>
  
<script>
  export default {
    name: 'QuestionDisplay',
    props: {
      question: {
        type: Object,
        required: true
      }
    }
  }
</script>
  
  <style>
  .question-display {
    text-align: center;
  }
  </style>