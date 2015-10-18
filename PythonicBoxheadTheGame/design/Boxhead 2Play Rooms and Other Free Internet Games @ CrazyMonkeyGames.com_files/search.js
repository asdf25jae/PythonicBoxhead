/* Added PNG fix to the search.js because it is on every page */
$(document).ready(function(){
	$("input.search").attr("value", "Game Search");
	$("input.search").click(function() {
		$("input.search").attr("value", "");
	});
    var data = ""
    $(".search").autocomplete("/services/search.php", {
		dataType: "json",
		parse: function(data) {
          var rows = new Array();
          for(var i=0; i<data.length; i++){
              rows[i] = { data:data[i], value:data[i].name, result:data[i].icon, result:data[i].link };
          }
          return rows;
      },
      formatItem: function(row, i, n) {
          return row.name;
      },
      mustMatch: true,
  }).result(function(event, item) {
  	location.href= item.link;
  });
});
