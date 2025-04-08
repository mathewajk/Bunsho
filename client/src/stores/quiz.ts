import { ref, reactive } from 'vue'
import { defineStore } from 'pinia'
import { useSentenceStore } from '@/stores/sentence'

import UrlPattern from 'url-pattern'
import type { Ref } from 'vue'

import axios from 'axios'

export const useQuizStore = defineStore('quiz', () => {

  const sentenceStore = useSentenceStore()
  const baseUrl = 'http://localhost:5000'
  const updateWordURL = new UrlPattern('/api/words(/:id)')

  const question = ref<Question>({
    sentence: null,
    target: null
  })

  const completedPercent = () => {
    return state.words.length != 0 ? state.index / state.words.length * 100 : 100
  }

  const sentencesCompletedPercent = () => {
    return state.sentences.length != 0 ? state.index / state.sentences.length * 100 : 100
  }

  const state = reactive({
    answerStatus: 'unanswered',
    hintActive: false,
    showGloss: false,
    inputDisabled: false,
    activeTransition: '',
    index: 0,
    words: <any>[],
    sentences: <any>[]
  })

  const initState = () => {
    state.answerStatus = 'unanswered'
    state.showGloss = false
    state.inputDisabled = false
    state.activeTransition = 'fade-in'
    state.hintActive = false
  }

  const initSession = () => {
    return new Promise((resolve, reject) => {
        sentenceStore.fetchDueWords().then( () => {
          if(sentenceStore.wordList.words.length) {
            state.words = sentenceStore.shuffle(sentenceStore.wordList.words)
            initState()
            setNextSentence()
          }
          resolve( new Response() )
        }).catch(() => {
          reject(new TypeError("Error!"))
      })
    })
  }

  const nextSentence = () => {
    if(state.index >= state.words.length) {
      return {
        sentence: null,
        target: null
      }
    }
    return {
      sentence: state.words[state.index].sentence,
      target: state.words[state.index].word
    }
  }

  const setNextSentence = ( ) => {          
    question.value = nextSentence()
  }

  const updateWord = async () => {
    if(!question.value.target) {
      return
    }
    if(state.answerStatus == 'incorrect') {
      question.value.target.interval = 1
      question.value.target.due = new Date(Date.now()).toISOString()
    } else {
      question.value.target.due = new Date(Date.now() + 10800000 * question.value.target.interval).toISOString()
      question.value.target.interval = question.value.target.interval * question.value.target.easing_factor
    }

    return axios.post(baseUrl + updateWordURL.stringify({ id: question.value.target.id }), question.value.target)
  }

  return { initSession, updateWord, initState, setNextSentence, question, state, completedPercent }
})