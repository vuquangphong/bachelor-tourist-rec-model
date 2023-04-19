import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './routers/index'
import VueGoogleMaps from '@fawmi/vue-google-maps'

const pinia = createPinia()

const app = createApp(App)

app.use(router)
app.use(pinia)
app.use(VueGoogleMaps, {
    load: {
        key: 'AIzaSyChKvIKcbVQKSRq3u7QJ7AIIHhYgj2wGDI'
    }
});

app.mount('#app')
