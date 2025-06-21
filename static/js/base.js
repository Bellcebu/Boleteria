document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.getElementById('navbar');
    let isScrolled = false;

    function updateNavbar() {
        const scrollY = window.scrollY;
        
        if (scrollY > 1000 && !isScrolled) {
            navbar.classList.add('expanded');
            isScrolled = true;
        } else if (scrollY <= 1000 && isScrolled) {
            navbar.classList.remove('expanded');
            isScrolled = false;
        }
    }

    let ticking = false;
    
    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(() => {
                updateNavbar();
                ticking = false;
            });
            ticking = true;
        }
    });

    updateNavbar();

    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert:not(.show)');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});