// this is identifier of all templates
const templates = {
    CONTEXT_LAYER_GROUP: '#_context-layer-group',
    CONTEXT_LAYER: '#_context-layer',
    ADMINISTRATIVE_POPUP: '#_administrative-popup',
    INDICATOR_INFO: '#_indicator-info',
    SCENARIO_BULLET: '#_scenario-bullet',
}
define([], function () {
    return Backbone.View.extend({
        initialize: function () {
            $.each(templates, function (key, value) {
                templates[key] = _.template($(value).html())
            });
        }
    });
});