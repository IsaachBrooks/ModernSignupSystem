import { drawSelected, updateSectionInfo, showSectionInfo, hideSectionInfo } from './selectTimes.js';
import { showCurrentEnrolled } from './drawCurrent.js'
import { enrollStudent, removeEnrolledClass, completeCurSections, hasLinkedClass, checkCanEnroll, getSectionsInfo } from './databaseAccess.js';
import { updateCurTimes } from './drawTimes.js';
import { reloadSections } from './options.js';

export let scaleFactor = 1.5;

let lastTimeSlotHolderIndex;
let lastTimeSlotHolderBGC;
let lastClicked;
const signupHolder = $("#signup-holder");
const esHold = $('#extra-select-holder');

let clickColor = "#fc0";


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

function setupWindowScaling() {
    let dayHolders = $('.day-holder');
    let canvasHolder = $('#signup-grid-canvas');
    
}

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
                reloadSections(alert=false);
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
                        reloadSections(alert=false);
                        hideExtraSelect();
                        resetExtraSelect();
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
            collapseAlerts();
            showSectionInfo();
        }
    }, "div.selected-list-elem");

    $("#current-holder").on({
        click: function() {
            updateSectionInfo(
                $(this).data('crn'),
                $(this).data('cid'),
            );
            collapseAlerts();
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
            drawSelected(crnSel, $(this)[0].style.backgroundColor);
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
            collapseAlerts();
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
    createAlert(alertClass, alertHead, alertBody);
}

export function clearMajorAlerts() {
    const alertBox = $('#alert-box-major')
    alertBox.remove()
}
export function clearMinorAlerts() {
    const alertBox = $('#alert-box-minor')
    alertBox.remove()
}

export function collapseAlerts() {
    const alertBox = $('#alert-box-major')
    if (alertBox.css('display') !== 'none')
        alertBox.stop();
}

function forceExtraSelect(crn, sections) {    
    const esHead = $('#extra-sel-header');
    esHead.data('crn', crn);
    const esList = $('#extra-sel-list');
    esList.empty();
    
    getSectionsInfo(sections).then((reply) => {
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
            label.innerHTML += ` ${sect.crn} ${sect.sec} ${sect.cNumber} ${sect.cName}, ${sect.days} ${getTimeStartEnd(sect.tStart, sect.tEnd)}`;
            esList.append(label);
        }
    });
    showExtraSelect();
}

export function getTimeStartEnd(tStart, tEnd) {
    const dateMatcher = /(\d\d):(\d\d):(\d\d)/;
    let start = tStart.split(dateMatcher);
    let end = tEnd.split(dateMatcher);
    let startString, endString;
    let startAMPM = 'AM';
    let endAMPM = 'AM';
    if (+start[1] >= 12) {
        startAMPM = 'PM'
        if (+start[1] > 12) {
            start[1] = +start[1] % 12;
        }
    }
    if (+end[1] >= 12) {
        endAMPM = 'PM'
        if (+end[1] > 12) {
            end[1] = +end[1] % 12;
        }
    }
    startString = `${start[1].toString().padStart(2, '0')}:${start[2]}${startAMPM}`;
    endString = `${end[1].toString().padStart(2, '0')}:${end[2]}${endAMPM}`;
    return startString + ' - ' + endString;
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

/*
*   Creates and displays a custom alert using bootstrap classes. 
*/
export function createAlert(alertClass = 'alert-primary', headText, bodyText, minor=false) {
    let alertBox = document.createElement('div');
    alertBox.className = `alert ${alertClass}`;
    if (minor) {
        clearMinorAlerts();
        alertBox.id = 'alert-box-minor';
        alertBox.className += ' alert-minor';
    } else {
        clearMajorAlerts();
        alertBox.id = 'alert-box-major';
        alertBox.className += ' alert-major';
    }
    alertBox.setAttribute('role', 'alert');
    alertBox.style.display = 'none';
    if (headText) {
        let head;
        if (minor) {
            head = document.createElement('h5');
        } else {
            head = document.createElement('h4');
        }
        head.id = 'alert-box-heading';
        head.className = 'alert-heading';
        head.innerHTML = headText;
        alertBox.appendChild(head);
    }
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
    
    alertBox.appendChild(body);
    alertBox.appendChild(btn);
    signupHolder.prepend(alertBox);
    $(alertBox).animate({width: 'toggle'}).delay(30000).animate({width: 'toggle'});
}
