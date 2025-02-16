document.getElementById('form-foto-perfil').addEventListener('submit', function(event) { 
    event.preventDefault(); 

    const fileInput = document.getElementById('foto_perfil'); 
    const file = fileInput.files[0]; 

    if (!file) { 
        Swal.fire({
            title: 'Erro',
            text: 'Nenhuma foto foi selecionada.',
            icon: 'error',
            confirmButtonText: 'OK',
            scrollbarPadding: false
        });
        return; 
    } 
    if (file.size > 2 * 1024 * 1024) {
        Swal.fire({
            title: 'Erro',
            text: 'O arquivo é muito grande. O tamanho máximo permitido é 2MB.',
            icon: 'error',
            confirmButtonText: 'OK',
            scrollbarPadding: false
        });
        return;
    } 
    if (!file.type.startsWith('image')) {
        Swal.fire({
            title: 'Erro',
            text: 'O arquivo deve ser uma imagem.',
            icon: 'error',
            confirmButtonText: 'OK',
            scrollbarPadding: false
        });
        return; 
    } 

    const formData = new FormData(this); 

    fetch(this.action, { 
        method: 'POST', 
        body: formData, 
        headers: { 
            'X-CSRFToken': '{{ csrf_token }}', 
        }, 
    }) 
    .then(response => response.json()) 
    .then(data => { 
        if (data.success) { 
            Swal.fire({
                title: 'Sucesso',
                text: data.message,
                icon: 'success',
                confirmButtonText: 'OK',
                scrollbarPadding: false
            }).then(() => {
                window.location.reload();
            });
        }
    }) 
    .catch(error => { 
        console.error('Erro:', error); 
        Swal.fire({
            title: 'Erro',
            text: 'Erro ao atualizar a foto de perfil. Tente novamente.',
            icon: 'error',
            confirmButtonText: 'OK',
            scrollbarPadding: false
        });
    }); 
});