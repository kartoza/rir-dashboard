$(document).ready(function () {

    //create map
    let map = L.map('map').setView([0, 0], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // country geometry
    const countryLayer = L.geoJSON(
        countryGeometry, {
            style: {
                color: "#ff7800",
                weight: 1,
                fillOpacity: 0
            }
        });
    countryLayer.addTo(map);
    map.fitBounds(countryLayer.getBounds());

    // Indicator Layer
    const indicatorGeojson = {};
    const indicatorLayer = L.geoJSON(null, {
            style: function (feature) {
                return {
                    color: "#ffffff",
                    weight: 2,
                    fillColor: feature.properties.background_color
                };
            },
            onEachFeature: function (feature, layer) {
                layer.bindPopup('' +
                    '<table>' +
                    `<tr><td><b>Geography</b></td><td>${feature.properties.geometry_name} (${feature.properties.geometry_identifier})</td></tr>` +
                    `<tr><td><b>Value</b></td><td>${feature.properties.value}</td></tr>` +
                    `<tr style="background-color: ${feature.properties.background_color}; color: ${feature.properties.text_color}"><td><b>Scenario</b></td><td>${feature.properties.scenario_value}</td></tr>` +
                    '</table>');
            }
        }
    );
    indicatorLayer.addTo(map);

    // LEVELS
    let identifierSelected = null;
    const $levelSelection = $('#level-selection');
    selectLevel($($levelSelection.find('div')[0]));

    // Function when level selected
    function selectLevel($level) {
        const level = $level.data('level');
        const url = $level.data('url');
        $levelSelection.find('div').removeClass('active');
        $level.addClass('active');

        // save identifier
        const identifier = level;
        identifierSelected = identifier;

        // get geojson
        indicatorLayer.clearLayers();
        if (!indicatorGeojson[identifier]) {
            $.ajax({
                url: url,
                dataType: 'json',
                success: function (geojson, textStatus, request) {
                    indicatorGeojson[identifier] = geojson;
                    if (identifierSelected === identifier) {
                        selectLevel($level);
                    }
                }
            });
        } else {
            indicatorLayer.addData(indicatorGeojson[identifier]);
        }
    }

    $levelSelection.find('div').click(function () {
        selectLevel($(this));
    })
});