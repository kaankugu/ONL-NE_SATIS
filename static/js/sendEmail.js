function redirect(){   
    const email = document.getElementById("email").value;
    
    $.ajax({
        url: "api/sendEmail/",
        type: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        },
        data: { email : email  },
        
        success: function(response) {
            if (response.success === 'Password reset link sent to your email.') {
                alert(response.success); // Mesajı göster
                window.location.href = "/login/"; // Giriş sayfasına yönlendir
            } else if (response.success === 'Password reset link updated and sent to your email.') {
                alert(response.success); // Mesajı göster
                // Başka bir işlem yapabilirsiniz
            } else {
                alert("Bir hata oluştu."); // İşlem başarısızsa hata mesajı göster
            }
        },
        error: function(error) {
            console.error(error);
        }
    })

}