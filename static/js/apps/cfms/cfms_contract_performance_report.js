$(document).ready(function() {

  $('#cfms_contract_performance_report_filter').submit(function(e){
    e.preventDefault();
    submitFilter();
  });

  function submitFilter() {
    var r_filters = $("#cfms_contract_performance_report_filter").serialize(),
        active_view = $('#chk_view_switcher').is(":checked");
    resetTable();
    if( ! active_view ) {
      initTable( r_filters,"monthly" );
    } else {
      initTable( r_filters,"lifetime" );
    }
  }

  $("input[type='reset']").closest('form').on('reset', function(event) {
     document.getElementById("cfms_contract_performance_report_filter").reset(); submitFilter();
  });

  function resetTable() {
    $("#tbl_cfms_contract_repos").DataTable().destroy(true);
    $('#table_holder').append('<table id="tbl_cfms_contract_repos" class="display nowrap" width="100%"></table>')
  }

   initTable( null, "monthly" );

   $('#chk_view_switcher').change(function(){
     if($(this).is(":checked")) {
       $("#lbl_view_name").text("Contract Lifetime Performance")
       resetTable();
       initTable( null, "lifetime")
     } else {
       $("#lbl_view_name").text("Contract Monthly Performance")
       resetTable();
       initTable( null, "monthly" )
     }
   });

   $('input[name="f_daterange"]').daterangepicker({
     opens: 'left',
     startDate:moment(),
     locale:{
	"format":"YYYY-MM-DD",
     },
   });

  function initTable( r_filters, option ) {
    if ( option=="lifetime" ) {
      r_columns = [
        {"title": "Contract Code", "data": "contract_code","orderable":false},
        {"title": "Total Revenue (USD)", "orderable":true, "data": "total_revenue"},
      ];
      extra_data = {'custom_filter':r_filters, "view_type":"lifetime"   }
    } else if( option == "monthly") {
      r_columns = [
        {"title": "Contract Code", "data": "contract_code","orderable":false},
        {"title": "Total Revenue (USD)", "orderable":true, "data": "total_revenue"},
        {"title": "Month","data": "month", "orderable":false }
      ];
      extra_data = {'custom_filter':r_filters, "view_type":"monthly" }
    }
     var markups = [{
      "mRender": function( data, type, row ){
          return '<a href="contract_report_dv?ctr='+row["id"]+'"' + '>'+data+'</a>';
      },"aTargets":[0] ,
     }], resp = createDataTable("#tbl_cfms_contract_repos", r_columns, extra_data );
    resp.create("cfms/contract_performance","POST",markups)
    resp.action()
  }



});

