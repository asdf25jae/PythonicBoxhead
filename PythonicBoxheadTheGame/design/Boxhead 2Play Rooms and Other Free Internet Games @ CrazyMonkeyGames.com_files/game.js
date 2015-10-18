$(document).ready(function(){
	$("#controls").toggle(function(){
		$("#game-controls").hide();
	}, function() {
	    $("#game-controls").show();
	});
});


function fsToggle(type) {
  if (type == 'on') {
    // changes to allow full-screen
    $('body').addClass('fullscreen');
    $('body.fullscreen #flash-space object').attr('width', 500);
    $('body.fullscreen #flash-space embed').attr('width', 500);

  } else {
    // changes to restore regular screen
    $('body').removeClass('fullscreen');
  }
}
