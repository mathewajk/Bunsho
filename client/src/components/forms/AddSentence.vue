<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios';
import { getNode } from '@formkit/core'
import router from '@/router';

const parseSentenceUrl = 'http://localhost:5001/api/sentence/process'
const addSentenceUrl = 'http://localhost:5001/api/sentences'

const parseSentence = ( fields:any ) => {
    const splitSentence = fields.sentence.split(' ')
    if(splitSentence.length > 1) {
        parsedSentence.value = splitSentence
    } else {
        axios.post(parseSentenceUrl, fields).then( (result) => {
                parsedSentence.value = result.data.result
            }
        )
    }
}

const addSentence = ( fields:any ) => {
    let data = {sentence: '', words: <string[]>[], gloss: <string[]>[]}
    parsedSentence.value.forEach( (word, i) => {
        data.sentence += fields['word-' + i]
        data.words.push(fields['word-' + i])
        data.gloss.push(fields['gloss-' + i])
    })
    axios.post(addSentenceUrl, data).then( (result) => {
        router.push('sentences')
    })
}

const addWord = ( pos:number ) => {
    parsedSentence.value.splice(pos + 1, 0, '')
    parsedSentence.value.forEach( (word, i) => {
        if (i < pos + 1) {
            getNode('word-' + i)?.input(getNode('word-' + i)?.value)
        } else if (i == pos + 1) {
            getNode('word-' + i)?.input('')
        } else if (i > pos + 1) {
            getNode('word-' + i)?.input(getNode('word-' + (i-1))?.value)
        }
    })
}

const removeWord = ( pos:number ) => {
    parsedSentence.value.splice(pos, 1)
    parsedSentence.value.forEach( (word, i) => {
        if (i < pos) {
            getNode('word-' + i)?.input(getNode('word-' + i)?.value)
        } else if (i >= pos) {
            getNode('word-' + i)?.input(getNode('word-' + (i+1))?.value)
        }
    })
}

const parsedSentence = ref<string[]>([])

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
        <FormKit type="form" @submit="addSentence">
            <div class="gloss-wrapper">
                <div class="gloss-pair" v-for="word, i in parsedSentence">
                    <label class="formkit-outer">
                        Word {{ i+1 }}
                    </label>
                    <FormKit 
                        type="text"
                        :name="'word-' + i"
                        :id="'word-' + i"
                        :value="word"
                        help=""
                        validation="required"
                        placeholder="Lexical item"
                    />
                    <FormKit 
                        type="text"
                        :name="'gloss-' + i"
                        :id="'gloss-' + i"
                        help=""
                        validation="required"
                        placeholder="Gloss"
                    />
                    <div class="formkit-outer">
                        <span class="update-form" @click="addWord(i)">Add</span> / <span class="update-form" @click="removeWord(i)">Remove</span>
                    </div>
                </div>
            </div>
        </FormKit>
    </template>
    </div>
</template>

<style>

h1 {
 margin-bottom: 50px;
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