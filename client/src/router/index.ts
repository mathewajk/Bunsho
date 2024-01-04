import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SentenceListView from '../views/SentenceListView.vue'
import SentenceStudyView from '../views/SentenceStudyView.vue'
import AddSentenceView from '../views/AddSentenceView.vue'
import LoginView from '../views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/sentences',
      name: 'sentences',
      component: SentenceListView
    },
    {
      path: '/sentences/:id',
      name: 'sentence',
      component: HomeView
    },
    {
      path: '/learn',
      name: 'learn',
      component: SentenceStudyView
    },
    {
      path: '/add',
      name: 'add',
      component: AddSentenceView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
  ]
})

export default router
