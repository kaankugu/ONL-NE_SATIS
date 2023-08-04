
function goToHomePage() {
    window.location.href = ("/");
}

function redirect() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    
    $.ajax({
        url: "/api/login/",
        type: "POST",
        data: { email: email, password: password },
        
        success: function(response) {

            const token = response.access_token;
            document.cookie = `apiData=${JSON.stringify({ access_token: token })}; expires= Thu, 21 Aug 2025 20:00:00 UTC; path=/ `;
            window.location.href = "/";


        },
        error: function(error) {
            console.error(error);
        }
    });
    $(document).ready(function() {
        handleUserLogin();  
    })
}
