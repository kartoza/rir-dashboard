$(document).ready(function () {
    // -------------------------------------------------
    // THIS IS FOR INDICATOR
    // -------------------------------------------------
    const $inputs = $('.indicator-checkbox input');
    const indicatorsLayer = {}

    $inputs.click(function () {
        inputIndicatorClicked(this, currentLevelIdentifier);
    });

    let currentLevelIdentifier = null;

    function inputIndicatorClicked(input, level) {
        const $row = $(input).closest('.indicator-row');
        if (!geojsonLevel[level]) {
            return
        }
        const geojson = JSON.parse(JSON.stringify(geojsonLevel[level]));
        $(input).attr('disabled', 'disabled');
        const levelName = level.split('-')[0]
        const url = $(input).data('url').replaceAll('level', levelName);
        const id = $(input).data('id');
        let layer = null;
        if (!indicatorsLayer[id]) {
            indicatorsLayer[id] = {}
        }

        const levelActivated = []
        $row.find('.legend-row.active').each(function () {
            levelActivated.push($(this).data('level'));
        })

        const style = function (feature) {
            if (levelActivated.includes(feature.properties.scenario_value)) {
                return {
                    color: "#ffffff",
                    weight: 1,
                    fillColor: feature.properties.background_color,
                    fillOpacity: 0.7
                };
            } else {
                return {
                    opacity: 0,
                    fillOpacity: 0
                };
            }
        }

        // we get the saved layer
        // if not there we request to API
        if (indicatorsLayer[id][level]) {
            layer = indicatorsLayer[id][level];
        } else {
            if (url) {
                $.ajax({
                    url: url,
                    dataType: 'json',
                    success: function (data, textStatus, request) {
                        // process data
                        // we need to make sure all layer are turned off
                        const cleanGeojson = {
                            type: "FeatureCollection",
                            features: []
                        }
                        $.each(geojson.features, function (idx, feature) {
                            $.each(data, function (idx, rowData) {
                                if (feature.id === rowData.geometry_id) {
                                    feature['properties'] = rowData;
                                    cleanGeojson['features'].push(feature)
                                    return false;
                                }
                            })
                        });
                        indicatorsLayer[id][level] = L.geoJSON(
                            cleanGeojson, {
                                onEachFeature: function (feature, layer) {
                                    if (feature.properties.background_color) {
                                        let defaultHtml =
                                            `<tr style="background-color: ${feature.properties.background_color}; color: ${feature.properties.text_color}"><td><b>Scenario</b></td><td>${feature.properties.scenario_text}</td></tr>`

                                        // check others properties
                                        $.each(feature.properties, function (key, value) {
                                            if (!['background_color', 'text_color', 'scenario_text', 'scenario_value', 'geometry_id'].includes(key)) {
                                                defaultHtml += `<tr><td><b>${key.capitalize()}</b></td><td>${numberWithCommas(value)}</td></tr>`
                                            }
                                        });
                                        layer.bindPopup('' +
                                            '<table>' + defaultHtml + '</table>');
                                    }
                                }
                            }
                        );
                        inputIndicatorClicked(input, level)
                    }
                });
            }
            return false;
        }

        // by checking input state, we show/hide the layer
        $(input).removeAttr('disabled');
        if (input.checked) {
            if (level === currentLevelIdentifier) {
                // we need to make sure all layer are turned off
                $.each(indicatorsLayer[id], function (idx, layer) {
                    try {
                        layer.removeFrom(map);
                    } catch (e) {

                    }
                });
                layer.setStyle(style)
                layer.addTo(map);
            }
        } else {
            // we need to make sure all layer are turned off
            $.each(indicatorsLayer[id], function (idx, layer) {
                try {
                    layer.removeFrom(map);
                } catch (e) {

                }
            });
        }
    }

    // for the legend
    $('.legend-row').click(function () {
        $(this).toggleClass('active');
        inputIndicatorClicked(
            $('#indicator-checkbox-' + $(this).data('id'))[0],
            currentLevelIdentifier
        );
    })

    // For the level management
    initGeometryLevel(map, function onLevelChanged(level) {
        currentLevelIdentifier = level;
        $('#indicator input:checkbox:checked').each(function (index) {
            inputIndicatorClicked(this, level);
        });
    });
})