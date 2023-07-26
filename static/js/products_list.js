function saveData(productId) {
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
