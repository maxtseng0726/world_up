import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import Home from "../views/Home.vue";
import Goals from "../views/Goals.vue";
import Levels from "../views/Levels.vue";
import Vocabs from "../views/Vocabs.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Greet",
    component: Goals, // Root path '/' loads Home.vue
  },
  {
    path: "/home",
    name: "Home",
    component: Home, // Optional: handles /home just in case
  },
  {
    path: "/goals",
    name: "Goals",
    component: Goals,
  },
  {
    path: "/levels",
    name: "Levels",
    component: Levels,
  },
  {
    path: "/vocabs/:filename",
    name: "Vocabs",
    component: Vocabs,
    props: true,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
