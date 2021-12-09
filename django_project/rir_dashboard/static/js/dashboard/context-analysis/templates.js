// this is identifier of all templates
const templates = {
    CONTEXT_LAYER_GROUP: '#_context-layer-group',
    CONTEXT_LAYER: '#_context-layer',
    ADMINISTRATIVE_POPUP: '#_administrative-popup',
}
define([
    'backbone'], function (Backbone) {
    return Backbone.View.extend({
        initialize: function () {
            $.each(templates, function (key, value) {
                templates[key] = _.template($(value).html())
            });
        }
    });
});