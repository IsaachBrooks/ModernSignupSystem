import { getDepartmentNamesIDs, getSectionsByDepartment, searchForSections, showLoading } from "./databaseAccess.js";
import { updateAllTimes } from "./drawTimes.js";

export default switchView;

const switchStr = [' Full View', ' Cur View'];

function setupSubjectSelector() {
    const dSel = document.getElementById('subject-selector');
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
        if (dSel.value) {
            showLoading();
            response = getSectionsByDepartment(dSel.value)
            response.then(data => {
                updateAllTimes(data);
            });
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
                });
            }
        }
    });
}

export function switchView() {
    let vis = $("#curClasses-main").css('visibility');
    let sv = $("#switch-view");
    let fa = sv.children()[0];
    let span = sv.children()[1];

    if (span.innerHTML === switchStr[0]) {
        span.innerHTML = switchStr[1];
        fa.className = 'fa fa-arrow-circle-o-left'
    } else {
        span.innerHTML = switchStr[0];
        fa.className = 'fa fa-arrow-circle-o-right'
    }
    $("#curClasses-main").css('visibility', $("#signup-main").css('visibility'));
    $("#signup-main").css('visibility', vis);
}

setupSubjectSelector();
setupSearchBar();