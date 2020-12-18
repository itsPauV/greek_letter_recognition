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

async function save() {
    // docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' greek_cnn_web_1
    const response = await fetch('http://localhost:8501/v1/models/exported_model:predict', {
        method: 'POST',
        body: JSON.stringify({"instances": getArray()}),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const myJson = await response.json();
    console.log(myJson);
}

function getArray() {
    var context = document.getElementById("can").getContext("2d");
    var imgd = context.getImageData(0, 0, canvas.width, canvas.height);
    var pix = imgd.data;
    var pixels = Array.from(Array(canvas.width), () => new Array(canvas.height));
    let alphaValue;
    let x_count = 0;
    let y_count = 0;
    for (let i = 3; i < pix.length; i += 4) {
        try {
            // console.log(`i: ${i}: [${y_count}|${x_count}] is valued: ${pix[i]}`);
            // 3 -> 7 -> 11 -> ... -> 102 (34th value)
            // 0 -> 4 -> 8 -> 12
            // 100*4 + 3 values pro Reihe
            // bei i=403 -> 99
            // bei i=256+3 -> 1|0
            alphaValue = pix[i];

            
            pixels[y_count][x_count] = new Array(1);
            pixels[y_count][x_count][0] = (alphaValue > 100) ? 0 : 1;
            if (x_count === 63) {
                x_count = 0;
                y_count++;
            } else {
                x_count++;
            }
        } catch (error) {
            console.log("error at i: " + i);
        }
    }
    pixels_shell = new Array(1);
    pixels_shell[0] = pixels;
    console.log(pixels_shell);
    return pixels_shell;
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