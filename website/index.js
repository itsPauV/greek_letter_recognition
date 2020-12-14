var canvas, ctx, flag = false,
    prevX = 0,
    currX = 0,
    prevY = 0,
    currY = 0,
    dot_flag = false,
    scale = 0.1;

var x = "black",
    y = 2;

function init() {
    canvas = document.getElementById('can');
    ctx = canvas.getContext("2d");
    canvas.width = 640 * scale;
    canvas.height = 640 * scale;
    w = canvas.width;
    h = canvas.height;
    console.log(w + " " + h);

    canvas.addEventListener("mousemove", function (e) {
        findxy('move', e)
    }, false);
    canvas.addEventListener("mousedown", function (e) {
        findxy('down', e)
    }, false);
    canvas.addEventListener("mouseup", function (e) {
        findxy('up', e)
    }, false);
    canvas.addEventListener("mouseout", function (e) {
        findxy('out', e)
    }, false);
}

function draw() {
    ctx.beginPath();
    ctx.moveTo(prevX, prevY);
    ctx.lineTo(currX, currY);
    ctx.strokeStyle = x;
    ctx.lineWidth = y;
    ctx.stroke();
    ctx.closePath();
}

function erase() {
    var m = confirm("Want to clear");
    if (m) {
        ctx.clearRect(0, 0, w, h);
        document.getElementById("canvasimg").style.display = "none";
    }
}

function save() {
    var context = document.getElementById("can").getContext("2d");
    var imgd = context.getImageData(0, 0, canvas.width, canvas.height);
    var pix = imgd.data;
    var pixels = Array.from(Array(canvas.width), () => new Array(canvas.height));
    for (var i=3; i<pix.length; i+=4) {
        try {
            // console.log(`i: ${i}: [${Math.floor(i/(canvas.width*4+3))}|${((i-3)%(canvas.width*4))/4}] is valued: ${pix[i]}`);
            // 3 -> 7 -> 11 -> ... -> 102 (34th value)
            // 0 -> 4 -> 8 -> 12
            // 100*4 + 3 values pro Reihe
            // bei i=403 -> 99
            alphaValue = pix[i];
            if (alphaValue > 100) {
                pixels[Math.floor(i/(canvas.width*4+3))][((i-3)%(canvas.width*4))/4] = 255;
            } else {
                pixels[Math.floor(i/(canvas.width*4+3))][((i-3)%(canvas.width*4))/4] = 0;
            }
        } catch (error) {
            console.log("error at i: " + i);
        }
    }
    console.log(pixels);
}

function findxy(res, e) {
    if (res == 'down') {
        prevX = currX;
        prevY = currY;
        currX = (e.clientX - canvas.offsetLeft)*scale;
        currY = (e.clientY - canvas.offsetTop)*scale;

        flag = true;
        dot_flag = true;
        if (dot_flag) {
            ctx.beginPath();
            ctx.fillStyle = x;
            ctx.fillRect(currX, currY, 2, 2);
            ctx.closePath();
            dot_flag = false;
        }
    }
    if (res == 'up' || res == "out") {
        flag = false;
    }
    if (res == 'move') {
        if (flag) {
            prevX = currX;
            prevY = currY;
            currX = (e.clientX - canvas.offsetLeft)*scale;
            currY = (e.clientY - canvas.offsetTop)*scale;
            draw();
        }
    }
}