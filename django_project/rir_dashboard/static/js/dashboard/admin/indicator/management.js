$(document).ready(function () {
    const $dropArea = $('#drop-area');
    let $temporary = null;
    let $dropAreaOver = null;

    function dragFunction(evt) {
        if ($dropAreaOver) {
            removeTemporary();
            var relY = $(evt.target).position().top - $dropAreaOver.offset().top;
            let $blockElement = null;
            $dropAreaOver.find('.block-value').each(function (index) {
                const levelY = $(this).position().top - $dropAreaOver.offset().top
                if (relY < levelY) {
                    $blockElement = $(this);
                    return false
                }
            });
            const htmlTemporary = `<div id="temporary" class="block"><div class="block-content">Temporary</div></div>`
            if (!$blockElement) {
                $dropAreaOver.append(htmlTemporary);
            } else {
                $blockElement.before(htmlTemporary)
            }
            $temporary = $('#temporary')
        }
    }

    /**
     * Remove temporary level
     */
    function removeTemporary() {
        if ($temporary) {
            $temporary.remove();
            $temporary = null;
        }
    }

    /**
     * When the element dropped
     */
    function onDropArea($elm, $dropArea) {
        const id = $elm.data('id');
        const htmlNewElement = `<div id="data-${id}" class="block block-value" data-id="${id}">${$elm.html()}</div>`;
        if ($temporary) {
            $temporary.replaceWith(htmlNewElement)
        }
        $elm.remove()
        $(`#data-${id}`).draggable({
            drag: dragFunction,
            revert: 'invalid'
        });

        const orders = [];
        $dropArea.find('.block-value').each(function () {
            orders.push($(this).data('id'));
        });
        $('#order-input').val(orders.join(','))
    }

    // init
    $('.block').draggable({
        drag: dragFunction,
        revert: 'invalid'
    });
    $dropArea.droppable({
        hoverClass: "ui-state-hovered",
        drop: function (e, ui) {
            onDropArea($(ui.draggable), $dropArea);
        },
        over: function () {
            $dropAreaOver = $dropArea;
        },
        out: function () {
            $dropAreaOver = null;

            // delete temporary
            removeTemporary();
        },
    });
    $('.block').draggable('disable')
    $('#cancel-order').click(function () {
        $dropArea.removeClass('ordering');
        $('.block').draggable('disable');
        return false;
    })
    $('#change-order').click(function () {
        $dropArea.addClass('ordering');
        $('.block').draggable('enable');
    })
});