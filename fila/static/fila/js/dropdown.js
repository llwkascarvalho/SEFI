document.addEventListener('DOMContentLoaded', () => {
    const dropdown = document.querySelector('.dropdown');
    const selected = dropdown.querySelector('.selected');
    const caret = selected.querySelector('.caret');
    const list = dropdown.querySelector('.list');
    const items = list.querySelectorAll('.item');

    const updateList = () => {
        const selectedText = selected.querySelector('span').textContent;

        const updatedList = Array.from(items).filter(i => i.textContent !== selectedText);

        list.innerHTML = '';
        updatedList.forEach(i => list.appendChild(i));
    };

    selected.addEventListener('click', () => {
        list.classList.toggle('show');
        caret.classList.toggle('caret-rotate');
    });

    document.addEventListener('click', (e) => {
        if (!dropdown.contains(e.target)) {
            list.classList.remove('show');
            caret.classList.remove('caret-rotate');
        }
    });

    list.addEventListener('click', (e) => {
        const clickedItem = e.target;

        if (clickedItem.classList.contains('item')) {
            selected.querySelector('span').textContent = clickedItem.textContent;
            selected.className = `selected ${clickedItem.className.split(' ')[1]}`;

            updateList();

            list.classList.remove('show');
            caret.classList.remove('caret-rotate');
        }
    });

    updateList();
});
