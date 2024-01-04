<script setup lang="ts">
import ProgressBar from './ProgressBar.vue';
import { ref } from 'vue'

defineProps<{
    progress: number,
    complete: number,
    total: number
}>()

const refresh = () => {
    window.location.reload()
}
</script>

<template>
    <div class="progress-container">
        <div class="session-header"><h2 class="progress-item">Progress</h2></div>
        <ProgressBar class="progress-item" :progress="progress" :complete="complete" :total="total"/>
        <div class="progress-item">{{ complete }} / {{ total }}</div>
        <div class="progress-item"><a @click="refresh">Refresh?</a></div>
    </div>
</template>

<style scoped>

a:hover {
    cursor: pointer;
}
.progress-container {
    display: flex;
    flex-direction: row;
    margin: 0rem auto 6rem auto;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

.progress-item {
    margin: 0px 10px;
}

.session-header {
    width: min-content;
}
h2 {
    font-size: 1rem;
    font-weight: 500;
    line-height: 1rem;
}

</style>