import { createApp, ref } from "vue";
import App from "./App.vue";
import router from "./router";

import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "bootstrap/dist/css/bootstrap.min.css";

export const ctx = ref({});

createApp(App).use(router).mount("#app");
