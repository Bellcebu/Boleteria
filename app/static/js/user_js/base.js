document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.getElementById('navbar');
    const hoverZone = document.getElementById('navbar-hover-zone');
    const currentPath = window.location.pathname;
    let isScrolled = false;
   
    const isHomePage = currentPath === '/' || currentPath === '/home/';
   
    if (!isHomePage) {
        navbar.classList.add('expanded');
        navbar.classList.add('hidden');
       
        function showNavbar() {
            navbar.classList.remove('hidden');
        }
       
        function hideNavbar() {
            navbar.classList.add('hidden');
        }
       
        navbar.addEventListener('mouseenter', showNavbar);
        navbar.addEventListener('mouseleave', hideNavbar);
        if (hoverZone) {
            hoverZone.addEventListener('mouseenter', showNavbar);
            hoverZone.addEventListener('mouseleave', hideNavbar);
        }
       
        navbar.addEventListener('focusin', showNavbar);
        navbar.addEventListener('focusout', function(e) {
            setTimeout(() => {
                if (!navbar.contains(document.activeElement)) {
                    hideNavbar();
                }
            }, 100);
        });
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
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    const unreadItems = document.querySelectorAll('.notification-item.unread');
    const badge = document.querySelector('.notification-badge');
    const headerCount = document.querySelector('.dropdown-header small');
    
    const unreadCount = unreadItems.length;
    
    if (unreadCount > 0) {
        badge.textContent = unreadCount;
        badge.style.display = 'flex';
        if (headerCount) {
            headerCount.textContent = `${unreadCount} nueva${unreadCount > 1 ? 's' : ''}`;
        }
    } else {
        badge.style.display = 'none';
        if (headerCount) {
            headerCount.textContent = 'Sin nuevas';
        }
    }
    
    unreadItems.forEach(item => {
        item.style.fontWeight = 'bold';
        item.style.backgroundColor = '#f8f9ff';
        item.style.borderLeft = '3px solid #667eea';
    });
});