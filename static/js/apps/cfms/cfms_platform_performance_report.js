$(document).ready(function() {

  $('#cfms_platform_performance_report_filter').submit(function(e){
    e.preventDefault();
    submitFilter();
  });

  function submitFilter() {
    var r_filters = $("#cfms_platform_performance_report_filter").serialize(),
        active_view = $('#chk_view_switcher').is(":checked");
    resetTable();
    if( ! active_view ) {
      initTable( r_filters,"monthly" );
    } else {
      initTable( r_filters,"lifetime" );
    }
  }

  $("input[type='reset']").closest('form').on('reset', function(event) {
     document.getElementById("cfms_platform_performance_report_filter").reset(); submitFilter();
  });

  function resetTable() {
    $("#tbl_cfms_platform_repos").DataTable().destroy(true);
    $('#table_holder').append('<table id="tbl_cfms_platform_repos" class="display nowrap" width="100%"></table>')
  }

   initTable( null, "monthly" );

   $('#chk_view_switcher').change(function(){
     if($(this).is(":checked")) {
       $("#lbl_view_name").text("Platform Lifetime Performance")
       resetTable();
       initTable( null, "lifetime")
     } else {
       $("#lbl_view_name").text("Platform Monthly Performance")
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
        {"title": "Platform Code", "data": "platform_code","orderable":true},
        {"title": "Platform Name", "orderable":true, "data": "platform_name"},
        {"title": "Gross Earning", "orderable":true, "data": "gross_earning"},
      ];
      extra_data = {'custom_filter':r_filters, "view_type":"lifetime"   }
    } else if( option == "monthly") {
      r_columns = [
        {"title": "Platform Code", "data": "platform_code","orderable":true},
        {"title": "Platform Name", "orderable":true, "data": "platform_name"},
        {"title": "Gross Earning", "orderable":true, "data": "gross_earning"},
        {"title": "Month", "orderable":true, "data": "month"},
      ];
      extra_data = {'custom_filter':r_filters, "view_type":"monthly" }
    }
    var resp = createDataTable("#tbl_cfms_platform_repos", r_columns, extra_data );
    resp.create("/cfms/platform_performance","POST",[])
  }




});

