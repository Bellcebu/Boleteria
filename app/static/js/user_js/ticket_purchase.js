const UNIT_PRICE = window.TICKET_DATA.UNIT_PRICE;
const PROMOTIONS = window.TICKET_DATA.PROMOTIONS;

let currentDiscount = 0;

console.log('UNIT_PRICE:', UNIT_PRICE);
console.log('PROMOTIONS cargadas:', PROMOTIONS);

function updateTotal() {
    const qty = parseInt(document.getElementById('quantity').value) || 1;
    let total = qty * UNIT_PRICE;
    
    if (currentDiscount > 0) {
        const discount = (total * currentDiscount) / 100;
        total = total - discount;
        document.getElementById('discount-info').style.display = 'block';
        document.getElementById('discount-text').textContent = `${currentDiscount}% (-${discount.toFixed(2)})`;
    } else {
        document.getElementById('discount-info').style.display = 'none';
    }
    
    document.getElementById('total').textContent = total.toFixed(2);
}

document.getElementById('quantity').addEventListener('input', updateTotal);

document.getElementById('check-promo').addEventListener('click', function() {
    console.log('Click en verificar');
    
    const code = document.getElementById('promotion_code').value.trim().toUpperCase();
    const status = document.getElementById('promo-status');
    
    console.log('Código ingresado:', code);
    
    if (!code) {
        status.innerHTML = '<small class="text-warning">Ingresa un código</small>';
        currentDiscount = 0;
        updateTotal();
        return;
    }
    
    console.log('Buscando en PROMOTIONS:', PROMOTIONS);
    console.log('¿Existe el código?', PROMOTIONS.hasOwnProperty(code));
    
    if (PROMOTIONS.hasOwnProperty(code)) {
        const promo = PROMOTIONS[code];
        console.log('Promoción encontrada:', promo);
        
        if (promo.valid) {
            currentDiscount = promo.discount;
            status.innerHTML = `<small class="text-success">✓ ${currentDiscount}% descuento aplicado</small>`;
            console.log('Descuento aplicado:', currentDiscount);
        } else {
            currentDiscount = 0;
            status.innerHTML = '<small class="text-warning">⚠ Código expirado</small>';
        }
    } else {
        currentDiscount = 0;
        status.innerHTML = '<small class="text-danger">✗ Código no válido</small>';
        console.log('Código no encontrado');
    }
    
    updateTotal();
});

document.getElementById('promotion_code').addEventListener('input', function() {
    this.value = this.value.toUpperCase();
    currentDiscount = 0;
    document.getElementById('promo-status').innerHTML = '';
    updateTotal();
});

updateTotal();