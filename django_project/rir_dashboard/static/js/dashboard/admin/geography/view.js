$(document).ready(function () {

    //create map
    let map = L.map('map').setView([0, 0], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Indicator Layer
    const indicatorGeojson = {};
    const indicatorLayer = L.geoJSON(null, {
            style: {
                color: "#ff7800",
                weight: 1,
                fillOpacity: 0
            },
            onEachFeature: function (feature, layer) {
                layer.bindPopup('' +
                    '<table>' +
                    `<tr><td>Name</td><td>: ${feature.properties.name} (${feature.properties.identifier})</td></tr>` +
                    `<tr><td>Alias</td><td>: ${feature.properties.alias}</td></tr>` +
                    '</table>');
            }
        }
    );
    indicatorLayer.addTo(map);

    // LEVELS
    let init = true;
    let identifierSelected = null;
    const $levelSelection = $('#level-selection');
    const date = `${new Date().getUTCFullYear()}-${new Date().getUTCMonth() + 1}-${new Date().getUTCDate()}`;
    selectLevel($($levelSelection.find('div')[0]));

    function selectLevel($level) {
        const level = $level.data('level');
        $levelSelection.find('div').removeClass('active');
        $level.addClass('active');

        // save identifier
        const identifier = `${level}-${date}`;
        identifierSelected = identifier;

        // get geojson
        indicatorLayer.clearLayers();
        if (!indicatorGeojson[identifier]) {
            const urlRequest = url.replace('level', level).replace('date', date)
            $.ajax({
                url: urlRequest,
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
            if (init) {
                map.fitBounds(indicatorLayer.getBounds());
            }
            init = false;
        }
    }

    $levelSelection.find('div').click(function () {
        selectLevel($(this));
    })
});