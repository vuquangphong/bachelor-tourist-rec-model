<template>
  <router-view />
</template>

<script>
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
