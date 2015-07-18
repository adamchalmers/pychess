TILE_SIZE = 50;
CANVAS_SCALE = 2;
OFFSET = 10;
HL_SIZE = 5;

/*
 * Draw a board. Parameter is an 8x8 array of strings - pieces to draw.
 */
function drawBoard(board) {
    ctx.fillStyle = "#aaa";
    ctx.fillRect(0, 0, CANVAS_SCALE*(TILE_SIZE*8 + OFFSET*2), CANVAS_SCALE*(TILE_SIZE*8 + OFFSET*2));
    for (var i = 0; i < 8; i++) {
        for (var j = 0; j < 8; j++) {
            drawCell(i, j, board[i][j].substring(1), board[i][j].substring(0,1) == "w");
        }
    }
}

function drawCell(i, j, text, color, leaveHighlight) {
  // Draw the board cell
  if ((i*8 + j + i%2)%2===0) {
    ctx.fillStyle = "#fff";
  } else {
    ctx.fillStyle = "#000";
  }
  if (leaveHighlight) {
    ctx.fillRect(
        CANVAS_SCALE * (OFFSET + HL_SIZE + i*TILE_SIZE), 
        CANVAS_SCALE * (OFFSET + HL_SIZE + j*TILE_SIZE), 
        CANVAS_SCALE * (TILE_SIZE - 2*HL_SIZE), 
        CANVAS_SCALE * (TILE_SIZE - 2*HL_SIZE)
    );
  } else {
    ctx.fillRect(
        CANVAS_SCALE * (OFFSET + i*TILE_SIZE), 
        CANVAS_SCALE * (OFFSET + j*TILE_SIZE), 
        CANVAS_SCALE * (TILE_SIZE), 
        CANVAS_SCALE * (TILE_SIZE)
    );
  }

  // Write in the piece
  if (text != ".") {
    ctx.font = "" + 24*CANVAS_SCALE + "px serif ";
    if (color) {
        ctx.fillStyle = "#DB0";
    } else {
        ctx.fillStyle = "#999";
    }
    ctx.fillText(
        text, 
        CANVAS_SCALE*(OFFSET + i*TILE_SIZE + 15), 
        CANVAS_SCALE*(4*OFFSET + j*TILE_SIZE)
    );
  }
}

function highlightCell(i, j) {
    ctx.fillStyle = "orange";
    ctx.fillRect(
        CANVAS_SCALE * (OFFSET + i*TILE_SIZE), 
        CANVAS_SCALE * (OFFSET + j*TILE_SIZE), 
        CANVAS_SCALE * (TILE_SIZE), 
        CANVAS_SCALE * (TILE_SIZE)
    );
    drawCell(i, j, board[i][j].substring(1), board[i][j].substring(0,1) == "w", true);
}