async function getMapInfo() {
    let response = await axios.get("https://www.arcgis.com/sharing/rest/content/items/cc11a895caa848a886014c75835d2d91/data?f=json");
    bathrooms = response.data.operationalLayers.featureCollection.layers[0][featureSet][features][0].map(result => {
        bathroom = result.attributes;
        return {
            name: `${bathroom.building_name} ${bathroom.building_type}`,
            address: bathroom.address,
            zip_code: bathroom.zip,
            latitude: bathroom.latitude,
            longitude: bathroom.longitude,
            website: bathroom.site_link
        };
    });
    return bathrooms;
};