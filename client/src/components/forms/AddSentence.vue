<script setup lang="ts">
import { ref, computed } from 'vue'
import axios from 'axios';
import { getNode } from '@formkit/core'
import router from '@/router';

const parseSentenceUrl = 'http://localhost:5000/api/sentence/process'
const addSentenceUrl = 'http://localhost:5000/api/sentences'

let id = 0
const incrementId = () => {
    return id++
}

const parsedSentence = ref<any[]>([])
const parseSentence = ( fields:any ) => {
    const splitSentence = fields.sentence.split(' ')
    if(splitSentence.length > 1) {
        parsedSentence.value = splitSentence.map((word:string, i:number) => { return {'id': incrementId(), 'word': word, 'gloss': 'test', 'deleted': false} })
    } else {
        axios.post(parseSentenceUrl, fields).then( (result) => {
                parsedSentence.value = result.data.result.map((word:string, i:number) => { return {'id': incrementId(), 'word': word, 'gloss': 'test', 'deleted': false} })
            }
        )
    }
}

const getIndex = (word:any) => {
    return parsedSentence.value.findIndex( (parsedWord:any) => parsedWord.id == word.id)
}

const filteredWords = computed(() => parsedSentence.value.filter( (word) => word.deleted == false) )
const getFilteredIndex = (word:any) => {
    return filteredWords.value.findIndex( (parsedWord:any) => parsedWord.id == word.id)
}

const addSentence = ( fields:any ) => {
    let data = {sentence: '', words: <string[]>[], gloss: <string[]>[]}
    parsedSentence.value.forEach( (word, i) => {
        if(word.deleted) { return }
        data.sentence += word
        data.words.push(word.word)
        data.gloss.push(word.gloss)
    })
    axios.post(addSentenceUrl, data).then( (result) => {
        router.push('sentences')
    })
}

const syncInput = () => {
    parsedSentence.value.forEach( (word, i) => {
        getNode('word-' + i)?.input(word.word)
        getNode('gloss-' + i)?.input(word.gloss)
    })
}

const addWord = ( pos:number ) => {
    console.log("Adding word at " + pos)
    parsedSentence.value.splice(pos, 0, {
        word: '',
        gloss: '',
        deleted: false,
        id: incrementId()
    })
    syncInput()
}

const removeWord = ( pos:number ) => { parsedSentence.value[pos].deleted = true }

const updateSentence = () => {
    parsedSentence.value.forEach( (word, i) => {
        word.word = formData.value['word-' + i]
        word.gloss = formData.value['gloss-' + i]
    })
}

const formData = ref()

</script>

<template>
    <div class="wrapper">
    <h1>Add a sentence</h1>
    <template v-if="!parsedSentence.length">
        <FormKit type="form" @submit="parseSentence" submit-label="Next">
            <FormKit
                type="text"
                name="sentence"
                id="sentence"
                label="Sentence*"
                validation="required"
                help="Enter the sentence you would like to gloss."
                placeholder="吾輩は猫である"
            />
        </FormKit>
    </template>
    <template v-else>
        {{  filteredWords }}
        <FormKit v-model="formData" type="form" @submit="addSentence" @change="updateSentence">
            <div class="gloss-wrapper">
                <div class="gloss-pair" v-for="word, i in parsedSentence">
                    <label class="formkit-outer" v-if="!word.deleted">
                        Word {{ getFilteredIndex(word) + 1 }}
                    </label>
                    <FormKit 
                        type="text"
                        :outer-class="word.deleted ? 'hidden' : ''"
                        :id="'word-' + i"
                        :name="'word-' + i"
                        :value="word.word"
                        help=""
                        validation="required"
                        placeholder="Lexical item"
                    />
                    <FormKit
                        type="text"
                        :outer-class="word.deleted ? 'hidden' : ''"
                        :value="word.gloss"
                        :id="'gloss-' + i"
                        :name="'gloss-' + i"
                        help=""
                        validation="required"
                        placeholder="Gloss"
                    />
                    <div class="formkit-outer" v-if="!word.deleted">
                        <span class="update-form" @click="addWord(i + 1)">Add</span> / <span class="update-form" @click="removeWord(i)">Remove</span>
                    </div>
                </div>
            </div>
        </FormKit>
    </template>
    </div>
</template>

<style>

.hidden {
    display: none;
}

h1 {
 margin-bottom: 50px;
 font-size: 2rem;
}

.wrapper {
    min-width: 50%;
}

form {
    width: 100%;
    font-size: 1.25rem;
}

form input {
    border: 1px solid;
    border-radius: 10px;
    padding: 10px;
    font-size: 1.25rem;
}

form .formkit-outer {
    margin-bottom: 50px;
}

form .formkit-wrapper button {
    background-color: rgb(0, 107, 189);
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 50px;
    font-size: 1.25rem;
}

form .formkit-wrapper button:hover {
    cursor: pointer;
}

form .formkit-help {
    font-size: 0.75em;
    color: hsl(231, 7%, 37%)
}

span.update-form {
    color: rgb(0, 107, 189);
}

span.update-form:hover {
    cursor: pointer;
    color: rgb(0, 47, 178);
    transition: color 0.5s;
}

.formkit-label {
    margin-right: 15px;
}

.gloss-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-around;
    margin-bottom: 50px;
}

.gloss-pair {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}

.gloss-wrapper .formkit-outer {
    margin: 10px 10px;
}

</style>