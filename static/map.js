let lng
let lat
let zip = document.getElementById('zip-code');
let bathrooms = [];

mapboxgl.accessToken = 'pk.eyJ1IjoiZWR1YXJkbzA3OTYiLCJhIjoiY2xjd3BtcW1zMWJsNDQxcDV3OW1ybGkxbyJ9.MGOMpqBI1QdQu27kFXBVww';//make environment variable
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v12', // style URL
    center: [-87.6565, 41.9491], // starting position [lng, lat]
    zoom: 9, // starting zoom
});

async function getMarkers() {
    let response = await axios.get("/bathrooms");
    let result = response.data.bathrooms;
    for (let i = 0; i < result.length; i++) {
        let currBathroom = {
            'name': result[i]["name"],
            'address': result[i]["address"],
            'zip_code': result[i]['zip_code'],
            'longitude': result[i]['longitude'],
            'latitude': result[i]['latitude']
        };
        bathrooms.push(currBathroom);
    };
};

zip.addEventListener("click", async function (event) {
    event.preventDefault();
    const options = {
        method: 'GET',
        url: 'https://google-maps-geocoding.p.rapidapi.com/geocode/json',
        params: { address: zip.value, language: 'en' },
        headers: {
            'X-RapidAPI-Key': 'ad9e5957c1msh43164e3dccfa3d0p1ea1f0jsn6c20c5aeb72b',
            'X-RapidAPI-Host': 'google-maps-geocoding.p.rapidapi.com'
        }
    };
    axios.request(options).then(function (response) {
        address = response.data.results[0]["formatted_address"];
        zipCode = response.data.results[0]["address_components"][0]["long_name"];
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
                const popup = new mapboxgl.Popup({ offset: 25 }).setHTML(
                    `<a href="/bathroom/${i}">${bathrooms[i]["address"]}</a>`
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
    }).catch(function (error) {
        console.error(error);
    });
});