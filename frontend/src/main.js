import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import { createStore } from 'vuex';
import ElementPlus from 'element-plus';
import 'element-plus/lib/theme-chalk/index.css';
import { auth } from "./helper/auth";

import App from './App.vue';
import Home from './pages/Home.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Home', component: Home },
  ],
})

const store = createStore({
  modules: {
    auth,
  },
});


const app = createApp(App);
app.use(router);
app.use(store);
app.use(ElementPlus);
app.mount('#app');
