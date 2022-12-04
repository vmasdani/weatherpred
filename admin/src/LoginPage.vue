<script setup lang="ts">
import { ctx } from "./main";

ctx;
</script>
<template>
  <div class="vh-100 vw-100 d-flex justify-content-center align-items-center">
    <div class="border border-dark shadow shadow-md p-3">
      <!-- <div>
        <input class="form-control form-control-sm" placeholder="Username..." />
      </div> -->
      <div>
        <input
          class="form-control form-control-sm"
          placeholder="Passphrase..."
        />
      </div>
      <div>
        <div
          class="btn btn-sm btn-primary"
          @click="
            () => {
              ctx.loggedIn = true;
            }
          "
        >
          Login
        </div>
      </div>
    </div>
  </div>
</template>
