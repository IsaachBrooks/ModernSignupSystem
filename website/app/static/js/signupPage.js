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
            let crnSel = $(this)[0].getAttribute('data-crn')
            let fullSect = $(`[data-crn="${crnSel}"]`);
            for (let i = 0; i < fullSect.length; i++) {
                lastTimeSlotHolderIndex = fullSect[i].style.zIndex;
                fullSect[i].style.zIndex = 9999;
                fullSect[i].style.border = '1px solid white';
            }
        },
        mouseleave: function() {
            let crnSel = $(this)[0].getAttribute('data-crn')
            let fullSect = $(`[data-crn="${crnSel}"]`);
            for (let i = 0; i < fullSect.length; i++) {
                fullSect[i].style.zIndex = lastTimeSlotHolderIndex;
                fullSect[i].style.border = 'unset';
            }
            lastTimeSlotHolderIndex = null;
        }
        
    }, 'div.time-slot-holder');

})