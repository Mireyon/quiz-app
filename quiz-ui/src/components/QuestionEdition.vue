<template>
  <div class="center margin-top form-container">
    <button type="button" class="btn btn-outline-danger margin-element" @click="goBack">Retour</button>
    <button type="button" class="btn btn-outline-success margin-element" @click="editQuestion">Editer</button>
    <button type="button" class="btn btn-outline-danger margin-element" @click="deleteQuestion(question.id)">Supprimer</button>
  </div>

  <div class="question-display">
    <div class="container-question" style="background-color: white;">
      <div class="question-heading">
        <span class="question-title">Question {{ question.position }} : </span>
        <span class="question-title">{{ question.title }}</span>
      </div>
      <div class="row-question">
        <div class="image-question">
          <img class="square-image rounded-borders" v-if="question.image" :src="question.image" />
        </div>
        <div class="text-question">
          <p class="question">{{ question.text }}</p>
          <div class="wrapper">
            <button class="btn" type="button" pointer-events="auto" v-for="(answer,index) in question.possibleAnswers" :class="buttonClass(answer)">{{ answer.text }}</button>
          </div>
        </div>
      </div>
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