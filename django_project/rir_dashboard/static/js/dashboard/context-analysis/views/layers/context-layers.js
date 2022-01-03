/**
 * Layers of map controlled in here.
 * Add layers in here.
 */
define([], function () {
    return Backbone.View.extend({
        /** Initialization
         */
        layers: {},
        initialize: function (data) {
            this.data = data;
            this.listener();
        },
        /** Init listener for layers
         */
        listener: function () {
        },
        /** Render the views
         */
        render: function () {
            const self = this;
            // ----------------------------------------
            // Init Layers
            // ----------------------------------------
            const $layerList = $('#layer-list .side-panel-content');
            this.data.forEach(
                (layer, idx) => {
                    let $appendElement = $layerList;
                    if (layer.group_name) {
                        let $group = $layerList.find(`div[data-group="${layer.group_name}"]`);
                        if ($group.length === 0) {
                            $layerList.append(templates.CONTEXT_LAYER_GROUP(layer))
                        }
                        $appendElement = $layerList.find(`div[data-group="${layer.group_name}"] .layer-list-group`);

                    }
                    $appendElement.append(templates.CONTEXT_LAYER(layer));
                    self.layers[layer.id] = layer;
                    self.initLayer(layer);
                }
            );
            // ----------------------------------------
            // Initiate toggle group event
            // ----------------------------------------
            $('#layer-list .group-name .group-toggle').click(function () {
                const $row = $(this).closest('.group');
                const $i = $(this);
                $i.toggleClass('fa-caret-down').toggleClass('fa-caret-up').toggleClass('hidden');
                if (!$i.hasClass('fa-caret-down')) {
                    $row.find('.layer-list-group').show()
                } else {
                    $row.find('.layer-list-group').hide()
                }
            });
            // ----------------------------------------
            // Initiate toggle legend
            // ----------------------------------------
            $('#layer-list .legend-toggle').click(function () {
                const $row = $(this).closest('.layer-row');
                const $i = $(this);
                $i.toggleClass('fa-caret-down').toggleClass('fa-caret-up').toggleClass('hidden');
                if (!$i.hasClass('fa-caret-down')) {
                    $row.find('.legend').show()
                } else {
                    $row.find('.legend').hide()
                }
            });

            // ----------------------------------------
            // Initiate group checkbox event
            // ----------------------------------------
            $('.group-checkbox').click(function () {
                const checked = this.checked;
                $(this).closest('.group').find('.layer-row input').each(function (index) {
                    if (!checked && $(this).prop("checked")) {
                        $(this).click()
                    } else if (checked && !$(this).prop("checked")) {
                        $(this).click()
                    }
                });
            });

            // ----------------------------------------
            // Initiate layer checkbox event
            // ----------------------------------------
            $('.layer-row input').click(function () {
                self.checkboxLayerClicked(this)
            })
        },
        checkboxLayerClicked: function (element) {
            const layer = this.layers[$(element).data('id')];
            const $element = $(`#context-layer-${layer.id}`);
            const $legend = $element.find('.legend');
            const $toggleButton = $element.find('.legend-toggle');
            layer.show = element.checked;
            if (element.checked) {
                $toggleButton.show();
                $toggleButton.addClass('fa-caret-down');
                $toggleButton.removeClass('fa-caret-up');
            } else {
                $legend.hide();
                $toggleButton.hide();
            }
            event.trigger(evt.RERENDER_CONTEXT_LAYER);
        },

        /**
         * Initiate layer from the data
         */
        initLayer: function (layerData) {
            const self = this;
            const name = layerData.name;
            const url = layerData.url;
            const params = {};
            $.each(layerData.parameters, function (index, value) {
                params[index] = value;
                if (!Number.isInteger(value)) params[index] = decodeURIComponent(value);
            });
            const options = {
                token: layerData.token
            };
            const style = layerData.style;
            const layerType = layerData.layer_type;
            switch (layerType) {
                case 'ARCGIS':
                    const argisLayer = (new EsriLeafletLayer(
                        name, url, params, options, style
                    ));
                    argisLayer.load().then(layer => {
                        self.addLayerToData(layerData, layer, argisLayer.getLegend());
                    });
                    break;
                case 'Raster Tile':
                    const layer = L.tileLayer.wms(url, params);
                    let legend = '';
                    if (layerData.url_legend) {
                        legend = `<img src="${layerData.url_legend}">`
                    }
                    self.addLayerToData(layerData, layer, legend);
                    break;
            }
        },

        /**
         * Add layer
         * @param layerData - The data of layer
         * @param layer - The leaflet layer
         * @param legend - The legend for the layer
         */
        addLayerToData: function (layerData, layer, legend) {
            if (layer) {
                layer.options.pane = evt.CONTEXT_LAYER_PANE;
                const $element = $(`#context-layer-${layerData.id}`);
                const $legend = $element.find('.legend');
                const $input = $element.find('input');
                layerData['layer'] = layer;
                layerData['show'] = layerData.enable_by_default;
                $legend.html(legend);
                $input.removeAttr('disabled');
                if (layerData.enable_by_default) {
                    $input.click();
                    this.checkboxLayerClicked($input[0]);
                }
            }
        }
    })
});