<script setup lang="ts">

defineProps<{
    word: {
        pos: string,
        text: string
    },
    question: {
        target: {
            pos: string
        }
    },
    answer: string,
    status: string,
    disabled: boolean
}>()

</script>

<template>
    <div class="word">
    <template v-if="word.pos == question.target.pos">
        <input 
        type="text"
        ref="input"
        v-model="answer"
        :class="status"
        :disabled="disabled"
        :size="word.text.length + 1">
    </template>
    <template v-else>
        {{ word.text }}
    </template>
    </div>
</template>