<script setup lang="ts">
import WordReview from '../components/study/WordReview.vue'
import { useSessionStore } from '@/stores/session';
const session = useSessionStore()
</script>

<template>
    <main>
      <div class="wrapper">
        <WordReview v-if="session.isAuthenticated" />
        <div class="welcome-card" v-else>
          <h1>Welcome to Bunsho!</h1>
          <p>Please <RouterLink to="login">log in</RouterLink>.</p>
        </div>
      </div>
    </main>
</template>

<style scoped>
.welcome-card {
  text-align: center;
}
</style>
