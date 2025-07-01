document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.getElementById('navbar');
    const currentPath = window.location.pathname;
    let isScrolled = false;
    let hideTimeout;
    
    const isHomePage = currentPath === '/' || currentPath === '/home/';
    
    if (!isHomePage) {
        navbar.classList.add('expanded');
        
        function showNavbar() {
            navbar.classList.remove('hidden');
            clearTimeout(hideTimeout);
        }
        
        function hideNavbar() {
            navbar.classList.add('hidden');
        }
        
        document.addEventListener('mousemove', function(e) {
            if (e.clientY <= 100 && navbar.classList.contains('hidden')) {
                showNavbar();
            }
        });
        
        navbar.addEventListener('mouseenter', showNavbar);
        
        navbar.addEventListener('mouseleave', function() {
            clearTimeout(hideTimeout);
            hideTimeout = setTimeout(hideNavbar, 2000);
        });
        
        hideTimeout = setTimeout(hideNavbar, 1000);
    }
    
    function updateNavbar() {
        if (!isHomePage) return;
        
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
    window.addEventListener('scroll', function() {
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
            new bootstrap.Alert(alert).close();
        });
    }, 5000);
});
