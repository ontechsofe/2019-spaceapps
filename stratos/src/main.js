import Vue from 'vue';
import App from './App.vue';
import './registerServiceWorker';
import router from './router';
import vuetify from './plugins/vuetify';
import VueCesium from 'vue-cesium';

Vue.config.productionTip = false;

Vue.use(VueCesium, {
  cesiumPath: 'https://unpkg.com/cesium/Build/Cesium/Cesium.js',
  accessToken: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJmZmM0YTRiZi05OTAzLTQ2ZTAtYmNmOS05ZTY5OWRmYjU5NDEiLCJpZCI6MTcwMzcsInNjb3BlcyI6WyJhc3IiLCJnYyJdLCJpYXQiOjE1NzE1MTE3ODZ9.N6cBSqS8AmfmQ9iOskB5JHJJhwge1kUGSXV3IhFDdxA'
});

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app');
