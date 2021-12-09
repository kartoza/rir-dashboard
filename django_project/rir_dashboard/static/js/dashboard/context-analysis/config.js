let mapView;
let map;
let event;
let Request;

require.config(requireConfig);
require([
    // libs
    'jquery',
    'backbone',
    'underscore',

    // projects static
    'js/request',
    'js/templates',
    'js/event',
    'js/views/map',
    'js/views/layers/control'
], function (
    $, Backbone, _, _Request, _Templates, _Event,
    Map, LayersControl) {

    new _Templates();
    event = new _Event();
    Request = new _Request();
    initEvent();

    // initiate all view
    mapView = new Map();
    map = mapView.map;
    new LayersControl(map);

    function initEvent() {
        // --------------------------------------------------------------------
        // INIT BUTTONS EVENT
        // --------------------------------------------------------------------

        // checking hash to check the tab
        const $list = $('.context-analysis-nav');
        $list.click(function () {
            $list.removeClass('active');
            $(this).addClass('active');
            $('.scenario-section').hide();

            const target = $(this).data('target');
            $(`div[data-program="${target}"]`).show();
            $('#content').scrollTop(0);
        });
        if (!window.location.hash) {
            $($list[0]).click();
        } else {
            const hash = window.location.hash.replaceAll('#', '');
            const $target = $(`.context-analysis-nav[data-target="${hash}"]`);
            if ($target.length === 0) $($list[0]).click();
            else $target.click();
        }

        // table toggle to show/hide all indicators or not
        $('#toggle-table').click(function () {
            $(this).toggleClass('all');
            if ($(this).hasClass('all')) {
                $(this).html('Show just context indicator analysis');
                $('.no-context-analysis').removeClass('hide');
            } else {
                $(this).html('Show all indicators');
                $('.no-context-analysis').addClass('hide');
            }
            $('#indicator .group-name.hidden').click();
        });

        // Left side panel of map
        // Event for toggling side panel
        const $leftSide = $('#left-side');
        const $leftSideToggleButton = $('#left-side .toggle-button');
        const width = $leftSide.width();
        $leftSideToggleButton.click(function () {
            const isHidden = $(this).hasClass('hidden');
            $leftSideToggleButton.addClass('hidden');
            $('#left-side .content').hide();
            $(this).removeClass('hidden');
            $(`#${$(this).data('target')}`).show();

            // doing toggle side panel
            if (!isHidden) {
                if (!$leftSide.data('hidden')) {
                    $leftSide.animate({ left: `-${width}px` }, 100, function () {
                        $leftSide.data('hidden', true)
                    });
                } else {
                    $leftSide.animate({ left: `0` }, 100, function () {
                        $leftSide.data('hidden', false)
                    });
                }
            } else {
                $leftSide.animate({ left: `0` }, 100, function () {
                    $leftSide.data('hidden', false)
                });
            }
        });
        // indicator shows by default
        $('#indicator-toggle-button').click();

        // Event for toggling full screen
        const $fullScreen = $('.left-side-fullscreen');
        const $indicator = $('#indicator');
        const $exitFullScreen = $('.left-side-exit-fullscreen');
        $fullScreen.click(function () {
            $leftSide.width('100%');
            $exitFullScreen.show();
            $fullScreen.hide();
            $indicator.find('table').addClass('full-screen');
        });
        $exitFullScreen.click(function () {
            $leftSide.width(width);
            $exitFullScreen.hide();
            $fullScreen.show();
            $indicator.find('table').removeClass('full-screen');
        });

        // Event for toggling indicator group
        $('#indicator .group-name').click(function () {
            const $row = $(this).closest('tbody');
            const $i = $(this).find('.group-toggle');
            $i.toggleClass('fa-caret-down');
            $i.toggleClass('fa-caret-up');
            $(this).toggleClass('hidden');
            if (!$i.hasClass('fa-caret-down')) $row.find('tr').show();
            else $row.find('.group-row').hide();
        })
    }
});