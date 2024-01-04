<script setup lang="ts">
  import { RouterView, RouterLink } from 'vue-router'
  import NavBar from './components/NavBar.vue'
  import { useSessionStore } from '@/stores/session'

  const session = useSessionStore();
  session.refreshJwtToken()
  setInterval(session.refreshJwtToken, 60000);
</script>

<template>
  <NavBar />
  <RouterView v-if="!session.isLoading"/>
</template>

<style scoped>
</style>
