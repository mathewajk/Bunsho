<script setup lang="ts">
import LearnSentence from '../components/study/LearnSentence.vue'
import { useSessionStore } from '@/stores/session';
const session = useSessionStore()
</script>

<template>
    <main>
      <div class="wrapper">
        <LearnSentence v-if="session.isAuthenticated"/>
      </div>
    </main>
</template>

<style scoped>

</style>
