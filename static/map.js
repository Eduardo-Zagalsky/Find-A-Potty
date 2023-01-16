async function getMapInfo() {
    let response = await axios.get("https://www.arcgis.com/sharing/rest/content/items/cc11a895caa848a886014c75835d2d91/data?f=json");
    let result = response.data.operationalLayers[0]["featureCollection"]["layers"][0]["featureSet"]["features"];
    for (let i = 0; i < result.length; i++) {
        let bathroom = result[i]["attributes"];
        let bathrooms = {
            'name': `${bathroom.building_name} ${bathroom.building_type}`,
            'address': bathroom.address,
            'zip_code': bathroom.zip,
            'latitude': bathroom.latitude,
            'longitude': bathroom.longitude,
            'website': bathroom.site_link
        };
        // Set marker options.
        const marker = new mapboxgl.Marker({
            color: "#a83232",
            draggable: false
        }).setLngLat([bathroom.longitude, bathroom.latitude])
            .addTo(map);
        await axios.post("/initiate", bathrooms)
    };
};

mapboxgl.accessToken = 'pk.eyJ1IjoiZWR1YXJkbzA3OTYiLCJhIjoiY2xjd3BtcW1zMWJsNDQxcDV3OW1ybGkxbyJ9.MGOMpqBI1QdQu27kFXBVww';
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v12', // style URL
    center: [-87.6565, 41.9491], // starting position [lng, lat]
    zoom: 10, // starting zoom
});
getMapInfo()