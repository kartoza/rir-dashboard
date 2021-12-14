/**
 * Layers of map controlled in here.
 * Add layers in here.
 */
define([
    'js/views/layers/context-layers',
    'js/views/layers/indicator-layer',
    'js/views/layers/administrative-level',
], function (ContextLayers, IndicatorLayer, AdministrativeLevelLayer) {
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
                dateToYYYYMMDD(new Date()),
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
            event.register(this, evt.INDICATOR_VALUES_CHANGED, this.indicatorValuesChanged);

            const self = this;
            const $wrapper = $('#map-wrapper');
            $('#comparing-toggle').click(function () {
                if ($wrapper.hasClass('top-bottom')) {
                    $wrapper.removeClass('top-bottom');
                    $wrapper.addClass('left-right');
                } else {
                    $wrapper.addClass('top-bottom');
                    $wrapper.removeClass('left-right');
                }
                self.indicatorChanged(true);
            })
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
                    if (self.indicatorLeft && self.indicatorRight) {
                        return false
                    }
                    // check which side is it and assign in
                    let side = '';
                    if (!self.indicatorLeft) {
                        side = evt.INDICATOR_LEFT_PANE;
                        self.indicatorLeft = indicatorLayer;
                    } else if (!self.indicatorRight) {
                        side = evt.INDICATOR_RIGHT_PANE;
                        self.indicatorRight = indicatorLayer;
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
        indicatorChanged: function (force) {
            $('#comparing-toggle').hide();
            let position = null;
            if (this.controlComparison) {
                if (!force) {
                    position = this.controlComparison._getPosition();
                }
                this.controlComparison.remove();
                this.controlComparison = null;
                this.map.getPane(evt.INDICATOR_LEFT_PANE).style.clip = '';
                this.map.getPane(evt.INDICATOR_RIGHT_PANE).style.clip = '';
            }

            $('#info-toggle').show();

            if (this.indicatorRight && this.indicatorLeft) {
                $('#comparing-toggle').show();
                this.controlComparison = L.control.layerSwiper(
                    {
                        id: 'lyrSwiper',
                        title: 'lyrSwiper',
                        position: 'topright',
                        orientation: $('#map-wrapper').hasClass('top-bottom') ? 'h' : 'v',
                        ratio: 0.5,
                        swipeLyrConf: {
                            base: { layer: this.indicatorRight.layer, clip: null },
                            compare: { layer: this.indicatorLeft.layer, clip: null }
                        }
                    }
                ).addTo(this.map);
                if (position) {
                    this.controlComparison._setPosition(position);
                }
            } else if (!this.indicatorRight && !this.indicatorLeft) {
                $('#info-toggle').hide();
                if (!$('#right-side').data('hidden')) {
                    $('#info-toggle').click();
                }
            }
        },
        /**
         * When indicator value changed
         */
        indicatorValuesChanged: function () {
            let dates = []
            if (this.indicatorRight && this.indicatorRight.values) {
                $.each(this.indicatorRight.values, function (idx, value) {
                    const date = new Date(value.date);
                    dates.push(dateToYYYYMMDD(date));
                });
            }
            if (this.indicatorLeft && this.indicatorLeft.values) {
                $.each(this.indicatorLeft.values, function (idx, value) {
                    const date = new Date(value.date);
                    dates.push(dateToYYYYMMDD(date));
                });
            }
            if (dates.length !== 0) {
                $('#time-slider-wrapper').show();
                const $slider = $('#time-slider');
                dates.sort();
                dates = [...new Set(dates), dateToYYYYMMDD(new Date())];
                $slider.show();
                $slider.attr('min', 0);
                $slider.attr('max', (dates.length - 1));
                $slider.val((dates.length - 1));

                $slider.off('input');
                $slider.on('input', e => {
                    const date = dates[e.target.value];
                    $('#time-slider-indicator').text(dateToDDMMYYY(new Date(date)));
                    if (this.indicatorLeft) {
                        this.indicatorLeft.date = date;
                        this.indicatorLeft._addLayer();
                    }
                    if (this.indicatorRight) {
                        this.indicatorRight.date = date;
                        this.indicatorRight._addLayer();
                    }
                });
                $slider.trigger('input');
            } else {
                $('#time-slider-wrapper').hide();
            }
        }
    });
});