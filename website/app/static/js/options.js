import { getDepartmentNamesIDs, getSectionsByDepartment, searchForSections, showLoading } from "./databaseAccess.js";
import { updateAllTimes } from "./drawTimes.js";

export default switchView;

const switchStr = [' Full View', ' Cur View'];
export let noOverlaps = false;
export let showCanTake = false;
export let hideCompleted = false;
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
    let SOL = document.getElementById('showOverlaps');
    SOL.onchange = () => {
        noOverlaps = SOL.checked;
        reloadSections();
    };
    let HC = document.getElementById('hideCompleted');
    HC.onchange = () => {
        hideCompleted = HC.checked;
        reloadSections();
    }

}

function reloadSections() {
    if (dSel.value) {
        showLoading();
        getSectionsByDepartment(dSel.value).then(data => {
            updateAllTimes(data);
        });
    }
}

export function switchView() {
    let vis = $("#curClasses-main").css('visibility');
    let sv = $("#switch-view");
    let fa = sv.children()[0];
    let span = sv.children()[1];

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
    $("#curClasses-main").css('visibility', $("#signup-main").css('visibility'));
    $("#signup-main").css('visibility', vis);
}

setupSubjectSelector();
setupSearchBar();
setupCheckBoxes();