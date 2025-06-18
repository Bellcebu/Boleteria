lucide.createIcons();

  document.addEventListener('click', () => {
    document.getElementById('notifDropdown')?.classList.remove('show');
    document.getElementById('userDropdown')?.classList.remove('show');
  });

  document.getElementById('notifButton')?.addEventListener('click', (e) => {
    e.stopPropagation();
    document.getElementById('notifDropdown').classList.toggle('show');
    document.getElementById('userDropdown')?.classList.remove('show');
  });

  document.getElementById('userButton')?.addEventListener('click', (e) => {
    e.stopPropagation();
    document.getElementById('userDropdown').classList.toggle('show');
    document.getElementById('notifDropdown')?.classList.remove('show');
  });