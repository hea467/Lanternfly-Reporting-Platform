// Initialize and add the map
let map;

async function initMap() {
    // The location of Uluru
    const position = { lat: 40.4440365, lng: -79.9442245 };
    // Request needed libraries.
    //@ts-ignore
    const { Map, InfoWindow } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");

    // The map, centered at Uluru
    map = new Map(document.getElementById("map"), {
        zoom: 16,
        center: position,
        mapId: "DEMO_MAP_ID",
    });

    // Create an info window to share between markers.
    const infoWindow = new InfoWindow();



    //Parsing the coordinates that correspond to the marker
    var coordinatesData = JSON.parse(document.getElementById('coordinates_data').innerHTML);

    var mylist = coordinatesData.split('], [')

   
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


    //Parsing the lanternfly reports that correspond to the marker
    var flyData = JSON.parse(document.getElementById('fly_report').innerHTML);
    // console.log(flyData)
    
    var fly_list = flyData.split('], [')
    // console.log(fly_list)


    for (let i = 0; i < fly_list.length; i++){
        if (i == 0) {
            fly_list[i] = fly_list[i].slice(2)
        }
        if (i == fly_list.length - 1){
            fly_list[i] = fly_list[i].slice(0, -2)
        }

        var sep_info = fly_list[i].split(',')
        for (let j = 0; j < sep_info.length; j++){
            sep_info[j] = parseFloat(sep_info[j])
        }

        fly_list[i] = sep_info

    }

    // console.log(fly_list)

    //Parsing the usernames that correspond to the marker
    var username = JSON.parse(document.getElementById('usernamee').innerHTML);
    console.log(username)
    var user_list = username.split(', ')
    console.log(user_list)

    for (let i = 0; i < user_list.length; i++){
        if (i == 0) {
            user_list[i] = user_list[i].slice(1)
            // console.log(user_list[i])
            
        }
        if (i == user_list.length - 1){
            user_list[i] = user_list[i].slice(0, -1)
            // console.log(user_list[i])
        }

        user_list[i] = user_list[i].slice(1, -1)

    }


    for (let i = 0; i < mylist.length; i++){
        const marker = new google.maps.marker.AdvancedMarkerElement({
            position: getLatLng(mylist[i]),
            map: map,
            title: `Reported by: ${user_list[i]}, 
                    Lanternflies seen: ${fly_list[i][0]},
                    Lanternflies killed: ${fly_list[i][1]},
                    Trees killed: ${fly_list[i][2]},`
            
        });

        marker.addListener("click", ({ domEvent, latLng }) => {
            const { target } = domEvent;
      
            infoWindow.close();
            infoWindow.setContent(marker.title);
            infoWindow.open(marker.map, marker);
          });

    }



}

function getLatLng(coord){
    return new google.maps.LatLng(coord[0], coord[1]);
}

initMap();

