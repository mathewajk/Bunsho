import { ref, reactive, computed } from 'vue'
import { defineStore } from 'pinia'
import router from '@/router'
import type { Ref } from 'vue'
import UrlPattern from 'url-pattern'
import axios from 'axios'

export const useSessionStore = defineStore('session', () => {

  const baseUrl = import.meta.env.VITE_API_URL
  const tokenUrl = `${baseUrl}/auth/token`
  const loginUrl = `${baseUrl}/auth/login`
  const logoutUrl = `${baseUrl}/auth/logout`
  const registerUrl = `${baseUrl}/auth/register`

  const state = reactive({
    token: localStorage.getItem('token'),
    csrf: '',
    user: <any>{},
    loading: true
  })

  const isLoading = computed(() => {
    return state.loading
  })

  const isAuthenticated = computed(() => {
    return state.token
  })

  const setJwtToken = (payload:any) => {
    localStorage.setItem('token', payload.token)
    state.token = payload.token
    state.user = payload.user
    axios.defaults.headers.common['Authorization'] = localStorage.getItem('token')
  }

  const clearJwtToken = () => {
    console.log("Clearing token!")
    state.user = null
    state.token = ''
    localStorage.setItem('token', '')
    axios.defaults.headers.common['Authorization'] = null
  }

  const isValidJwt = (token:string) => {
    console.log("Validating!")
    if (!token || token.split('.').length < 3) {
      console.log("Not valid format...")
        return false
    }
    const data = JSON.parse(atob(token.split('.')[1]))
    const exp = new Date(data.exp * 1000)
    const now = new Date()
    console.log(exp)
    console.log(now)
    console.log(now < exp)
    return now < exp
  }

  const refreshJwtToken = () => {
    axios.defaults.headers.common['Authorization'] = localStorage.getItem('token')
    axios.get(tokenUrl).then( (response) => {
      console.log(localStorage.getItem('token'))
      console.log("Refreshing token!")
      console.log(response)
      if(isValidJwt(response.data.token)) {
        setJwtToken(response.data)
        fetchStats()
      } else {
        clearJwtToken()
      }
      state.loading = false;
    });
  }

  const login = (username:string, password:string) => {
    axios.post(loginUrl, {
      username: username,
      password: password,
    }).then( (response) => {
      if(isValidJwt(response.data.token)) {
        setJwtToken(response.data)
        state.csrf = response.headers["X-CSRFToken"]
        console.log(router)
        console.log(state.csrf)
        router.push('/')
      } else {
        console.log("Error!")
      }
    })
  }

  const logout = () => {
    axios.post(logoutUrl, {username: 'mathewajk'})
    clearJwtToken()
    router.push('/')
  }

  const register = (email:string, username:string, password:string) => {
    return axios.post(registerUrl, {
      email: email,
      username: username,
      password: password,
    })
  }

  const statsURL = new UrlPattern('/api/stats')
  type UserStats = {
    available_sentences: number,
    available_words: number
  }

  const userStats = ref<UserStats>({ available_sentences: 0, available_words: 0 })
  const fetchStats = () => {
    return axios.get(baseUrl + statsURL.stringify())
        .then((response) => {
          userStats.value = response.data
        })
  }

  const getUser = () => {
    return state.user
  }

  return { isLoading, isAuthenticated, setJwtToken, refreshJwtToken, login, logout, fetchStats, userStats, getUser, register }
})