/**
 * Handler of dispatcher event
 */
const evt = {}
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