function toggleMenu() { 
    const menu = document.getElementById('menu'); 
    const main = document.querySelector('main');
    menu.classList.toggle('active'); 
    main.classList.toggle('menu-active');
    
    localStorage.setItem('menuState', menu.classList.contains('active') ? 'closed' : 'open');
} 

document.addEventListener('DOMContentLoaded', function() { 
    const menu = document.getElementById('menu');
    const main = document.querySelector('main');
    const menuItems = document.querySelectorAll('.menu a'); 
    const currentPath = window.location.pathname;  

    const menuState = localStorage.getItem('menuState');
    if (menuState === 'closed') {
        menu.classList.add('active');
        main.classList.add('menu-active');
    }

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
