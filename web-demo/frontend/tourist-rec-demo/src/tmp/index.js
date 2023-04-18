// Initialize and add the map
let map, mapTemp;

async function initMap() {
    const position1 = { lat: 21.036584, lng: 105.834904 };
    const position2 = { lat: 21.026297, lng: 105.851560 };
    const position3 = { lat: 21.035636, lng: 105.841324 };

    // Request needed libraries.
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerView } = await google.maps.importLibrary("marker");


    // The map, centered at Uluru
    map = new Map(document.getElementById("map"), {
        zoom: 16,
        center: position1,
        mapId: "DEMO_MAP_ID",
    });

    mapTemp = new Map(document.getElementById('map-temp'), {
        zoom: 16,
        center: position3,
        mapId: "DEMO_MAP_ID_TEMP",
    })

    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer({
        map: map
    });

    const directionsRendererTemp = new google.maps.DirectionsRenderer({
        map: mapTemp
    });

    const marker1 = new AdvancedMarkerView({
        map: map,
        position: position1,
        title: "Lăng Chủ tịch Hồ Chí Minh",
    });

    const marker2 = new AdvancedMarkerView({
        map: map,
        position: position2,
        title: "Hồ Gươm",
    });

    const markerTemp = new AdvancedMarkerView({
        map: mapTemp,
        position: position3,
        title: "Hoàng Thành Thăng Long",
    });

    const request = {
        origin: position1,
        destination: position2,
        travelMode: 'DRIVING'
    };

    // const request = {
    //     origin: position1,
    //     destination: position3,
    //     waypoints: [
    //         {
    //             location: position2,
    //             stopover: true
    //         }
    //     ],
    //     optimizeWaypoints: true,
    //     travelMode: 'WALKING'
    // };

    directionsService.route(request, (response, status) => {
        if (status == 'OK') {
            directionsRenderer.setDirections(response);

            var route = response.routes[0];
            var distance = 0;

            for (var i = 0; i < route.legs.length; i++) {
                distance += route.legs[i].distance.value;
            }

            // Hiển thị độ dài đường đi
            console.log('Độ dài đường đi: ' + distance + 'm');
        }
    });
}

initMap();