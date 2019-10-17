$(document).ready(function () {

    let lastTimeSlotHolderIndex;
    let lastTimeSlotHolderBGC;
    let lastClicked;

    $(".day-holder").on({
        mousedown: function() {
            lastClicked = $(this)
            lastTimeSlotHolderBGC = lastClicked.css('background-color');
            lastClicked.css('background-color', '#fc0');
        },
        mouseup: function() {
            lastClicked.css('background-color', lastTimeSlotHolderBGC);
            lastTimeSlotHolderBGC = null;
            lastClicked = null;
        },
        mouseenter: function () {
            lastTimeSlotHolderIndex = $(this).css('z-index');
            $(this).css('z-index', '9999');
            $(this).css('border', '1px solid white');
        },
        mouseleave: function() {
            $(this).css('z-index', `${lastTimeSlotHolderIndex}`);
            $(this).css('border', 'unset')
            lastTimeSlotHolderIndex = null;
        }
        
    }, 'div.time-slot-holder');

})