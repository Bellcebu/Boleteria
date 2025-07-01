document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.getElementById('navbar');
    const currentPath = window.location.pathname;
    let isScrolled = false;
    let lastScrollTop = 0;
    let hideTimeout;
    
    const isHomePage = currentPath === '/' || currentPath === '/home/';
    
    // Original navbar expansion logic
    if (!isHomePage) {
        navbar.classList.add('expanded');
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
    
    // Auto-hiding functions
    function showNavbar() {
        navbar.classList.remove('hidden');
        clearTimeout(hideTimeout);
    }
    
    function hideNavbar() {
        if (window.pageYOffset > 30) {
            navbar.classList.add('hidden');
        }
    }
    
    // Scroll handler
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        // Original expansion logic
        updateNavbar();
        
        // Auto-hiding logic
        if (currentScroll > lastScrollTop && currentScroll > 50) {
            // Scrolling down
            clearTimeout(hideTimeout);
            hideTimeout = setTimeout(hideNavbar, 0);
        } else {
            // Scrolling up
            showNavbar();
        }
        
        lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
    });
    
    // Mouse detection
    document.addEventListener('mousemove', function(e) {
        if (e.clientY <= 80) {
            showNavbar();
        }
    });
    
 navbar.addEventListener('mouseleave', function() {
    // Hide after 2 seconds regardless of scroll position
    // (but only if user has scrolled at least a little bit)
    if (window.pageYOffset > 30) {
        clearTimeout(hideTimeout);
        hideTimeout = setTimeout(hideNavbar, 2000);
    }
});
    
    // Initialize
    updateNavbar();
    
    // Alert auto-close
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert:not(.show)');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});