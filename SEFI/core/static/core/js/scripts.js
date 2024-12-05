
// Menu
function toggleMenu() {
    const menu = document.getElementById('menu');
    menu.classList.toggle('active');
}

// Evento de clique em todos os links do menu
document.querySelectorAll('.menu a').forEach(item => {
    item.addEventListener('click', function () {
        
        document.querySelectorAll('.menu a').forEach(link => link.classList.remove('active'));
        
        this.classList.add('active');
    });
});