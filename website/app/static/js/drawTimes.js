import { getSectionTimesDaysFull, getSectionTimesDay } from './databaseAccess.js';

const weekdays = ['mon', 'tue', 'wed', 'thu', 'fri'];

function newTimeSlot(day, time, count, rgb, classes, crns) {
    let dayElement = document.getElementById(`${day}-header`);
    let dayRect = dayElement.getBoundingClientRect();
    let newTime = document.createElement('div');

    let tStartHr = Math.floor((time[0] - 800) / 100);
    let tStartMin = (time[0] % 100) / 60;
    let tStart = tStartHr + tStartMin
    newTime.className = 'time-slot-holder';
    newTime.style.height = '75px';
    newTime.style.zIndex = `${time[0]}`;
    newTime.style.top = `${tStart * 85 + 40}px`;
    let crnConcat = crns.reduce((accumulator, currentValue) => {
        return accumulator.toString() +',' + currentValue.toString();
    })
    newTime.setAttribute('data-crn', crnConcat);
    let r = rgb[0];
    let g = rgb[1];
    let b = rgb[2];
    let bgColor = "rgba(" + r + "," + g + "," + b + ", 0.65)";
    newTime.style.backgroundColor = bgColor;
    newTime.innerHTML = `<p>${time[0]} - ${time[1]}<br>${count} classes<br>${classes}</p>`
    //newTime.className = `time-slot-${time} ${day}-obj`;
    let dayHolder = document.getElementById(`${day}-holder`);
    dayHolder.appendChild(newTime); 
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

function getSectionLength(tStart, tEnd) {
    //TODO:
}


const sections = getSectionTimesDaysFull().then((data) => {

    drawTimesFull(data);

});

