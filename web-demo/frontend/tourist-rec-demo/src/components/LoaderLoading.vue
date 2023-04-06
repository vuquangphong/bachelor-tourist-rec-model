<template>
  <div class="loader-container" v-if="isLoading">
    <div class="loader"></div>
  </div>
</template>

<script>
export default {
  props: ["isLoading"],
};
</script>

<style scoped>
.loader-container {
  z-index: 1000;
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(216, 215, 215, 0.4);
  transition: 0.5s;
}
.loader {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: transparent;
  height: 50px;
  width: 50px;
  background: url("https://raw.githubusercontent.com/vuquangphong/misa-web12-vuejs-mf1050-phongvq/master/web12-tcdn-amis/src/assets/loading.svg?token=GHSAT0AAAAAAB6UUBBADWTFDDEXR6WQZIEUZBORQTQ")
    no-repeat center center;
  background-size: 50px;
  -webkit-animation: spin 1.3s linear infinite;
  animation: spin 1.3s linear infinite;
}
@-webkit-keyframes spin {
  0% {
    -webkit-transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
  }
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>