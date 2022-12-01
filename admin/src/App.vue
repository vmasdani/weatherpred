<script setup lang="ts">
import LoginPage from "./LoginPage.vue";
import { ctx } from "./main";
import MainComponent from "./MainComponent.vue";
</script>
<template>
  <div v-if="ctx.loggedIn">
    <MainComponent />
  </div>
  <div v-else>
    <LoginPage />
  </div>
</template>
