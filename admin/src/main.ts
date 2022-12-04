import { createApp, ref } from "vue";
import App from "./App.vue";
import router from "./router";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "bootstrap/dist/css/bootstrap.min.css";
import "vue-select/dist/vue-select.css";

export const ctx = ref({
  loggedIn: false,
});

createApp(App).use(router).mount("#app");
