<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
    progress: number,
    complete: number,
    total: number
}>()

</script>

<template>
    <div class="graph-container">
        <div class="graph-bar" :style="{'width': `${progress}%`}">
        </div>
        <!-- <div>{{ complete }} of {{ total }}</div> -->
    </div>
</template>

<style scoped>

.graph-container {
    width: 500px;
    border-radius: 10px;
    border: 3px solid rgb(0, 107, 189);
    height: 20px;
    position: relative;
}

.graph-bar {
    background-color: rgb(0, 107, 189);
    height: 100%;
    position: absolute;
    top: 0;
}

</style>