import { getCurStudentSections, getClassInfoMinimal } from './databaseAccess.js'

export default showCurrentEnrolled;


export function showCurrentEnrolled() {
    const currentHolder = $('#current-holder');
    const currentListHolder = $('#current-list-holder');
    currentListHolder.empty();
    getCurStudentSections().then((data) => {
        if (data) {
            if (currentHolder.css('visibility') === 'hidden') {
                currentHolder.css('visibility', 'unset');
            }
            data.forEach((elem) => {
                getClassInfoMinimal(elem.cID).then((classData) => {
                    let crn = elem.crn;
                    let cName = classData.name;
                    let dCode = classData.deptCode;
                    let cNumber = classData.cNumber.toString()
                    let cCodeNum =  dCode + cNumber;
                    let sec = elem.sec;
                    let sectLi = document.createElement('div');
                    sectLi.className = 'current-list-elem list-elem';
                    sectLi.innerHTML = `${sec} ${cCodeNum} ${cName}`;
                    sectLi.setAttribute('data-crn', crn);
                    sectLi.setAttribute('data-cid', elem.cID);
                    currentListHolder.append(sectLi);
                });
            });
        }
    });
}