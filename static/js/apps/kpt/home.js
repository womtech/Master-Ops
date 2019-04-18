$(document).ready(function() {
        $("#submit").click(function(e) {
          e.preventDefault();
          $("#submit").prop('disabled', true);
          var property = document.getElementById('inputGroupFile01').files[0],
          option = $("select#sel1 option:checked").val(),
          uploadUrl = $("#submit").attr("upload_url");
          var form_data = new FormData();
          form_data.append("file",property);
          form_data.append("import_type",option);
          callAJAXMultipart( uploadUrl, {"X-CSRFToken": getCookie("csrftoken") },  form_data  , 'post',
		  function( data ){
                     $(':input[type="submit"]').prop('disabled', false);
                     $('#successRecords').html(data.sucessfull_records);
                     $('#totalRecords').html(data.total_records);
                     $('#msg').html(data.message);
                     $('#msgdivision').hide().fadeIn(100).fadeOut(10000);
                	},
		  function() {
		             $('#msg').html('Uploading......');
		            }, null
	       );

      });
});
