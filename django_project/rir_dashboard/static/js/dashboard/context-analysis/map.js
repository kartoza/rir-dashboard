let map = null;
let basemapLayer = null;
$(document).ready(function () {
    map = L.map('map', { zoomControl: false });
    $('#basemap-list .basemap-box').click(function () {
        $('#basemap-list .basemap-box').removeClass('active');
        $(this).addClass('active');
        basemapChange(basemapLayers[$(this).data('id')])
    })
    $(`#basemap-list .basemap-box[data-id="${basemapDefault}"]`).click()

    function basemapChange(basemapDetail) {
        try {
            map.removeLayer(basemapLayer)
        } catch (e) {

        }
        basemapLayer = L.tileLayer(basemapDetail.url, basemapDetail.parameters);
        basemapLayer.addTo(map);
    }
});