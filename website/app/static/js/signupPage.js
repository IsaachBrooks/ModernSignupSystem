import { drawSelected, updateSectionInfo } from './selectTimes.js';
import { showCurrentEnrolled } from './drawCurrent.js'
import { enrollStudent, removeEnrolledClass } from './databaseAccess.js';

$(document).ready(function () {

    let lastTimeSlotHolderIndex;
    let lastTimeSlotHolderBGC;
    let lastClicked;

    $(".day-holder").on({
        click: function() {
            let crnSel = $(this)[0].getAttribute('data-crn');
            drawSelected(crnSel);
        },
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
            let crnSel = $(this)[0].getAttribute('data-crn');
            let fullSect = $(`[data-crn="${crnSel}"]`);
            for (let i = 0; i < fullSect.length; i++) {
                let cur = fullSect[i];
                lastTimeSlotHolderIndex = cur.style.zIndex;
                cur.style.zIndex = 9999;
                cur.style.border = '1px solid white';
                cur.setAttribute('data-orig-width', cur.style.width);
                cur.style.width = '100%'
                cur.setAttribute('data-orig-offset-left', cur.style.left);
                cur.style.left = '0px';
            }
        },
        mouseleave: function() {
            let crnSel = $(this)[0].getAttribute('data-crn');
            let fullSect = $(`[data-crn="${crnSel}"]`);
            for (let i = 0; i < fullSect.length; i++) {
                let cur = fullSect[i];
                cur.style.zIndex = lastTimeSlotHolderIndex;
                cur.style.border = '1px black solid';
                cur.style.width = cur.getAttribute('data-orig-width');
                cur.style.left = cur.getAttribute('data-orig-offset-left');
            }
            lastTimeSlotHolderIndex = null;
        }
        
    }, 'div.time-slot-holder');


    const sectionInfo = $('.section-info-main');

    $("#selected-holder").on({
        click: function() {
            updateSectionInfo(
                $(this).data('crn'),
                $(this).data('cid')
            );
            sectionInfo.css('visibility', 'unset');
        }
    }, "div.selected-list-elem");

    $("#current-holder").on({
        click: function() {
            updateSectionInfo(
                $(this).data('crn'),
                $(this).data('cid')
            );
            sectionInfo.css('visibility', 'unset');
        }
    }, "div.current-list-elem");

    $("#section-info-close").on({
        click: function() {
            sectionInfo.css('visibility', 'hidden');
        }
    });

    $("#section-info-register").on({
        click: function() {
            let crn = $('#sec-info-content').data('crn');
            let response = enrollStudent(crn).then((data) => {
                alert(data.reply);
                showCurrentEnrolled();
                updateSectionInfo();
            });
        }
    });
    $("#section-info-unregister").on({
        click: function() {
            let crn = $('#sec-info-content').data('crn');
            let response = removeEnrolledClass(crn).then((data) => {
                alert(data.reply);
                showCurrentEnrolled();
                updateSectionInfo();
            });
        }
    });
    showCurrentEnrolled();
})