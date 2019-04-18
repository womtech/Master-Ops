$(document).ready(function() {

 function getCols(contract_id) {
  var extra_data = {'custom_filter':{'query_type':"cols", 'ctr_data':contract_id}};
  var r_columns;
  callAJAX( "/cfms/contract_report_dv",
    {"X-CSRFToken": getCookie("csrftoken") },
    parameters=extra_data,
    'post',
    function(data){
     r_columns = data
  }, null, null );
  return r_columns;
 }

 function initTable( r_filters, table_id, ctr_data ) {
    var r_columns = getCols( ctr_data );
    var extra_data = {'custom_filter':r_filters  };
    var resp = createDataTable( table_id , r_columns, extra_data );
    resp.create("/cfms/contract_report_dv","POST",[])
  }

  function resetTable( table_id, table_holder_id) {
    if ( $.fn.DataTable.isDataTable("#"+table_id) ) {
      $("#"+table_id).DataTable().destroy(true);
      $("#"+table_holder_id).append('<table id="'+table_id+'" class="display nowrap" width="100%"></table>')
    }
  }


  $(".a_monthly_rev_breakup").click(function(){
    var month = $(this).attr('data-month'),
    offset = $(this).attr('data-month-offset'),
    table_id = "tbl_cfms_contract_rep_dv_" + offset,
    table_holder_id = "table_holder_" + offset,
    ctr_id = $(this).attr('data-ctr'),
    currency_selector = $("input.chk_monthly_breakup:checkbox").is(":checked"), r_filters;
    r_filters = {"for_month":month, "converted_currency":"no","ctr_data":ctr_id};
    if ( currency_selector  ) {
      r_filters = {"for_month":month, "converted_currency":"yes","ctr_data":ctr_id};
    }
    initTable( r_filters, "#"+table_id, ctr_id )
  });


  $(".chk_monthly_breakup").change(function(){
    var month = $(this).attr('data-month'),
    status = $(this).is(":checked"),
    offset = $(this).attr('data-month-offset')
    table_id = "tbl_cfms_contract_rep_dv_" + offset
    table_holder_id = "table_holder_" + offset,
    ctr_id = $(this).attr('data-ctr');
    resetTable(table_id,table_holder_id)
    if (status) {
      r_filters = {"for_month":month, "converted_currency":"yes","ctr_data":ctr_id}
    } else {
      r_filters = {"for_month":month, "converted_currency":"no","ctr_data":ctr_id}
    }
    initTable( r_filters, "#"+table_id, ctr_id )
  });





});

