<script setup lang="ts">

import { useQuizStore } from '@/stores/quiz'
import { ref, onMounted, nextTick } from 'vue'
import ProgressContainer from './progress/ProgressContainer.vue';

const quiz = useQuizStore()

const input  = ref()
const answer = ref('')

const focusInput = () => {
  nextTick(() => {
    if(input.value) {
      input.value[0].focus()
    }
  })
}

const handleInput = () => {
  if(answer.value) {
    quiz.state.index++
    quiz.state.showGloss = true
    quiz.state.inputDisabled = true
    if (answer.value == quiz.question.target?.text) {
      quiz.state.answerStatus = 'correct'
    } else {
      quiz.state.answerStatus = 'incorrect'  
    }
  }
}

const hintActive = ( word : Word) => {
  if(quiz.state.hintActive && word === quiz.question.target) {
    return 'hint-active'
  }
}

const toNextSentence = ( event : Event ) => {
  let element = event.target as HTMLElement
  if(quiz.state.answerStatus !== 'unanswered' && element.tagName != "INPUT") {
    quiz.updateWord().then( (response) => {
      quiz.state.activeTransition = 'fade-out'
      setTimeout(() => { 
        answer.value = ''
        quiz.setNextSentence()
        quiz.initState()
        focusInput()
      }, 500)
    })
  }
}

onMounted( () => {
  window.addEventListener("keyup", e => {
		if(e.key === 'Enter') {
      toNextSentence(e)
    }
    if(e.key == 'Escape') {
      quiz.state.hintActive = true
    }
	});
  quiz.initSession().then(() => { focusInput() })
})


</script>

<template>
  <ProgressContainer :progress="quiz.completedPercent()" :complete="quiz.state.index" :total="quiz.state.words.length"/>
  <div v-if=quiz.question.sentence class="sentence" :class="quiz.state.activeTransition">
    <div v-for="word in quiz.question.sentence.words">
      <div class="word">
        <template v-if="word.pos == quiz.question.target?.pos">
          <input 
          type="text"
          ref="input"
          v-model="answer"
          :class="quiz.state.answerStatus"
          :disabled="quiz.state.inputDisabled"
          @keyup.enter="handleInput"
          :size="word.text.length + 1">
        </template>
        <template v-else>
          {{ word.text }}
        </template>
      </div>
      <Transition name="grow-fade">
          <div class="gloss" :class="hintActive(word)" v-if="quiz.state.showGloss || hintActive(word)">{{ word.gloss }}</div>
      </Transition>
    </div>
    <div class="word">
      。
    </div>
    <Transition name="grow-fade">
          <div class="gloss" v-if="quiz.state.showGloss"></div>
    </Transition>
  </div>
  <div v-else class="study-finished" :class="quiz.state.activeTransition">
      <p>おめでとうございます！学習が終わりました。</p>
      <p>再読み込み、または新しい文章を勉強しますか？</p>
  </div>
</template>

<style scoped>

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
