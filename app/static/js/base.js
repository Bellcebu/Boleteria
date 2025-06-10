<script>
  const notifBtn = document.getElementById('notifButton');
  const notifDropdown = document.getElementById('notifDropdown');

  notifBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    notifDropdown.classList.toggle('show');
  });

  document.addEventListener('click', () => {
    notifDropdown.classList.remove('show');
  });
</script>
