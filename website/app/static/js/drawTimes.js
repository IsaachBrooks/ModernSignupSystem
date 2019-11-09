import { getSectionTimesDaysFull, getStudentSectionsDraw } from './databaseAccess.js';

export default drawTimesFull;

const weekdays = ['mon', 'tue', 'wed', 'thu', 'fri'];
let allTimes = {};

let scaleFactor = 1.5;

function newTimeSlot(day, time, count, rgb, classes, crns, cNums, slot) {
    let dayElement = document.getElementById(`${slot}-${day}-header`);
    let dayHolder = document.getElementById(`${slot}-${day}-holder`);
    let dayRect = dayElement.getBoundingClientRect();
    let newTime = document.createElement('div');

    let tStartHr = Math.floor((time[0] - 800) / 100);
    let tStartMin = (time[0] % 100) / 60;
    let tStart = tStartHr + tStartMin;
    let len = getSectionLength(time[0], time[1]);
    newTime.className = `time-slot-holder ${slot}-slot`;
    newTime.style.height = `${1.5 * len}px`;
    newTime.style.zIndex = `${time[0]}`;
    newTime.style.top = `${tStart * (1.5 * 60) + 40}px`;
    let crnConcat;
    if (typeof crns == typeof []) {
        crnConcat = crns.reduce((accumulator, currentValue) => {
            return accumulator.toString() +',' + currentValue.toString();
        })
    } else {
        crnConcat = crns.toString();
    }
    newTime.setAttribute('data-crn', crnConcat);
    let r = rgb[0];
    let g = rgb[1];
    let b = rgb[2];
    let bgColor = "rgba(" + r + "," + g + "," + b + ", 1)";
    newTime.style.backgroundColor = bgColor;
    //newTime.innerHTML = `<p>${time[0]} - ${time[1]}<br>${count} Classes</p>`
    newTime.innerHTML = `
            <p class='time-slot-classes'>${cNums}</p>
            <p class='time-slot-time'>${timeConvert(time[0])} - ${timeConvert(time[1])}<p>`

    //Deals with multiple times within the same slot only in full list.
    if (slot === 'full') {
        if (!allTimes[`${day}-${time[0]}`]) {
            allTimes[`${day}-${time[0]}`] = [];
        } else {
            let existing = allTimes[`${day}-${time[0]}`];
            let numSects = existing.length + 1;
            let width = (100/numSects);
            newTime.style.width = `${width}%`;
            let widthOffset;
            let count = 0;
            existing.forEach((ex) => {
                ex.style.width = `${width}%`;
                if (!widthOffset) widthOffset = ex.clientWidth+2;
                ex.style.left = `${width * count++}%`;
            })
            newTime.style.left = `${width * count}%`;
        }
        allTimes[`${day}-${time[0]}`].push(newTime);
    }
    dayHolder.appendChild(newTime);
}

export function getSectionLength(tStart, tEnd) {
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
        let cNums = data.cNumbers
        let rgb = [
            Math.floor((tStart * 393181 * classes.reduce((a,b) => a+b) - 128) % 255), 
            Math.floor((tStart * 3187 * classes.reduce((a,b) => a+b) - 128) % 255), 
            Math.floor((tStart * 477 * classes.reduce((a,b) => a+b) - 128) % 255),
        ];
        for (let i = 0; i < 5; i++) {
            if (data.days[i]) {
                newTimeSlot(weekdays[i], time, count, rgb, classes, crns, cNums, 'full');
            }
        }
    });
}

export function drawCurTimes(times) {
    times.forEach( (data) => {
        let crn = data.crn;
        let tStart = data.tStart;
        let tEnd = data.tEnd;
        let time = [tStart, tEnd];
        let count = data.count;
        let classes = data.cID;
        let cNums = data.cNumbers
        let cShort = data.cShort
        let rgb = [
            Math.floor((tStart * 393181 * +cNums - 128) % 255), 
            Math.floor((tStart * 3187 * +cNums - 128) % 255), 
            Math.floor((tStart * 477 * +cNums - 128) % 255),
        ];
        for (let i = 0; i < 5; i++) {
            if (data.days[i]) {
                newTimeSlot(weekdays[i], time, count, rgb, classes, crn, cShort, 'cur');
            }
        }
    });
}

function timeConvert(time) {
    let hr = Math.floor(time / 100);
    let min = time % 100;
    let post = 'AM'
    if (hr >= 12) {
        post = 'PM'
    }
    if (hr > 12) {
        hr -= 12;
    }
    return `${hr.toString()}:${min.toString().padStart(2, '0')}${post}`
}

function emptyTimes(slot) {
    weekdays.forEach(day => {
        let dayElement = $(`#${slot}-${day}-header`);
        let dayHolder = $(`#${slot}-${day}-holder`);
        dayHolder.empty();
        dayHolder.append(dayElement);

    })
}

export function updateCurTimes() {
    const curSections = getStudentSectionsDraw().then((data) => {
        emptyTimes('cur');
        drawCurTimes(data);
    });
}

export function updateAllTimes(data) {
    allTimes = {};
    emptyTimes('full');
    drawTimesFull(data);
}

updateCurTimes();
