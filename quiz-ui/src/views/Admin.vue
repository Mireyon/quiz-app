<template>
  <button v-if="this.adminMode!='login'" type="button" class="btn right btn-outline-warning" @click="clearToken">Déconnexion</button>
  <div v-if="this.adminMode=='login'">
    <div class="form-container">
      <form @submit.prevent="connectAdmin">
        <label for="password">Password&nbsp;:</label>
        <p class="form-row"><input autocomplete="off" type="password" placeholder="password" v-model="password" /></p>

        <p class="form-row"><button type="submit" class="btn btn-outline-danger">Connexion</button></p>
        <div v-if="this.status==401"><p class="form-row red">Mauvais mot de passe !</p></div>
      </form>
    </div>
  </div>
  <div v-else-if="this.adminMode=='question-list'">
    <QuestionList @question-selected="questionClickedHandler" @question-creation="createNewQuestion"></QuestionList>
  </div>
  <div v-else-if="this.adminMode=='question-edition'">
    <QuestionEdition @go-back="goBack" @question-edit="questionEdition" @question-deleted="questionDeleted" v-bind:question="this.question"></QuestionEdition>
  </div>
  <div v-else-if="this.adminMode=='question-edition-display'">
    <QuestionEditionDisplay @update-question="updateQuestion" @send-question="sendQuestion" @go-back="goBack" v-bind:question="this.question"></QuestionEditionDisplay>
  </div>
</template>

<script>
  import TokenManager from "@/services/TokenManager"
  import QuestionList from "@/components/QuestionList.vue"
  import QuestionEdition from "@/components/QuestionEdition.vue"
  import QuestionEditionDisplay from "@/components/QuestionEditionDisplay.vue"
  import QuizApiService from "@/services/QuizApiService";

  export default {
    data() {
      return {adminMode:'login',
              password: '',
              status:200,
              question:null};
    },
    components:{
      QuestionList,
      QuestionEdition,
      QuestionEditionDisplay
    },
    async created(){
      var token = await TokenManager.getToken();
      if(token){
        this.adminMode = 'question-list';
      }
    },
    methods: {
      async connectAdmin() {
        var loginResult = await QuizApiService.sendLogin({"password": this.password})
        this.status = loginResult.status
        if(this.status!=401){
          TokenManager.saveToken(loginResult.data.token);
          this.adminMode='question-list';
        }
        this.password = '';
      },
      clearToken(){
        TokenManager.clear();
        this.adminMode='login';
      },
      questionClickedHandler(question){
        this.adminMode='question-edition';
        this.question = question;
      },
      async questionDeleted(id){
        var token = await TokenManager.getToken();
        if(token){
          var response = await QuizApiService.deleteQuestion(id, token);
          this.adminMode='question-list';
        }
        else{
          this.clearToken();
        }
      },
      questionEdition(question){
        this.adminMode='question-edition-display';
        this.question = question;
      },
      createNewQuestion(){
        this.adminMode='question-edition-display';
        this.question = null;
      },
      goBack(question){
        if(question==null){this.adminMode='question-list';}
        else{this.questionClickedHandler(question)}
      },
      async sendQuestion(payload){
        var token = await TokenManager.getToken();
        if(token){
          var response = await QuizApiService.sendQuestion(payload, token);
          this.adminMode='question-list';
        }
        else{
          this.clearToken();
        }
      },
      async updateQuestion(questionId, payload){
        var token = await TokenManager.getToken();
        if(token){
          var response = await QuizApiService.updateQuestion(questionId, payload, token);
          this.adminMode='question-list';
        }
        else{
          this.clearToken();
        }
      }
    } 
}
</script>