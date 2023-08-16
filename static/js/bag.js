const productContainer = document.getElementById('productList'); // Ürünlerin ekleneceği alana erişim
function createPrdList(data, productCount) {
    const groupedData = {};
       
    // Verilerin kesilmeden gruplandırılması
    data.forEach(item => {
        const productId = item.product;
        if (!groupedData[productId]) {
            groupedData[productId] = [];
        }
        groupedData[productId].push(item);
    });

    for (const productId in groupedData) {
        if (groupedData.hasOwnProperty(productId)) {
            const productGroup = groupedData[productId];
            
            const card = createProductCard(productGroup, productCount);
            productContainer.appendChild(card);
        }
    }
}


function createProductCard(productGroup, productCount) {
    console.log("DATA3",productGroup)

    const card = document.createElement('div');
    card.classList.add('product-card');
    const productName = document.createElement('h2');
    productName.textContent = productGroup[1][0]?.title;
    

    const productDescription = document.createElement('p');
    productDescription.textContent = productGroup[1][0]?.description;

    const productPrice = document.createElement('p');
    productPrice.textContent = 'Price: ' + (productGroup[1][0]?.price || 'N/A') + ' TL'; 
    

    // Kartın içeriğini kart elementine ekleyin
    card.appendChild(productName);
    card.appendChild(productDescription);
    card.appendChild(productPrice);

    for (let i = 0; i < productGroup[0].length; i++) {
        const productImage = document.createElement('img');
        productImage.src = productGroup[0][i].image; 
        productImage.alt = productGroup[0][i].title;
        card.appendChild(productImage); 
    }

    // Ürün adedini ekleyin
    const productCountElement = document.createElement('p');
    productCountElement.textContent = 'Adet: ' + productCount;
    card.appendChild(productCountElement);

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Sil';
    deleteButton.addEventListener('click', () => {
        removeProduct(productGroup[1][0].id); 
        location.reload(); 
    });

    card.appendChild(deleteButton);

    return card;
}




function removeProduct(productId) {
    console.log(productId)
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
                console.log("DATA2",data)

                const card = createPrdList(Object.values(data), productCount); // Verilere göre kartı oluşturalım
                

                productList.appendChild(card);
                console.log(productList)
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