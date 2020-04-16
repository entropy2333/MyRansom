import Vue from 'vue';
import Router from 'vue-router';
import Victims from './components/Victims.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Victims',
      component: Victims,
    },
  ],
});
