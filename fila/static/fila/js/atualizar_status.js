document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.list .item').forEach(item => {
        item.addEventListener('click', function() {
            const novoStatus = this.dataset.value;
            const url = this.dataset.url;
            const statusAtual = document.querySelector('.selected.default span').textContent;

            if (novoStatus === statusAtual) {
                return;
            }

            Swal.fire({
                title: 'Confirmar alteração?',
                text: `Deseja alterar o status para "${this.textContent}"?`,
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#30465F',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sim',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(url, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: `novo_status=${novoStatus}`
                    })
                    .then(response => response.json())
                    .then(data => {
                        if(data.success) {
                            Swal.fire({
                                title: 'Sucesso!',
                                text: data.message,
                                icon: 'success',
                                confirmButtonColor: '#30465F',
                                confirmButtonText: 'OK'
                            }).then(() => {
                                window.location.reload();
                            });
                        } else {
                            Swal.fire({
                                title: 'Erro!',
                                text: data.message,
                                icon: 'error',
                                confirmButtonText: 'OK'
                            });
                        }
                    })
                    .catch(error => {
                        console.error('Erro:', error);
                        Swal.fire({
                            title: 'Erro!',
                            text: 'Ocorreu um erro ao atualizar o status',
                            icon: 'error',
                            confirmButtonText: 'OK'
                        });
                    });
                }
            });
        });
    });
}); 