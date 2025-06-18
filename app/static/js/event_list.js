function confirmDelete(eventId, eventTitle) {
    const modal = document.getElementById('deleteModal');
    const titleSpan = document.getElementById('eventTitle');
    const deleteForm = document.getElementById('deleteForm');
  
    deleteForm.action = `/admin-panel/events/${eventId}/borrar/`;
  
    deleteForm.innerHTML = `
      <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">
      <button type="submit" class="action-btn confirm-delete">
        <i class="fas fa-trash"></i> Sí, eliminar
      </button>
    `;
  
    titleSpan.textContent = eventTitle;
    modal.style.display = 'flex';
  }
  
  function closeDeleteModal() {
    document.getElementById('deleteModal').style.display = 'none';
  }
  
  function getCookie(name) {
    let value = null;
    document.cookie.split(';').forEach(cookie => {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        value = decodeURIComponent(cookie.slice(name.length + 1));
      }
    });
    return value;
  }
  
  window.onclick = e => {
    const modal = document.getElementById('deleteModal');
    if (e.target === modal) closeDeleteModal();
  };
  