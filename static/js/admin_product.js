$(document).ready(function() {
    $(".update-button").click(function() {
        var item_id = $(this).data("item-id");
        $.ajax({
            url: "/update-permission/" + item_id + "/",
            type: "POST",
            headers: {
                "X-CSRFToken": '{{ csrf_token }}' 
            },
            success: function(response) {
                alert(response.message); 
                window.location.reload(); 
            },
            error: function(error) {
                console.log(error);
            }
           
        });
    });
});