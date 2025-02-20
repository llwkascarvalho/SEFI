document.getElementById('btn-marcar-entregue').addEventListener('click', function() {
    Swal.fire({
        title: 'Confirmar entrega',
        text: 'Tem certeza que deseja marcar esta solicitação como entregue?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#30465F',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sim',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const url = this.dataset.url || window.location.href + 'marcar-entregue/';
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Accept': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => Promise.reject(data));
                }
                return response.json();
            })
            .then(data => {
                Swal.fire({
                    title: 'Sucesso!',
                    text: data.message,
                    icon: 'success'
                }).then(() => {
                    window.location.reload();
                });
            })
            .catch(error => {
                Swal.fire({
                    title: 'Erro!',
                    text: error.message || 'Ocorreu um erro ao processar sua solicitação.',
                    icon: 'error'
                });
            });
        }
    });
});
