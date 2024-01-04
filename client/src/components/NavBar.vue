<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useSessionStore } from '@/stores/session';
import { onMounted, ref, nextTick } from 'vue';
const session = useSessionStore()
const accordionLinks = ref()

onMounted( () => {
  if(session.isAuthenticated) {
    session.fetchStats()
  }
})

const menuOpen = ref(false)
const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
  nextTick(() => {
    console.log(accordionLinks)
    accordionLinks.value.focus()
  })
}

</script>

<template>
  <nav v-if="session.isAuthenticated" class="nav-full">
    <div class="logo"><RouterLink to="/">ぶんしょう</RouterLink></div>
    <div class="link-container-full">
      <div class="progress-link">
        <RouterLink to="/" class="nav-link">Study</RouterLink>
        <div class="progress-badge"><div class="progress-text">{{ session.userStats?.available_words }}</div></div>
      </div>
      <div class="progress-link">
        <RouterLink to="/learn" class="nav-link">Learn</RouterLink>
        <div class="progress-badge"><div class="progress-text"> {{ session.userStats?.available_sentences }}</div></div>
      </div>
      <RouterLink to="/sentences" class="nav-link">Sentences</RouterLink>
      </div>
      <div class="link-container-full account-links">
        <a class="nav-link">{{ session.getUser().username }}</a>
        <a class="nav-link logout" @click="session.logout()">Log out</a>
      </div>
    </nav>
    <nav class="nav-full" v-else>
      <div class="logo"><RouterLink to="/">ぶんしょう</RouterLink></div>
      <RouterLink to="/login" class="nav-link">Login</RouterLink>
    </nav>
  <nav class="nav-small" :class="`${menuOpen ? 'open' : ''}`" v-if="session.isAuthenticated">
    <div class="logo"><RouterLink to="/">ぶんしょう</RouterLink></div>
    <button @click="toggleMenu"><img src="/menu.svg" /></button>
  </nav>
  <nav class="nav-small" v-else>
    <div class="logo"><RouterLink to="/">ぶんしょう</RouterLink></div>
    <RouterLink to="/login" class="nav-link">Login</RouterLink>
  </nav>
  <nav v-if="session.isAuthenticated" class="link-container-mobile" :class="`${menuOpen ? 'open' : 'closed'}`">
      <div @blur="toggleMenu" ref="accordionLinks" class="accordion-links">
          <div class="link-container user-link">
            <a>{{ session.getUser().username }}</a>
          </div>
          <div class="progress-link">
            <RouterLink to="/" @click="toggleMenu" tabindex="0" class="nav-link">Study</RouterLink>
            <div class="progress-badge"><div class="progress-text">{{ session.userStats?.available_words }}</div></div>
          </div>
          <div class="progress-link">
            <RouterLink to="/learn" @click="toggleMenu" class="nav-link">Learn</RouterLink>
            <div class="progress-badge"><div class="progress-text"> {{ session.userStats?.available_sentences }}</div></div>
          </div>
          <div class="link-container">
            <RouterLink to="/sentences" @click="toggleMenu" class="nav-link">Sentences</RouterLink>
          </div>
          <div class="link-container">
            <button class="logout-button"><a class="nav-link" @click="session.logout()">Log out</a></button>
          </div>
      </div>
    </nav>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Slackside+One&display=swap');

nav {
  width: 100%;
  margin: 1rem 0rem 2rem 0rem;
  padding: 0rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1rem;
  text-align: center;
}

nav button {
  background-color: rgb(0, 107, 189);
  color: white;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  height: fit-content;
  /* transition: ease-in 0.25s; */
}

.user-link a {
  color: white;
}

.user-link a:hover {
  color: rgb(209, 209, 209);
}

.logout-button a {
  color: white;
  font-size: 1.25rem;
  transition: ease-out 0.15s;
}

.login-container {
  display: flex;
  justify-content: right;
  transition: ease-in 0.25s;
}

a + a {
  border-left: 1px solid var(--color-border);
  height: fit-content;
}

nav a.nav-link.logout {
  color: rgb(149, 28, 28);
  transition: ease-out 0.15s;
}

nav a.nav-link.logout:hover {
  color: rgb(80, 11, 11);
  transition: ease-in 0.25s;
}

nav img {
  height: 25px;
}

nav.link-container-mobile {
  margin-top: 0px;
  width: 100%;
  color: white;
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 100;
  
  text-align: center;
  overflow: hidden;
  background-color: rgb(248, 248, 248);
  border-bottom: 2px solid rgb(0, 107, 189);
}
.accordion-links {
  width: 100%;
  font-size: 1.25rem;
}

.accordion-links > div {
  padding: 0.5rem 0rem;
}
.accordion-links > div:nth-child(odd) {
  background-color: rgb(252, 252, 252);
}

.accordion-links div.user-link {
  background-color: rgb(0, 107, 189)
}

button.logout-button {
  background-color: rgb(214, 0, 0);
  transition: ease-out 0.15s;
}

button.logout-button:hover {
  background-color: rgb(145, 8, 8);
  transition: ease-in 0.25s;
}

nav.nav-small {
  border-bottom: 2px solid rgb(0, 107, 189);
}
nav.link-container-mobile {
  padding: 0px;
}
nav.link-container-mobile.closed {
  max-height: 0px;
  transition: max-height 0.25s ease-out;
}

nav.link-container-mobile.open {
  max-height: 500px;
  transition: max-height 0.3s ease-in;
}

nav .accordion-links .nav-link {
  padding: 5px 10px;
}

nav .accordion-links .progress-badge {
  padding: 5px 10px;
}

.link-container-full {
  display: flex;
}

.nav-small {
  display: none;
}

nav.nav-small {
  margin-bottom: 0px;
}

nav.nav-full {
  margin-bottom: 4rem;
}

@media only screen and (max-width: 600px) {
  .nav-full {
    display: none;
  }

  .nav-small {
    display: flex;
  }
  nav.link-container-mobile {
    display: flex;
  }
}

.progress-link {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding-right: 7px;
  height: fit-content;
  justify-content: center;
}
.nav-full .progress-link {
  border-right: 1px solid var(--color-border);
}
.progress-badge {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgb(25, 56, 143);
  height: 1.5rem;
  width: 1.5rem;
  border-radius: 50px;
}

.progress-text {
  color: white;
  font-size: 0.75rem;
}

nav .logo a {
    font-family: 'Slackside One', cursive;
    font-size: 2.5rem;
    color: black;
    position: relative;
    top: -10px;
}

nav .logo a:hover {
    color: rgb(25, 56, 143);
  }

nav a.nav-link {
  display: inline-block;
  padding: 0px 10px;
}

nav a:first-of-type {
  border: 0;
}

nav a.router-link-active {
  color: black;
}

a:hover {
  cursor: pointer;
}

</style>
