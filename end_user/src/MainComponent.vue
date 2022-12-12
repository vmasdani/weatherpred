<script setup lang="ts">
import Nav from "./Nav.vue";

const baseUrl = process.env.VUE_APP_BASE_URL

</script>
<template>
  <Nav />
  <!-- <h1>
    This is the end user home page. Backend URL:
    {{ baseUrl }}
  </h1> -->

  <router-view />
</template>
