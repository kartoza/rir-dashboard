/**
 * Layers of map controlled in here.
 * Add layers in here.
 */
define([
    'backbone',
    'jquery',
    'js/views/layers/context-layers',
    'js/views/layers/indicator-layer',
    'js/views/layers/administrative-level',
], function (
    Backbone, $, ContextLayers, IndicatorLayer, AdministrativeLevelLayer) {
    return Backbone.View.extend({
        /** Initialization **/
        indicatorLayers: {},
        $lastIndicatorInput: null,

        indicatorLeft: null,
        indicatorRight: null,
        initialize: function (map) {
            this.map = map;
            map.createPane(evt.INDICATOR_LEFT_PANE);
            map.createPane(evt.INDICATOR_RIGHT_PANE);
            map.createPane(evt.CONTEXT_LAYER_PANE);

            this.listener();
            this.contextLayers = new ContextLayers(contextLayers);
            this.contextLayers.render();


            // init administrative
            this.administrativeLevelLayer = new AdministrativeLevelLayer();
            this.administrativeLevelLayer.getLayer(
                'Country',
                `${new Date().getUTCFullYear()}-${new Date().getUTCMonth() + 1}-${new Date().getUTCDate()}`,
                function (layer) {
                    mapView.flyTo(layer.getBounds());
                }
            )

            this.indicatorInit();
        },
        /** Init listener for layers
         */
        listener: function () {
            event.register(this, evt.RERENDER_CONTEXT_LAYER, this.contextLayersChanged);
            event.register(this, evt.INDICATOR_CHANGED, this.indicatorChanged);
        },
        /** When context layer changed
         */
        contextLayersChanged: function () {
            $.each(this.contextLayers.layers, function (index, layer) {
                mapView.removeLayer(layer.layer);
                if (layer.show && layer.layer) {
                    mapView.addLayer(layer.layer);
                }
            })
        },


        // -------------------------------------------------
        // INDICATOR INITITALIZE
        // -------------------------------------------------
        indicatorInit: function () {
            const self = this;
            const $inputs = $('.indicator-checkbox input');
            $inputs.click(function () {
                // click last indicator input
                if (!self.indicatorLayers[$(this).data('id')]) {
                    self.indicatorLayers[$(this).data('id')] = new IndicatorLayer(
                        self.administrativeLevelLayer,
                        $(this).data('id'), $(this).data('name'), $(this).data('url'), JSON.parse($(this).data('levels').replaceAll('\'', '"')), $(this).data('scenario'))
                }
                const indicatorLayer = self.indicatorLayers[$(this).data('id')];
                if (this.checked) {
                    // check which side is it and assign in
                    let side = '';
                    if (!self.indicatorRight) {
                        side = evt.INDICATOR_RIGHT_PANE;
                        self.indicatorRight = indicatorLayer;
                    } else if (!self.indicatorLeft) {
                        side = evt.INDICATOR_LEFT_PANE;
                        self.indicatorLeft = indicatorLayer;
                    } else {
                        return false;
                    }
                    indicatorLayer.show(side);
                } else {
                    // check which side is it and make it null
                    if (indicatorLayer === self.indicatorLeft) {
                        self.indicatorLeft = null;
                    } else if (indicatorLayer === self.indicatorRight) {
                        self.indicatorRight = null;
                    }
                    indicatorLayer.hide();
                }
            });
        },
        /**
         * When indicator layer added/removed
         */
        indicatorChanged: function () {
            let position = null;
            let value = null;
            if (this.controlComparison) {
                position = this.controlComparison.getPosition();
                value = $('.leaflet-sbs-range').val();
                this.controlComparison.remove();
                this.controlComparison = null;
                this.map.getPane(evt.INDICATOR_LEFT_PANE).style.clip = '';
                this.map.getPane(evt.INDICATOR_RIGHT_PANE).style.clip = '';
            }

            $('#info-toggle').show();

            if (this.indicatorRight && this.indicatorLeft) {
                this.controlComparison = L.control.sideBySide(
                    this.indicatorLeft.layer, this.indicatorRight.layer
                ).addTo(this.map);
                if (position && value) {
                    $('.leaflet-sbs-divider').css('left', position + 'px')
                    $('.leaflet-sbs-range').val(value);
                    this.controlComparison._updateLayers();
                } else {
                    const position = this.controlComparison.getPosition();
                }
            } else if (!this.indicatorRight && !this.indicatorLeft) {
                $('#info-toggle').hide();
                if (!$('#right-side').data('hidden')) {
                    $('#info-toggle').click();
                }
            }
        },
    });
});