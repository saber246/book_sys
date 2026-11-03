import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './assets/main.css'   // 必须放在 element-plus 的 css 之后，才能覆盖它的默认样式
import zhCn from 'element-plus/es/locale/lang/zh-cn'

const app = createApp(App)

app.use(router).use(ElementPlus,{locale: zhCn})

app.mount('#app')
