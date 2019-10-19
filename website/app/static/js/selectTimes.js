import { getSectionsInfo, getClassInfoMinimal } from "./databaseAccess.js";


export default drawSelected;

const selectListHolder = $('#selected-list-holder');
export function drawSelected(selectedCRNs) {
    selectListHolder.empty();
    const sections = getSectionsInfo(selectedCRNs).then((data) => {
        data.forEach((elem) => {
            const curClass = getClassInfoMinimal(elem.cID).then((classData) => {
                let crn = elem.crn;
                let cName = classData.name;
                let cCodeNum = classData.deptCode + classData.cNumber.toString();
                let sec = elem.sec;
                let sectLi = document.createElement('li');
                sectLi.className = 'selected-list-elem';
                sectLi.innerHTML = `${sec} ${cCodeNum} ${cName}`;
                selectListHolder.append(sectLi);
            });
        });
    });
}