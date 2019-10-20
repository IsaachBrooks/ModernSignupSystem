function drawGrid() {
    const width = screen.width;
    const gridCanvas = document.createElement('canvas');
    const signupMain = document.getElementById('signup-main');
    gridCanvas.id = 'signup-grid-canvas';
    gridCanvas.width = width;
    gridCanvas.height = '2400';
    const ctx = gridCanvas.getContext("2d");
    ctx.strokeStyle = "black";
    let hr = 8;
    ctx.scale(2, 2);
    ctx.font = "12px Arial";
    ctx.beginPath()
    for (let y = 40; y <= 2400; y+=85) {
        ctx.moveTo(0, y);
        ctx.lineTo(width * 2, y);
        if (hr > 13)
            ctx.fillText(`${hr.toString().padStart(0,2)}:00PM`, 2, y-3);
        else if (hr == 12) 
            ctx.fillText("12:00PM", 2, y-3);
        else 
            ctx.fillText(`${hr.toString().padStart(0,2)}:00AM`, 2, y-3);
        hr++;
    }
    /*
    //Far left Monday line
    ctx.moveTo(60, 0);
    ctx.lineTo(60, 2400);

    //Monday Tuesday seperator
    ctx.moveTo(214.4, 0);
    ctx.lineTo(214.4, 2400);

    //Tuesday Wednesday seperator
    ctx.moveTo(368.5, 0);
    ctx.lineTo(368.5, 2400);

    //Wednesday Thursday seperator
    ctx.moveTo(540, 0);
    ctx.lineTo(540, 2400);

    //Thursday Friday seperator
    ctx.moveTo(697.3, 0);
    ctx.lineTo(697.3, 2400);
    */

    ctx.stroke();

    ctx.beginPath();
    ctx.setLineDash([5]);
    for (let y = 85; y <= 2400; y+=85) {
        ctx.moveTo(30, y);
        ctx.lineTo(width * 2, y);
    }
    ctx.stroke();

    ctx.beginPath();
    
    signupMain.append(gridCanvas);
}

drawGrid();