<script setup lang="ts">
import { ref } from "vue";
import { fetchSnapshots, fetchCamera } from "@/helpers";

const snapshots = ref([] as any[]);
const cameras = ref([] as any[]);

const init = async () => {
  snapshots.value = await fetchSnapshots();
  cameras.value = await fetchCamera();
};

const baseUrl = process.env.VUE_APP_BASE_URL;

init();
</script>
<template>
  <div>
    <h4>Prediction Snapshot</h4>
  </div>
  <hr class="border border-dark" />
  <div class="container">
    <div
      class="overflow-auto shadow shadow-md border border-dark"
      style="height: 75vh"
    >
      <table
        class="table table-sm table-hover"
        style="border-collapse: separate"
      >
        <tr>
          <th
            style="position: sticky; top: 0"
            class="bg-dark text-light"
            v-for="h in ['#', 'Camera', 'Prediction', 'Created', 'View Image']"
          >
            {{ h }}
          </th>
        </tr>
        <tr v-for="(s, i) of snapshots">
          <td class="border border-dark">{{ i + 1 }}</td>
          <td class="border border-dark">
            {{ cameras.find((c) => `${c.id}` === `${s.camera_id}`)?.name }}
          </td>
          <td class="border border-dark">{{ s?.prediction }}</td>
          <td class="border border-dark">{{ s?.created }}</td>
          <td class="border border-dark">
            <a :href="`${baseUrl}/snapshots/${s?.id}`" target="_blank"
              ><button>Preview</button></a
            >
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>
