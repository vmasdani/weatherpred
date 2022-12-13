import { createApp, ref } from "vue";
import App from "./App.vue";
import router from "./router";

import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "bootstrap/dist/css/bootstrap.min.css";
import OpenLayersMap from "vue3-openlayers";
import "vue3-openlayers/dist/vue3-openlayers.css";

export const ctx = ref({});

const app = createApp(App);

app.use(OpenLayersMap);
app.use(router);

app.mount("#app");
