let lng
let lat
let bathrooms = [];

mapboxgl.accessToken = 'pk.eyJ1IjoiZWR1YXJkbzA3OTYiLCJhIjoiY2xjd3BtcW1zMWJsNDQxcDV3OW1ybGkxbyJ9.MGOMpqBI1QdQu27kFXBVww';
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v12', // style URL
    center: [-87.6565, 41.9491], // starting position [lng, lat]
    zoom: 9, // starting zoom
});

async function getMarkers() {
    let response = await axios.get("https://www.arcgis.com/sharing/rest/content/items/cc11a895caa848a886014c75835d2d91/data?f=json");
    let result = response.data.operationalLayers[0]["featureCollection"]["layers"][0]["featureSet"]["features"];
    for (let i = 0; i < result.length; i++) {
        let bathroom = result[i]["attributes"];
        let currBathroom = {
            'name': bathroom.building_name,
            'address': bathroom.address,
            'zip_code': bathroom.zip,
            'longitude': bathroom.longitude,
            'latitude': bathroom.latitude,
            'website': bathroom.site_link
        };
        bathrooms.push(currBathroom);
    };
};
// async function makeRoute() {
//     const start = [lng, lat];
//     // create a function to make a directions request
//     async function getRoute(end) {
//         // make a directions request using cycling profile
//         // an arbitrary start will always be the same
//         // only the end or destination will change
//         let result = await axios.get(`https://api.mapbox.com/directions/v5/mapbox/cycling/${start[0]},${start[1]};${end[0]},${end[1]}?steps=true&geometries=geojson&access_token=${mapboxgl.accessToken}`);
//         let route = result.data.routes[0]["geometry"]["coordinates"];
//         const geojson = {
//             type: 'Feature',
//             properties: {},
//             geometry: {
//                 type: 'LineString',
//                 coordinates: route
//             }
//         };
//         // if the route already exists on the map, we'll reset it using setData
//         if (map.getSource('route')) {
//             map.getSource('route').setData(geojson);
//         }
//         // otherwise, we'll make a new request
//         else {
//             map.addLayer({
//                 id: 'route',
//                 type: 'line',
//                 source: {
//                     type: 'geojson',
//                     data: geojson
//                 },
//                 layout: {
//                     'line-join': 'round',
//                     'line-cap': 'round'
//                 },
//                 paint: {
//                     'line-color': '#3887be',
//                     'line-width': 5,
//                     'line-opacity': 0.75
//                 }
//             });
//         }
//         // get the sidebar and add the instructions
//         const instructions = document.getElementById('instructions');
//         const steps = data.legs[0].steps;

//         let tripInstructions = '';
//         for (const step of steps) {
//             tripInstructions += `<li>${step.maneuver.instruction}</li>`;
//         }
//         instructions.innerHTML = `<p><strong>Trip duration: ${Math.floor(
//             data.duration / 60
//         )} min 🚗 </strong></p><ol>${tripInstructions}</ol>`;
//     }

//     map.on('load', () => {
//         // make an initial directions request that
//         // starts and ends at the same location
//         getRoute(start);

//         // Add starting point to the map
//         map.addLayer({
//             id: 'point',
//             type: 'circle',
//             source: {
//                 type: 'geojson',
//                 data: {
//                     type: 'FeatureCollection',
//                     features: [
//                         {
//                             type: 'Feature',
//                             properties: {},
//                             geometry: {
//                                 type: 'Point',
//                                 coordinates: start
//                             }
//                         }
//                     ]
//                 }
//             },
//             paint: {
//                 'circle-radius': 10,
//                 'circle-color': '#3887be'
//             }
//         });
//         map.on('click', (event) => {
//             const coords = Object.keys(event.lngLat).map((key) => event.lngLat[key]);
//             const end = {
//                 type: 'FeatureCollection',
//                 features: [
//                     {
//                         type: 'Feature',
//                         properties: {},
//                         geometry: {
//                             type: 'Point',
//                             coordinates: coords
//                         }
//                     }
//                 ]
//             };
//             if (map.getLayer('end')) {
//                 map.getSource('end').setData(end);
//             } else {
//                 map.addLayer({
//                     id: 'end',
//                     type: 'circle',
//                     source: {
//                         type: 'geojson',
//                         data: {
//                             type: 'FeatureCollection',
//                             features: [
//                                 {
//                                     type: 'Feature',
//                                     properties: {},
//                                     geometry: {
//                                         type: 'Point',
//                                         coordinates: coords
//                                     }
//                                 }
//                             ]
//                         }
//                     },
//                     paint: {
//                         'circle-radius': 10,
//                         'circle-color': '#f30'
//                     }
//                 });
//             }
//             getRoute(coords);
//         });
//     });
// };
// map.addControl(
//     new MapboxDirections({
//         accessToken: mapboxgl.accessToken
//     }),
//     'top-left'
// );
let searchButton = document.getElementById("search-button");
searchButton.addEventListener("click", async function (event) {
    event.preventDefault();
    let search = document.getElementById("search").value;
    const options = {
        method: 'GET',
        url: 'https://google-maps-geocoding.p.rapidapi.com/geocode/json',
        params: { address: search, language: 'en' },
        headers: {
            'X-RapidAPI-Key': 'ad9e5957c1msh43164e3dccfa3d0p1ea1f0jsn6c20c5aeb72b',
            'X-RapidAPI-Host': 'google-maps-geocoding.p.rapidapi.com'
        }
    };
    axios.request(options).then(function (response) {
        address = response.data.results[0]["formatted_address"];
        zipCode = response.data.results[0]["address_components"][7]["long_name"];
        lng = response.data.results[0]["geometry"]["location"].lng;
        lat = response.data.results[0]["geometry"]["location"].lat;
        const popup = new mapboxgl.Popup({ offset: 25 }).setText(
            `${address}`
        );
        // Set marker options.
        const marker = new mapboxgl.Marker({
            color: "#4169e1",
            draggable: false
        }).setLngLat([lng, lat])
            .setPopup(popup) // sets a popup on this marker
            .addTo(map);
        getMarkers();

        for (let i = 0; i < bathrooms.length; i++) {
            if (bathrooms[i]['zip_code'] == zipCode) {
                // create the popup
                const popup = new mapboxgl.Popup({ offset: 25 }).setText(
                    `${bathrooms[i]["address"]}`
                );
                // Set marker options.
                const marker = new mapboxgl.Marker({
                    color: "#a83232",
                    draggable: false
                }).setLngLat([bathrooms[i]['longitude'], bathrooms[i]['latitude']])
                    .setPopup(popup) // sets a popup on this marker
                    .addTo(map);

            };
        };
        // // Listen for a click on the map
        // map.on('click', makeRoute);
    }).catch(function (error) {
        console.error(error);
    });
});
