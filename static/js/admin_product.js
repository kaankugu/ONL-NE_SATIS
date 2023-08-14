function update_button(item_id) {
    var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    fetch("/update-permission/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ id: item_id }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        window.location.reload();
    })
    .catch(error => {
        console.error(error);
    });
}
function delete_button(item_id) {
    var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    fetch("/api/products/" + item_id + "/", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ id: item_id }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        window.location.reload();
    })
    .catch(error => {
        console.error(error);
    });
}

 
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

    products.forEach(product => {
    const productCard = document.createElement('div');
        productCard.classList.add('product-card');
    
        const productContainer = document.getElementById('product-container');
        const Permission = product.permission;

        const permissionStatus = Permission ? 'Ürün yayında' : 'Ürün yayında değil';
        const permissionButtonText = Permission ? 'Yayını Kaldır' : 'Ürünü Yayınla';
       
 
                    
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
        <p class="price">Price: $${product.price}</p>
        <p class="permission-status">${permissionStatus}</p>
        ${productImageDiv.outerHTML}
        
        <div>

        <button class="update-button" onclick=update_button(${product.id})>${permissionButtonText}</button> <!-- Sınıf eklendi -->
        <button class="delete-button" onclick=Delete_button(${product.id})>Ürünü Sil </button> <!-- Sınıf eklendi -->
        
        </div>
        `;

        productContainer.appendChild(productCard);
    });
    
}


window.onload = displayProducts;
     