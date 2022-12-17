<script setup lang="ts">
import { fetchCameras, fetchCamerasLatestPrediction } from "@/fetchers";
import {
  LMap,
  LIcon,
  LTileLayer,
  LMarker,
  LControlLayers,
  LTooltip,
  LPopup,
  LPolyline,
  LPolygon,
  LRectangle,
} from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";
import { ref } from "vue";

let zoom = ref(11);
let cameras = ref([] as any[]);

const fetchCamerasData = async () => {
  cameras.value = await fetchCamerasLatestPrediction();
};

const handleInit = () => {
  fetchCamerasData();
};

handleInit();
// export default {
//   components: {
//     LMap,
//     LIcon,
//     LTileLayer,
//     LMarker,
//     LControlLayers,
//     LTooltip,
//     LPopup,
//     LPolyline,
//     LPolygon,
//     LRectangle,
//   },
//   data() {
//     return {
//       zoom: 11,
//       iconWidth: 25,
//       iconHeight: 40,
//     };
//   },
//   computed: {
//     iconUrl() {
//       return `https://placekitten.com/${this.iconWidth}/${this.iconHeight}`;
//     },
//     iconSize() {
//       return [this.iconWidth, this.iconHeight];
//     },
//   },
//   methods: {
//     log(a) {
//       console.log(a);
//     },
//     changeIcon() {
//       this.iconWidth += 2;
//       if (this.iconWidth > this.iconHeight) {
//         this.iconWidth = Math.floor(this.iconHeight / 2);
//       }
//     },
//   },
// };
</script>

<template>
  <div class="container">
    <div style="height: 75vh; width: 100%">
      <l-map
        v-model="zoom"
        v-model:zoom="zoom"
        :minZoom="3"
        :maxZoom="18"
        :center="[-6.218327, 106.783918]"
      >
        <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        ></l-tile-layer>
        <l-control-layers />
        <!-- <l-marker
          :lat-lng="[-6.262565, 106.707178]"
          draggable
          @moveend="log('moveend')"
        >
          <l-tooltip :options="{ permanent: true }"> lol </l-tooltip>
        </l-marker>

        <l-marker :lat-lng="[-6.262565, 106.707178]">
          <l-icon :icon-url="iconUrl" :icon-size="iconSize" />
        </l-marker>

        <l-marker
          :lat-lng="[-6.218327, 106.783918]"
          draggable
          @moveend="log('moveend')"
        >
          <l-popup> lol </l-popup>
        </l-marker> -->

        <l-marker
          v-for="c in cameras"
          :lat-lng="
            c?.camera?.lat && c?.camera?.lng
              ? [c.camera.lat, c.camera.lng]
              : [0, 0]
          "
        >
          <l-tooltip :options="{ permanent: true }">
            <div>
              <div>{{ c?.camera?.name ?? "No name" }}</div>
              <div><strong>{{c?.snapshot?.prediction}}</strong></div>
            </div>
          </l-tooltip>
        </l-marker>
      </l-map>
      <!-- <button @click="changeIcon">New kitten icon</button> -->
    </div>
  </div>
</template>
