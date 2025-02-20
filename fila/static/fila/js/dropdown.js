document.addEventListener('DOMContentLoaded', () => {
    const dropdown = document.querySelector('.dropdown');
    if (!dropdown) return;

    const selected = dropdown.querySelector('.selected');
    const caret = selected.querySelector('.caret');
    const list = dropdown.querySelector('.list');

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

    document.querySelectorAll(".list .item").forEach((item) => {
        item.addEventListener("click", function(e) {
            e.stopPropagation();
            list.classList.remove('show');
            caret.classList.remove('caret-rotate');
        });
    });
});
