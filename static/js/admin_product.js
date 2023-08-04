$(document).ready(function() {
    $(".update-button").click(function() {
        var item_id = $(this).data("item-id");
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        $.ajax({
            url: "/update-permission/",
            type: "POST",
            headers: {
                "X-CSRFToken": csrfToken
            },
            success: function(response) {
                alert(response.message); 
                window.location.reload(); 
            },
            data : {id : item_id},
            error: function(error) {
                console.log(error);
            }
           
        });
    });
});