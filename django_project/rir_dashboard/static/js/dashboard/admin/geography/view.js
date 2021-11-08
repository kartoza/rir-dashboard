$(document).ready(function () {

    //create map
    let map = L.map('map').setView([0, 0], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Indicator Layer
    const onEachFeature = function onEachFeature(feature, layer) {
        layer.bindPopup('' +
            '<table>' +
            `<tr><td style="text-align: right"><b>Name</b></td><td>${feature.properties.name} (${feature.properties.identifier})</td></tr>` +
            `<tr><td style="text-align: right"><b>Alias</b></td><td>${feature.properties.alias}</td></tr>` +
            '</table>');
    }
    const geometry = {};
    const geometryLayer = L.geoJSON(null, {
            style: {
                color: "#ff7800",
                weight: 1,
                fillOpacity: 0
            },
            onEachFeature: onEachFeature
        }
    );
    geometryLayer.addTo(map);

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
        geometryLayer.clearLayers();
        if (!geometry[identifier]) {
            const urlRequest = url.replace('level', level).replace('date', date)
            $.ajax({
                url: urlRequest,
                dataType: 'json',
                success: function (geojson, textStatus, request) {
                    geometry[identifier] = geojson;
                    if (identifierSelected === identifier) {
                        selectLevel($level);
                    }
                }
            });
        } else {
            geometryLayer.addData(geometry[identifier]);
            if (init) {
                map.fitBounds(geometryLayer.getBounds());
            }
            init = false;
        }
    }

    $levelSelection.find('div').click(function () {
        selectLevel($(this));
    })
});