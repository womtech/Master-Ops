// Initializing Base URL
var BASE_URL = "//mops.wom.co.in:8001/"

class HTMLElement {
  render() {
  }
}

class Checkbox extends HTMLElement {
  constructor() {
    super();
  }
  render( fieldId, tdValue, isHidden, cType ) {
    var string,
    checkedStatus = ( tdValue ) ? "checked":"";
    string = '<input onChange="inlineUpdater( this, null, &apos; checkbox &apos; )" data="'+ tdValue +'" type="checkbox"' + ' id="'+ fieldId + '" '+checkedStatus+'/>'
    return string;
  }
}

class Textbox extends HTMLElement {
  constructor( ) {
    super();
  }
  render( fieldId, tdValue, isHidden, cType ) {
    var string = "";
    if ( isHidden ) {
      string += "<div style='display:none;'>";
      string += "<input type='text' id='"+fieldId+"' value='"+ tdValue + "' onfocusout='inlineUpdater(this,  &apos;onfocusout&apos; , &apos; "+cType+" &apos; )' />";
      string += "</div>";
    } else {
      string = "<input type='text' id='"+fieldId+"' value='"+ tdValue + "' onfocusout='inlineUpdater(this,  &apos;onfocusout&apos; , &apos; "+cType+" &apos; )' />";
    }
    return string;
  }
}

class Textarea extends HTMLElement {
  constructor() {
    super();
  }
  render( fieldId, tdValue, isHidden, cType ) {
    var string="";
    if( isHidden ) {
      string += "<div style='display:none;'>";
      string += "<textarea rows='4' cols='20' maxlength='250' id='"+ fieldId +"' onfocusout='inlineUpdater(this, &apos;onfocusout&apos;, &apos;"+cType+"&apos; )' >"+tdValue+"</textarea>";
      string += "</div>";
    } else {
      string = "<textarea rows='4' cols='20' maxlength='250' id='"+ fieldId +"' onfocusout='inlineUpdater(this, &apos;onfocusout&apos;, &apos;"+cType+"&apos; )' >"+tdValue+"</textarea>";
    }
    return string;
  }
}

const ELEMENT_ARR = {
  "text":Textbox,
  "textarea":Textarea,
  "checkbox":Checkbox,
}

class Elements {
  constructor(className,opts) {
    return new ELEMENT_ARR[className](opts);
  }
}

//Function to take care of inline updation from data table
function inlineUpdater( obj, op_type, control_type ) {
  var new_value = {},
      tableID = $(obj).closest('table').attr('id'),
      cdt = createDataTable();
  switch( control_type.trim() ){
    case "checkbox":
      var r = confirm("Are you sure to update it?")
      if ( r ) {
        var changedValue = $( obj ).is(':checked');
        new_value[$(obj).prop("id")] = changedValue
        cdt.update( obj, new_value, tableID, "remove_row" )
      }
    default:
      if ( op_type=="onfocusout" ) {
        $(obj).parent("div").css({'display':'none'});
	$(obj).closest("td").find("span").css({'display':'block'})
        new_value[$(obj).prop("id")] = $(obj).val()
        if($(obj).closest("td").find("span").html() !== $(obj).val()) {
	  cdt.update( obj, new_value, tableID,"default" )
	}
      }
  }
}

// Generic Function to Read Cookie
function getCookie(cname) {
  var name = cname + "=",
  decodedCookie = decodeURIComponent(document.cookie),
  ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

// Generic Function to process Ajax Calls
function callAJAX(url, header, parameters, req_type, successCallback, beforeSendCallback, completeCallback ) {
    jQuery.ajax({
        type : req_type,
        url : url,
        headers : header ,
        data :  parameters,
        beforeSend : beforeSendCallback,
        complete : completeCallback,
        success : successCallback,
        error : function(xhr, textStatus, errorThrown) {
            console.log( 'error' + textStatus + ' ' + xhr + ' ' + errorThrown );
        },
        async: false
    });
}

// Generic Function to process Ajax Multipart
function callAJAXMultipart(url, header, parameters, req_type, successCallback, beforeSendCallback, completeCallback ) {
    jQuery.ajax({
        type : req_type,
        url : url,
        contentType: false,
        headers : header ,
        processData: false,
        data : parameters ,
        beforeSend : beforeSendCallback,
        complete : completeCallback,
        success : successCallback,
        error : function(xhr, textStatus, errorThrown) {
            console.log( 'error' + textStatus + ' ' + xhr + ' ' + errorThrown );
        },
        async: false
    });
}

//Factory Function To Create DataTable
var createDataTable = function ( targetID, r_columns, r_filters ) {
  var response =  {
    targetID,
    r_columns,
    r_filters,
    update: function( obj, param, tableID, postUpdateAction ) {
	var temp = tableID.split("_").pop(), updateURL = "/"+temp+"/update/";
        callAJAX( updateURL ,
          {"X-CSRFToken": getCookie("csrftoken") },
    	  param,
	  'POST',
    	  function( data, postUpdateAction ){
            if ( data["affected_rows"] ) {
	     $(obj).closest("td").find("span").text($(obj).val())
	    }
          },
    	  function( ){
      	    $(obj).prop('disabled',true)
    	  },function(){
      	    $(obj).prop('disabled',false)
    	} );
	if ( postUpdateAction =="remove_row" ) { $(obj).closest('tr').fadeOut(); }
    },

    create: function( r_url, r_type, r_markups, r_table_nature ){
      $(targetID).DataTable({
        "ajax": {
	  "url":r_url,
	  "type":r_type,
          "data": r_filters,
	  "contentType":"application/x-www-form-urlencoded; charset=UTF-8",
          "beforeSend": function(request) {
	    request.setRequestHeader("X-CSRFToken", getCookie("csrftoken") );
	  },
	 "dataSrc":'data',
        },
	"dom":"Bfrtip",
	"bProcessing":true,
	"bServerSide":true,
  	"bDestroy":true,
	"columns":r_columns,
	"aoColumnDefs": r_markups,
        "fnRowCallback": function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) {
          if ( r_table_nature == "rich" ) {
            var j = 0;
	    for ( var i = 0; i < aData.length; i++ ) {
              var pkeyValue = aData[0], string="",
                className = r_columns[i][r_columns[i]["title"]][0],
                cType = r_columns[i][r_columns[i]["title"]][1],
                fieldId = r_columns[i][r_columns[i]["title"]][2]+"_"+pkeyValue;
	      if( className.trim() == "editable" ) {
		if (cType == "checkbox") {
		  string = response.inlineAppender( aData[i], cType, fieldId)
		} else {
                  string = "<span>"+aData[i]+"</span>"+" "+ response.inlineAppender( aData[i], cType, fieldId);
		}
	        $('td:eq('+i+')', nRow).html( string ).addClass( className );
              }
	    }
          } // End of else

        }
      });
    },
    inlineAppender: function(td_value, cType, fieldId) {
     var string="", element = new Elements(cType);
     if ( cType=="textarea" || cType =="text" ) {
       string = element.render(fieldId, td_value, 1, 'textarea');
     } else if( cType == "checkbox" ) {
       string = element.render( fieldId, td_value, 0, 'checkbox' );
     }
     return string;
    },

   action: function() {
     $(targetID + " tbody").on('click','.editable',function(){
	$(this).children('span').css({"display":"none"})
	$(this).children('div').css({"display":'block'})
     });
   },
  }
  return response;
};


