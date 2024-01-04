<script setup lang="ts">
import ProgressContainer from './progress/ProgressContainer.vue';
import { ref, computed, onMounted } from 'vue'
import { useLearnStore } from '@/stores/learn';

const learn = useLearnStore()

const loading = ref(true)
const showGloss = ref(false)
const activeTransition = ref('')

const toggleGloss = () => showGloss.value = !showGloss.value
const handleEnter = () => showGloss.value ? toNextSentence() : toggleGloss()

const setTransition = (value:string) => activeTransition.value = value

const toNextSentence = () => {
    learn.updateSentence().then( () => {
        setTransition('fade-out')
        setTimeout(() => { 
            toggleGloss()
            getNextSentence() 
        }, 500)
    })
}

const getNextSentence = () => {
    learn.getNextSentence()
    setTransition('fade-in')
}

onMounted ( () => {
    window.addEventListener("keyup", e => {
        if(e.key === 'Enter') {
          handleEnter()
        }
    })
    learn.fetchNewSentences().then( () => {
        loading.value = false
    })
})

</script>

<template>
    <template v-if="!loading"><ProgressContainer :progress="learn.completedPercent" :complete="learn.completedSentences" :total="learn.totalSentences"/>
    <div v-if="learn.sentence" class="sentence" :class="activeTransition">
      <div v-for="word in learn.sentence.words">
        <div class="word">
            {{ word.text }}
        </div>
        <Transition name="grow-fade">
            <div class="gloss" v-if="showGloss">{{ word.gloss }}</div>
        </Transition>
      </div>
      <div class="word">
        。
      </div>
      <Transition name="grow-fade">
            <div class="gloss" v-if="showGloss"></div>
      </Transition>
    </div>
    <div v-else class="study-finished" :class="activeTransition">
        <p>おめでとうございます！新しい文章を全て学習しました。</p>
        <p><RouterLink to='/'>復習に進む</RouterLink>、または<RouterLink to='/sentences'>文章を追加</RouterLink>しましょう。</p>
    </div>
  </template>
  <div class="loading-container" v-else>
    Loading session...
  </div>
</template>
  
<style scoped>

.loading-container {
  text-align: center;
}
.gloss {
  display: flex;
  justify-content: space-around;
  font-size: 1rem;
  top: 10px;
  padding: 0px 20px;
  color: rgb(145, 146, 148);
}

.grow-fade-enter-active {
  transition: opacity 1s ease-in 0.75s, font-size 1.25s cubic-bezier(0,1.02,.31,.95) 0s;
}

.grow-fade-enter-active.hint-active {
  transition: opacity 0.5s ease-in 0.25s, font-size 0.5s cubic-bezier(0,1.02,.31,.95) 0s;
}

.fade-out {
  transition: opacity 0.1s linear;
  opacity: 0;
}

.fade-in {
  transition: opacity 0.25s ease-in;
  opacity: 1;
}

.grow-fade-enter-from,
.grow-fade-leave-to {
  opacity: 0;
  font-size: 0rem;
}

.fade-enter-from, 
.fade-leave-to {
  opacity: 0;
}

.sentence, .unanswered {
  color: rgb(0, 107, 189);
}

.correct {
  text-decoration: none;
  color: rgb(105, 204, 102);
  transition: 0.4s;
}

.incorrect {
  text-decoration: none;
  color: rgb(216, 116, 58);
  transition: 0.4s;
}

.hidden {
  display: none;
}

.word {
  text-align: center;
}

input {
  display: inline-block;
  position: relative;
  border: none;
  border-bottom: 1px solid rgb(145, 146, 148);
  text-decoration: none;
  font-size: 1em;
  height: 1.25em;
  text-align: center;
  margin: 0px 5px;
}

input:focus {
  border: none;
  outline: 2px solid rgb(0, 0, 0);
  border-radius: 5px;
}

.sentence {
  font-weight: 500;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  font-size: 2rem;
  position: relative;
  top: -10px;
  justify-content: center;
}

</style>
