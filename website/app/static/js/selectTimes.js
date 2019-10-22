import { getSectionsInfo, getClassInfoMinimal, getSectionInfo } from "./databaseAccess.js";


export default drawSelected;

const selectListHolder = $('#selected-holder');
const siHeader = $('.si-header');
const siTime = $('.si-time');
const siDays = $('.si-days');
const siDate = $('.si-date');
const siExtra = $('.si-extra');
const siInstructor = $('.si-instructor');
const siDesc = $('.si-description');



export function drawSelected(selectedCRNs) {
    selectListHolder.empty();
    const sections = getSectionsInfo(selectedCRNs).then((data) => {
        data.forEach((elem) => {
            const curClass = getClassInfoMinimal(elem.cID).then((classData) => {
                let crn = elem.crn;
                let cName = classData.name;
                let dCode = classData.deptCode;
                let cNumber = classData.cNumber.toString()
                let cCodeNum =  dCode + cNumber;
                let sec = elem.sec;
                let sectLi = document.createElement('div');
                sectLi.className = 'selected-list-elem';
                sectLi.innerHTML = `${sec} ${cCodeNum} ${cName}`;
                sectLi.setAttribute('data-crn', crn);
                sectLi.setAttribute('data-dcode', dCode);
                sectLi.setAttribute('data-cnumber', cNumber);
                sectLi.setAttribute('data-cname', cName);
                selectListHolder.append(sectLi);
            });
        });
    });
}

export function updateSectionInfo(crn, dCode, cNumber, cName) {
    const sectionInfoHolder = $('#section-info-holder');
    const section = getSectionInfo(crn).then((sectData) => {
        let sec = sectData.sec;
        let tStart = sectData.tStart;
        let tEnd = sectData.tEnd;
        let days = sectData.days;
        let instructor = sectData.instructor;
        let dateStart = sectData.dateStart;
        let dateEnd = sectData.dateEnd;
        let capacity = sectData.capacity;
        let numCur = sectData.numCurEnrolled;
        let description = sectData.description;
        siHeader.html(`${crn} - Section ${sec} - ${cName} - ${dCode + cNumber}`);
        siTime.html(`Times: ${tStart} - ${tEnd}`);
        siDays.html(`Days: ${days}`);
        siDate.html(`${dateStart} - ${dateEnd}`);
        siInstructor.html(`Instructor: ${instructor.fname + ' ' + instructor.mname + ' ' + instructor.lname}`);
        siDesc.html(`${description}`);


    });
}