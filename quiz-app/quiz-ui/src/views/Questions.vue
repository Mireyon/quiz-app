<template>
  <div class="question">
    <h1>This is a Question page</h1>
    <button type="button" @click =launchTest>Test</button>
  </div>
</template>

<script>
  import test from "@/components/test";

export default {
    data() {
      return {username: ''}
    },
    methods: {
        launchTest() {
            // question = questionManager.components
            // console.log(question)
             // Code à exécuter lorsque le bouton est cliqué
    }

    // Autres propriétés et méthodes du composant vue.js
    } 
}
</script>

<style>
@media (min-width: 1024px) {
  .question {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
