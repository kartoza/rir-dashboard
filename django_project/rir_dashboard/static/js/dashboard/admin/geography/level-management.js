$(document).ready(function () {
    const $dropLevelArea = $('#level-drop-area');
    const $dropLevelListArea = $('#level-list-drop-area');
    let $temporary = null;
    let $dropAreaOver = null;

    function dragFunction(evt) {
        $(evt.target).css('z-index', 9999);
        $(evt.target).css('height', 0);
        if ($dropAreaOver) {
            removeTemporary();
            var relY = $(evt.target).position().top - $dropAreaOver.offset().top;
            let $blockElement = null;
            $dropAreaOver.find('.level-block-value').each(function (index) {
                const levelY = $(this).position().top - $dropAreaOver.offset().top
                if (relY < levelY) {
                    $blockElement = $(this);
                    return false
                }
            });
            const htmlTemporary = `<div id="level-temporary" class="level-block"><div class="level-block-content">Temporary</div></div>`
            if (!$blockElement) {
                $dropAreaOver.append(htmlTemporary);
            } else {
                $blockElement.before(htmlTemporary)
            }
            $temporary = $('#level-temporary')
        }
    }

    $('.level-block').draggable({
        drag: dragFunction
    });
    $dropLevelArea.droppable({
        hoverClass: "ui-state-hovered",
        drop: function (e, ui) {
            onDropArea($(ui.draggable), $dropLevelArea);
        },
        over: function () {
            $dropAreaOver = $dropLevelArea;
        },
        out: function () {
            $dropAreaOver = null;

            // delete temporary
            removeTemporary();
        },
    });

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
        const htmlNewElement = `<div id="level-${id}" class="level-block level-block-value" data-id="${id}">${$elm.html()}</div>`;
        if ($temporary) {
            $temporary.replaceWith(htmlNewElement)
        } else {
            $dropArea.append(htmlNewElement)
        }
        $elm.remove()
        $(`#level-${id}`).draggable({
            drag: dragFunction,
            stop: function () {
                if ($dropArea === $dropLevelArea && !$temporary) {
                    onDropArea($(`#level-${id}`), $dropLevelListArea)
                }
            }
        });

        const levels = [];
        $dropLevelArea.find('.level-block-value').each(function () {
            levels.push($(this).data('id'));
        });
        $('#level-input').val(levels.join(','))
    }

    // init instance level
    $(instanceLevels).each(function (idx, level) {
        onDropArea($(`#level-${level}`), $dropLevelArea)
    })
});