$(document).ready(function(){
   var gameID = $("#gameID").text();
   var img='<div style="padding-left: 50px;"><img src="assets/images/ajax-loader.gif" /></div>';
   
   $("#ranking-update").append("Please rate this game");
   $("#rank-select").change(function(){
       
       var userRanking = $("#rank-select").val();

       if (userRanking != "-") {
           $("#ranking-list").html(img);
           $.post(
			"/services/update_ranking.php",
			{ 'ranking': userRanking,
			  'gameID':  gameID			},
			function(data) {
				$('#ranking-list').html(data);
			});
       }
   });
   
});





/*
$(document).ready(function(){
	var gameID = $("#gameID").text();
	var img = '<div style="padding-left: 50px;"><img src="assets/images/ajax-loader.gif" /></div>';


	$("#ranking-update").append("Please rate this game: ");
	$("#rank-select").change(function(){
		$('#ranking-list').html(img);
		var userRanking = $(this).val();
		if (userRanking != "-") {
			$.post(
			"/services/update_ranking.php",
			{ 'ranking': userRanking,
			  'gameID':  gameID			},
			function(data) {
				$('#ranking-list').html(data);
			});
		}
	});
});
*/

