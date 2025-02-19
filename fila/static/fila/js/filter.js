document.addEventListener('DOMContentLoaded', () => {
    const filterButton = document.querySelector('.filter');
    const filterList = document.querySelector('.filter-list');
    const clearButton = document.querySelector('.btn-clear');
    const applyButton = document.querySelector('.btn-apply');

    filterButton.addEventListener('click', (e) => {
        e.stopPropagation();
        if (!filterList.classList.contains('show')) {
            filterList.style.display = 'flex';
            filterList.offsetHeight;
            filterList.classList.add('show');
        } else {
            filterList.classList.remove('show');
            setTimeout(() => {
                if (!filterList.classList.contains('show')) {
                    filterList.style.display = 'none';
                }
            }, 0);
        }
        filterButton.classList.toggle('active');
    });

    document.addEventListener('click', (e) => {
        if (!filterButton.contains(e.target) && !filterList.contains(e.target)) {
            filterList.classList.remove('show');
            filterButton.classList.remove('active');
            setTimeout(() => {
                if (!filterList.classList.contains('show')) {
                    filterList.style.display = 'none';
                }
            }, 0);
        }
    });

    clearButton?.addEventListener('click', () => {
        const checkboxes = filterList.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => checkbox.checked = false);
    });

    applyButton?.addEventListener('click', () => {
        const selectedFilters = {
            status: [],
            tipo: []
        };

        filterList.querySelectorAll('input[type="checkbox"]:checked').forEach(checkbox => {
            selectedFilters[checkbox.name].push(checkbox.value);
        });

        const params = new URLSearchParams();
        Object.entries(selectedFilters).forEach(([key, values]) => {
            if (values.length) {
                params.append(key, values.join(','));
            }
        });

        window.location.search = params.toString();
    });
}); 