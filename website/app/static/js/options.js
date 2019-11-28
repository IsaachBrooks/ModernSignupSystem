import { getDepartmentNamesIDs, getSectionsByDepartment, searchForSections, showLoading } from "./databaseAccess.js";
import { updateAllTimes } from "./drawTimes.js";
import { hideSectionInfo } from "./selectTimes.js";

export default switchView;

const switchStr = [' Full View', ' Cur View'];
export let noOverlaps = false;
export let showCanTake = false;
export let hideCompleted = false;
export let hideCurrent = false;
export let viewing_full = true;
export let viewing_cur = false;

const dSel = document.getElementById('subject-selector');

function setupSubjectSelector() {
    let response = getDepartmentNamesIDs();
    response.then((data) => {
        for (let dept of data) {
            let entry = dept.name.split('Department of ')[1]
            let id = dept.dpID;
            let opt = document.createElement('option')
            opt.innerHTML = entry;
            opt.value = id;
            dSel.appendChild(opt);
        }
    });
    dSel.onchange = () => {
        reloadSections();
        if (viewing_cur) {
            switchView();
        }
    }
}

function setupSearchBar() {
    let sBar = $('#opt-search-input');
    $('#opt-search-btn').on({
        click: function() {
            if (sBar.val()) {
                showLoading();
                searchForSections(sBar.val()).then((data) => {
                    updateAllTimes(data);
                    if (viewing_cur) {
                        switchView();
                    }
                    sBar.val('');
                });
            }
        }
    })
    sBar.keypress(function(event) {
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
            if (sBar.val()) {
                showLoading();
                searchForSections(sBar.val()).then((data) => {
                    updateAllTimes(data);
                    if (viewing_cur) {
                        switchView();
                    }
                });
                sBar.val('');
            }
        }
    });
}

function setupCheckBoxes() {
    let SCT = document.getElementById('showCanTake');
    SCT.onchange = () => {
        showCanTake = SCT.checked;
        reloadSections();
    };
    let NOL = document.getElementById('showOverlaps');
    NOL.onchange = () => {
        noOverlaps = NOL.checked;
        reloadSections();
    };
    let HCom = document.getElementById('hideCompleted');
    HCom.onchange = () => {
        hideCompleted = HCom.checked;
        reloadSections();
    }
    let HCur = document.getElementById('hideCurrent');
    HCur.onchange = () => {
        hideCurrent = HCur.checked;
        reloadSections();
    }

    //Check for existing values from cache
    showCanTake = SCT.checked;
    noOverlaps = NOL.checked;
    hideCompleted = HCom.checked;
    hideCurrent = HCur.checked;
}

export function reloadSections() {
    if (dSel.value) {
        showLoading();
        getSectionsByDepartment(dSel.value).then(data => {
            updateAllTimes(data);
        });
    }
}

/*
*   Switch view between current classes and full view
*/
function setupSwitchView() {
    $("#switch-view").on({
        click: function() {
            switchView();
        }
    });
}

/*
*   Switch view between current classes and all loaded sections
*/
export function switchView() {
    let sv = $("#switch-view");
    let fa = sv.children()[0];
    let span = sv.children()[1];
    let scroll = 0;
    if (span.innerHTML === switchStr[0]) {
        span.innerHTML = switchStr[1];
        fa.className = 'fa fa-arrow-circle-o-left'
        viewing_cur = false;
        viewing_full = true;
    } else {
        span.innerHTML = switchStr[0];
        fa.className = 'fa fa-arrow-circle-o-right'
        viewing_cur = true;
        viewing_full = false;
    }
    if (viewing_cur) {
        scroll = $("#signup-main").scrollTop();
    } else {
        scroll = $("#curClasses-main").scrollTop();
    }
    hideSectionInfo();
    $("#curClasses-main").fadeToggle(300);
    $("#signup-main").fadeToggle(300);

    //Set scrolling to be the same
    $("#curClasses-main").scrollTop(scroll);
    $("#signup-main").scrollTop(scroll);
}

$(
    setupSwitchView(),
    setupSubjectSelector(),
    setupSearchBar(),
    setupCheckBoxes()
);