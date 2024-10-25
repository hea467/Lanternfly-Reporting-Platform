// Initialize and add the map
let map;

async function initMap() {
    // The location of Uluru
    const position = { lat: 40.4440365, lng: -79.9442245 };
    // Request needed libraries.
    //@ts-ignore
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

    // The map, centered at Uluru
    map = new Map(document.getElementById("map"), {
        zoom: 16,
        center: position,
        mapId: "DEMO_MAP_ID",
    });

    // The marker, positioned at CMU
    const marker = new AdvancedMarkerElement({
        map: map,
        position: position,
        title: "CMU",
    });

    // Create the initial InfoWindow.
    let infoWindow = new google.maps.InfoWindow({
        content: "Click the map!",
        position: position,
    });

    infoWindow.open(map);
    // Configure the click listener.
    map.addListener("click", (mapsMouseEvent) => {
        // Close the current InfoWindow.
        infoWindow.close();
        // Create a new InfoWindow.
        infoWindow = new google.maps.InfoWindow({
            position: mapsMouseEvent.latLng,
        });
        // Logging to console for debugging purposes
        console.log(JSON.stringify(mapsMouseEvent.latLng.toJSON(), null, 2));
        var json = JSON.parse(JSON.stringify(mapsMouseEvent.latLng.toJSON()));
        document.getElementById("latlong_output_demo").innerHTML = "latitude: " + json["lat"] + " longtitude: " + json["lng"]
        fill_long_lat(json["lat"], json["lng"]);
        infoWindow.setContent(
            "saw lanternflys here?",
        );
        infoWindow.open(map);
    });


}

function fill_long_lat(la, lo) {
    var latitude_div = document.getElementById("id_latitude")
    latitude_div.value = la
    var longitude_div = document.getElementById("id_longtitude")
    longitude_div.value = lo
    console.log(la)
}

initMap();
