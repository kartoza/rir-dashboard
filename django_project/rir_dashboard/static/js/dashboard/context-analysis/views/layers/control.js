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
        initialize: function (map) {
            this.map = map;
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
                        $(this).data('id'), $(this).data('url'), JSON.parse($(this).data('levels').replaceAll('\'', '"')))
                }
                const indicatorLayer = self.indicatorLayers[$(this).data('id')];
                if (this.checked) {
                    if (self.$lastIndicatorInput && self.$lastIndicatorInput !== $(this) && self.$lastIndicatorInput.prop('checked')) {
                        self.$lastIndicatorInput.click();
                    }
                    self.$lastIndicatorInput = $(this);
                    indicatorLayer.show();
                } else {
                    self.$lastIndicatorInput = null;
                    indicatorLayer.hide();
                }
            });
        }
    });
});