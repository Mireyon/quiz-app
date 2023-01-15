<template>
    <div class="question-display">
      <div class="container-question" style="background-color: white;">
        <div class="question-heading">
          <span class="question-title" v-if="totalNumberOfQuestion!=0">Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }} : </span>
          <span class="question-title">{{ question.title }}</span>
        </div>

        <div class="row-question">
          <div class="image-question">
            <img class="square-image rounded-borders" v-if="question.image" :src="question.image" />
          </div>
          <div class="text-question">
            <p class="question">{{ question.text }}</p>
            <div class="wrapper">
              <button class="btn btn-primary" type="button" pointer-events="auto" v-for="(answer,index) in question.possibleAnswers" @click="emitAnswer(index)" :id=index>{{ answer.text }}</button>
            </div>
          </div>
        </div>
      </div>
      <div class="timebar" v-if="totalNumberOfQuestion!=0">
        <div id="timebar-fill" class="timebar-fill" :style="{width: timebarWidth + '%'}"></div>
      </div>
    </div>
</template>

  
<script>
  export default {
    data() {
      return {
        timebarWidth: 100,
        interval: null
      }
    },

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
    watch: {
      question: function(newQuestion, oldQuestion){
        for(var i = 0; i < newQuestion.possibleAnswers.length; i++){
          var button = document.getElementById(i);
          if(button!=null){
            button.style.pointerEvents = "auto";
            button.className = "btn btn-primary";
          }
        }
        this.timebarWidth = 100;
        var timebar = document.getElementById("timebar-fill")
          if(timebar!=null)
            timebar.style.backgroundColor = "#007bff";
        this.interval = setInterval(() => {
          this.timebarWidth -= 0.05;
          if(this.timebarWidth <= 0) {
            this.emitAnswer(-1);
          }
          else if(this.timebarWidth <= 20){
            var timebar = document.getElementById("timebar-fill")
            if(timebar!=null)
              timebar.style.backgroundColor = "#ff1100";
          }
          else if(this.timebarWidth <= 50){
            var timebar = document.getElementById("timebar-fill")
            if(timebar!=null)
              timebar.style.backgroundColor = "#ff7300";
          }
        }, 15); // 1000ms = 1s
      },
    },
    methods: {
      colorAnswer(index){
        for(var i = 0; i < this.question.possibleAnswers.length; i++){
            var button = document.getElementById(i);
            if(button==null)
              continue;
            button.style.pointerEvents = "none";
            button.blur();
            if(this.question.possibleAnswers[i].isCorrect)
              button.className = "btn btn-success";
            else if(!this.question.possibleAnswers[i].isCorrect && i==index)
              button.className = "btn btn-danger";
          }
      },

      async emitAnswer(index){
        clearInterval(this.interval)
        this.colorAnswer(index)
        await new Promise(r => setTimeout(r, 1200));
        this.$emit('answer-selected', index);
      }
    },
  }
</script>