// Funcionalidad del navbar
document.addEventListener('DOMContentLoaded', function() {
  const navbar = document.getElementById('navbar');
  let isExpanded = false;
  
  // Función para actualizar el navbar según el scroll
  function updateNavbar() {
    const y = window.scrollY;
    const noScrollPage = document.querySelector('.no-scroll-page');
   
    // Si es página sin scroll, mantener expandida
    if (noScrollPage) {
      if (!isExpanded) {
        navbar.classList.add('expanded');
        isExpanded = true;
      }
      return;
    }
   
    // Lógica normal para páginas con scroll
    if (y > 50 && !isExpanded) {
      navbar.classList.add('expanded');
      isExpanded = true;
    } else if (y <= 50 && isExpanded) {
      navbar.classList.remove('expanded');
      isExpanded = false;
    }
  }
  
  // Event listeners para el scroll
  window.addEventListener('scroll', updateNavbar);
  window.addEventListener('resize', updateNavbar);
 
  // Ejecutar al cargar la página
  updateNavbar();
  
  // Funcionalidad de los dropdowns
  document.querySelectorAll('.dropdown-toggle').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault();
      const dropdownMenu = btn.nextElementSibling;
      const isShown = dropdownMenu.classList.contains('show');
     
      // Cerrar cualquier otro dropdown abierto
      document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
        if(menu !== dropdownMenu) {
          menu.classList.remove('show');
        }
      });
     
      // Toggle del dropdown actual
      if(!isShown) {
        dropdownMenu.classList.add('show');
      } else {
        dropdownMenu.classList.remove('show');
      }
    });
  });
  
  // Cerrar dropdown si se hace click fuera
  document.addEventListener('click', e => {
    if(!e.target.closest('.dropdown')) {
      document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
        menu.classList.remove('show');
      });
    }
  });
});