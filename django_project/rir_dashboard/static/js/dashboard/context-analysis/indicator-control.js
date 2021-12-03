$(document).ready(function () {
    // -------------------------------------------------
    // THIS IS FOR INDICATOR
    // -------------------------------------------------
    const $inputs = $('.indicator-checkbox input');
    const indicatorsLayer = {}

    $inputs.click(function () {
        inputIndicatorClicked(this, currentLevel);
    });

    let currentLevel = null;

    function inputIndicatorClicked(input, level) {
        const $row = $(input).closest('.indicator-row');
        $(input).attr('disabled', 'disabled');
        const url = $(input).data('url').replaceAll('level', currentLevel);
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
                    success: function (geojson, textStatus, request) {
                        indicatorsLayer[id][level] = L.geoJSON(
                            geojson, {
                                onEachFeature: function (feature, layer) {
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
                        );
                        inputIndicatorClicked(input, level)
                    }
                });
            }
            return false;
        }

        // by checking input state, we show/hide the layer
        $(input).removeAttr('disabled');
        console.log(layer)
        if (input.checked) {
            if (level === currentLevel) {
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
            currentLevel
        );
    })

    // For the level management
    initGeometryLevel(map, function onLevelChanged(level) {
        currentLevel = level;
        $('#indicator input:checkbox:checked').each(function (index) {
            inputIndicatorClicked(this, level);
        });
    });
})