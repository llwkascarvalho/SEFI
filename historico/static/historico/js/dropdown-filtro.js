document.addEventListener('DOMContentLoaded', () => {
    const filterButton = document.querySelector('.filter');
    const filterList = document.querySelector('.filter-list');

    filterButton.addEventListener('click', (e) => {
        e.stopPropagation();
        filterList.classList.toggle('show');
    });

    document.addEventListener('click', (e) => {
        if (!filterButton.contains(e.target) && !filterList.contains(e.target)) {
            filterList.classList.remove('show');
        }
    });
});