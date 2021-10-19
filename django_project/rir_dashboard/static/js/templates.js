// this is identifier of all templates
const templates = {}
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