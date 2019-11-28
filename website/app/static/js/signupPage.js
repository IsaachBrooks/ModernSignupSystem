import { drawSelected, updateSectionInfo, showSectionInfo, hideSectionInfo } from './selectTimes.js';
import { showCurrentEnrolled } from './drawCurrent.js'
import { enrollStudent, removeEnrolledClass, completeCurSections, hasLinkedClass, checkCanEnroll, getSectionsInfoMinimal } from './databaseAccess.js';
import { updateCurTimes } from './drawTimes.js';
import { reloadSections } from './options.js';

let lastTimeSlotHolderIndex;
let lastTimeSlotHolderBGC;
let lastClicked;
const signupHolder = $("#signup-holder");
const esHold = $('#extra-select-holder');

let clickColor = "#fc0"

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
    setupExtraSelect();
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
            checkCanEnroll(crn).then( (canEnroll) => {
                if (canEnroll.success) {
                    hasLinkedClass(crn).then( (linkedReply) => {
                        if (linkedReply.hasLinkedClass) {
                            let linkedSections = linkedReply.crns;
                            hideSectionInfo();
                            forceExtraSelect(crn, linkedSections);
                        }  else {
                            enrollStudent(crn).then((enrollReply) => {
                                showCurrentEnrolled();
                                updateSectionInfo();
                                updateCurTimes();
                                reloadSections();
                                showAlert({reply: enrollReply.reply, success: enrollReply.success});
                            });
                        }
                    });
                } else {
                    hideSectionInfo();
                    showAlert({reply: canEnroll.reply, success: canEnroll.success});
                }
            });
        }
    });

    $("#section-info-unregister").on({
        click: function() {
            let crn = $('#sec-info-content').data('crn');
            removeEnrolledClass(crn).then((data) => {
                showCurrentEnrolled();
                updateSectionInfo();
                updateCurTimes();
                reloadSections();
                showAlert({reply: data.reply, success: data.success});
            });
        }
    });
}

/*
 *  Setup buttons for controlling when extra selection is required
 */
function setupExtraSelect() {
    
    $('#extra-select-confirm').on({
        click: () => {
            let input = +$('input[name="extra"]:checked').val()
            let crn = $('#extra-sel-header').data('crn');
            checkCanEnroll(input).then( (canEnroll) => {
                if (canEnroll.success) {
                    enrollStudent([crn, input]).then( (enrollReply) => {
                        showCurrentEnrolled();
                        updateSectionInfo();
                        updateCurTimes();
                        reloadSections();
                        hideExtraSelect();
                        resetExtraSelect();
                        console.log(enrollReply);
                        showAlert(enrollReply);
                    });
                } else {
                    hideExtraSelect();
                    resetExtraSelect();
                    showAlert(canEnroll);
                }
            });
        }
    });
    $('#extra-select-cancel').on({
        click: () => {
            hideExtraSelect();
            resetExtraSelect();
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
                fullSect.css('background-color', clickColor);
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
        
    }, 'div.full-slot');

    $(".day-holder").on({
        click: function() {
            let crnSel = $(this)[0].getAttribute('data-crn');
            let cidSel = $(this)[0].getAttribute('data-cid');
            updateSectionInfo(
                crnSel,
                cidSel
            );
            showSectionInfo();
        },
        mousedown: function() {
            lastClicked = $(this)
            lastTimeSlotHolderBGC = lastClicked.css('background-color');
            let crnSel = $(this)[0].getAttribute('data-crn');
            let cName = $(this)[0].className.replace(' ', '.');
            let fullSect = $(`[data-crn="${crnSel}"].${cName}`);
            for (let i = 0; i < fullSect.length; i++) {
                fullSect.css('background-color', clickColor);
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
                cur.style.border = '1px black solid';
                cur.style.width = cur.getAttribute('data-orig-width');
                cur.style.left = cur.getAttribute('data-orig-offset-left');
            }
        }
        
    }, 'div.cur-slot');
}

function showAlert(reply) {
    clearAlerts();
    let success = reply.success; 
    let body = reply.reply;
    let alertClass, alertHead, alertBody;
    if (success) {
        alertClass = 'alert-success';
        alertHead = 'Success';
    } else {
        alertClass = 'alert-danger';
        alertHead = 'Failure';
    }
    alertBody = body;
    const alertBox = createAlert(alertClass, alertHead, alertBody);
    signupHolder.prepend(alertBox);
    $(alertBox).fadeIn(500).delay(10000).fadeOut(3000)
}

export function clearAlerts() {
    const alertBox = $('#alert-box')
    alertBox.remove()
}

function forceExtraSelect(crn, sections) {    
    const esHead = $('#extra-sel-header');
    esHead.data('crn', crn);
    const esList = $('#extra-sel-list');
    esList.empty();
    getSectionsInfoMinimal(sections).then((reply) => {
        for (let sect of reply) {
            let crn = sect.crn;
            let id = `crnID${crn}`;
            let label = document.createElement('label');
            let input = document.createElement('input');
            input.setAttribute('type', 'radio');
            input.setAttribute('name', 'extra');
            input.setAttribute('id', id);
            input.setAttribute('value', crn);
            label.className = "extra-input-label";
            label.setAttribute('for', id);
            label.appendChild(input);
            label.innerHTML += ` ${sect.sec} ${sect.shortName} ${sect.cName}`;
            esList.append(label);
        }
    });
    showExtraSelect();
}

export function showExtraSelect() {
    esHold.fadeIn(300);
}

export function hideExtraSelect() {
    esHold.fadeOut();
}

function resetExtraSelect() {
    const esHead = $('#extra-sel-header');
    esHead.data('crn', undefined);
    const esList = $('#extra-sel-list');
    esList.empty();
}

export function createAlert(alertClass = 'alert-primary', headText, bodyText) {
    let alertBox = document.createElement('div');
    alertBox.id = 'alert-box';
    alertBox.className = `alert ${alertClass}`;
    alertBox.setAttribute('role', 'alert');
    alertBox.style.display = 'none';
    let head = document.createElement('h4');
    head.id = 'alert-box-heading';
    head.className = 'alert-heading';
    head.innerHTML = headText;
    let body = document.createElement('p');
    body.id = 'alert-box-body';
    body.innerHTML = bodyText;
    let btn = document.createElement('button');
    btn.setAttribute('type', 'button');
    btn.className = 'close';
    btn.setAttribute('data-dismiss', 'alert');
    btn.setAttribute('aria-label', 'close');
    let btnSpan = document.createElement('span');
    btnSpan.setAttribute('aria-hidden', 'true');
    btnSpan.innerHTML = '&times;'
    btn.appendChild(btnSpan);
    alertBox.appendChild(head);
    alertBox.appendChild(body);
    alertBox.appendChild(btn);
    return alertBox;
}