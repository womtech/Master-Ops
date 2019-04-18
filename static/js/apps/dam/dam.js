

$(document).ready(function() {

  var r_columns;

  // Data retrieval Via Generic callAJAX Function
  callAJAX( "/dam/lookups/",
    {"X-CSRFToken": getCookie("csrftoken") },
    parameters={},
    'post',
    function(data){
      console.log(data)
      r_columns = data["columns"];
  }, null, null );

   initializeDatatable ( r_columns )
   function initializeDatatable( r_columns ) {
     var markups = [{
      "mRender": function( data, type, row ){
	  if (data) {
		return "<button type='button' data-href="+row[0]+" class='btn btn-link'>Download</button>"
	  } else {
		return "<button type='button'  data-href="+row[0]+" class='btn btn-link'>Place Request</button>"
	  }
      },"aTargets":[5] ,
     }], resp = createDataTable("#tbl_dam", r_columns );
     resp.create( "/dam/lookups/", "POST", markups );
     resp.action()
   }

});
