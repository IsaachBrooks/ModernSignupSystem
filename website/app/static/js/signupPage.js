import { drawSelected, updateSectionInfo, showSectionInfo, hideSectionInfo } from './selectTimes.js';
import { showCurrentEnrolled } from './drawCurrent.js'
import { enrollStudent, removeEnrolledClass, completeCurSections } from './databaseAccess.js';
import { updateCurTimes } from './drawTimes.js';
import { reloadSections } from './options.js';

let lastTimeSlotHolderIndex;
let lastTimeSlotHolderBGC;
let lastClicked;
const signupHolder = $("#signup-main");
const curClassesHolder = $("#curClasses-main");

$(document).ready(function () {

    /*
    *   Demo button
    */
    $('#complete-classes').on({
        click: function() {
            completeCurSections().then(() => {
                showCurrentEnrolled();
                updateCurTimes();
            });
        }
    });
    setupTimeslotCards()
    setupSelectors();
    setupSectionInfoViewer();
    showCurrentEnrolled();
});

function setupSectionInfoViewer() {
    /*
    *   Section info buttons
    */
   $("#section-info-close").on({
    click: function() {
        hideSectionInfo();
    }
    });

    /*
    * Register and unregister buttons  
    */
    $("#section-info-register").on({
        click: function() {
            let crn = $('#sec-info-content').data('crn');
            enrollStudent(crn).then((data) => {
                alert(data.reply);
                showCurrentEnrolled();
                updateSectionInfo();
                updateCurTimes();
                reloadSections();
            });
        }
    });

    $("#section-info-unregister").on({
        click: function() {
            let crn = $('#sec-info-content').data('crn');
            removeEnrolledClass(crn).then((data) => {
                alert(data.reply);
                showCurrentEnrolled();
                updateSectionInfo();
                updateCurTimes();
                reloadSections();
            });
        }
    });
}

/*
    *   Show section info once a section is selected
    */
function setupSelectors() {
   $("#selected-holder").on({
        click: function() {
            updateSectionInfo(
                $(this).data('crn'),
                $(this).data('cid')
            );
            showSectionInfo();
        }
    }, "div.selected-list-elem");

    $("#current-holder").on({
        click: function() {
            updateSectionInfo(
                $(this).data('crn'),
                $(this).data('cid')
            );
            showSectionInfo();
        }
    }, "div.current-list-elem");
}

/*
*   Handle interactivity with all time slots.
*   Adjust borders on mouseover and mouseout, and click color.
*/
function setupTimeslotCards() {
    $(".day-holder").on({
        click: function() {
            let crnSel = $(this)[0].getAttribute('data-crn');
            drawSelected(crnSel);
        },
        mousedown: function() {
            lastClicked = $(this)
            lastTimeSlotHolderBGC = lastClicked.css('background-color');
            let crnSel = $(this)[0].getAttribute('data-crn');
            let cName = $(this)[0].className.replace(' ', '.');
            let fullSect = $(`[data-crn="${crnSel}"].${cName}`);
            for (let i = 0; i < fullSect.length; i++) {
                fullSect.css('background-color', '#fc0');
            }
        },
        "mouseup mouseleave": function() {
            if (lastClicked != null) {
                let crnSel = $(this)[0].getAttribute('data-crn');
                let cName = $(this)[0].className.replace(' ', '.');
                let fullSect = $(`[data-crn="${crnSel}"].${cName}`);
                for (let i = 0; i < fullSect.length; i++) {
                    fullSect.css('background-color', lastTimeSlotHolderBGC);
                }
            }
            lastTimeSlotHolderBGC = null;
            lastClicked = null;
        },
        mouseenter: function () {
            let crnSel = $(this)[0].getAttribute('data-crn');
            let cName = $(this)[0].className.replace(' ', '.');
            let fullSect = $(`[data-crn="${crnSel}"].${cName}`);
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
            let cName = $(this)[0].className.replace(' ', '.');
            let fullSect = $(`[data-crn="${crnSel}"].${cName}`);
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
}