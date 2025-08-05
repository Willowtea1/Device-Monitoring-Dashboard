import { createApp } from 'vue'
import App from './App.vue'
import { createVuetify } from 'vuetify'
import 'vuetify/styles'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import router from './router'
import './styles/global.css'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light', // or 'dark'
    themes: {
      light: {
        colors: {
          background: '#ffffffff', // 👈 your custom background color
        },
      },
      dark: {
        colors: {
          background: '#121212',
        },
      },
    },
  },
})

createApp(App).use(router).use(vuetify).mount('#app')
