$(document).ready(function () {
    let map = L.map('map', { zoomControl: false });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        noWrap: true,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map)

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

    $('.layer-row .fa-list-ul').click(function () {
        $(this).closest('.layer-row').find('.legend').toggle();
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
        inputIndicatorClicked(this);
    })

    function inputIndicatorClicked(input) {
        $(input).attr('disabled', 'disabled');
        const url = $(input).data('url');
        const id = $(input).data('id');
        let layer = null;
        if (indicatorsLayer[id]) {
            layer = indicatorsLayer[id];
        } else {
            if (url) {
                $.ajax({
                    url: url,
                    dataType: 'json',
                    success: function (geojson, textStatus, request) {
                        indicatorsLayer[id] = L.geoJSON(
                            geojson, {
                                style: function (feature) {
                                    return {
                                        color: "#ffffff",
                                        weight: 2,
                                        fillColor: feature.properties.background_color,
                                        fillOpacity: 0.7
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
                        )
                        inputIndicatorClicked(input)
                    }
                });
            }
            return false;
        }
        $(input).removeAttr('disabled');
        if (input.checked) {
            layer.addTo(map);
        } else {
            layer.removeFrom(map);
        }

    }
});