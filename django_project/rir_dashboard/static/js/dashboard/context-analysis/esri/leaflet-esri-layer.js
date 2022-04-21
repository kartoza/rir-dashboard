class EsriLeafletLayer {

    constructor(name, url, params, options, style) {
        this.name = name;
        this.url = url;
        this.params = params;

        // for the options
        if (!options) {
            options = {}
        }
        this.token = options.token;
        this.username = options.username;
        this.password = options.password;
        this.$legend = $('#legend');
        this.layer = null;
        this.defaultStyle = style;
    }

    preFetch(url) {
        /**
         * Prepare fetch request headers.
         * Either a key/token or user/pass.
         *
         * TODO currently only tested for ArcREST token. Basic auth for WFS needs work.
         * @param  {string} url URL that will be requested
         * @return {array}     str url and fetch options (including GET method and headers)
         */
        let options = { method: 'GET', mode: "cors" }
        if (this.token) {
            url += `&token=${this.token}`
        } else if (this.username && this.password) {
            options['headers'] = new Headers({
                'Authorization': 'Basic ' + btoa(`${this.username}:${this.password}`)
            })
        }
        return [url, options]
    }


    async load() {
        /**
         * Fetch the drawing info from the service before we can load features
         * ESRI Alpha is scaled up tp 255 - use maxTrans ceiling
         * Return Leaflet layer
         */
        const url = this.url;
        const that = this;
        return fetch(...this.preFetch(url + '?f=json'))
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    return {
                        layer: null,
                        error: data.error.details ? data.error.details : data.error
                    }
                }
                if (data.drawingInfo === undefined) {
                    if (data.type === "Raster Layer" || (data.layers && data.layers[0] && data.layers[0].type === "Raster Layer")) {
                        return {
                            layer: null,
                            error: 'Drawing info is empty'
                        }
                    }
                }
                return {
                    layer: that.toLeafletLayer(data),
                    error: null
                }
            })
            .catch(error => {
                return {
                    layer: null,
                    error: error.details ? error.details : error
                }
            })
    }

    overrideStyle() {
        try {
            if (this.defaultStyle.icon) {
                this.style.style.style.iconUrl = this.defaultStyle.icon
            }
        } catch (e) {

        }
    }

    /**
     * get leaflet layer
     */
    toLeafletLayer(data) {
        this.style = parseArcRESTStyle(data);
        const style = this.style;
        const self = this;
        this.overrideStyle();

        const params = JSON.parse(JSON.stringify(this.params));
        const forEachFeature = function (feature, layer) {
            // check others properties
            let defaultHtml = '';
            $.each(feature.properties, function (key, value) {
                defaultHtml += `<tr><td valign="top"><b>${key.capitalize()}</b></td><td valign="top">${numberWithCommas(value)}</td></tr>`
            });
            layer.bindPopup('' +
                '<table><tr><td colspan="2" style="text-align: center; background: #eee"><b>' + self.name + '</b></td></tr>' + defaultHtml + '</table>');
        }
        params.url = this.url;
        if (this.token) {
            params.token = this.token;
        }
        switch (style.geometryType) {
            // This is for polygon
            case "esriGeometryPolygon":
            case "esriGeometryPolyline": {
                params.style = function (geojson) {
                    const value = geojson['properties'][style.fieldName];
                    let leafletStyle = null;
                    switch (style.classificationValueMethod) {
                        case "classMaxValue":
                            $.each(style.classifications, function (index, classification) {
                                if (value <= classification.classMaxValue) {
                                    leafletStyle = classification.style;
                                    return false;
                                }
                            });
                            if (!leafletStyle) {
                                leafletStyle = style.classifications[style.classifications.length - 1].style;
                            }
                            break
                        case "classExactValue":
                            $.each(style.classifications, function (index, classification) {
                                if ('' + value === '' + classification.value) {
                                    leafletStyle = classification.style;
                                    return false;
                                }
                            });
                            break
                        case "noClassification":
                            leafletStyle = style.style;
                            break
                    }

                    if (leafletStyle) {
                        return leafletStyle.style;
                    }
                }

                params['onEachFeature'] = forEachFeature;
                return L.esri.featureLayer(params);
            }

            // This is for point
            case 'esriGeometryPoint': {
                params.pointToLayer = function (geojson, latlng) {
                    const value = geojson['properties'][style.fieldName];
                    let leafletStyle = null;

                    switch (style.classificationValueMethod) {
                        case "classMaxValue":
                            $.each(style.classifications, function (index, classification) {
                                if (value <= classification.classMaxValue) {
                                    leafletStyle = classification.style;
                                    return false;
                                }
                            });
                            if (!leafletStyle) {
                                leafletStyle = style.classifications[style.classifications.length - 1].style;
                            }
                            break
                        case "classExactValue":
                            $.each(style.classifications, function (index, classification) {
                                if ('' + value === '' + classification.value) {
                                    leafletStyle = classification.style;
                                    return false;
                                }
                            });
                            break
                        case "noClassification":
                            leafletStyle = style.style;
                            break
                    }

                    if (leafletStyle) {
                        switch (leafletStyle.type) {
                            case 'circle':
                                return L.circleMarker(
                                    latlng, leafletStyle.style
                                );
                            case 'icon':
                                const icon = L.icon(leafletStyle.style);
                                return L.marker(
                                    latlng, {
                                        icon: icon
                                    }
                                );

                        }
                    }
                };

                params['onEachFeature'] = forEachFeature;
                return L.esri.featureLayer(params);
            }

        }
        return null;
    };

    /**
     * Add Legend
     */

    getLegend() {
        const style = this.style;
        if (!style) {
            return null
        }
        const that = this;
        let legend = '';
        switch (style.geometryType) {
            // This is for polygon
            case "esriGeometryPolygon": {
                if (style.classifications) {
                    $.each(style.classifications, function (index, classification) {
                        const color = classification.style.style.fillColor;
                        legend += '' +
                            '<tr>' +
                            `<td><div class="polygon" style="background-color: ${color}"></div></td>` +
                            `<td>${classification.label}</td>` +
                            '</tr>'
                    });
                } else {
                    const color = style.style.style.fillColor;
                    legend += '' +
                        '<tr>' +
                        `<td><div class="polygon" style="background-color: ${color}"></div></td>` +
                        `<td>${that.name}</td>` +
                        '</tr>'
                }
                break;
            }
            // This is for line
            case "esriGeometryPolyline": {
                if (style.classifications) {
                    $.each(style.classifications, function (index, classification) {
                        const color = classification.style.style.color;
                        const width = classification.style.style.width * 2;
                        legend += '' +
                            '<tr>' +
                            `<td><div class="line" style="height: ${width}px; background-color: ${color}"></div></td>` +
                            `<td>${classification.label}</td>` +
                            '</tr>'
                    });
                }
                break;
            }
            // This is for point
            case 'esriGeometryPoint': {
                if (style.classifications) {
                    $.each(style.classifications, function (index, classification) {
                        switch (classification.style.type) {
                            case 'circle':
                                const size = classification.style.style.radius;
                                const fillColor = classification.style.style.fillColor;
                                legend += '' +
                                    '<tr>' +
                                    `<td><div class="circle" style="width: ${size}px; height: ${size}px; background-color: ${fillColor}"></div></td>` +
                                    `<td>${classification.label}</td>` +
                                    '</tr>'
                                break
                            case 'icon':
                                legend += '' +
                                    '<tr>' +
                                    `<td><img src="${classification.style.style.iconUrl}"></td>` +
                                    `<td>${classification.label}</td>` +
                                    '</tr>'
                                break
                        }
                    });
                } else {
                    switch (style.style.type) {
                        case 'circle':
                            const fillColor = style.style.style.fillColor;
                            legend += '' +
                                '<tr>' +
                                `<td><div class="circle" style="width: 10px; height: 10px; background-color: ${fillColor}"></div></td>` +
                                `<td>${that.name}</td>` +
                                '</tr>'
                            break
                        case 'icon':
                            legend += '' +
                                '<tr>' +
                                `<td><img src="${style.style.style.iconUrl}"></td>` +
                                `<td>${that.name}</td>` +
                                '</tr>'
                            break
                    }
                }
                break;
            }
        }

        return `<table>${legend}</table>`;
    }
}