$(document).ready(function () {

    let map = L.map('map').setView([0, 0], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // country geometry
    const countryLayer = L.geoJSON(
        JSON.parse(country_geometry), {
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
                console.log(feature.properties)
                layer.bindPopup('' +
                    '<table>' +
                    `<tr><td>Geography</td><td>: ${feature.properties.geometry_name} (${feature.properties.geometry_identifier})</td></tr>` +
                    `<tr><td>Value</td><td>: ${feature.properties.value}</td></tr>` +
                    `<tr style="background-color: ${feature.properties.background_color}; color: ${feature.properties.text_color}"><td>Scenario</td><td>: ${feature.properties.scenario_value}</td></tr>` +
                    '</table>');
            }
        }
    );
    indicatorLayer.addTo(map);

    // LEVELS
    const $levelSelection = $('#level-selection')
    selectLevel($($levelSelection.find('div')[0]));

    function selectLevel($level) {
        const level = $level.data('level');
        const url = $level.data('url');
        $levelSelection.find('div').removeClass('active');
        $level.addClass('active');

        // get geojson
        indicatorLayer.clearLayers();
        if (!indicatorGeojson[level]) {
            $.ajax({
                url: url,
                dataType: 'json',
                beforeSend: function (xhrObj) {

                },
                success: function (geojson, textStatus, request) {
                    indicatorGeojson[level] = geojson;
                    selectLevel($level);
                },
                error: function (error, textStatus, request) {

                }
            });

        } else {
            indicatorLayer.addData(indicatorGeojson[level]);
        }
    }

    $levelSelection.find('div').click(function () {
        selectLevel($(this));
    })
});