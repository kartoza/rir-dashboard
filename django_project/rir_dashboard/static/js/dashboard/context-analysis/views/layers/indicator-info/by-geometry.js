/**
 * Layers of map controlled in here.
 * Add layers in here.
 */
define(['js/views/layers/indicator-info/base'], function (Base) {
    return Base.extend({
        /** Initialization
         */
        panelID: 'indicator-list-by-geometry',
        opened: false,
        /**
         * Init listener for layers
         */
        listener: function () {
            event.register(this, evt.GEOMETRY_CLICKED, this.geometryClicked);
            event.register(this, evt.DATE_CHANGED, this.dateChanged);
        },
        changed: function () {
            if (this.opened && this.geometry && this.date) {
                const self = this;
                this.$el.find('tr').hide();
                this.$el.find('.indicator-info-title .col').html(
                    `${this.geometry.properties.geometry_name} (${this.geometry.properties.geometry_code})`
                );
                this.control.detailPanelOpened(this.panelID);
                const url = urls['indicators-values-by-geometry-level-date-api'].replaceAll(
                    'geometry_identifier', this.geometry.properties.geometry_code).replaceAll(
                    'geometry_level', this.geometry.properties.geometry_level).replaceAll(
                    'date', this.date)
                Request.get(
                    url, {}, {},
                    function (data) {
                        const groupsValue = {}
                        const allValues = []
                        $.each(data, function (idx, rowData) {
                            const $row = $('#indicator-by-geometry-' + rowData.indicator_id);
                            const $rowGroup = $row.closest('.group').find('.group-name');
                            $rowGroup.show();
                            $row.show();
                            $($row.find('td')[1]).css('background', rowData.background_color);
                            $($row.find('td')[2]).html(rowData.scenario_text);

                            if (!groupsValue[rowData['group_name']]) {
                                groupsValue[rowData['group_name']] = []
                            }
                            groupsValue[rowData['group_name']].push(rowData.scenario_value);
                            allValues.push(rowData.scenario_value);
                        });

                        // get the common value for each group
                        $.each(groupsValue, function (groupName, array) {
                            const scenario = scenarios[returnMostOccurring(array)[0]];
                            const $groupEl = self.$el.find(`.group-name[data-name="${groupName}"]`);
                            $($groupEl.find('td')[1]).css('background', scenario.color);
                            $($groupEl.find('td')[2]).html(scenario.text);
                        })
                        // for all values
                        const $bullet = self.$el.find('.indicator-info-title .scenario-bullet')
                        $.each(scenarios, function (scenarioLevel, data) {
                            $bullet.removeClass('scenario-' + scenarioLevel);
                        })
                        $bullet.addClass('scenario-' + returnMostOccurring(allValues)[0]);
                    }, function (e) {
                        console.log(e)
                    })
            }
        },
        /**
         * Open the panel
         */
        open: function () {
            Base.prototype.open.apply(this);
            event.trigger(evt.GEOMETRY_INDICATOR_CLICKED, this.geometry);
        },
        /**
         * Open the panel
         */
        close: function () {
            Base.prototype.close.apply(this);
            this.opened = false;
        },
        /**
         * When geometry clicked
         */
        geometryClicked: function (geometry) {
            this.geometry = geometry;
            this.opened = true;
            this.changed();
        },
        /**
         * When date changed
         */
        dateChanged: function (date) {
            this.date = date;
            this.changed();
        }
    })
});