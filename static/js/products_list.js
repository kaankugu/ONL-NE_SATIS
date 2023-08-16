function saveData(productId) {
    console.log('productId')
    const quantitySelect = document.getElementById('quantitySelect' + productId);
    const selectedQuantity = parseInt(quantitySelect.value);
    if (selectedQuantity < 1 || isNaN(selectedQuantity)) {
        alert('Geçerli bir ürün adedi seçiniz.');
        return;
    } 
 
    const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
    for (let i = 0; i < selectedQuantity; i++) {
        cartItems.push(productId);
    }

    localStorage.setItem('cartItems', JSON.stringify(cartItems));
    alert('Ürün(ler) sepete eklendi!');
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

    const productsPerRow = 4;
    const imagesPerSlide = 4;

    const productContainer = document.getElementById('product-container');
    productContainer.classList.add('product-container');

    products.forEach((product) => {
        const imagesCount = product.images.length;

        

        const productCard = document.createElement('div');
        productCard.classList.add('product-card');

        const quantitySelect = document.createElement('select');
        quantitySelect.classList.add('quantity-select');
        quantitySelect.id = 'quantitySelect' + product.id;
        for (let i = 1; i <= 10; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = i;
            quantitySelect.appendChild(option);
        }

        const productImageDiv = document.createElement('div');
        productImageDiv.classList.add('product-images-slider');

        const slideContainer = document.createElement('div');
        slideContainer.classList.add('slide-container');

        const totalSlides = Math.ceil(imagesCount / imagesPerSlide);

        for (let slideIndex = 0; slideIndex < totalSlides; slideIndex++) {
            const slide = document.createElement('div');
            slide.classList.add('slide');

            const imageRow = document.createElement('div');
            imageRow.classList.add('image-row');

            for (let i = slideIndex * imagesPerSlide; i < (slideIndex + 1) * imagesPerSlide; i++) {
                if (i >= imagesCount) {
                    break;
                }

                const imgElement = document.createElement('img');
                imgElement.src = product.images[i].image;
                imgElement.alt = `${product.title} Image`;

                imageRow.appendChild(imgElement);
            }

            slide.appendChild(imageRow);
            slideContainer.appendChild(slide);
        }

        productImageDiv.appendChild(slideContainer);
        productCard.appendChild(productImageDiv);

        productCard.innerHTML = `
            <h3>Ürün Başlığı : ${product.title}</h3>
            <p>Ürün Açıklaması : ${product.description}</p>
            <p class="price">Fiyat: $${product.price}</p>
            <div class="quantity-select">
                <label>Adet:</label>
                ${quantitySelect.outerHTML}
           
            </div> 
            ${productImageDiv.outerHTML}
            <button onclick="saveData(${product.id})">Sepete Ekle</button>
        `;

        productContainer.appendChild(productCard);
    });

    window.onload = () => {
        displayProducts();
    
        let slideIndex = 0;
        const slides = document.querySelectorAll('.slide');
    
        setInterval(() => {
            const totalSlides = slides.length;
            slideIndex = (slideIndex + 1) % totalSlides;
            const translateXValue = -slideIndex * 100;
            slides.forEach(slide => {
                slideContainer.style.transform = `translateX(${translateXValue}%)`;
            });
        }, 3000);
    };
}
window.onload = displayProducts;

