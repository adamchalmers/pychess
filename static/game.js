TILE_SIZE = 50;
SELECT_BORDER = 5;
OFFSET = 10;
ctx = null;

$(document).ready(function() {
    ctx = $("#canvas")[0].getContext("2d");
    $(window).keydown(function(e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            $("#submit").click();
        }
    });
    $("#submit").on("click", function() {
        $.ajax({
            type: "POST",
            url: "/auth",
            data: $("#authForm").serialize(),
            success: function(data) {
                if (data == "TRUE") {
                    $("#login").hide();
                    drawBoard();
                    $("#game").show();
                } else {
                    $("#login").append("<p>Wrong pw</p>");
                }
            }
        });
        return false;
    });
});

function drawBoard() {
    ctx.fillStyle = "#aaa";
    ctx.fillRect(0, 0, TILE_SIZE*8 + OFFSET*2, TILE_SIZE*8 + OFFSET*2);
    for (var i = 0; i < 8; i++) {
        for (var j = 0; j < 8; j++) {
            drawCell(i, j);
        }
    }
}

function drawCell(i, j) {
  if ((i*8 + j + i%2)%2==0) {
    ctx.fillStyle = "#fff";
  } else {
    ctx.fillStyle = "#000";
  }
  ctx.fillRect(OFFSET + i*TILE_SIZE, OFFSET + j*TILE_SIZE, TILE_SIZE, TILE_SIZE);
}