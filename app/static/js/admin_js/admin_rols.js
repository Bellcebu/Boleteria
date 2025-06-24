document.addEventListener('DOMContentLoaded', function() {
    const userSearch = document.getElementById('userSearch');
    const clearSearch = document.getElementById('clearSearch');
    const roleForm = document.getElementById('roleForm');
    const cancelAssign = document.getElementById('cancelAssign');
    const cardHeader = document.querySelector('.card');

    document.querySelectorAll('.assign-role-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const userData = {
                id: this.dataset.userId,
                username: this.dataset.username,
                currentRole: this.dataset.currentRole
            };
            loadUserForRoleEdit(userData);
        });
    });

    document.querySelectorAll('input[name="roleFilter"]').forEach(filter => {
        filter.addEventListener('change', function() {
            filterUsersByRole(this.value);
        });
    });

    userSearch.addEventListener('input', function() {
        filterTableBySearch(this.value.toLowerCase().trim());
    });

    clearSearch.addEventListener('click', function() {
        userSearch.value = '';
        showAllUsers();
        resetRoleForm();
    });

    cancelAssign.addEventListener('click', function() {
        resetRoleForm();
    });

    function loadUserForRoleEdit(userData) {
        document.getElementById('selectedUserId').value = userData.id;
        document.getElementById('selectedUserName').textContent = userData.username;
        
        const roleInfo = getRoleInfo(userData.currentRole);
        document.getElementById('currentRoleBadge').innerHTML = 
            `<span class="badge bg-${roleInfo.color}">${roleInfo.icon} ${roleInfo.name}</span>`;
        
        roleForm.style.display = 'block';
        cardHeader.classList.add('edit-mode');
        cardHeader.scrollIntoView({ behavior: 'smooth' });
    }

    function resetRoleForm() {
        roleForm.style.display = 'none';
        cardHeader.classList.remove('edit-mode');
        document.getElementById('roleSelect').value = '';
    }

    function filterUsersByRole(roleFilter) {
        document.querySelectorAll('.user-row').forEach(row => {
            row.style.display = (roleFilter === 'all' || row.dataset.role === roleFilter) ? '' : 'none';
        });
    }

    function filterTableBySearch(query) {
        if (!query) {
            showAllUsers();
            return;
        }
        
        document.querySelectorAll('.user-row').forEach(row => {
            const username = row.querySelector('strong').textContent.toLowerCase();
            const email = row.cells[1].textContent.toLowerCase();
            row.style.display = (username.includes(query) || email.includes(query)) ? '' : 'none';
        });
    }

    function showAllUsers() {
        document.querySelectorAll('.user-row').forEach(row => {
            row.style.display = '';
        });
    }

    function getRoleInfo(role) {
        const roles = {
            'admin': { color: 'primary', icon: '👑', name: 'Administrador' },
            'vendedor': { color: 'info', icon: '💼', name: 'Vendedor' },
            'usuario': { color: 'success', icon: '👤', name: 'Usuario' }
        };
        return roles[role] || roles['usuario'];
    }
});