<template>
  <div>
    <div :ref="refMap" class="map"></div>
  </div>
</template>

<script>
export default {
  name: "BaseMap",

  props: {
    startLat: Number,
    startLng: Number,
    endLat: Number,
    endLng: Number,
    refMap: String,
  },

  data() {
    return {
      map: null,
      directionsService: null,
      directionsRenderer: null,
      routeInfo: "",
    };
  },

  mounted() {
    const script = document.createElement("script");
    const YOUR_API_KEY = "AIzaSyChKvIKcbVQKSRq3u7QJ7AIIHhYgj2wGDI";
    script.src = `https://maps.googleapis.com/maps/api/js?key=${YOUR_API_KEY}&callback=initializeMap`;

    script.defer = true;
    script.async = true;
    script.addEventListener("load", () => {
      this.initializeMap();
    });
    document.head.appendChild(script);
  },

  methods: {
    initializeMap() {
      // Create a new map
      console.log('ref maps');
      console.log(this.$refs);

      this.map = new google.maps.Map(this.$refs[this.refMap], {
        zoom: 8,
        center: { lat: this.startLat, lng: this.startLng },
      });

      // Initialize the directions service and renderer
      this.directionsService = new google.maps.DirectionsService();
      this.directionsRenderer = new google.maps.DirectionsRenderer({
        map: this.map,
      });

      // Define the locations for the start and end points
      const start = new google.maps.LatLng(this.startLat, this.startLng);
      const end = new google.maps.LatLng(this.endLat, this.endLng);

      // Define the request for the directions
      const request = {
        origin: start,
        destination: end,
        travelMode: google.maps.TravelMode.DRIVING,
      };

      // Call the directions service to get the route
      this.directionsService.route(request, (response, status) => {
        if (status == google.maps.DirectionsStatus.OK) {
          // Display the route on the map
          this.directionsRenderer.setDirections(response);

          // Display the distance and duration of the route
          const distance = response.routes[0].legs[0].distance.text;
          const duration = response.routes[0].legs[0].duration.text;
          this.routeInfo = `Distance: ${distance}, Duration: ${duration}`;
        } else {
          alert("Directions request failed due to " + status);
        }
      });
    },
  },
};
</script>

<style>
.map {
  height: 500px;
}
.route-info {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: white;
  padding: 10px;
  border-radius: 4px;
}
</style>