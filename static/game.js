TILE_SIZE = 50;
SELECT_BORDER = 5;
OFFSET = 10;
REFRESH_RATE = 3 * 1000
ctx = null;
game_id = $("#game_id").val();


$(document).ready(function() {
    ctx = $("#canvas")[0].getContext("2d");

    // Ensure the form doesn't submit when the user presses 'enter'
    $(window).keydown(function(e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            $("#submit").click();
        }
    });

    // When the user presses submit, authenticate them.
    $("#submit").on("click", function() {

        // Send a post request to the server for validation
        $.ajax({
            type: "POST",
            url: "/auth",
            data: $("#authForm").serialize(),
            success: function(data) {

                // If there's no error
                if (!data.error) {
                    $("#login").hide();

                    // Get the board state, parse it and draw the board.
                    window.setInterval(function(){
                      getBoard();
                    }, REFRESH_RATE);
                // If there is an error
                } else {
                    $("#login").append("<p>Wrong pw</p>");
                }
            }
        });
        return false;
    });
});

/* 
 * Parse a serialized board string
 * Returns an 8x8 array of strings.
 * Empty squares are '..'
 * A black king is 'bK'
 */
function unpackBoard(string) {
    string = string.split("")
    board = []
    for (var i = 0; i < 8; i++) {
        board.push([]);
        for (var j = 0; j < 16; j+=2) {
            board[i].push(string[i*16+j] + string[i*16+j+1])
        }
    }
    return board
}

/*
 * GET the board, then draw it.
 */
function getBoard() {
    $.get("/state/" + game_id, function(data) {
        if (!data.error) {
            board = unpackBoard(data.data.board);
            drawBoard(board);
            $("#game").show();
        }
    });
}

/*
 * Draw a board. Parameter is an 8x8 array of strings - pieces to draw.
 */
function drawBoard(board) {
    ctx.fillStyle = "#aaa";
    ctx.fillRect(0, 0, TILE_SIZE*8 + OFFSET*2, TILE_SIZE*8 + OFFSET*2);
    for (var i = 0; i < 8; i++) {
        for (var j = 0; j < 8; j++) {
            drawCell(j, i, board[i][j]);
        }
    }
}

function drawCell(i, j, text) {
  // Draw the board cell
  if ((i*8 + j + i%2)%2==0) {
    ctx.fillStyle = "#fff";
  } else {
    ctx.fillStyle = "#000";
  }
  ctx.fillRect(OFFSET + i*TILE_SIZE, OFFSET + j*TILE_SIZE, TILE_SIZE, TILE_SIZE);

  // Write in the piece
  if (text != "..") {
    ctx.font = "24px serif ";
    ctx.fillStyle = "#09f";
    ctx.fillText(text, OFFSET + i*TILE_SIZE + 10, 4*OFFSET + j*TILE_SIZE)
  }
  
}