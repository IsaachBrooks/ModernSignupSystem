import { getDepartmentNamesIDs } from "./databaseAccess.js";

function setOptions() {
    const dSel = $('#degree-selector');
    let response = getDepartmentNamesIDs();
    response.then((data) => {
        for (let dept of data) {
            let entry = dept.name.split('Department of ')[1]
            let id = dept.dpID;
            let opt = document.createElement('option')
            opt.innerHTML = entry;
            opt.value = id;
            dSel.append(opt);
            console.log(entry, id);
        }
    });
}

setOptions();