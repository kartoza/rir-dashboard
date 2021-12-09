/**
 * Handler of dispatcher event
 */
const evt = {
    MAP_PAN: 'map:pan', // Pan the map
    MAP_FLY: 'map:fly', // Fly the map
    MAP_ADD_LAYER: 'map:layer:add', // add layer to map
    MAP_REMOVE_LAYER: 'map:layer:remove', // remove layer from map

    RERENDER_CONTEXT_LAYER: 'layers:context-layer:rerender', // When layers changed
    ADMINISTRATIVE_GET_LAYER: 'administrative:get-layer', // When layers changed
}
define([
    'backbone'], function (Backbone) {
    return Backbone.View.extend({

        initialize: function () {
            this.dispatcher = _.extend({}, Backbone.Events);
        },
        /** Register event with specific name for an objecy
         * @param obj
         * @param name, name of event that will be used
         * @param func, function that will be called for the event
         */
        register: function (obj, name, func) {
            obj.listenTo(this.dispatcher, name, func);
        },
        /** Trigger event with specific name
         * @param name, name of event that will be used
         * @param args, any parameters that will be passed to function
         */
        trigger: function (name, ...args) {
            this.dispatcher.trigger(name, ...args)
        }
    });
});