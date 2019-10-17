import { getSectionTimesDaysFull, getSectionTimesDay } from './databaseAccess.js';

const weekdays = ['mon', 'tue', 'wed', 'thu', 'fri'];

function newTimeSlot(day, time, count, rgb, classes) {
    let dayElement = document.getElementById(`${day}-header`);
    let dayRect = dayElement.getBoundingClientRect();
    let newTime = document.createElement('div');

    let tStartHr = Math.floor((time[0] - 800) / 100);
    let tStartMin = (time[0] % 100) / 60;
    let tStart = tStartHr + tStartMin
    newTime.style.height = '75px';
    newTime.style.width = '100%';
    newTime.style.cssFloat = 'left';
    newTime.style.position = 'absolute';
    newTime.style.zIndex = `${time[0]}`;
    newTime.style.top = `${tStart * 85 + 40}px`;
    newTime.className = 'time-slot-holder';
    let r = rgb[0];
    let g = rgb[1];
    let b = rgb[2];
    let bgColor = "rgba(" + r + "," + g + "," + b + ", 1)";
    newTime.style.backgroundColor = bgColor;
    newTime.innerHTML = `<p>${day} ${time[0]} -- ${count} classes</p><p>${classes}</p>`
    //newTime.className = `time-slot-${time} ${day}-obj`;
    let dayHolder = document.getElementById(`${day}-holder`);
    dayHolder.appendChild(newTime); 
}

function drawTimesFull(times) {
    times.forEach( (data) => {
        let tStart = data.tStart;
        let tEnd = data.tEnd;
        let time = [tStart, tEnd];
        let count = data.count;
        let classes = data.cID;
        let rgb = [
            Math.floor(Math.random() * 128), 
            Math.floor(Math.random() * 128), 
            Math.floor(Math.random() * 128)
        ];
        for (let i = 0; i < 5; i++) {
            if (data.days[i]) {
                newTimeSlot(weekdays[i], time, count, rgb, classes);
            }
        }
    });
}


const sections = getSectionTimesDaysFull().then((data) => {

    drawTimesFull(data);

});


