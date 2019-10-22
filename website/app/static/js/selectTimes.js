import { getSectionsInfo, getClassInfoMinimal, getSectionInfo, getClassInfo } from "./databaseAccess.js";

export default drawSelected;

const selectListHolder = $('#selected-holder');

const siHeader = $('.si-header');
const siTime = $('.si-time');
const siDays = $('.si-days');
const siDate = $('.si-date');
const siChrs = $('.si-chrs');
const siExtra = $('.si-extra');
const siInstructor = $('.si-instructor');
const siDesc = $('.si-description');



export function drawSelected(selectedCRNs) {
    if (selectListHolder.css('visibility') === 'hidden') {
        selectListHolder.css('visibility', 'unset');
    }
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
                sectLi.setAttribute('data-cid', elem.cID);
                selectListHolder.append(sectLi);
            });
        });
    });
}

export function updateSectionInfo(crn, cID) {
    const sectionInfoHolder = $('#section-info-holder');
    const section = getSectionInfo(crn).then((sectData) => {
        const cl = getClassInfo(cID).then((classData) => {

            $('#sec-info-content').data('crn', crn);
            //class data
            let cName = classData.name;
            let dCode = classData.dCode;
            let cNumber = classData.cNumber;
            let description = classData.description;
            let credHrs = classData.creditHours;
            let prereqs = classData.prereqs;
            let linkedClass = classData.linkedClass;
            let elective = classData.elective;
            let lab = classData.lab;
            //section data
            let sec = sectData.sec;
            let tStart = sectData.tStart;
            let tEnd = sectData.tEnd;
            let days = sectData.days;
            let instructor = sectData.instructor;
            let dateStart = sectData.dateStart;
            let dateEnd = sectData.dateEnd;
            let capacity = sectData.capacity;
            let numCur = sectData.numCurEnrolled;

            siHeader.html(`<span id="header-info">${crn} - Section ${sec} - ${cName} - ${dCode + cNumber.toString()}</span>`);
            siTime.html(`<span id="times-info">Times: ${tStart} - ${tEnd}</span>`);
            siDays.html(`<span id="days-info">Days: ${days}</span>`);
            siDate.html(`<span id="date-info">${dateStart} - ${dateEnd}</span>`);
            siInstructor.html(`<span id="description-info">Instructor: ${instructor.fname + ' ' + instructor.mname + ' ' + instructor.lname}</span>`);
            siDesc.html(`<p id="description-info">${description}</p>`);
            siChrs.html(`Credit Hrs: ${credHrs}`);
            let extraString = '<span id="extra-info">';
            extraString += `CRN: ${crn}<br>Section: ${sec}<br>Department: ${dCode}<br>Capacity: ${numCur}/${capacity}`;
            if (prereqs) {  
                extraString += '<br>Prereqs: [';
                for (let i = 0; i < prereqs.length; i++) {
                    extraString += `${prereqs[i].dCode + prereqs[i].cNumber.toString()}`;
                    if (i+1 < prereqs.length) {
                        extraString += ', ';
                    }
                }
                extraString += ']';
            }
            if (linkedClass & !lab) {
                extraString += `<br>Has Lab: Yes`;
            } else if (lab) {
                extraString += `<br>Is Lab Section for ${dCode + cNumber.toString()}`;
            }
            if (elective) {
                extraString += `<br>Is Elective: Yes`;
            }
            extraString += '</span>';
            siExtra.html(extraString);
        });
    });
}