$(document).ready(
    function(){
        $("#picture").hide();
        $(".moleculeMod").hide();

        $("#selectAndDisplay").submit(function(event){
            event.preventDefault();
            
            $.ajax({
                url: "/display_button",
                type: "POST",
                data: {molSelected: $("#chooseMol").val()},
                success: function(data){
                    $(".showImage").html(data);
                    $("#picture").show();
                    $(".moleculeMod").show();
                    $("html, body").animate(
                        {scrollTop: $(document).height()
                        }, 
                        500);
                },
                error: function(){
                    alert("Molecule unavailable.");
                }
            });
        });

        $("#modifyMol").submit(function(event){
            event.preventDefault();

            $.ajax({
                url: "/mod_svg.html",
                type: "POST",
                data: {axisChange: $("#xyz").val(), degreeChange: $("#degreeNum").val()},
                success: function(data){
                    $(".showImage").html(data);
                },
                error: function(){
                    alert("Rotation cannot be made.");
                }
            });
        });
    });