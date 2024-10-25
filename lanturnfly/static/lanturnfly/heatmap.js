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

    // Create the initial InfoWindow.
    // let infoWindow = new google.maps.InfoWindow({
    //     // content: "Click the map!",
    //     position: position,
    // });

    // infoWindow.open(map);

    var coordinatesData = JSON.parse(document.getElementById('coordinates_data').innerHTML);

    var mylist = coordinatesData.split('], [')

    //This is very inefficient, but idk how else to do it. Mainyl because JSON.parse would give me a string and when I trying to
    //index into the nested list, it'll only give me one letter. So I came up with this crazy parsing shit 
    for (let i = 0; i < mylist.length; i++){
        if (i == 0) {
            mylist[i] = mylist[i].slice(2)

        }
        if (i == mylist.length - 1){
            mylist[i] = mylist[i].slice(1, -2)
        }
        else{
            mylist[i] = mylist[i].slice(1)
        }

        var tempList = mylist[i].split('", "')
        for (let j = 0; j < tempList.length; j++){
            tempList[j] = parseFloat(tempList[j])
        }

        mylist[i] = tempList
        
    }

    var flyData = JSON.parse(document.getElementById('fly_report').innerHTML);
    var fly_list = flyData.split(', ')
    // console.log(fly_list)

    for (let i = 0; i < fly_list.length; i++){
        if (i == 0) {
            fly_list[i] = fly_list[i].slice(1)
        }
        if (i == fly_list.length - 1){
            fly_list[i] = fly_list[i].slice(0, -1)
        }
        console.log(fly_list[i])
    }



    var heatmapData = []

    for (let i = 0; i < mylist.length; i++){
        for (let j = 0; j < fly_list[i]; j++){
            heatmapData.push(getLatLng(mylist[i]))
        }
    }

    console.log(heatmapData.length)

    // for (let i = 0; i < mylist.length; i++){
    //     heatmapData.push(getLatLng(mylist[i]))
    // }
    
    
    // console.log(heatmapData)

    var heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatmapData,
        map: map,
      });
    heatmap.setMap(map);



}

function getLatLng(coord){
    // console.log(coord)
    // console.log(coord[0])
    // console.log(coord[1])
    return new google.maps.LatLng(coord[0], coord[1]);
}

initMap();

