import { getSectionsInformation, getClassInformation } from "./databaseAccess.js";


export default drawSelected;

const selectHolder = $('#selected-list-holder');
export function drawSelected(selectedCRNs) {
    selectHolder.empty();
    const sections = getSectionsInformation(selectedCRNs).then((data) => {
        data.forEach((elem) => {
            const curClass = getClassInformation(elem.cID).then((classData) => {
                let crn = elem.crn;
                let className = classData.name;
                let credHrs = classData.creditHours;
                let instructor = `${elem.instructor.fname} ${elem.instructor.mname} ${elem.instructor.lname}`;
                let sec = elem.sec;
                selectHolder.append(`<li class="selected-list-elem">${crn}, ${sec}, ${credHrs}hrs, ${className}, ${instructor} </li>`);
            });
        });
    });
}