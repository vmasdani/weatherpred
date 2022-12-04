<script setup lang="ts">
import { fetchCamera } from "@/helpers";
import { Ref, ref } from "vue";

const cameras = ref([]) as Ref<any[]>;

const handleSave = async () => {
  try {
    const resp = await fetch(
      `${process.env.VUE_APP_BASE_URL}/cameras-save-bulk`,
      {
        method: "post",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(cameras.value),
      }
    );
  } catch (e) {
    console.error(e);
  }
};

const init = async () => {
  cameras.value = await fetchCamera();
};

init();
</script>
<template>
  <div class="container">
    <div class="d-flex align-items-center">
      <h2>Camera list page</h2>
      <button
        class="btn btn-sm btn-primary"
        @click="
          () => {
            handleSave();
          }
        "
      >
        Save
      </button>
    </div>
    <hr class="border border-dark" />
    <div>
      <button
        class="btn btn-sm btn-primary"
        @click="
          () => {
            cameras?.push({});
          }
        "
      >
        Add
      </button>
    </div>
    <div
      class="overflow-auto border border-dark shadow shadow-md"
      style="height: 75vh"
    >
      <table
        class="table table-sm table-hover"
        style="border-collapse: separate"
      >
        <tr>
          <th
            v-for="h in ['#', 'Name', 'IP address', 'Created']"
            style="position: sticky; top: 0"
            class="bg-dark text-light"
          >
            {{ h }}
          </th>
        </tr>
        <tr v-for="(c, i) of (cameras as any)">
          <td class="border border-dark">{{ i + 1 }}</td>
          <td class="border border-dark">
            <input
              placeholder="Camera name..."
              class="form-control form-control-sm p-1"
              :value="c?.name"
              @blur="(e) => {
              if (c) {
                c.name = (e.target as HTMLInputElement).value
              }
            }"
            />
            <!-- {{ c?.name }} -->
          </td>
          <td class="border border-dark">
            <input
              placeholder="Camera IP address..."
              class="form-control form-control-sm p-1"
              :value="c?.ip_address"
              @blur="(e) => {
              if (c) {
                c.ip_address = (e.target as HTMLInputElement).value
              }
            }"
            />
            <!-- {{ c?.ip_address }} -->
          </td>
          <td class="border border-dark">{{ c?.created }}</td>
        </tr>
      </table>
    </div>
  </div>
</template>
