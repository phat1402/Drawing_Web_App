var drawingApp = (function() {





    "use strict";

    var
        canvas,
        context,
        canvaso,
        contexto,
        canvasWidth = 1024,
        canvasHeight = 600,
        coloringPic = new Image(),
        loadedIMG = new Image(),
        locationFixX = -50,
        locationFixY = -120,
        i,
        paint = false,
        curColor = "rgb(0, 0, 255)",
        curTool = "pen",
        curSize = 19,
        drawingAreaX = 0,
        drawingAreaY = 0,
        drawingAreaWidth = 1024,
        drawingAreaHeight = 600,
        totalLoadResources = 2,
        curLoadResNum = 0,
        curHexColor = "0000ff",
        curColorR = 0,
        curColorG = 0,
        curColorB = 255,
        size_select,
        undo_button,
        clear_button,
        save_button,
        imgURL,
        saveInt = 0,
        x0,
        y0,
        colorRGB,
        colorLayerData,
        outlineLayerData,
        saveImageToServer,
        undoData = [],
        undoImg = new Image(),
        changeColoringImage = function(imgFile) {
            for (i = 1; i < undoData.length; i++) {
                undoData.pop();
            }
            clearCanvasO();
            clearCanvas();
            coloringPic.src = imgFile;
            outlineCreate();
        },

        saveToServerFunction = function() {
            document.getElementById("data").value = imgURL;
            console.log(imgURL);
        },
        cutHex = function(h) {
            return (h.charAt(0) === "#") ? h.substring(1, 7) : h;
        },
        hexToRGB = function(h) {
            curColorR = parseInt((cutHex(h)).substring(0, 2), 16);
            curColorG = parseInt((cutHex(h)).substring(2, 4), 16);
            curColorB = parseInt((cutHex(h)).substring(4, 6), 16);
        },
        toHex = function(n) {
            var hex = n.toString(16);
            return hex.length == 1 ? "0" + hex : hex;
        },
        RGBToHex = function(r, g, b) {
            return "#" + toHex(r) + toHex(g) + toHex(b);
        },
        changeToBrush = function() {
            curTool = "pen";
            document.getElementById("toolImage").src = "static/DrawingTool/images/brush.png";
        },
        changeToEraser = function() {
            curTool = "eraser";
            document.getElementById("toolImage").src = "static/DrawingTool/images/eraser.png";
        },
        changeToRectangle = function() {
            curTool = "rect";
            document.getElementById("toolImage").src = "static/DrawingTool/images/rectangle.png";
        },
        changeToLine = function() {
            curTool = "line";
            document.getElementById("toolImage").src = "static/DrawingTool/images/line.png";
        },
        changeToBucket = function() {
            curTool = "bucket";
            document.getElementById("toolImage").src = "static/DrawingTool/images/bucket.png";
        },
        changeToEyedrop = function() {
            curTool = "eyedrop";
            document.getElementById("toolImage").src = "static/DrawingTool/images/eyedrop.png";
        },
        changeToTriangle = function() {
            curTool = "triangle";
            document.getElementById("toolImage").src = "static/DrawingTool/images/triangle.png";
        },
        changeToCircle = function() {
            curTool = "circle";
            document.getElementById("toolImage").src = "static/DrawingTool/images/circle.png";
        },
        ev_color_change = function(e) {
            curColor = this.value;
            colorRGB = hexToRgb(curHexColor);
        },
        ev_size_change = function(e) {
            curSize = this.value / 3;
        },
        drawImg = function() {

        },
        undoAction = function() {
            contexto.clearRect(0, 0, canvasWidth, canvasHeight);
            contexto.drawImage(undoImg, 0, 0, canvasWidth, canvasHeight);
            imgURL = canvaso.toDataURL("image/png");


            if (undoData.length > 1) {
                undoData.pop();
            }

            if (undoData.length > 1) {
                undoImg.src = undoData[undoData.length - 2];
            } else {
                undoImg.src = undoData[0];
                contexto.fillStyle = "#ffffff";
                outlineCreate();
                contexto.fillRect(0, 0, canvasWidth, canvasHeight);
            }



        },
        clearCanvas = function() {

            context.clearRect(0, 0, canvasWidth, canvasHeight);
        },
        clearCanvasO = function() {
            contexto.clearRect(0, 0, canvasWidth, canvasHeight);
            contexto.fillStyle = "#ffffff";
            contexto.fillRect(0, 0, canvasWidth, canvasHeight);
            outlineCreate();
        },
        img_update = function() {
            contexto.drawImage(canvas, 0, 0);
            context.clearRect(0, 0, canvasWidth, canvasHeight);
            outlineLayerData = contexto.getImageData(0, 0, canvasWidth, canvasHeight);
            colorLayerData = contexto.getImageData(0, 0, canvasWidth, canvasHeight);
        },
        outlineCreate = function() {
            context.drawImage(coloringPic, drawingAreaX, drawingAreaY, drawingAreaWidth, drawingAreaHeight);

        },
        matchOutlineColor = function(r, g, b, a) {

            return (r + g + b < 5 && a === 255);
        },
        matchStartColor = function(pixelPos, startR, startG, startB) {
            var r = outlineLayerData.data[pixelPos],
                g = outlineLayerData.data[pixelPos + 1],
                b = outlineLayerData.data[pixelPos + 2],
                a = outlineLayerData.data[pixelPos + 3];
            //alert(r + g + b);
            // If current pixel of the outline image is black
            if (matchOutlineColor(r, g, b, a)) {
                return false;
            }

            r = colorLayerData.data[pixelPos];
            g = colorLayerData.data[pixelPos + 1];
            b = colorLayerData.data[pixelPos + 2];

            // If the current pixel matches the clicked color
            if (r === startR && g === startG && b === startB) {
                return true;
            }

            // If current pixel matches the new color
            if (r === curColorR && g === curColorG && b === curColorB) {
                return false;
            }

            return (Math.abs(r - startR) + Math.abs(g - startG) + Math.abs(b - startB) < 255);
        },
        colorPixel = function(pixelPos, r, g, b, a) {

            colorLayerData.data[pixelPos] = r;
            colorLayerData.data[pixelPos + 1] = g;
            colorLayerData.data[pixelPos + 2] = b;
            colorLayerData.data[pixelPos + 3] = 255;
        },
        floodFill = function(startX, startY, startR, startG, startB) {

            var newPos,
                x,
                y,
                pixelPos,
                reachLeft,
                reachRight,
                drawingBoundLeft = drawingAreaX,
                drawingBoundTop = drawingAreaY,
                drawingBoundRight = drawingAreaX + drawingAreaWidth - 1,
                drawingBoundBottom = drawingAreaY + drawingAreaHeight - 1,
                pixelStack = [
                    [startX, startY]
                ];

            while (pixelStack.length) {
                newPos = pixelStack.pop();
                x = newPos[0];
                y = newPos[1];

                // Get current pixel position
                pixelPos = (y * canvasWidth + x) * 4;

                // Go up as long as the color matches and are inside the canvas
                while (y >= drawingBoundTop && matchStartColor(pixelPos, startR, startG, startB)) {
                    y--;
                    pixelPos -= canvasWidth * 4;
                }

                pixelPos += canvasWidth * 4;
                y += 1;
                reachLeft = false;
                reachRight = false;

                // Go down as long as the color matches and in inside the canvas
                while (y <= drawingBoundBottom && matchStartColor(pixelPos, startR, startG, startB)) {
                    y++;

                    colorPixel(pixelPos, curColorR, curColorG, curColorB);

                    if (x > drawingBoundLeft) {
                        if (matchStartColor(pixelPos - 4, startR, startG, startB)) {
                            if (!reachLeft) {
                                // Add pixel to stack
                                pixelStack.push([x - 1, y]);
                                reachLeft = true;
                            }
                        } else if (reachLeft) {
                            reachLeft = false;
                        }
                    }

                    if (x < drawingBoundRight) {
                        if (matchStartColor(pixelPos + 4, startR, startG, startB)) {
                            if (!reachRight) {
                                // Add pixel to stack
                                pixelStack.push([x + 1, y]);
                                reachRight = true;
                            }
                        } else if (reachRight) {
                            reachRight = false;
                        }
                    }

                    pixelPos += canvasWidth * 4;
                }
            }
        },
        // Start painting with paint bucket tool starting from pixel specified by startX and startY
        paintAt = function(startX, startY) {

            var pixelPos = (startY * canvasWidth + startX) * 4,
                r = colorLayerData.data[pixelPos],
                g = colorLayerData.data[pixelPos + 1],
                b = colorLayerData.data[pixelPos + 2],
                a = colorLayerData.data[pixelPos + 3];

            if (r === curColorR && g === curColorG && b === curColorB) {
                // Return because trying to fill with the same color
                return;
            }



            floodFill(startX, startY, r, g, b);
        },
        createUserEvents = function() {

            var press = function(e) {;
                    var radius,
                        mouseX,
                        mouseY;

                    mouseX = e.pageX + locationFixX;
                    mouseY = e.pageY + locationFixY;

                    if (curTool === "bucket") {
                        img_update();
                        colorLayerData = contexto.getImageData(0, 0, canvasWidth, canvasHeight);

                        paintAt(mouseX, mouseY);
                        context.putImageData(colorLayerData, 0, 0);
                        img_update();

                    }

                    if (curTool !== "bucket") {
                        paint = true;

                        if (curTool === "eyedrop") {
                            colorLayerData = contexto.getImageData(0, 0, canvasWidth, canvasHeight);
                            var pixelPos = (mouseY * canvasWidth + mouseX) * 4,
                                r = colorLayerData.data[pixelPos],
                                g = colorLayerData.data[pixelPos + 1],
                                b = colorLayerData.data[pixelPos + 2],
                                a = colorLayerData.data[pixelPos + 3];

                            curColorR = r;
                            curColorG = g;
                            curColorB = b;

                            curColor = RGBToHex(r, g, b);
                            $('#color').css('background-color', curColor);
                        }

                        radius = curSize;



                        context.lineCap = "round";
                        context.lineJoin = "round";
                        context.lineWidth = radius;

                        if (curTool === "eraser") {
                            context.strokeStyle = 'white';
                        } else {
                            context.strokeStyle = curColor;
                        }


                        if (curTool === "pen" || curTool === "eraser") {
                            context.beginPath();
                            context.moveTo(mouseX, mouseY);
                        }

                        x0 = mouseX;
                        y0 = mouseY;

                        outlineCreate();
                    }
                },
                drag = function(e) {

                    var mouseX;
                    var mouseY;

                    mouseX = e.pageX + locationFixX;
                    mouseY = e.pageY + locationFixY;



                    if (paint) {

                        if (curTool === "eyedrop") {
                            colorLayerData = contexto.getImageData(0, 0, canvasWidth, canvasHeight);
                            var pixelPos = (mouseY * canvasWidth + mouseX) * 4,
                                r = colorLayerData.data[pixelPos],
                                g = colorLayerData.data[pixelPos + 1],
                                b = colorLayerData.data[pixelPos + 2],
                                a = colorLayerData.data[pixelPos + 3];
                            curColorR = r;
                            curColorG = g;
                            curColorB = b;
                            curColor = RGBToHex(r, g, b);
                            $('#color').css('background-color', curColor);
                        }

                        if (curTool === "pen" || curTool === "eraser") {
                            context.lineTo(mouseX, mouseY);

                        } else if (curTool === "rect") {
                            var x = Math.min(mouseX, x0),
                                y = Math.min(mouseY, y0),
                                w = Math.abs(mouseX - x0),
                                h = Math.abs(mouseY - y0);

                            clearCanvas();

                            if (!w || !h) {
                                return;
                            }

                            context.strokeRect(x, y, w, h);
                        } else if (curTool === "circle") {
                            var
                                w = Math.abs(mouseX - x0),
                                h = Math.abs(mouseY - y0);

                            clearCanvas();

                            if (!w || !h) {
                                return;
                            }
                            context.beginPath();
                            context.ellipse((x0 + mouseX) / 2, (y0 + mouseY) / 2, w / 2, h / 2, 0, 0, 360);
                        } else if (curTool === "triangle") {
                            var x = Math.min(mouseX, x0),
                                y = Math.min(mouseY, y0),
                                w = Math.abs(mouseX - x0),
                                h = Math.abs(mouseY - y0);

                            clearCanvas();

                            if (!w || !h) {
                                return;
                            }
                            if (x0 < mouseX) {
                                context.beginPath();
                                context.moveTo(Math.abs(x0 + mouseX) / 2, y0);
                                context.lineTo(Math.abs(mouseX - w), mouseY);
                                context.lineTo(mouseX, mouseY);
                                context.lineTo(Math.abs(x0 + mouseX) / 2, y0);
                            } else {
                                context.beginPath();
                                context.moveTo(Math.abs(x0 + mouseX) / 2, y0);
                                context.lineTo(Math.abs(mouseX + w), mouseY);
                                context.lineTo(mouseX, mouseY);
                                context.lineTo(Math.abs(x0 + mouseX) / 2, y0);
                            }


                        } else if (curTool === "line") {
                            clearCanvas();
                            context.beginPath();
                            context.moveTo(x0, y0);
                            context.lineTo(mouseX, mouseY);
                        }


                        context.stroke();

                    }



                    outlineCreate();
                },
                release = function(e) {
                    if (paint) {
                        context.beginPath();
                        drag(e);
                        paint = false;

                        if (curTool !== "bucket") {
                            img_update();
                        }
                        undoData.push(canvaso.toDataURL("image/png"));
                        undoImg.src = undoData[undoData.length - 2];
                        imgURL = canvaso.toDataURL("image/png");




                    }
                },
                cancel = function(e) {
                    drag(e);
                    paint = false;
                    if (curTool !== "bucket") {
                        img_update();
                    }
                };



            size_select.addEventListener('click', ev_size_change, false);
            undo_button.addEventListener('click', undoAction, false);
            clear_button.addEventListener('click', clearCanvasO, false);
            saveToServer.addEventListener('click', saveToServerFunction, false);




            canvas.addEventListener("mousedown", press, false);
            canvas.addEventListener("mousemove", drag, false);
            canvas.addEventListener("mouseup", release, false);
            canvas.addEventListener("mouseout", cancel, false);

            canvas.addEventListener("touchstart", press, false);
            canvas.addEventListener("touchmove", drag, false);
            canvas.addEventListener("touchend", release, false);
            canvas.addEventListener("touchcancel", cancel, false);


        },
        resourceLoaded = function() {

            curLoadResNum += 1;
            if (curLoadResNum === totalLoadResources) {
                createUserEvents();
            }
        },
        SetColor = function(id) { // Set the color of the drawing tool when a color swatch is clicked
            curColor = document.getElementById(id).style.backgroundColor;
            $('#color').css('background-color', curColor);

            if (id[12] != null && id[13] != null)
                curHexColor = colorPalette[id[11] + id[12] + id[13]];
            else if (id[12] != null)
                curHexColor = colorPalette[id[11] + id[12]];
            else
                curHexColor = colorPalette[id[11]];

            hexToRGB(curHexColor);
            //alert(curColorR+ " "+ curColorG + " "+ curColorB);


        },
        LoadColorTable = function() {
            for (i = 0; i < colorPalette.length; i++) {
                var colorDiv = document.createElement("div");
                colorDiv.className = "color";
                colorDiv.id = "colorSwatch" + i;
                colorDiv.style.backgroundColor = colorPalette[i];
                colorDiv.setAttribute("onclick", "drawingApp.SetColor(id);");
                document.getElementById("colorTable").appendChild(colorDiv);

            };
        },

        init = function(inputURL, wallURL) {

            canvaso = document.getElementById("drawingCanvas");
            contexto = canvaso.getContext("2d");


            canvas = document.getElementById('tempCanvas');
            context = canvas.getContext("2d");

            img_update();

            size_select = document.getElementById("sizeSelector");
            undo_button = document.getElementById("undoButton");
            clear_button = document.getElementById("clearButton");
            saveToServer = document.getElementById("saveToServer");

            context.fillStyle = "#ffffff";
            context.fillRect(0, 0, canvasWidth, canvasHeight);


            coloringPic.onload = resourceLoaded;

            coloringPic.src = inputURL;

            loadedIMG.onload = resourceLoaded;
            loadedIMG.src = wallURL;

            undoData[0] = wallURL;

            console.log("loaded");

            saveImageToServer = document.getElementById("data");
            saveImageToServer.value = canvaso.toDataURL("image/png");

            LoadColorTable();

            hexToRGB(curHexColor);
            outlineCreate();
            context.drawImage(loadedIMG, drawingAreaX, drawingAreaY, drawingAreaWidth, drawingAreaHeight);



        };

    return {
        init: init,
        SetColor: SetColor,
        changeToBrush: changeToBrush,
        changeToEraser: changeToEraser,
        changeToRectangle: changeToRectangle,
        changeToLine: changeToLine,
        changeToBucket: changeToBucket,
        changeToEyedrop: changeToEyedrop,
        changeToTriangle: changeToTriangle,
        changeToCircle: changeToCircle,
        changeColoringImage: changeColoringImage

    };
}());


var colorPalette = [ //Begin array of color table hex color codes. 21 x 12

    "#000000", "#000000", "#000000", "#000000", "#003300", "#006600", "#009900", "#00CC00", "#00FF00", "#330000", "#333300", "#336600", "#339900", "#33CC00", "#33FF00", "#660000", "#663300", "#666600", "#669900", "#66CC00", "#66FF00",
    "#000000", "#333333", "#000000", "#000033", "#003333", "#006633", "#009933", "#00CC33", "#00FF33", "#330033", "#333333", "#336633", "#339933", "#33CC33", "#33FF33", "#660033", "#663333", "#666633", "#669933", "#66CC33", "#66FF33",
    "#000000", "#666666", "#000000", "#000066", "#003366", "#006666", "#009966", "#00CC66", "#00FF66", "#330066", "#333366", "#336666", "#339966", "#33CC66", "#33FF66", "#660066", "#663366", "#666666", "#669966", "#66CC66", "#66FF66",
    "#000000", "#999999", "#000000", "#000099", "#003399", "#006699", "#009999", "#00CC99", "#00FF99", "#330099", "#333399", "#336699", "#339999", "#33CC99", "#33FF99", "#660099", "#663399", "#666699", "#669999", "#66CC99", "#66FF99",
    "#000000", "#CCCCCC", "#000000", "#0000CC", "#0033CC", "#0066CC", "#0099CC", "#00CCCC", "#00FFCC", "#3300CC", "#3333CC", "#3366CC", "#3399CC", "#33CCCC", "#33FFCC", "#6600CC", "#6633CC", "#6666CC", "#6699CC", "#66CCCC", "#66FFCC",
    "#000000", "#FFFFFF", "#000000", "#0000FF", "#0033FF", "#0066FF", "#0099FF", "#00CCFF", "#00FFFF", "#3300FF", "#3333FF", "#3366FF", "#3399FF", "#33CCFF", "#33FFFF", "#6600FF", "#6633FF", "#6666FF", "#6699FF", "#66CCFF", "#66FFFF",
    "#000000", "#FF0000", "#000000", "#990000", "#993300", "#996600", "#999900", "#99CC00", "#99FF00", "#CC0000", "#CC3300", "#CC6600", "#CC9900", "#CCCC00", "#CCFF00", "#FF0000", "#FF3300", "#FF6600", "#FF9900", "#FFCC00", "#FFFF00",
    "#000000", "#00FF00", "#000000", "#990033", "#993333", "#996633", "#999933", "#99CC33", "#99FF33", "#CC0033", "#CC3333", "#CC6633", "#CC9933", "#CCCC33", "#CCFF33", "#FF0033", "#FF3333", "#FF6633", "#FF9933", "#FFCC33", "#FFFF33",
    "#000000", "#0000FF", "#000000", "#990066", "#993366", "#996666", "#999966", "#99CC66", "#99FF66", "#CC0066", "#CC3366", "#CC6666", "#CC9966", "#CCCC66", "#CCFF66", "#FF0066", "#FF3366", "#FF6666", "#FF9966", "#FFCC66", "#FFFF66",
    "#000000", "#FFFF00", "#000000", "#990099", "#993399", "#996699", "#999999", "#99CC99", "#99FF99", "#CC0099", "#CC3399", "#CC6699", "#CC9999", "#CCCC99", "#CCFF99", "#FF0099", "#FF3399", "#FF6699", "#FF9999", "#FFCC99", "#FFFF99",
    "#000000", "#00FFFF", "#000000", "#9900CC", "#9933CC", "#9966CC", "#9999CC", "#99CCCC", "#99FFCC", "#CC00CC", "#CC33CC", "#CC66CC", "#CC99CC", "#CCCCCC", "#CCFFCC", "#FF00CC", "#FF33CC", "#FF66CC", "#FF99CC", "#FFCCCC", "#FFFFCC",
    "#000000", "#FF00FF", "#000000", "#9900FF", "#9933FF", "#9966FF", "#9999FF", "#99CCFF", "#99FFFF", "#CC00FF", "#CC33FF", "#CC66FF", "#CC99FF", "#CCCCFF", "#CCFFFF", "#FF00FF", "#FF33FF", "#FF66FF", "#FF99FF", "#FFCCFF", "#FFFFFF"

];




$(document).ready(function() {
    // Handles showing/hiding the color table
    $("#colorTable").hide();

    $("#color").click(function() {
        $("#colorTable").show();
    });
    $(document).click(function() {
        $("#colorTable").hide();
    });
    $("#color").click(function(event) {
        event.stopPropagation();
    });

    //-------------------------------
    $("#toolSelector").hide();

    $("#tool").click(function() {
        $("#toolSelector").show();
    });
    $(document).click(function() {
        $("#toolSelector").hide();
    });
    $("#tool").click(function(event) {
        event.stopPropagation();
    });
});
