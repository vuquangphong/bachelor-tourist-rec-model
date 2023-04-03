import { createWebHistory, createRouter } from "vue-router";
import AttractionPage from '../pages/AttractionPage.vue';
import HotelPage from '../pages/HotelPage.vue';

const routes = [
    { path: '/attractions', component: AttractionPage },
    { path: '/hotels', component: HotelPage }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;