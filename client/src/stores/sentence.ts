import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import UrlPattern from 'url-pattern'

import { getNode } from '@formkit/core'

export const useSentenceStore = defineStore('sentence', () => {
  
  const baseUrl = 'http://localhost:5000'
  const sentenceListURL = 'http://localhost:5000/api/sentences'
  const dueSentencesURL = 'http://localhost:5000/api/sentences/due/1'

  const parseSentenceUrl = 'http://localhost:5000/api/sentence/process'
  const addSentenceUrl = 'http://localhost:5000/api/sentences'

  const dueWordsURL = 'http://localhost:5000/api/words/due/1'

  const sentenceList = ref({
    next_page: -1,
    prev_page: -1,
    sentences: [{
      id: -1,
      text: '',
      created_at: '',
      seen: false,
      due: '',
      words: []
    }]
  })

  const wordList = ref({
    next_page: -1,
    prev_page: -1,
    words: [{
      word: {
        id: -1,
        pos: -1, 
        text: '',
        gloss: '',
        seen: false,
        last_seen: '',
        due: '',
        interval: 0,
        easing_factor: 0
      },
      sentence: {
        id: -1,
        text: '',
        created_at: '',
        seen: false,
        due: '',
        words: []
      }
    }]
  })

  const shuffle = ( array:any[] ) => {
    let currentIndex = array.length,  randomIndex;
  
    // While there remain elements to shuffle.
    while (currentIndex != 0) {
  
      // Pick a remaining element.
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex--;
  
      // And swap it with the current element.
      [array[currentIndex], array[randomIndex]] = [
        array[randomIndex], array[currentIndex]];
    }
  
    return array;
  }

  const fetchAllSentences = () => {
      return new Promise( (resolve, reject) => {
        axios.get(sentenceListURL)
          .then((response) => {
            sentenceList.value = response.data
            resolve(new Response())
          })
          .catch((error) => {
            reject(new TypeError(error))
        });
    })
  }

  // const fetchDueSentences = async () => {
  //   return new Promise( (resolve, reject) => {
  //     axios.get(dueSentencesURL)
  //       .then((response) => {
  //         sentenceList.value = response.data
  //         resolve(new Response())
  //       })
  //       .catch((error) => {
  //         reject(new TypeError(error))
  //     });
  //   })
  // }

  const fetchDueWords= async () => {
    return new Promise( (resolve, reject) => {
      axios.get(dueWordsURL)
        .then((response) => {
          wordList.value = response.data
          resolve(new Response())
        })
        .catch((error) => {
          reject(new TypeError(error))
      });
    })
  }

  return { 
    fetchAllSentences,
    fetchDueWords, 
    sentenceList, 
    wordList, 
    shuffle,
    parseSentenceUrl,
    addSentenceUrl
  }

})
