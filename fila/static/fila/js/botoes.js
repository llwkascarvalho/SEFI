document.addEventListener("DOMContentLoaded", function() {
    const btnExcluir = document.getElementById('excluir-solicitacao');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if(btnExcluir) {
        btnExcluir.addEventListener('click', () => {
            Swal.fire({
                title: 'Confirmar exclusão',
                text: 'Tem certeza que deseja excluir esta solicitação?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#30465F',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sim',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = btnExcluir.dataset.url;
                    
                    const csrfInput = document.createElement('input');
                    csrfInput.type = 'hidden';
                    csrfInput.name = 'csrfmiddlewaretoken';
                    csrfInput.value = csrfToken;
                    
                    form.appendChild(csrfInput);
                    document.body.appendChild(form);
                    form.submit();
                }
            });
        });
    }
});
