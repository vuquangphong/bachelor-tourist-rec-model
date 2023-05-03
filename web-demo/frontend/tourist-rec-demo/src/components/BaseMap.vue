<template>
  <div class="base-map-contain">
    <GMapMap
      :ref="myMapRef"
      :center="center.position"
      :zoom="13"
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
  </div>

  <div class="distance" v-if="displayDistance">{{ distanceFinal }}</div>
</template>

<script>
/* eslint-disable no-undef */

import { onMounted, ref, getCurrentInstance } from "vue";

export default {
  props: {
    firstMarker: Object,
    secondMarker: Object,
    myMapRef: String,
  },

  created() {
    this.center["position"] = {
      lat: this.firstMarker.location[0],
      lng: this.firstMarker.location[1],
    };
    this.center["title"] = this.firstMarker.name;

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

    if (
      this.firstMarker.location[0] === this.secondMarker.location[0] &&
      this.firstMarker.location[1] === this.secondMarker.location[1]
    ) {
      this.displayDistance = false;
    } else {
      this.displayDistance = true;
    }
  },

  data() {
    return {
      center: {},
      markers: [],
      displayDistance: false,
    };
  },

  setup() {
    const proxy = getCurrentInstance();
    const distanceFinal = ref("");

    onMounted(async () => {
      const curMap = proxy.refs[proxy.props.myMapRef];

      curMap.$mapPromise.then((map) => {
        const directionsService = new google.maps.DirectionsService();
        const directionsRenderer = new google.maps.DirectionsRenderer({
          map: map,
        });

        const request = {
          origin: {
            lat: proxy.props.firstMarker.location[0],
            lng: proxy.props.firstMarker.location[1],
          },
          destination: {
            lat: proxy.props.secondMarker.location[0],
            lng: proxy.props.secondMarker.location[1],
          },
          travelMode: "DRIVING",
        };

        directionsService.route(request, (response, status) => {
          if (status == "OK") {
            directionsRenderer.setDirections(response);

            var route = response.routes[0];
            var distance = 0;

            for (var i = 0; i < route.legs.length; i++) {
              distance += route.legs[i].distance.value;
            }

            // Hiển thị độ dài đường đi
            console.log("Độ dài đường đi: " + distance + "m");

            distanceFinal.value = `Quãng đường di chuyển: ${
              distance / 1000
            } km.`;
          }
        });
      });
    });

    return { proxy, distanceFinal };
  },
};
</script>

<style scoped>
.base-map-contain {
  width: 870px !important;
  height: 400px !important;
}

.base-map-contain .vue-map-container {
  height: 100%;
}

.distance {
  padding: 20px;
  font-weight: 600;
}
</style>
