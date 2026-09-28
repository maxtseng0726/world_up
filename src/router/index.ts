import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import Home from "../views/Home.vue";
import Goals from "../views/Goals.vue";
import Levels from "../views/Levels.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: Home, // Root path '/' loads Home.vue
  },
  {
    path: "/home",
    name: "HomeAlias",
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
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
