<script setup lang="ts">
import { fetchCamera } from "@/helpers";
import { Ref, ref } from "vue";
import VueSelect from "vue-select";

const img = ref(null) as Ref<string | null>;
const cameras = ref([]) as Ref<any[]>;
const selectedCamera = ref(null) as Ref<any>;
const predictionResult = ref(null) as Ref<any>;

const handleSelectFile = async (e: Event) => {
  const f = (e.target as HTMLInputElement).files?.[0];

  if (f) {
    const r = new FileReader();
    r.readAsDataURL(f);

    r.onerror = () => {};
    r.onload = () => {
      img.value = r.result as string;
    };
  }
};

const init = async () => {
  cameras.value = await fetchCamera();
};

const predict = async () => {
  try {
    const resp = await fetch(`${process.env.VUE_APP_BASE_URL}/predict`, {
      method: "post",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        camera_id: selectedCamera?.value?.id,
        image_base_64: img?.value?.split("base64,")?.[1],
        dummy: false,
      }),
    });

    if (resp.status !== 200) throw await resp.text();

    predictionResult.value = await resp.json();
  } catch (e) {
    console.error(e);
  }
};

init();
</script>
<template>
  <div class="container">
    <div>
      <h2>Prediction simulation page</h2>
    </div>
    <hr class="border border-dark" />

    <div>
      <input type="file" @input="handleSelectFile" />
    </div>

    <div>
      <VueSelect
        :options="cameras"
        :getOptionLabel="(c: any) => c?.name"
        @update:modelValue="(c: any) => {
        selectedCamera = c
      }"
      />
    </div>

    <div v-if="selectedCamera">
      <strong>Selected cam: </strong>{{ JSON.stringify(selectedCamera) }}
    </div>

    <div v-if="img">
      <div v-if="selectedCamera">
        <button
          class="btn btn-sm btn-primary"
          @click="
            () => {
              predict();
            }
          "
        >
          Predict
        </button>
      </div>
      <div class="w-100 d-flex justify-content-center">
        <img :src="img" style="width: 30vw" />
      </div>
    </div>

    <div v-if="predictionResult">
      <strong>Prediction Result:</strong>{{ JSON.stringify(predictionResult) }}
    </div>
  </div>
</template>
