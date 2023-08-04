function createProductCard(data, productCount) {
    const card = document.createElement('div');
    card.classList.add('product-card');

    // Kartın içeriği
    const productName = document.createElement('h2');
    productName.textContent = data.title; // API'den dönen veriye göre ürün adını güncelleyin

    const productDescription = document.createElement('p');
    productDescription.textContent = data.description; // API'den dönen veriye göre ürün açıklamasını güncelleyin

    const productPrice = document.createElement('p');
    productPrice.textContent = 'Price: ' + data.price + ' TL'; // API'den dönen veriye göre ürün fiyatını güncelleyin
    
    // Kartın içeriğini kart elementine ekleyin
    card.appendChild(productName);
    card.appendChild(productDescription);
    card.appendChild(productPrice);

    // Ürün resmini ekleyin
    const productImage = document.createElement('img');
    productImage.src = data.image; // API'den dönen veriye göre ürün resminin URL'sini güncelleyin
    productImage.alt = data.title; // Ürün adını alternatif metin olarak ekleyebilirsiniz

    // Kartın içeriğine ürün resmini ekleyin
    card.appendChild(productImage);

    // Ürün adedini ekleyin
    const productCountElement = document.createElement('p');
    productCountElement.textContent = 'Adet: ' + productCount;
    card.appendChild(productCountElement);
    
    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Sil';
    deleteButton.addEventListener('click', () => {
        removeProduct(data.id);
        location.reload(); // Sayfayı yenileyerek güncel ürün listesini göster
    });


    card.appendChild(deleteButton);


    return card;
}

function removeProduct(productId) {
    const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
    const index = cartItems.indexOf(productId);
    if (index !== -1) {
        cartItems.splice(index, 1);
        localStorage.setItem('cartItems', JSON.stringify(cartItems));
    }
}

window.onload = function() {
    const apiUrl = '/api/products/'; // API adresini burada değiştirin
    const productList = document.getElementById('productList');
    const savedProducts = JSON.parse(localStorage.getItem('cartItems')) || [];

    if (savedProducts && savedProducts.length > 0) {
        const uniqueProducts = Array.from(new Set(savedProducts));
        uniqueProducts.forEach(product => {
            const productCount = savedProducts.filter(item => item === product).length;

            // API'ye GET isteği atalım
            fetch(`${apiUrl}${product}/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('API isteği başarısız oldu.');
                }
                return response.json();
            })
            .then(data => {
                const card = createProductCard(data, productCount); // Verilere göre kartı oluşturalım
                productList.appendChild(card);
            })
            .catch(error => {
                console.error('API isteği sırasında bir hata oluştu:', error);
            });
        });
    } else {
        const li = document.createElement('li');
        li.textContent = 'Henüz ürün yok.';
        productList.appendChild(li);
    }
};