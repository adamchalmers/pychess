TILE_SIZE = 50;
OFFSET = 10;
REFRESH_RATE = 3 * 1000;
HL_SIZE = 5;
ctx = undefined;
game_id = $("#game_id").val();
board = undefined;
now = -1;
// Will be 'white' or 'black'
turn = undefined;
squareSelected = null;
player = undefined;


$(document).ready(function() {
    ctx = $("#chessBoard")[0].getContext("2d");
    $("#game").hide();

    // Ensure the form doesn't submit when the user presses 'enter'
    $(window).keydown(function(e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            $("#submit").click();
        }
    });

    $("#chessBoard").on("click", handleClick);
    $("#submit").on("click", authenticateUser);
});

function authenticateUser() {
// Send a post request to the server for validation
    $.ajax({
        type: "POST",
        url: "/auth",
        data: $("#authForm").serialize(),
        success: function(data) {

            // If there's no error
            if (!data.error || data.error=="NEWAUTH") {

                if (data.error=="NEWAUTH") {
                    alert("Welcome to the game.")
                }
                $(".error").text("");
                $("#welcome").hide();
                player = data.data;
                $(".player").text(player);

                // Draw the board every few seconds
                getBoard();
                window.setInterval(function(){
                    getBoard();
                }, REFRESH_RATE);

            // If there is an error
            } else {
                $(".error").text("Wrong password.");
            }
        }
    });
    return false;
}

function handleClick(evt) {
    if (player == turn) {
        var x = Math.floor((evt.offsetX - OFFSET)/TILE_SIZE);
        var y = Math.floor((evt.offsetY - OFFSET)/TILE_SIZE);
        if (x >= 0 && y >= 0 && x < 8 && y<8) {
            canvasClick(x,y);
        }
    }
}

/**
 * Called when a player clicks square (x,y) on the board.
 */
function canvasClick(x, y) {

    // No squares selected
    if (squareSelected === null) {
        // Ignore clicks that aren't on your pieces.
        if (board[x][y].substring(0,1) != turn.substring(0,1)) {
            return;
        }
        squareSelected = [x, y];
        highlightCell(x,y);

    // Square already selected
    } else {
        i = squareSelected[0];
        j = squareSelected[1];
        // Ignore clicks on your pieces.
        if (board[x][y].substring(0,1) == turn.substring(0,1)) {
            return;
        }

        url = ["/move", game_id, turn, i, j, x, y].join("/");
        console.log(url);
        $.get(url, function(data) {
            if (!data.error) {
                getBoard();
                $(".error").text("");
            } else {
                $(".error").text(data.error);
            }
        });
        drawCell(i, j, board[i][j].substring(1), board[i][j].substring(0,1) == "w");
        squareSelected = null;
    }
}

/* 
 * Parse a serialized board string
 * Returns an 8x8 array of strings.
 * Empty squares are '..'
 * A black king is 'bK'
 */
function unpackBoard(string) {
    string = string.split("")
    board = []
    newBoard = [];
    for (var i = 0; i < 8; i++) {
        board.push([]);
        newBoard.push([]);
        for (var j = 0; j < 16; j+=2) {
            board[i].push(string[i*16+j] + string[i*16+j+1])
        }
    }
    for (var i = 0; i < 8; i++) {
        for (var j = 0; j < 8; j++) {
            newBoard[i][j] = board[j][i];
        }
    }
    return newBoard;
}

/*
 * GET the board, then update with it.
 */
function getBoard() {
    $.get("/state/" + game_id, function(data) {
        if (!data.error) updateBoard(data.data); 
    });
}

/* 
 * If new moves have occurred, update and redraw the board.
 */
function updateBoard(state) {
    if (state.moves.length > now) {
        now = state.moves.length;

        turn = state.turn;
        $(".turn").text(state.turn);

        board = unpackBoard(state.board);
        drawBoard(board);
        $("#game").show();
    }
}

/*
 * Draw a board. Parameter is an 8x8 array of strings - pieces to draw.
 */
function drawBoard(board) {
    ctx.fillStyle = "#aaa";
    ctx.fillRect(0, 0, TILE_SIZE*8 + OFFSET*2, TILE_SIZE*8 + OFFSET*2);
    for (var i = 0; i < 8; i++) {
        for (var j = 0; j < 8; j++) {
            drawCell(i, j, board[i][j].substring(1), board[i][j].substring(0,1) == "w");
        }
    }
}

function drawCell(i, j, text, color, leaveHighlight) {
  // Draw the board cell
  if ((i*8 + j + i%2)%2==0) {
    ctx.fillStyle = "#fff";
  } else {
    ctx.fillStyle = "#000";
  }
  if (leaveHighlight) {
    ctx.fillRect(
        OFFSET + HL_SIZE + i*TILE_SIZE, 
        OFFSET + HL_SIZE + j*TILE_SIZE, 
        TILE_SIZE - 2*HL_SIZE, 
        TILE_SIZE - 2*HL_SIZE
    );
  } else {
    ctx.fillRect(
        OFFSET + i*TILE_SIZE, 
        OFFSET + j*TILE_SIZE, 
        TILE_SIZE, 
        TILE_SIZE
    );
  }

  // Write in the piece
  if (text != ".") {
    ctx.font = "24px serif ";
    if (color) {
        ctx.fillStyle = "#840";
    } else {
        ctx.fillStyle = "#048";
    }
    ctx.fillText(text, OFFSET + i*TILE_SIZE + 10, 4*OFFSET + j*TILE_SIZE)
  }
}

function highlightCell(i, j) {
    ctx.fillStyle = "orange";
    ctx.fillRect(
        OFFSET + i*TILE_SIZE, 
        OFFSET + j*TILE_SIZE, 
        TILE_SIZE, 
        TILE_SIZE
    );
    drawCell(i, j, board[i][j].substring(1), board[i][j].substring(0,1) == "w", true);
}