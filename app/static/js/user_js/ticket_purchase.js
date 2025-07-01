const { UNIT_PRICE, PROMOTIONS } = window.TICKET_DATA;
let currentDiscount = 0;

function updateTotal() {
    const qty = parseInt(document.getElementById('quantity').value) || 1;
    let total = qty * UNIT_PRICE;
   
    if (currentDiscount > 0) {
        const discount = (total * currentDiscount) / 100;
        total -= discount;
        document.getElementById('discount-info').style.display = 'block';
        document.getElementById('discount-text').textContent = `${currentDiscount}% (-$${discount.toFixed(2)})`;
    } else {
        document.getElementById('discount-info').style.display = 'none';
    }
   
    document.getElementById('total').textContent = total.toFixed(2);
}

document.getElementById('quantity').addEventListener('input', updateTotal);

document.getElementById('check-promo').addEventListener('click', function() {
    const code = document.getElementById('promotion_code').value.trim().toUpperCase();
    const status = document.getElementById('promo-status');
   
    if (!code) {
        status.innerHTML = '<small class="text-warning">Ingresa un código</small>';
        currentDiscount = 0;
        updateTotal();
        return;
    }
   
    if (PROMOTIONS[code]) {
        currentDiscount = PROMOTIONS[code].discount;
        status.innerHTML = `<small class="text-success">✓ ${currentDiscount}% descuento aplicado</small>`;
    } else {
        currentDiscount = 0;
        status.innerHTML = '<small class="text-danger">✗ Código no válido</small>';
    }
   
    updateTotal();
});

updateTotal();