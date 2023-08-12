function aredirect(){    
    const email = document.getElementById("email").value;
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    $.ajax({

        url: "api/sendEmail/",
        type: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        },
        data: { email : email  },
        
        success: function(response) {
            if (response.message === 'E-posta gönderildi.') {
                // Özelleştirilmiş bir iletişim kutusu oluşturma
                var customMessage = "E-posta başarıyla gönderildi!";
                var redirectUrl = response.redirectUrl; // Redirection URL

                var alertContainer = document.createElement("div");
                alertContainer.classList.add("custom-alert");

                var message = document.createElement("p");
                message.textContent = customMessage;
                alertContainer.appendChild(message);

                document.body.appendChild(alertContainer);

                // Belirli bir süre sonra iletişim kutusunu kaldırma
                setTimeout(function() {
                    document.body.removeChild(alertContainer);
                    window.location.href = redirectUrl; // Yönlendirme yapma
                }, 3000);
            } else {
                showErrorAlert("Bir hata oluştu.");
            }
        },
        error: function(error) {
            console.error(error);
        }
        
    });
}