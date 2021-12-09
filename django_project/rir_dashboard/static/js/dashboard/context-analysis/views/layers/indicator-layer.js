/**
 * Layers of map controlled in here.
 * Add layers in here.
 */
define([
    'backbone',
    'jquery'
], function (
    Backbone, $) {
    return Backbone.View.extend({
        /** Initialization
         */
        initialize: function (administrativeLevelLayer, id, name, url, levels, scenario) {
            this.name = name;
            this.administrativeLevelLayer = administrativeLevelLayer;
            this.$el = $(`#indicator-` + id);
            this.$input = this.$el.find('input');
            this.$legend = this.$el.find('.legend');
            this.levels = levels;
            this.date = `${new Date().getUTCFullYear()}-${new Date().getUTCMonth() + 1}-${new Date().getUTCDate()}`;
            this.level = this.levels[0];
            this.url = url;
            this.id = id;
            this.layers = {};
            this.layer = null;
            this.scenario = scenario;


            // for the legend
            const self = this;
            this.$legend.find('.legend-row').click(function () {
                $(this).toggleClass('active');
                self.setStyle();
            })
        },
        /**
         * Get layer with identifier
         * @returns {string}
         */
        getLayer: function (callback) {
            const self = this;
            const id = this.id;
            const level = this.level;
            const date = this.date;
            const identifier = `${level}-${date}`;
            if (!self.layers[id]) {
                self.layers[id] = {}
            }

            const layer = self.layers[id][identifier];
            if (!layer) {
                Request.get(
                    self.url.replace('level', level).replace('date', date), {}, {},
                    function (data) {
                        // process data
                        // we need to make sure all layer are turned off
                        const cleanGeojson = {
                            type: "FeatureCollection",
                            features: []
                        }
                        self.administrativeLevelLayer.getLayer(level, date, function (geometryLayer) {
                            if (geometryLayer) {
                                const geometryData = JSON.parse(JSON.stringify(geometryLayer.toGeoJSON()));
                                $.each(geometryData.features, function (idx, feature) {
                                    $.each(data, function (idx, rowData) {
                                        if (feature.id === rowData.geometry_id) {
                                            feature['properties'] = rowData;
                                            cleanGeojson['features'].push(feature)
                                            return false;
                                        }
                                    })
                                });
                                self.layers[id][identifier] = cleanGeojson;
                                self.getLayer(callback);
                            } else {
                                callback(null);
                            }
                        });
                    }, function () {
                        callback(null);
                    })
            } else {
                callback(L.geoJSON(
                    layer, {
                        pane: self.side,
                        paneID: self.side,
                        name: self.name,
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
                ))
            }
        },

        /**
         * Show this indicator
         */
        show: function (side) {
            this.side = side;
            this.initLevelSelection();
            this._addLayer();
        },
        /**
         * Add specific layer to map
         */
        _addLayer: function () {
            const self = this;
            this._removeLayer();
            $('.indicator-checkbox input').prop('disabled', true);
            this.getLayer(function (layer) {
                self.layer = layer;
                $('.indicator-checkbox input').prop('disabled', false);
                self.setStyle();
                self.$legend.show();
                self.layer.options['pane'] = map.getPane(self.side);
                mapView.addLayer(self.layer);
                event.trigger(evt.INDICATOR_CHANGED);
            });
        },
        /**
         * hide this indicator
         */
        hide: function () {
            const $levelSelection = $(`#${this.side}-level-selection`);
            $levelSelection.html('');
            this.level = this.levels[0];
            this.$legend.hide();
            this._removeLayer();
        },
        /**
         * Remove specific layer from map
         */
        _removeLayer: function () {
            mapView.removeLayer(this.layer);
            event.trigger(evt.INDICATOR_CHANGED);
        },

        /**
         * Remove specific layer from map
         */
        initLevelSelection: function () {
            const self = this;
            const $levelSelection = $(`#${this.side}-level-selection`);
            $levelSelection.html('');
            $.each(this.levels, function (key, level) {
                let active = ''
                if (level === self.level) {
                    active = 'active'
                }
                $levelSelection.prepend(`<div id="level-${level}" data-level="${level}" class="${active}">${level}</div>`);
            });
            $levelSelection.find('div').click(function () {
                self.level = $(this).data('level');
                $levelSelection.find('div').removeClass('active')
                $(this).addClass('active');
                self._addLayer();
            })

            if (this.side === evt.INDICATOR_LEFT_PANE) {
                const width = $levelSelection.width()
                $levelSelection.css('right', '-' + (width + 10) + 'px')
            }
        },

        /**
         * Set Style
         */
        setStyle: function () {
            if (this.layer) {
                const levelActivated = [];
                this.$el.find('.legend-row.active').each(function () {
                    levelActivated.push($(this).data('level'));
                });
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
                this.layer.setStyle(style)
            }
        },
    })
});