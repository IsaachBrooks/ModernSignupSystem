import { getDepartmentNamesIDs, getSectionsByDepartment } from "./databaseAccess.js";
import { updateAllTimes } from "./drawTimes.js";

function setOptions() {
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
            response = getSectionsByDepartment(dSel.value)
            response.then(data => {
                updateAllTimes(data);
            });
        }
    }
}

setOptions();