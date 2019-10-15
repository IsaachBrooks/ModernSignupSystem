function newTimeSlot(day, time) {
    let dayElement = document.getElementsByClassName('day-header')[0];
    let dayRect = dayElement.getBoundingClientRect();
    console.log(dayRect);
    let newTime = document.createElement('div');
    newTime.style.height = '75px';
    newTime.style.width = '100%';
    newTime.style.cssFloat = 'left';
    //newTime.style.top = `${time % 8 * 75}px`;
    let r = Math.floor(Math.random() * 128);
    let g = Math.floor(Math.random() * 128);
    let b = Math.floor(Math.random() * 128);
    let bgColor = "rgba(" + r + "," + g + "," + b + ", 0.5)";
    newTime.style.backgroundColor = bgColor;

    //newTime.className = `time-slot-${time} ${day}-obj`;
    let dayHolder = document.getElementById(`${day}-holder`);
    dayHolder.appendChild(newTime); 
}

newTimeSlot('mon', '9');
newTimeSlot('mon', '10');
newTimeSlot('mon', '11');
newTimeSlot('mon', '12');
newTimeSlot('mon', '13');
newTimeSlot('mon', '14');
