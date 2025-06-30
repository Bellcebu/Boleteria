document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const eventFilter = document.getElementById('eventFilter');
    const dateFilter = document.getElementById('dateFilter');
    const table = document.getElementById('commentsTable');
    const rows = table.querySelectorAll('tbody tr');

    function filterTable() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedEvent = eventFilter.value;
        const selectedDate = dateFilter.value;
        
        rows.forEach(row => {
            if (row.children.length === 1) return;
            
            const text = row.textContent.toLowerCase();
            const eventId = row.dataset.eventId;
            const rowDate = new Date(row.dataset.date);
            const today = new Date();
            
            let showRow = true;
            
            if (searchTerm && !text.includes(searchTerm)) {
                showRow = false;
            }
            if (selectedEvent && eventId !== selectedEvent) {
                showRow = false;
            }
            if (selectedDate) {
                const diffTime = today - rowDate;
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                switch(selectedDate) {
                    case 'today':
                        if (diffDays > 1) showRow = false;
                        break;
                    case 'week':
                        if (diffDays > 7) showRow = false;
                        break;
                    case 'month':
                        if (diffDays > 30) showRow = false;
                        break;
                }
            }
            row.style.display = showRow ? '' : 'none';
        });
    }

    searchInput.addEventListener('input', filterTable);
    eventFilter.addEventListener('change', filterTable);
    dateFilter.addEventListener('change', filterTable);

    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const commentId = this.dataset.commentId;
            const row = this.closest('tr');
            const eventTitle = row.querySelector('strong').textContent;
            const eventImage = row.querySelector('.event-image, .no-image');
            const username = row.querySelectorAll('strong')[1].textContent;
            const email = row.querySelector('.text-muted').textContent;
            const title = row.querySelectorAll('strong')[2].textContent;
            const text = row.querySelector('.comment-content').title || row.querySelector('.comment-content').textContent;
            const date = row.querySelector('.badge').textContent;
            const time = row.querySelectorAll('.text-muted')[2].textContent;
            
            document.getElementById('commentDetails').innerHTML = `
                <div class="row">
                    <div class="col-md-4">
                        <h6><i class="bi bi-calendar-event me-2"></i>Evento</h6>
                        <div class="d-flex align-items-center mb-3">
                            ${eventImage.outerHTML}
                            <div class="ms-2">
                                <strong>${eventTitle}</strong>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <h6><i class="bi bi-person me-2"></i>Usuario</h6>
                        <div class="mb-3">
                            <strong>${username}</strong><br>
                            <small class="text-muted">${email}</small>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <h6><i class="bi bi-clock me-2"></i>Fecha</h6>
                        <div class="mb-3">
                            <span class="badge bg-secondary">${date}</span><br>
                            <small class="text-muted">${time}</small>
                        </div>
                    </div>
                </div>
                <hr>
                <h6><i class="bi bi-chat-square-text me-2"></i>Comentario</h6>
                <div class="comment-detail">
                    <h6 class="text-primary">${title}</h6>
                    <p class="mb-0">${text}</p>
                </div>
            `;
        });
    });

    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const commentId = this.dataset.commentId;
            const title = this.dataset.title;
            const user = this.dataset.user;
            const event = this.dataset.event;
            
            document.getElementById('deleteCommentId').value = commentId;
            document.getElementById('commentToDelete').innerHTML = `
                <strong>Título:</strong> ${title}<br>
                <strong>Usuario:</strong> ${user}<br>
                <strong>Evento:</strong> ${event}
            `;
            
            const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
            deleteModal.show();
        });
    });
});
