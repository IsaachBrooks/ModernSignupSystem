import { getCurStudentSectionsMinimal } from './databaseAccess.js'
import { pickColor } from './drawTimes.js';

export default showCurrentEnrolled;


export function showCurrentEnrolled() {
    const currentHolder = $('#current-holder');
    const currentListHolder = $('#current-list-holder');
    currentListHolder.empty();
    getCurStudentSectionsMinimal().then((data) => {
        if (data) {
            if (currentHolder.css('visibility') === 'hidden') {
                currentHolder.css('visibility', 'unset');
            }
            data.sort((a,b) => {return (a.cID - b.cID);})
            for (let elem of data) {
                    let crn = elem.crn;
                    let sec = elem.sec;
                    let cNum = elem.cNumber;
                    let cName = elem.name;
                    let cShortName =  elem.shortName;
                    let sectLi = document.createElement('div');
                    let rgb = pickColor(cNum);
                    let bgColor = "rgba(" + rgb[0] + "," + rgb[1] + "," + rgb[2] + ", 1)";
                    sectLi.className = 'current-list-elem list-elem';
                    sectLi.innerHTML = `${sec} ${cShortName} ${cName}`;
                    sectLi.setAttribute('data-crn', crn);
                    sectLi.setAttribute('data-cid', elem.cID);
                    sectLi.style.backgroundColor = bgColor;
                    currentListHolder.append(sectLi);
            };
        }
    });
}
