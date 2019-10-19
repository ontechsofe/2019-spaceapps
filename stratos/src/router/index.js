import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '../views/Main.vue'
import Upload from '../views/Upload.vue'
import Landing from '../views/Landing.vue'
import SelectVisualizer from "../views/SelectVisualizer";
// import Full from '../views/Full.vue'

Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        name: 'landing',
        component: Landing
    },
    {
        path: '/upload',
        name: 'upload',
        component: Upload
    },
    {
        path: '/visualizer',
        name: 'selector',
        component: SelectVisualizer
    },
    {
        path: '/visualizer/:id',
        name: 'visualizer',
        component: Main
    }
];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
});

export default router
