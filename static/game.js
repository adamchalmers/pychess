
// How many milliseconds the client waits before checking game state
REFRESH_RATE = 3 * 1000;
// Canvas 2d context
ctx = undefined;
// String containing game ID
game_id = $("#game_id").val();
// Board object containing the game state
board = undefined;
// Logical time of the game
now = -1;
// Pair of numbers representing the cell the player's clicked on
squareSelected = null;
// Strings, either 'white' or 'black'
turn = undefined;
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
                    alert("Welcome to the game.");
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
        // If you click a square which isn't occupied by your piece, try moving there.
        if (board[x][y].substring(0,1) != turn.substring(0,1)) {
            postMove(i, j, x, y, board[i][j].substring(1));
        }
        drawCell(i, j, board[i][j].substring(1), board[i][j].substring(0,1) == "w");
        squareSelected = null;
    }
}

/*
 * Asynchronously send a move order to the server.
 * If the server's move validation works, update the board and change turns.
 * Else, show the user rule violation.
 */
function postMove(i, j, x, y, rank_char) {
    // Board is flipped for black players; unflip it.
    if (isBlack()) {
        i = 7-i;
        j = 7-j;
        x = 7-x;
        y = 7-y;
    }
    var details = "?";
    if (rank_char == "P" && ((isBlack() && y == 7) || (!isBlack() && y === 0))) {
        details += "promo=Q";
    }
    url = ["/move", game_id, turn, i, j, x, y].join("/") + details;
    console.log(url);
    $.get(url, function(data) {
        if (!data.error) {
            getBoard();
            $(".error").text("");
        } else {
            $(".error").text(data.error);
        }
    });
    return;
}

/* 
 * Parse a serialized board string
 * Returns an 8x8 array of strings.
 * Empty squares are '..'
 * A black king is 'bK'
 */
function unpackBoard(string) {
    string = string.split("");
    board = [];
    for (var i = 0; i < 8; i++) {
        board.push([]);
        for (var j = 0; j < 16; j+=2) {
            board[i].push(string[i*16+j] + string[i*16+j+1]);
        }
    }
    if (!isBlack()) {
        return board;
    }

    /*
     * If player is playing black, rotate the board 180 degrees.
     */
    newBoard = [];
    for (var i = 0; i < 8; i++) {
        newBoard.push([]);
        for (var j = 0; j < 8; j++) {
            newBoard[i][j] = board[7-i][7-j];
        }
    }
    // return newBoard;
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
    if (state.time > now) {
        now = state.time;

        turn = state.turn;
        $(".turn").text(state.turn);

        board = unpackBoard(state.board);
        drawBoard(board);
        $("#game").show();
    }
}

function isBlack() {
    return player == "black";
}
