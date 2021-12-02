function initGeometryLevel(map, onLevelSelected) {
    // GEOMETRY LAYER
    const onEachFeature = function onEachFeature(feature, layer) {
        layer.bindPopup('' +
            '<table>' +
            `<tr><td style="text-align: right"><b>Identifier</b></td><td>${feature.properties.identifier}</td></tr>` +
            `<tr><td style="text-align: right"><b>Name</b></td><td>${feature.properties.name}</td></tr>` +
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

    // check if it is district
    let $defaultSelected = $levelSelection.find('*[data-level="District"]');
    if ($defaultSelected.length === 0) {
        $defaultSelected = $($levelSelection.find('div')[0]);
    }
    selectLevel($defaultSelected);

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
                },
                error: function () {
                    if (identifierSelected === identifier) {
                        selectLevel($level);
                    }
                }
            });
            return false
        } else {
            geometryLayer.addData(geometry[identifier]);
            if (init) {
                map.fitBounds(geometryLayer.getBounds());
            }
            init = false;
        }
        onLevelSelected(level);
    }

    $levelSelection.find('div').click(function () {
        selectLevel($(this));
    })

}