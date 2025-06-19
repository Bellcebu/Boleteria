// ===============================
// KRAI-inspired Home Page JavaScript
// ===============================

document.addEventListener('DOMContentLoaded', function() {
    initializeAnimations();
    setupEventCards();
    setupNavigation();
    setupScrollEffects();
    setupParallax();
});

// ===============================
// Animation Initialization
// ===============================

function initializeAnimations() {
    // Animate hero elements on load
    const heroTitle = document.querySelector('.hero-title');
    const heroSubtitle = document.querySelector('.hero-subtitle');
    const heroActions = document.querySelector('.hero-actions');
    const heroStats = document.querySelector('.hero-stats');
    
    if (heroTitle) {
        heroTitle.style.opacity = '0';
        heroTitle.style.transform = 'translateY(50px)';
        
        setTimeout(() => {
            heroTitle.style.transition = 'all 1s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            heroTitle.style.opacity = '1';
            heroTitle.style.transform = 'translateY(0)';
        }, 300);
    }
    
    if (heroSubtitle) {
        heroSubtitle.style.opacity = '0';
        heroSubtitle.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            heroSubtitle.style.transition = 'all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            heroSubtitle.style.opacity = '1';
            heroSubtitle.style.transform = 'translateY(0)';
        }, 600);
    }
    
    if (heroActions) {
        heroActions.style.opacity = '0';
        heroActions.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            heroActions.style.transition = 'all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            heroActions.style.opacity = '1';
            heroActions.style.transform = 'translateY(0)';
        }, 900);
    }
    
    if (heroStats) {
        heroStats.style.opacity = '0';
        heroStats.style.transform = 'translateX(50px)';
        
        setTimeout(() => {
            heroStats.style.transition = 'all 1s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            heroStats.style.opacity = '1';
            heroStats.style.transform = 'translateX(0)';
        }, 1200);
    }
    
    // Animate event cards
    animateEventCards();
}

function animateEventCards() {
    const eventCards = document.querySelectorAll('.event-card');
    
    eventCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(50px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 1500 + (index * 200));
    });
}

// ===============================
// Event Cards Interactions
// ===============================

function setupEventCards() {
    const eventCards = document.querySelectorAll('.event-card');
    
    eventCards.forEach(card => {
        // Add hover sound effect (visual feedback)
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-15px) scale(1.02)';
            
            // Add subtle glow effect
            this.style.boxShadow = '0 25px 50px rgba(255, 107, 53, 0.2), 0 0 0 1px rgba(255, 255, 255, 0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = 'none';
        });
        
        // Add click ripple effect
        card.addEventListener('click', function(e) {
            createRippleEffect(e, this);
        });
        
        // Add card tilt effect based on mouse position
        card.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            this.style.transform = `translateY(-15px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
        });
    });
}

function createRippleEffect(event, element) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple');
    
    // Add ripple styles
    ripple.style.position = 'absolute';
    ripple.style.borderRadius = '50%';
    ripple.style.background = 'rgba(255, 107, 53, 0.3)';
    ripple.style.transform = 'scale(0)';
    ripple.style.animation = 'ripple 0.6s linear';
    ripple.style.pointerEvents = 'none';
    
    element.style.position = 'relative';
    element.style.overflow = 'hidden';
    element.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Add ripple animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ===============================
// Navigation Setup
// ===============================

function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remove active class from all items
            navItems.forEach(nav => nav.classList.remove('active'));
            
            // Add active class to clicked item
            this.classList.add('active');
            
            // Add click animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });
    
    // Smooth scroll to eventos section
    const explorarBtn = document.querySelector('a[href="#eventos"]');
    if (explorarBtn) {
        explorarBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const eventosSection = document.getElementById('eventos');
            if (eventosSection) {
                eventosSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    }
}

// ===============================
// Scroll Effects
// ===============================

function setupScrollEffects() {
    let ticking = false;
    
    function updateScrollEffects() {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5;
        
        // Parallax effect for background elements
        const mountain = document.querySelector('.mountain');
        const clouds = document.querySelector('.clouds');
        
        if (mountain) {
            mountain.style.transform = `translateY(${rate * 0.3}px) translateX(${rate * 0.1}px)`;
        }
        
        if (clouds) {
            clouds.style.transform = `translateY(${rate * 0.2}px) translateX(${rate * 0.05}px)`;
        }
        
        // Update navigation visibility
        const bottomNav = document.querySelector('.bottom-nav');
        if (bottomNav) {
            if (scrolled > 100) {
                bottomNav.style.opacity = '1';
                bottomNav.style.transform = 'translateX(-50%) translateY(0)';
            } else {
                bottomNav.style.opacity = '0.7';
                bottomNav.style.transform = 'translateX(-50%) translateY(10px)';
            }
        }
        
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateScrollEffects);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestTick);
}

// ===============================
// Parallax Effects
// ===============================

function setupParallax() {
    const hero = document.querySelector('.hero-section');
    const eventsSection = document.querySelector('.events-section');
    
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe sections
    if (eventsSection) {
        observer.observe(eventsSection);
    }
    
    // Stats counter animation
    const statNumbers = document.querySelectorAll('.stat-number');
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                statsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    statNumbers.forEach(stat => {
        statsObserver.observe(stat);
    });
}

function animateCounter(element) {
    const text = element.textContent;
    const number = parseInt(text.replace(/\D/g, ''));
    const suffix = text.replace(/\d/g, '');
    
    if (isNaN(number)) return;
    
    let current = 0;
    const increment = number / 30;
    const timer = setInterval(() => {
        current += increment;
        if (current >= number) {
            current = number;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current) + suffix;
    }, 50);
}

// ===============================
// Dynamic Background Effects
// ===============================

function setupDynamicBackground() {
    const stars = document.querySelector('.stars');
    const mouse = { x: 0, y: 0 };
    
    // Mouse tracking for interactive effects
    document.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX / window.innerWidth;
        mouse.y = e.clientY / window.innerHeight;
        
        // Update background elements based on mouse position
        if (stars) {
            const translateX = (mouse.x - 0.5) * 20;
            const translateY = (mouse.y - 0.5) * 20;
            stars.style.transform = `translate(${translateX}px, ${translateY}px)`;
        }
    });
    
    // Dynamic gradient based on time
    setInterval(() => {
        const time = Date.now() * 0.0001;
        const hue1 = Math.sin(time) * 30 + 240;
        const hue2 = Math.sin(time + Math.PI) * 30 + 280;
        
        document.documentElement.style.setProperty(
            '--primary-gradient',
            `linear-gradient(135deg, hsl(${hue1}, 70%, 15%) 0%, hsl(${hue2}, 60%, 25%) 50%, hsl(${hue1 + 20}, 50%, 35%) 100%)`
        );
    }, 5000);
}

// ===============================
// Performance Optimizations
// ===============================

function setupPerformanceOptimizations() {
    // Lazy load event card images
    const images = document.querySelectorAll('.event-image img');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
    
    // Debounce resize events
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            handleResize();
        }, 250);
    });
}

function handleResize() {
    // Recalculate positions and sizes on resize
    const heroStats = document.querySelector('.hero-stats');
    const eventCards = document.querySelectorAll('.event-card');
    
    // Reset transforms to recalculate
    if (window.innerWidth <= 768) {
        eventCards.forEach(card => {
            card.style.transform = 'none';
        });
    }
}

// ===============================
// Accessibility Enhancements
// ===============================

function setupAccessibility() {
    // Add keyboard navigation for cards
    const eventCards = document.querySelectorAll('.event-card');
    
    eventCards.forEach(card => {
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', `Ver detalles del evento ${card.querySelector('.event-title')?.textContent}`);
        
        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const link = card.querySelector('.btn-explore');
                if (link) {
                    link.click();
                }
            }
        });
        
        // Focus styles
        card.addEventListener('focus', () => {
            card.style.outline = '2px solid #ff6b35';
            card.style.outlineOffset = '4px';
        });
        
        card.addEventListener('blur', () => {
            card.style.outline = 'none';
        });
    });
    
    // Reduce motion for users who prefer it
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        const style = document.createElement('style');
        style.textContent = `
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        `;
        document.head.appendChild(style);
    }
}

// ===============================
// Error Handling
// ===============================

function setupErrorHandling() {
    // Handle missing elements gracefully
    window.addEventListener('error', (e) => {
        console.warn('Non-critical error handled:', e.message);
    });
    
    // Fallback for unsupported features
    if (!window.IntersectionObserver) {
        // Fallback for older browsers
        const eventCards = document.querySelectorAll('.event-card');
        eventCards.forEach(card => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        });
    }
}

// ===============================
// Initialize All Features
// ===============================

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    try {
        initializeAnimations();
        setupEventCards();
        setupNavigation();
        setupScrollEffects();
        setupParallax();
        setupDynamicBackground();
        setupPerformanceOptimizations();
        setupAccessibility();
        setupErrorHandling();
        
        // Hide loading indicator if exists
        const loading = document.querySelector('.loading');
        if (loading) {
            loading.style.opacity = '0';
            setTimeout(() => loading.remove(), 500);
        }
        
        console.log('🎉 MiEvento home page initialized successfully!');
    } catch (error) {
        console.error('Error initializing home page:', error);
        // Ensure basic functionality works even if some features fail
        const eventCards = document.querySelectorAll('.event-card');
        eventCards.forEach(card => {
            card.style.opacity = '1';
            card.style.transform = 'none';
        });
    }
});

// ===============================
// Additional Utility Functions
// ===============================

// Smooth scroll polyfill for older browsers
if (!window.CSS || !CSS.supports('scroll-behavior', 'smooth')) {
    const scrollToElement = (element, duration = 800) => {
        const start = window.pageYOffset;
        const target = element.getBoundingClientRect().top + start;
        const distance = target - start;
        let startTime = null;
        
        const animation = (currentTime) => {
            if (startTime === null) startTime = currentTime;
            const timeElapsed = currentTime - startTime;
            const run = easeInOutQuad(timeElapsed, start, distance, duration);
            window.scrollTo(0, run);
            if (timeElapsed < duration) requestAnimationFrame(animation);
        };
        
        requestAnimationFrame(animation);
    };
    
    const easeInOutQuad = (t, b, c, d) => {
        t /= d / 2;
        if (t < 1) return c / 2 * t * t + b;
        t--;
        return -c / 2 * (t * (t - 2) - 1) + b;
    };
    
    // Override smooth scroll links
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            if (target) scrollToElement(target);
        });
    });
}

// Export functions for potential external use
window.MiEventoHome = {
    animateEventCards,
    createRippleEffect,
    animateCounter
};