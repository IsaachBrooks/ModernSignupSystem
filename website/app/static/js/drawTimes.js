import { getSectionTimesDaysFull, getSectionTimesDay } from './databaseAccess.js';

const weekdays = ['mon', 'tue', 'wed', 'thu', 'fri'];
const allTimes = {};

let scaleFactor = 1.5;

function newTimeSlot(day, time, count, rgb, classes, crns) {
    let dayElement = document.getElementById(`${day}-header`);
    let dayRect = dayElement.getBoundingClientRect();
    let newTime = document.createElement('div');
    let dayHolder = document.getElementById(`${day}-holder`);

    let tStartHr = Math.floor((time[0] - 800) / 100);
    let tStartMin = (time[0] % 100) / 60;
    let tStart = tStartHr + tStartMin;
    let len = getSectionLength(time[0], time[1]);
    newTime.className = 'time-slot-holder';
    newTime.style.height = `${1.5 * len}px`;
    newTime.style.zIndex = `${time[0]}`;
    newTime.style.top = `${tStart * (1.5 * 60) + 40}px`;
    let crnConcat = crns.reduce((accumulator, currentValue) => {
        return accumulator.toString() +',' + currentValue.toString();
    })
    newTime.setAttribute('data-crn', crnConcat);
    let r = rgb[0];
    let g = rgb[1];
    let b = rgb[2];
    let bgColor = "rgba(" + r + "," + g + "," + b + ", 1)";
    newTime.style.backgroundColor = bgColor;
    newTime.innerHTML = `<p>${time[0]} - ${time[1]}<br>${count} Classes</p>`


    //Deals with multiple times within the same slot.
    if (!allTimes[`${day}-${time[0]}`]) {
        allTimes[`${day}-${time[0]}`] = [];
    } else {
        let existing = allTimes[`${day}-${time[0]}`];
        let numSects = existing.length + 1;
        let width = Math.floor(100/numSects);
        newTime.style.width = `${width}%`;
        let widthOffset;
        let count = 0;
        existing.forEach((ex) => {
            ex.style.width = `${width}%`;
            if (!widthOffset) widthOffset = ex.clientWidth+2;
            ex.style.left = `${widthOffset * count++}px`;
        })
        newTime.style.left = `${widthOffset * count}px`;
    }
    allTimes[`${day}-${time[0]}`].push(newTime);

    dayHolder.appendChild(newTime);
}

//unused
function getSectionLength(tStart, tEnd) {
    let tStartHr = Math.floor(tStart / 100);
    let tStartMin = tStart % 100;
    let tEndHr = Math.floor(tEnd / 100);
    let tEndMin = tEnd % 100;
    let d1 = new Date(0, 0, 0, tStartHr, tStartMin, 0);
    let d2 = new Date(0, 0, 0, tEndHr, tEndMin, 0);
    return ((d2 - d1)/1000)/60
}

export function drawTimesFull(times) {
    times.forEach( (data) => {
        let crns = data.crn;
        let tStart = data.tStart;
        let tEnd = data.tEnd;
        let time = [tStart, tEnd];
        let count = data.count;
        let classes = data.cID;
        let rgb = [
            Math.floor((tStart * 393181 * crns.reduce((a,b) => a+b) - 128) % 255), 
            Math.floor((tStart * 3187 * crns.reduce((a,b) => a+b) - 128) % 255), 
            Math.floor((tStart * 477 * crns.reduce((a,b) => a+b) - 128) % 255),
        ];
        for (let i = 0; i < 5; i++) {
            if (data.days[i]) {
                newTimeSlot(weekdays[i], time, count, rgb, classes, crns);
            }
        }
    });
}




const sections = getSectionTimesDaysFull().then((data) => {

    drawTimesFull(data);

});

