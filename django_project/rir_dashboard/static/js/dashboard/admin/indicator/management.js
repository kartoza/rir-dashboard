$(document).ready(function () {
    const $dropArea = $('#drop-area');

    function updateDone() {
        // const orders = [];
        // $dropArea.find('.block-value').each(function () {
        //     orders.push($(this).data('id'));
        // });
        // $('#order-input').val(orders.join(','));

        const orders = {};
        $('.group-row').each(function () {
            const group = $(this).data('group');
            orders[group] = []
            $(this).find('.block-value').each(function () {
                orders[group].push($(this).data('id'));
            });
        })
        $('#order-input').val(JSON.stringify(orders));
    }

    function checkIndicatorList() {
        // check every group, if empty show No Indicator
        $('.group-row').each(function () {
            if ($(this).find('.block-value').not('.ui-sortable-helper').length === 0) {
                $(this).find('.no-value').remove();
                $(this).find('ul').append(
                    '<li class="block no-value"><i>No indicator</i></li>'
                )
            } else {
                $(this).find('.no-value').remove();
            }
        })
    }

    // for group list
    const $groupList = $("#group-list");
    $groupList.sortable({
        update: updateDone
    });
    $groupList.sortable('disable');

    // for the indicator list
    const $indicatorList = $(".indicator-list");
    $indicatorList.sortable({
        connectWith: '.indicator-list',
        update: updateDone,
        sort: checkIndicatorList
    });
    $indicatorList.sortable('disable');


    $('#cancel-order').click(function () {
        $dropArea.removeClass('ordering');
        $groupList.sortable('disable');
        $indicatorList.sortable('disable');
        return false;
    });
    $('#change-order').click(function () {
        $dropArea.addClass('ordering');
        $groupList.sortable('enable');
        $indicatorList.sortable('enable');
    });

    checkIndicatorList();
    updateDone();

    // this is for show/hide button
    function checkGroup($element) {
        if ($element.find('.indicator-name .fa-eye:visible').length === 0) {
            $element.addClass('hidden');
        } else {
            $element.removeClass('hidden');
        }
    }

    $('.indicator-name .fa-eye, .indicator-name .fa-eye-slash').click(function () {
        if ($(this).hasClass('fa-eye')) {
            $(this).closest('li').addClass('hidden');
        } else {
            $(this).closest('li').removeClass('hidden');
        }
        $.ajax({
            url: $(this).data('url'),
            type: 'POST',
            success: function (data, textStatus, request) {
            },
            error: function (error, textStatus, request) {
            },
            beforeSend: beforeAjaxSend
        });
        checkGroup($(this).closest('.group-row'));
    });

    // if group is clicked
    $('.group-name .fa-eye').click(function () {
        $(this).closest('li').find('.indicator-name .fa-eye').click();
    });
    $('.group-name .fa-eye-slash').click(function () {
        $(this).closest('li').find('.indicator-name .fa-eye-slash').click();
    });

    // init check group
    $('.group-row').each(function () {
        checkGroup($(this))
    })
});