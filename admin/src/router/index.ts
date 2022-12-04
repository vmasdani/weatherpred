import {
  createRouter,
  createWebHashHistory,
  createWebHistory,
  RouteRecordRaw,
} from "vue-router";
import HomeView from "../views/HomeView.vue";
import CameraListPage from "../views/CameraListPage.vue";
import PredictionSimulation from "../views/PredictionSimulation.vue";
import PredictionSnapshotHistory from "../views/PredictionSnapshotHistory.vue";

const routes: Array<RouteRecordRaw> = [
  // {
  //   path: "/",
  //   name: "home",
  //   component: HomeView,
  // },
  {
    path: "/cameralist",
    name: "cameralist",
    component: CameraListPage,
  },
  {
    path: "/predictionsimulation",
    name: "predictionsimulation",
    component: PredictionSimulation,
  },
  {
    path: "/snapshothistory",
    name: "snapshothistory",
    component: PredictionSnapshotHistory,
  },
];

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
});

export default router;
