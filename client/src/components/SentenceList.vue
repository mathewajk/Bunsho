<script setup lang="ts">
import PitchDisplay from './PitchDisplay.vue';
import axios from 'axios';
import {ref} from 'vue'

const path = 'http://localhost:5001/api/sentences';
const sentences = ref({
    sentences: <Sentence[]>[]
})

axios.get(path)
  .then((res) => {
    sentences.value = res.data;
    console.log(sentences.value)
  })
  .catch((error) => {
    console.error(error);
  });
</script>

<template>
  <div class="wrapper">
    <h1>Sentence Overview</h1>
    <div class="add-sentence"><RouterLink to="/add">+ Add sentence</RouterLink></div>
    <div class="sentence-list">
      <div class="sentence-wrapper" v-for="sentence, i in sentences.sentences">
        <div class="sentence-item bg-grey" v-if="i % 2 == 0">
            <span class="sentence-number">{{ i + 1 }}</span>
            {{ sentence.text }}
        </div>
        <div class="sentence-item bg-lgrey" v-else>
            <span class="sentence-number">{{ i + 1 }}</span>
            {{ sentence.text }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>

h1 {
 margin-bottom: 30px;
}

.add-sentence {
  text-align: right;
}
.add-sentence a {
  font-size: 1.25rem;
}

.wrapper {
    min-width: 75%;
}

.sentence-list {
    text-align: left;
    color: rgb(59, 60, 64);
    font-size: 1.5rem;
}

.sentence-item {
    padding: 0px 5px;
    margin-bottom: 10px;
    /* box-shadow: -8px 9px 12px -5px rgba(0,0,0,0.44);
  -webkit-box-shadow: -8px 9px 12px -5px rgba(0,0,0,0.44);
  -moz-box-shadow: -8px 9px 12px -5px rgba(0,0,0,0.44); */
}

.sentence-list {
  margin-top: 20px;
}
.sentence-wrapper .sentence-number {
    display: inline;
    color: rgb(105, 107, 114);
    padding: 0px 10px;
}
.sentence-list span {
    margin: 10px 0px;
}

.bg-grey {
    background-color: rgba(227, 229, 238, 0.5);
}

.bg-lgrey {
    background-color: rgba(227, 229, 238, 0.15);
}

</style>
