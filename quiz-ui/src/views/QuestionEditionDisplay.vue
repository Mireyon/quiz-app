<template>
  <form class="form-container form-column">
    <p>Position : </p>
    <input type="text" v-model="position" :title="position" />
    <p>Title : </p>
    <input type="text" v-model="title" :title="position" />
    <p>Question : </p>
    <input type="text" v-model="text" :title="position" />
    <p>Image : </p><input
      tabindex="-1"
      type="file"
      name="uploadInput"
      :disabled="isSaving"
      @change="fileChange"
      accept="image/jpeg, image/png, image/gif"
      class="input-file"
      ref="fileInput"
    />
    <a class="image-upload-remove-link" 
      href="#" 
      v-if="file" 
      @click="clickRemoveImageHandler">
        Supprimer l'image
    </a>

    <div class="container" v-if="this.image!='image'"><img class="center square-image rounded-borders" :src="this.image" /></div>

    <br><p>Possible answers</p>
    <div v-for="i in 4">
      <input name="button" type="radio" v-if="possibleAnswers[i-1].isCorrect" checked="checked"/>
      <input name="button" type="radio" v-else/>
      <input type="text" v-model="possibleAnswers[i-1].text" :title="position" />
    </div>
    <div class="side">    
      <button type="button" class="btn btn-outline-danger margin-element" @click="goBack">Back</button>
      <button type="button" class="btn btn-outline-success margin-element" @click="saveQuestion">Save</button>
      <div v-if="isNotImage"><p class="form-row red">You need an image</p></div>
    </div>
  </form>
</template>
<script>
export default {
  emits: ["file-change", "go-back", "send-question", "update-question"],
  data() {
    return {
      isSaving: false,
      fileReader: null,
      fileInput: null,
      file: null,

      isNotImage: false,
      position:'position',
      title: 'title',
      text:'question',
      image:'image',
      possibleAnswers:[{'text':'answer', 'isCorrect':true}, {'text':'answer', 'isCorrect':false}, {'text':'answer', 'isCorrect':false}, {'text':'answer', 'isCorrect':false}],
    };
  },
  props: {
      question: {
        required: true
      },
    },
  mounted() {
    this.fileInput = this.$refs.fileInput;
    this.fileReader = new FileReader();
    this.fileReader.addEventListener(
      "load",
      () => {
        // fileReader holds a b64 string of the image
        const fileDataUrl = this.fileReader?.result;
        this.isSaving = false;
        this.$emit("file-change", fileDataUrl);
        this.image = fileDataUrl;
      },
      false
    );
  },
  created(){
    if(this.question!=null){
      this.position = this.question.position;
      this.title = this.question.title;
      this.text = this.question.text;
      this.image = this.question.image;
      this.possibleAnswers = this.question.possibleAnswers;
    }
  },
  methods: {
    fileChange(event) {
      this.isSaving = true;
      const input = event.target;
      // pick the first file uploaded
      this.file = input.files[0];
      // feed the file to the asynchronous file reader
      // (next step is in the load eventListener defined in mounted)
      this.fileReader.readAsDataURL(this.file);
    },
    clickRemoveImageHandler() {
      this.file = null;
      this.$emit("file-change", "");
      if (this.fileInput) {
        this.fileInput.value = "";
      }
      this.image = 'image';
    },
    goBack(){
      this.$emit("go-back", this.question);
    },
    saveQuestion(){
      if(this.image=='image'){
        this.isNotImage = true;
        return;
      }
      // console.log(question);
      if(this.question==null){
        this.$emit("send-question", {"text":this.text, "title":this.title, "image":this.image, "position":this.position, "possibleAnswers":this.possibleAnswers});
      }
      else{
        this.$emit("update-question", this.question.id, {"text":this.text, "title":this.title, "image":this.image, "position":this.position, "possibleAnswers":this.possibleAnswers});
      }
    },
  }
};
</script>

<style>
.image-upload-remove-link {
  display: block;
}
</style>