import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { plugin } from '@formkit/vue'
import defaultConfig from '../formkit.config'

import timeago from 'vue-timeago3'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(timeago)
app.use(plugin, defaultConfig)

app.mount('#app')
