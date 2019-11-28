import { getSectionsInfoMinimal, getClassInfoMinimal, getSectionInfo, getClassInfo, isCurStudentRegisteredFor } from "./databaseAccess.js";

export default drawSelected;

const sectionInfo = $('.section-info-main');

export function drawSelected(selectedCRNs) {
    const selectHolder = $('#selected-holder');
    const selectListHolder =  $('#selected-list-holder');
    if (selectHolder.css('visibility') === 'hidden') {
        selectHolder.css('visibility', 'unset');
    }
    selectListHolder.empty();
    let count = 0;
    getSectionsInfoMinimal(selectedCRNs).then((data) => {
        for (let sect of data) {
            let crn = sect.crn;
            let cName = sect.cName;
            let cCodeNum =  sect.shortName;
            let sec = sect.sec;
            let sectLi = document.createElement('div');
            sectLi.className = 'selected-list-elem list-elem';
            sectLi.innerHTML = `${sec} ${cCodeNum} ${cName}`;
            sectLi.setAttribute('data-crn', crn);
            sectLi.setAttribute('data-cid', sect.cID);
            $(sectLi).css('display', 'none');
            selectListHolder.append(sectLi);
            $(sectLi).fadeIn(200 + count);
            count+=100;
        }
    });
}

export function updateSectionInfo(crn=$("#sec-info-content").data('crn'), cID=$("#sec-info-content").data('cid')) {
    const siHeader = $('.si-header');
    const siTime = $('.si-time');
    const siDays = $('.si-days');
    const siDate = $('.si-date');
    const siChrs = $('.si-chrs');
    const siExtra = $('.si-extra');
    const siInstructor = $('.si-instructor');
    const siDesc = $('.si-description');
    getSectionInfo(crn).then((sectData) => {
        getClassInfo(cID).then((classData) => {
            $('#sec-info-content').data('crn', crn);
            $('#sec-info-content').data('cid', cID);
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
    //If student is registered for section already, change view of unregister button
    isCurStudentRegisteredFor(crn).then((data) => {
        const unregister = $('#section-info-unregister');
        const register = $('#section-info-register');
        if (data.result) {
            unregister.addClass('btn-danger');
            unregister.removeClass('btn-dark');
            unregister.attr('disabled', false);
            register.removeClass('btn-success');
            register.addClass('btn-dark');
            register.attr('disabled', true);
        } else {
            unregister.removeClass('btn-danger');
            unregister.addClass('btn-dark');
            unregister.attr('disabled', true);
            register.addClass('btn-success');
            register.removeClass('btn-dark');
            register.attr('disabled', false);
        }
    });
}

export function showSectionInfo() {
    sectionInfo.css('visibility', 'visible');
}
export function hideSectionInfo() {
    sectionInfo.css('visibility', 'hidden');   
}