<template>
  <router-view />
</template>

<script>
/* eslint-disable no-undef */
export default {
  mounted() {
    if (this.$route.path === "/") {
      this.$router.push("/attractions");
    }
  },
};
</script>

<style>
@import url("./styles/main.css");
</style>
