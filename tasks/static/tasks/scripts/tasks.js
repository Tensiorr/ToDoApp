document.addEventListener('DOMContentLoaded', function () {

    function setDeleteAction(taskId) {
        const form = document.getElementById('deleteForm');
        form.action = `/tasks/delete/${taskId}/`;
    }

    function getSelectedTags() {
        return Array.from(document.querySelectorAll('input[name="tags"]:checked'))
            .map(cb => cb.value);
    }

    function buildTagParams() {
        const params = new URLSearchParams();
        getSelectedTags().forEach(tag => params.append('tags', tag));
        return params.toString();
    }

    function reloadTaskList() {
        fetch(`?${buildTagParams()}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('tasks-container').innerHTML = data.html;
            insertCSRFTokenIntoForms();
            syncTagStyles();
        });
    }

    function insertCSRFTokenIntoForms() {
        const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        document.querySelectorAll('form[method="post"]').forEach(form => {
            if (!form.querySelector('input[name="csrfmiddlewaretoken"]')) {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'csrfmiddlewaretoken';
                input.value = token;
                form.appendChild(input);
            }
        });
    }

    function syncTagStyles() {
        document.querySelectorAll('input[name="tags"]').forEach(checkbox => {
            const label = document.querySelector(`label[for="${checkbox.id}"]`);
            if (label) {
                if (checkbox.checked) {
                    label.classList.remove('btn-outline-primary');
                    label.classList.add('btn-primary');
                } else {
                    label.classList.remove('btn-primary');
                    label.classList.add('btn-outline-primary');
                }
            }
        });
    }

    // Event delegacja dla status buttonów
    document.addEventListener('click', function (e) {
        const button = e.target.closest('.status-form button');
        if (!button) return;

        e.preventDefault();

        const formDiv = button.closest('.status-form');
        const taskId = formDiv.dataset.taskId;
        const newStatus = button.dataset.status;

        fetch(`/tasks/status/${taskId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content'),
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ status: newStatus })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                reloadTaskList();
            } else {
                alert("Błąd przy aktualizacji statusu: " + data.error);
            }
        })
        .catch(err => {
            console.error("Błąd sieci", err);
            alert("Wystąpił błąd sieci");
        });
    });

    // Event delegacja do tagów
    document.addEventListener('change', function (e) {
        if (e.target.name === 'tags') {
            reloadTaskList();
        }
    });

    // Inicjalizacja
    insertCSRFTokenIntoForms();
    syncTagStyles();
});
document.addEventListener('click', function(e) {
    const btn = e.target.closest('button[data-bs-toggle="modal"][data-bs-target="#deleteModal"]');
    if (!btn) return;
    const taskId = btn.getAttribute('data-task-id');
    if (!taskId) return;
    const form = document.getElementById('deleteForm');
    form.action = `/tasks/delete/${taskId}/`;
});