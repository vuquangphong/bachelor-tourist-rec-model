<template>
  <GMapMap
    :center="center.position"
    :zoom="16"
    map-type-id="terrain"
    style="width: 100%; height: 100%"
    :title="center.title"
  >
    <GMapMarker
      :key="index"
      v-for="(m, index) in markers"
      :position="m.position"
      :clickable="true"
      :draggable="true"
      @click="center = m.position"
      :title="m.title"
    />
  </GMapMap>
</template>

<script>
export default {
  props: {
    firstMarker: Object,
    secondMarker: Object,
  },

  created() {
    this.center["position"] = {
      lat: this.firstMarker.location[0],
      lng: this.firstMarker.location[1],
    };
    this.center["title"] = this.firstMarker.name;

    // if (this.firstMarker) {
    //   if (typeof this.firstMarker.location === "string") {
    //     let tempLocation = this.firstMarker.location.split(", ");
    //     console.log({
    //       position: {
    //         lat: parseFloat(tempLocation[0]),
    //         lng: parseFloat(tempLocation[1]),
    //       },
    //       title: this.firstMarker.name,
    //     });
    //     this.markers.push({
    //       position: {
    //         lat: parseFloat(tempLocation[0]),
    //         lng: parseFloat(tempLocation[1]),
    //       },
    //       title: this.firstMarker.name,
    //     });
    //   } else {
    //     this.markers.push({
    //       position: {
    //         lat: this.firstMarker.location[0],
    //         lng: this.firstMarker.location[1],
    //       },
    //       title: this.firstMarker.name,
    //     });
    //   }
    // }

    // if (this.secondMarker) {
    //   if (typeof this.secondMarker.location === "string") {
    //     let tempLocation = this.secondMarker.location.split(", ");
    //     console.log({
    //       position: {
    //         lat: parseFloat(tempLocation[0]),
    //         lng: parseFloat(tempLocation[1]),
    //       },
    //       title: this.secondMarker.name,
    //     });
    //     this.markers.push({
    //       position: {
    //         lat: parseFloat(tempLocation[0]),
    //         lng: parseFloat(tempLocation[1]),
    //       },
    //       title: this.secondMarker.name,
    //     });
    //   } else {
    //     this.markers.push({
    //       position: {
    //         lat: this.secondMarker.location[0],
    //         lng: this.secondMarker.location[1],
    //       },
    //       title: this.secondMarker.name,
    //     });
    //   }
    // }

    this.markers.push({
      position: {
        lat: this.firstMarker.location[0],
        lng: this.firstMarker.location[1],
      },
      title: this.firstMarker.name,
    });

    this.markers.push({
      position: {
        lat: this.secondMarker.location[0],
        lng: this.secondMarker.location[1],
      },
      title: this.secondMarker.name,
    });
  },

  data() {
    return {
      center: {},
      markers: [],
    };
  },
};
</script>

<style>
</style>
