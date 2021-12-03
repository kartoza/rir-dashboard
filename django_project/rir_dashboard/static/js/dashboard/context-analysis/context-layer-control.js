$(document).ready(function () {
// -------------------------------------------------
// THIS IS FOR LAYER ROW
// -------------------------------------------------
    const initContextLayer = function () {
        const $layerList = $('#layer-list .side-panel-content');
        contextLayers.forEach(
            (layer, idx) => {
                let $appendElement = $layerList;
                if (layer.group_name) {
                    let $group = $layerList.find(`div[data-group="${layer.group_name}"]`);
                    if ($group.length === 0) {
                        $layerList.append(`
                      <div data-group="${layer.group_name}" class="group">
                        <div class="group-name row">
                            <div class="col"><input class="group-checkbox" type="checkbox" data-index="${idx}"> ${layer.group_name}</div>
                            <div><i class="group-toggle fa fa-caret-down" aria-hidden="true"></i></div>
                        </div>
                        <div class="layer-list-group">
                        
                        </div>
                      </div>`)
                    }
                    $appendElement = $layerList.find(`div[data-group="${layer.group_name}"] .layer-list-group`);

                }

                const checked = layer.enable_by_default ? 'checked' : '';
                $appendElement.append(
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

        // initiate caret to be click for group
        $('#layer-list .group-name .group-toggle').click(function () {
            const $row = $(this).closest('.group');
            const $i = $(this);
            $i.toggleClass('fa-caret-down');
            $i.toggleClass('fa-caret-up');
            $(this).toggleClass('hidden');
            if (!$i.hasClass('fa-caret-down')) {
                $row.find('.layer-list-group').show();
            } else {
                $row.find('.layer-list-group').hide();
            }
        })
        // When the group checkbox clicked
        $('.group-checkbox').click(function () {
            const $row = $(this).closest('.group');
            const checked = this.checked;
            $row.find('.layer-row input').each(function (index) {
                if (!checked) {
                    if ($(this).prop("checked")) {
                        $(this).click()
                    }
                } else {
                    if (!$(this).prop("checked")) {
                        $(this).click()
                    }

                }
            });
        })

        // When the checkbox clicked
        $('.layer-row input').click(function () {
            const layer = contextLayers[$(this).data('index')].layer;
            if (this.checked) {
                layer.addTo(map);
            } else {
                layer.removeFrom(map);
            }
        })

        // Event to show/hide legend
        $('.fa-list-ul').click(function () {
            $(this).closest('.layer-row, .row').find('.legend').toggle();
        })
    }
    initContextLayer();

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

    /** Initiate layer from the data
     */
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
})