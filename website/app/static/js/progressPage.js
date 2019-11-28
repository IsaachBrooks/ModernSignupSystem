import { getStudentCompleted } from "./databaseAccess.js";


const passedSpan = '<span class="text-center"><i class="fa fa-check text-success"></i></span>'
const failedSpan = '<span class="text-center"><i class="fa fa-check text-danger"></i></span>'

function drawTaken() {
    const table = $('#classes-taken');
    getStudentCompleted().then((data) => {
        if (data)
            for (let entry of data) {
                let cla = entry.classTaken;
                let pass = failedSpan;
                if (entry.passed) {
                    pass = passedSpan;
                }
                let row = 
                `<tr>
                    <td>${cla.dCode}</td>
                    <td>${cla.cNumber}</td>
                    <td>${cla.name}</td>
                    <td>${cla.creditHours}</td>
                    <td>${pass}</td>
                    <td>${entry.grade}</td>
                </tr>`
                table.append(row);
            }
    })
}

$(

    drawTaken()

);
