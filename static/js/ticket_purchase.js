document.addEventListener('DOMContentLoaded', function () {
    const quantityInput = document.getElementById('id_quantity');
    const decreaseBtn = document.getElementById('decrease-qty');
    const increaseBtn = document.getElementById('increase-qty');
    const totalPriceElement = document.getElementById('total-price');
    const quantityDisplayElement = document.getElementById('quantity-display');

    function updateTotalPrice() {
        const quantity = parseInt(quantityInput.value) || 1;
        const total = (quantity * UNIT_PRICE).toFixed(2);
        totalPriceElement.textContent = total;
        quantityDisplayElement.textContent = quantity;

        decreaseBtn.disabled = quantity <= 1;
        increaseBtn.disabled = quantity >= MAX_QUANTITY;
    }

    decreaseBtn.addEventListener('click', function () {
        let value = parseInt(quantityInput.value) || 1;
        if (value > 1) {
            quantityInput.value = value - 1;
            updateTotalPrice();
        }
    });

    increaseBtn.addEventListener('click', function () {
        let value = parseInt(quantityInput.value) || 1;
        if (value < MAX_QUANTITY) {
            quantityInput.value = value + 1;
            updateTotalPrice();
        }
    });

    quantityInput.addEventListener('input', function () {
        let value = parseInt(this.value) || 1;
        value = Math.min(Math.max(value, 1), MAX_QUANTITY);
        this.value = value;
        updateTotalPrice();
    });

    document.getElementById('purchase-form').addEventListener('submit', function (e) {
        const quantity = parseInt(quantityInput.value) || 1;

        if (quantity < 1 || quantity > MAX_QUANTITY) {
            e.preventDefault();
            alert(`Por favor, selecciona entre 1 y ${MAX_QUANTITY} entradas.`);
            return false;
        }

        const total = (quantity * UNIT_PRICE).toFixed(2);
        const confirmMessage = `¿Confirmas la compra de ${quantity} entrada(s) por un total de $${total}?`;

        if (!confirm(confirmMessage)) {
            e.preventDefault();
            return false;
        }
    });

    updateTotalPrice();
});
