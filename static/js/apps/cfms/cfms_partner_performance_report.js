$(document).ready(function() {

  $('#cfms_partner_performance_report_filter').submit(function(e){
    e.preventDefault();
    submitFilter();
  });

  function submitFilter() {
    var r_filters = $("#cfms_partner_performance_report_filter").serialize(),
        active_view = $('#chk_view_switcher').is(":checked");
    resetTable();
    if( ! active_view ) {
      initTable( r_filters,"monthly" );
    } else {
      initTable( r_filters,"lifetime" );
    }
  }

  $("input[type='reset']").closest('form').on('reset', function(event) {
     document.getElementById("cfms_partner_performance_report_filter").reset(); submitFilter();
  });

  function resetTable() {
    $("#tbl_cfms_partner_repos").DataTable().destroy(true);
    $('#table_holder').append('<table id="tbl_cfms_partner_repos" class="display nowrap" width="100%"></table>')
  }

   initTable( null, "monthly" );

   $('#chk_view_switcher').change(function(){
     if($(this).is(":checked")) {
       $("#lbl_view_name").text("Partner Lifetime Performance")
       resetTable();
       initTable( null, "lifetime")
     } else {
       $("#lbl_view_name").text("Partner Monthly Performance")
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
        {"title": "Partner Code", "data": "partner_code","orderable":true},
        {"title": "Partner Name", "orderable":true, "data": "partner_name"},
        {"title": "Total Revenue", "orderable":true, "data": "total_revenue"},
        {"title": "Partner Status", "orderable":false, "data": "partner_status"},
      ];
      extra_data = {'custom_filter':r_filters, "view_type":"lifetime"   }
    } else if( option == "monthly") {
      r_columns = [
        {"title": "Partner Code", "data": "partner_code","orderable":true},
        {"title": "Partner Name", "orderable":true, "data": "partner_name"},
        {"title": "Total Revenue", "orderable":true, "data": "total_revenue"},
        {"title": "Month", "orderable":true, "data": "month"},
        {"title": "Partner Status", "orderable":false, "data": "partner_status"},
      ];
      extra_data = {'custom_filter':r_filters, "view_type":"monthly" }
    }
    var resp = createDataTable("#tbl_cfms_partner_repos", r_columns, extra_data );
    resp.create("/cfms/partner_performance","POST",[])
  }




});

