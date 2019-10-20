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
    for (let y = 40; y <= 2800; y+=85) {
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
    for (let y = 85; y <= 2400; y+=85) {
        ctx.moveTo(30, y);
        ctx.lineTo(width * 2, y);
    }
    ctx.stroke();

    ctx.beginPath();
    
    signupMain.append(gridCanvas);
}

drawGrid();