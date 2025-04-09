import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

import axios from 'axios'
import UrlPattern from 'url-pattern'

export const useLearnStore = defineStore('learn', () => {
    const baseUrl = import.meta.env.VITE_API_URL
    const updateSentenceURL = new UrlPattern('/api/sentences(/:id)')
    const newSentencesURL = new UrlPattern('/api/sentences/new(/:page)')

    const sentences = ref(<Sentence[]>[])
    const pos = ref(-1)
    const sentence = ref<Sentence|null>(null)

    const totalSentences = computed(() => sentences.value.length)
    const completedSentences = computed(() => totalSentences.value ? pos.value : 0)
    const completedPercent = computed(() => totalSentences.value ? Math.floor(pos.value / totalSentences.value * 100) : 100)
    const hasNextSentence = computed(() => pos.value < totalSentences.value)

    const incrementPos  = () => pos.value++
    const setSentence   = () => sentence.value = sentences.value[pos.value]
    const clearSentence = () => sentence.value = null

    const setSentences  = (payload:Sentence[]) => sentences.value = shuffle(payload)

    const getNextSentence = () => {
        incrementPos()
        hasNextSentence ? setSentence() : clearSentence()
    }

    const fetchNewSentences = async () => {
        return new Promise( (resolve, reject) => {
            axios.get(baseUrl + newSentencesURL.stringify({ page: 1 })).then((response) => {
                setSentences(response.data.sentences)
                getNextSentence()
                resolve(new Response())
            })
            .catch((error) => {
                reject(new TypeError(error))
            })
        })
    }

    const shuffle = ( array:any[] ) => {
        let currentIndex = array.length,  randomIndex;
        while (currentIndex != 0) {
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex--;
            [array[currentIndex], array[randomIndex]] = [
            array[randomIndex], array[currentIndex]];
        }
        return array;
    }

    const updateSentence = async() => {
        if(sentence.value) {
            return axios.post(baseUrl + updateSentenceURL.stringify({ id: sentence.value.id }), sentence)
        }
    }

    return { sentence, fetchNewSentences, getNextSentence, updateSentence, completedSentences, completedPercent, totalSentences }
})