<script setup lang="ts">
import Nav from "./Nav.vue";

const baseUrl = process.env.VUE_APP_BASE_URL;
</script>
<template>
  <Nav />
  <div class="container">
    <small> This is the admin page. Backend URL: {{ baseUrl }} </small>
  </div>
  <hr class="border border-dark" />


  <router-view />
</template>
