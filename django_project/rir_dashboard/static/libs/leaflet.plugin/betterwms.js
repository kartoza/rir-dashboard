BetterWMS = L.TileLayer.WMS.extend({
    popup: null,
    added: false,
    addPopup: function (latlng, content) {
        this.popup = L.popup().setLatLng(latlng)
            .setContent(content)
            .openOn(this._map);
    },
    onAdd: function (map) {
        L.TileLayer.WMS.prototype.onAdd.call(this, map);
        map.on('click', this.getFeatureInfo, this);
        if (this.popup) {
            this.popup._close()
        }
        this.added = true;
    },

    onRemove: function (map) {
        L.TileLayer.WMS.prototype.onRemove.call(this, map);
        map.off('click', this.getFeatureInfo, this);
        if (this.popup) {
            this.popup._close()
        }
        this.added = false;
    },

    getFeatureInfo: function (evt) {
        const latlng = evt.latlng;
        let url = this.getFeatureInfoUrl(evt.latlng);
        this.addPopup(latlng, '<div style="padding: 10px 20px">Loading</div>')

        let showResults = L.Util.bind(this.showGetFeatureInfo, this);
        $.ajax({
            url: url,
            success: function (data, status, xhr) {
                showResults(data, evt.latlng);
            },
            error: function (xhr, status, error) {
                showResults({}, evt.latlng, xhr.statusText);
            }
        });
    },

    getFeatureInfoUrl: function (latlng) {
        // Construct a GetFeatureInfo request URL given a point
        var point = this._map.latLngToContainerPoint(latlng, this._map.getZoom()),
            size = this._map.getSize(),

            params = {
                request: 'GetFeatureInfo',
                service: 'WMS',
                srs: 'EPSG:4326',
                styles: this.wmsParams.styles,
                map: this.wmsParams.map,
                transparent: this.wmsParams.transparent,
                version: this.wmsParams.version,
                format: this.wmsParams.format,
                bbox: this._map.getBounds().toBBoxString(),
                height: size.y,
                width: size.x,
                layers: this.wmsParams.layers,
                query_layers: this.wmsParams.layers,
                info_format: 'application/json'
            };

        params[params.version === '1.3.0' ? 'i' : 'x'] = Math.floor(point.x);
        params[params.version === '1.3.0' ? 'j' : 'y'] = Math.floor(point.y);

        return this._url + L.Util.getParamString(params, this._url, true);
    },
    renderFeatureInfo: function (data) {
        return ''
    },
    renderError: function (error) {
        return ''
    },
    showGetFeatureInfo: function (data, latlng, error) {
        if (!error) {
            const content = this.renderFeatureInfo(data);

            // show content
            if (this.added && content) {
                this.addPopup(latlng, content);
            } else {
                this.popup._close();
            }
        } else {
            this.addPopup(latlng, this.renderError(error));
        }
    }
});

function tileLayerBetterWMS(url, options, methodOptions) {
    if (!methodOptions) {
        methodOptions = {}
    }
    const BetterWMSUpdate = BetterWMS.extend(methodOptions)
    return new BetterWMSUpdate(url, options);
}

L.tileLayer.betterWMS = tileLayerBetterWMS;