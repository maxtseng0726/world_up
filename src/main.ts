import { createApp } from "vue";
import App from "./App.vue";
import router from "./scripts/router.ts";
import "./assets/main.css";

createApp(App).use(router).mount("#app");
