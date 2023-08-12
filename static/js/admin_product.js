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

async function fetchProducts() {
    try {
        const response = await fetch('/api/products/'); 
        return await response.json();
    } catch (error) {
        console.error('Error fetching products:', error);
        return [];
    }
}

async function displayProducts() {
    const products = await fetchProducts();

    const productContainer = document.getElementById('product-container');
   
    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.classList.add('product-card');
        
        const Permission = product.permission;
        if (!Permission) {
            return ;}
 
                    
        const quantitySelect = document.createElement('select');
        quantitySelect.id = 'quantitySelect' + product.id;
        for (let i = 1; i <= 10; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = i;
            quantitySelect.appendChild(option);
        }
        

        const productImageDiv = document.createElement('div');
        productImageDiv.classList.add('product-images');
        
        for (let i = 0; i < Math.min(product.images.length, 15); i += 2) {
        const imageRow = document.createElement('div');
        imageRow.classList.add('image-row');

        const image1 = product.images[i];
        const imgElement1 = document.createElement('img');
        imgElement1.src = image1.image;
        imgElement1.alt = `${product.title} Image`;
        imageRow.appendChild(imgElement1);

        const image2 = product.images[i + 1];
        if (image2) {
            const imgElement2 = document.createElement('img');
            imgElement2.src = image2.image;
            imgElement2.alt = `${product.title} Image`;
            imageRow.appendChild(imgElement2);
        }

        productImageDiv.appendChild(imageRow);
        }
        
        productCard.innerHTML = `
        <h3>${product.title}</h3>
        <p>${product.description}</p>
        <p>Price: $${product.price}</p>
        ${productImageDiv.outerHTML}
        <div>
        </div>
        <button onclick=saveData(${product.id})>Sepete Ekle</button>
        `;

        productContainer.appendChild(productCard);
    });
    
}


window.onload = displayProducts;
     