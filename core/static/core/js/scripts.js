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