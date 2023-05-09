$(document).ready(
    function(){

        $("#loading").hide();

        $("#sendFile").submit(function(event){
            event.preventDefault();

            $("#loading").show();
            $("#uploadbut").prop("disabled", true);
            var dataSend = new FormData();

            var textInput = $('#askMolName').val();
            var fileInput = $('#fileUploader')[0].files[0];

            dataSend.append('txtInpt', textInput);
            dataSend.append('fileContent', fileInput);

            $.ajax({
                url: "/upload_button.html",
                type: "POST",
                data: dataSend,
                processData: false,
                contentType: false,
                success: function(data){
                    $("#loading").hide();
                    alert("Data: " + data);
                    $('#askMolName').val("");
                    $('#fileUploader').val("");
                    $("#uploadbut").prop("disabled", false);
                },
                error: function(){
                    $("#loading").hide();
                    alert("Error occured.");
                    $('#askMolName').val("");
                    $('#fileUploader').val("");
                    $("#uploadbut").prop("disabled", false);
                }
            });
        });

});