document.addEventListener('DOMContentLoaded', function() {
    const scrollIndicator = document.querySelector('.scroll-indicator');
    const eventsSection = document.querySelector('.events-section');

    if (scrollIndicator && eventsSection) {
        scrollIndicator.addEventListener('click', function() {
            eventsSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    }

    const heroSection = document.querySelector('.hero-section');
    const heroImage = document.querySelector('.hero-image');
    
    if (heroSection) {
        let ticking = false;
        
        function updateParallax() {
            const scrolled = window.pageYOffset;
            const heroHeight = heroSection.offsetHeight;
    
            if (scrolled < heroHeight) {
                const parallax = scrolled * 0.3; 
                
                const heroBackground = document.querySelector('.hero-background');
                if (heroBackground) {
                    heroBackground.style.transform = `translateY(${parallax}px)`;
                }
            }
            
            ticking = false;
        }

        window.addEventListener('scroll', function() {
            if (!ticking) {
                requestAnimationFrame(updateParallax);
                ticking = true;
            }
        });
    }