<script setup lang="ts">

import { useSentenceStore } from '@/stores/sentence'

const store = useSentenceStore()

defineProps<{
    i: number,
    word: string,
}>()

</script>

<template>
    <div class="gloss-wrapper">
        <div class="gloss-pair">
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
                <span class="update-form" @click="store.addWord(i)">Add</span> / <span class="update-form" @click="store.removeWord(i)">Remove</span>
            </div>
        </div>
    </div>
</template>