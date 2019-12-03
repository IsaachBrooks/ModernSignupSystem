const signupMain = document.getElementById('signup-main');
const curClassesMain = document.getElementById('curClasses-main');

function drawGrid() {
    const width = screen.width;
    const gridCanvas = document.createElement('canvas');
    gridCanvas.id = 'signup-grid-canvas';
    gridCanvas.width = width;
    gridCanvas.height = 2400;
    const ctx = gridCanvas.getContext("2d");
    ctx.strokeStyle = "black";
    let hr = 8;
    ctx.scale(2, 1.599);
    ctx.font = "12px Arial";
    ctx.beginPath()
    for (let y = 40; y <= 2800; y+= 90) { // y+= 90 because of pixel scaling factor of 1.5x   90 = 60 * 1.5
        ctx.moveTo(0, y);
        ctx.lineTo(width * 2, y);
        if (hr > 12)
            ctx.fillText(`${(hr-12).toString()}:00PM`, 2, y-3);
        else if (hr == 12) 
            ctx.fillText("12:00PM", 2, y-3);
        else 
            ctx.fillText(`${hr.toString()}:00AM`, 2, y-3);
        hr++;
    }

    ctx.stroke();

    ctx.beginPath();
    ctx.setLineDash([5]);
    for (let y = 85; y <= 2400; y+= 90) { // y+= 90 because of pixel scaling factor of 1.5x   90 = 60 * 1.5
        ctx.moveTo(30, y);
        ctx.lineTo(width * 2, y);
    }
    ctx.stroke();

    ctx.beginPath();
    return gridCanvas
}
$(() => {
grid1 = drawGrid();
grid2 = drawGrid();
signupMain.append(grid1);
curClassesMain.append(grid2);
})
