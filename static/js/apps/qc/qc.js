

$(document).ready(function() {

  var r_columns;

  // Data retrieval Via Generic callAJAX Function
  callAJAX( "/qc/list/",
    {"X-CSRFToken": getCookie("csrftoken") },
    parameters={},
    'post',
    function(data){
      r_columns = data["columns"];
  }, null, null );


   // Function to Initialize DataTable
   function initializeDatatable( r_columns, r_filters ) {
     var markups = [{
      "mRender": function( data, type, row ){
          return '<a href="https://www.youtube.com/watch?v='+row[0]+'"' + 'id="'+ data + '">'+data+'</a>'+
  	  '<br><br><a href="https://img.youtube.com/vi/'+ row[0] +'/0.jpg" target="_blank"><h6>Thumbnail</h6></a>';
      },"aTargets":[1] ,
     }], resp = createDataTable("#tbl_qc", r_columns, r_filters);
     resp.create( "/qc/list", "POST", markups, table_nature = "rich" );
     resp.action()
   }

   initializeDatatable ( r_columns, false )

   $('input[name="f_daterange"]').daterangepicker({
     opens: 'left',
     startDate:moment(),
     locale:{
	"format":"YYYY-MM-DD",
     },
   });

  $('#qc_list_filter').submit(function(e){
    e.preventDefault();
    $('#tbl_qc').dataTable().fnClearTable();
    $('#tbl_qc').dataTable().fnDestroy();
    //initializeDatatable( r_columns, JSON.stringify( $('#qc_list_filter').serialize() ) )
    initializeDatatable( r_columns, $(this).serialize() ) 
    console.log($(this).serialize())
  });

});
