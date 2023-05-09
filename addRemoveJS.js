$(document).ready(
    function(){
      $(".removeElement").hide();
      
      $("#switchButton").click(
        function(){
          $(".addElement").toggle();
          $(".removeElement").toggle();
        });
        
        $("#form1").submit(function(event) {
            event.preventDefault(); 
            $.post("/add_button.html", 
            {
              elNum: $("#elementNum").val(),
              elCode: $("#elementCode").val(),
              elName: $("#elementName").val(),
              elColor1: $("#color1").val(),
              elColor2: $("#color2").val(),
              elColor3: $("#color3").val(),
              elRadius: $("#radius").val()
            },
            function(data){
              alert("Data: " + data);
              $("#elementNum").val(1)
              $("#elementCode").val("")
              $("#elementName").val("")
              $("#color1").val("")
              $("#color2").val("")
              $("#color3").val("")
              $("#radius").val(20)
              window.location.reload();
            });
        });

        $("#form2").submit(function(event){
          event.preventDefault();
          $.post("/remove_button.html",
          {
            elementToDelete: $("#selectTable").val()
          },
          function(data){
            alert("Data: " + data);
            window.location.reload();
          });
        });




    });