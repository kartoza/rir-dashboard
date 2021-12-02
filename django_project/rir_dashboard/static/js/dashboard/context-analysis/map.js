$(document).ready(function () {
    let map = L.map('map', { zoomControl: false });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        noWrap: true,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // -------------------------------------------------
    // THIS IS FOR LAYER ROW
    // -------------------------------------------------
    const $layerList = $('#layer-list .side-panel-content');
    contextLayers.forEach(
        (layer, idx) => {
            const checked = layer.enable_by_default ? 'checked' : '';
            $layerList.append(
                `<div id="context-layer-${idx}" class="layer-row">
                    <div class="context-layer-title">
                        <input type="checkbox" data-index="${idx}" ${checked} disabled>
                        ${layer.name}
                        <i class="fa fa-list-ul pull-right" aria-hidden="true"></i>
                    </div>
                    <div class="legend"></div>
                </div>`
            );
            initLayer(layer, idx)
        }
    );

    $('.layer-row input').click(function () {
        const layer = contextLayers[$(this).data('index')].layer;
        if (this.checked) {
            layer.addTo(map);
        } else {
            layer.removeFrom(map);
        }
    })

    $('.fa-list-ul').click(function () {
        $(this).closest('.layer-row, .row').find('.legend').toggle();
    })

    function addLayer(layerData, idx, layer) {
        if (layer) {
            const $element = $(`#context-layer-${idx}`);
            layerData['layer'] = layer;
            $element.find('input').removeAttr('disabled');
            if (layerData.enable_by_default) {
                layer.addTo(map);
            }
        }
    }

    function initLayer(layerData, idx) {
        const name = layerData.name;
        const url = layerData.url;
        const params = {}
        $.each(layerData.parameters, function (index, value) {
            params[index] = value
            if (!Number.isInteger(value)) {
                params[index] = decodeURIComponent(value);
            }
        });
        const options = {
            token: layerData.token
        };
        const layerType = layerData.layer_type;
        const $element = $(`#context-layer-${idx}`);
        const $legend = $element.find('.legend');
        switch (layerType) {
            case 'ARCGIS':
                const argisLayer = (new EsriLeafletLayer(
                    name, url, params, options
                ))
                argisLayer.load().then(layer => {
                    addLayer(layerData, idx, layer);
                    $legend.html(argisLayer.getLegend())
                });
                break;
            case 'Raster Tile':
                const layer = L.tileLayer.wms(url, params);
                addLayer(layerData, idx, layer);

                if (layerData.url_legend) {
                    $legend.html(`<img src="${layerData.url_legend}">`)
                }
                break;
        }
    }

    // -------------------------------------------------
    // THIS IS FOR INDICATOR
    // -------------------------------------------------
    const $inputs = $('#indicator table input');
    const indicatorsLayer = {}

    $inputs.click(function () {
        inputIndicatorClicked(this, currentLevel);
    })

    let currentLevel = null;

    function inputIndicatorClicked(input, level) {
        $(input).attr('disabled', 'disabled');
        const url = $(input).data('url').replaceAll('level', currentLevel);
        const id = $(input).data('id');
        let layer = null;
        if (!indicatorsLayer[id]) {
            indicatorsLayer[id] = {}
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
                                style: function (feature) {
                                    return {
                                        color: "#ffffff",
                                        weight: 1,
                                        fillColor: feature.properties.background_color,
                                        fillOpacity: 0.7
                                    };
                                },
                                onEachFeature: function (feature, layer) {
                                    let defaultHtml =
                                        `<tr style="background-color: ${feature.properties.background_color}; color: ${feature.properties.text_color}"><td><b>Scenario</b></td><td>${feature.properties.scenario_text}</td></tr>`

                                    // check others properties
                                    $.each(feature.properties, function (key, value) {
                                        if (!['background_color', 'text_color', 'scenario_text', 'scenario_value', 'geometry_id'].includes(key)) {
                                            defaultHtml += `<tr><td><b>${key.capitalize()}</b></td><td>${value}</td></tr>`
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
        if (input.checked) {
            if (level === currentLevel) {
                // we need to make sure all layer are turned off
                $.each(indicatorsLayer[id], function (idx, layer) {
                    try {
                        layer.removeFrom(map);
                    } catch (e) {

                    }
                });
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

    // For the level management
    initGeometryLevel(map, function onLevelChanged(level) {
        currentLevel = level;
        $('#indicator input:checkbox:checked').each(function (index) {
            inputIndicatorClicked(this, level);
        });
    });
});