function toggleMenu() { 
    const menu = document.getElementById('menu'); 
    const main = document.querySelector('main');
    menu.classList.toggle('active'); 

    if (menu.classList.contains('active')) { 
        main.style.marginLeft = '0'; 
        main.style.marginRight = '0'; 
        main.style.margin = '0 auto'; 
        main.style.marginTop = '150px'; 
    } else { 
        main.style.marginLeft = '250px'; 
        main.style.marginTop = '150px'; 
        main.style.paddingLeft = '50px'; 
    } 
} 
document.addEventListener('DOMContentLoaded', function() { 
    const menuItems = document.querySelectorAll('.menu a'); 
    const currentPath = window.location.pathname;  

    menuItems.forEach(item => { 
        if (item.getAttribute('href') === currentPath) { 
            item.classList.add('active');  
        } 

        item.addEventListener('click', function() { 
            menuItems.forEach(i => i.classList.remove('active')); 
            item.classList.add('active');  
        }); 
    }); 
}); 

document.getElementById('form-foto-perfil').addEventListener('submit', function(event) { 
    event.preventDefault(); 

    const fileInput = document.getElementById('foto_perfil'); 
    const file = fileInput.files[0]; 

    if (!file) { 
        alert('Nenhuma foto foi selecionada.'); 
        return; 
    } 
    if (file.size > 2 * 1024 * 1024) {
        alert('O arquivo é muito grande. O tamanho máximo permitido é 2MB.');
        return;
    } 
    if (!file.type.startsWith('image')) {
        alert('O arquivo deve ser uma imagem.');
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
            alert(data.message); 
            window.location.reload(); 
        } else { 
            alert(data.message); 
        } 
    }) 
    .catch(error => { 
        console.error('Erro:', error); 
        alert('Erro ao atualizar a foto de perfil. Tente novamente.'); 
    }); 
});