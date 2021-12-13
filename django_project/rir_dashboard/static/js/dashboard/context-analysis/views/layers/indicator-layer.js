/**
 * Layers of map controlled in here.
 * Add layers in here.
 */
define([], function () {
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
            const level = this.level;
            const date = this.date;
            const identifier = `${level}-${date}`;
            const layer = self.layers[identifier];
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
                                self.layers[identifier] = cleanGeojson;
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
                                    `<tr style="background-color: ${feature.properties.background_color}; color: ${feature.properties.text_color}"><td>${feature.properties.scenario_text}</td><td valign="top"><b>Scenario</b></td valign="top"></tr>`

                                // check others properties
                                $.each(feature.properties, function (key, value) {
                                    if (!['background_color', 'text_color', 'scenario_text', 'scenario_value', 'geometry_id'].includes(key)) {
                                        defaultHtml += `<tr><td valign="top">${numberWithCommas(value)}</td><td valign="top"><b>${key.capitalize()}</b></td></tr>`
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
            $(`.${this.side}-text`).html(`<div class="scenario-${this.scenario}">${this.name}</div>`);
            $(`.${this.side}-info`).show();
            $(`.${this.side}-info`).html(templates.INDICATOR_INFO({
                name: this.name,
                classname: `scenario-${this.scenario}`,
                side: this.side
            }));

            this.renderValues();
            event.trigger(evt.INDICATOR_VALUES_CHANGED);
        },
        /**
         * Add specific layer to map
         */
        _addLayer: function () {
            const self = this;
            this._removeLayer();
            $('.indicator-checkbox input').prop('disabled', true);
            $(`.${this.side}-info .value-table`).html('<div style="margin-left: 10px; margin-bottom: 30px"><i>Loading</i></div>');
            this.getLayer(function (layer) {
                $(`.${self.side}-info .value-table`).html('<table></table>');


                self._removeLayer();
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
            const $levelSelection = $(`.${this.side}-level-selection`);
            $levelSelection.html('');
            this.level = this.levels[0];
            this.$legend.hide();
            this._removeLayer();
            $(`.${this.side}-text`).html(``);
            $(`.${this.side}-info`).hide();
            event.trigger(evt.INDICATOR_VALUES_CHANGED);
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
            const $levelSelection = $(`.${this.side}-level-selection`);
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
                $levelSelection.find(`div[data-level="${self.level}"]`).addClass('active');
                self._addLayer();
            })
        },

        /**
         * Set Style
         */
        setStyle: function () {
            const self = this;
            if (this.layer) {
                const levelActivated = [];
                this.$el.find('.legend-row.active').each(function () {
                    levelActivated.push($(this).data('level'));
                });
                const style = function (feature) {
                    if (levelActivated.includes(feature.properties.scenario_value)) {
                        $(`.${self.side}-info .value-table table`).append(
                            `<tr style="background-color: ${feature.properties.background_color}"><td valign="top">${feature.properties.geometry_name}</td><td valign="top">${feature.properties.scenario_text}</td></tr>
                        `);
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

        /**
         * Render all value of layer
         */
        renderValues: function () {
            const self = this;
            $(`.${this.side}-info .value-chart`).html('<i>Loading</i>')
            if (!self.values) {
                Request.get(
                    self.url.replace('level', self.levels[self.levels.length - 1]).replace('/date', ''), {}, {},
                    function (data) {
                        self.values = data;
                        self.renderValues();
                        event.trigger(evt.INDICATOR_VALUES_CHANGED);
                    }, function () {
                        $(`.${self.side}-info .value-chart`).html('<span class="error">Error</span>')
                        event.trigger(evt.INDICATOR_VALUES_CHANGED);
                        self.values = [];
                    }
                )
            } else {
                const data = [];
                $.each(this.values, function (idx, value) {
                    data.push([
                        new Date(value.date).getTime(),
                        value.value,
                    ])
                });
                const title = 'Value';
                const options = {
                    chart: {
                        zoomType: 'x'
                    },
                    title: {
                        text: title
                    },
                    xAxis: {
                        type: 'datetime',
                        title: {
                            text: 'date'
                        },
                        labels: {
                            format: '{%Y-%b-%e}'
                        },
                    },
                    legend: {
                        enabled: true
                    },
                    rangeSelector: {
                        buttons: [{
                            type: 'day',
                            count: 3,
                            text: '3d'
                        }, {
                            type: 'week',
                            count: 1,
                            text: '1w'
                        }, {
                            type: 'month',
                            count: 1,
                            text: '1m'
                        }, {
                            type: 'month',
                            count: 6,
                            text: '6m'
                        }, {
                            type: 'year',
                            count: 1,
                            text: '1y'
                        }, {
                            type: 'all',
                            text: 'All'
                        }]
                    },
                    plotOptions: {
                        series: {
                            showInLegend: false
                        }
                    },
                    series: [
                        {
                            type: 'line',
                            name: title,
                            data: data,
                            lineWidth: 1,
                            states: {
                                hover: {
                                    lineWidth: 1
                                }
                            },
                            color: '#F48020',
                            tooltip: {
                                valueDecimals: 0
                            }
                        }
                    ]
                };
                self.chart = Highcharts.stockChart(`${self.side}-value-chart`, options);
            }
        },
    })
});