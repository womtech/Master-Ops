$(document).ready(function() {

  

  var r_columns;

  // Data retrieval Via Generic callAJAX Function
  callAJAX( "/cfms/contract_performance",
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
     }], resp = createDataTable("#tbl_cfms_contract_repos", r_columns );
     resp.create( "/cfms/contract_performance", "POST", markups );
     resp.action()
   }

});
