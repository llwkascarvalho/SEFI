document.addEventListener('DOMContentLoaded', function() {
    const table = document.querySelector('table');
    if (!table) return;

    const getCellValue = (tr, idx) => {
        const cell = tr.children[idx];
        return cell.innerText.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
    };

    const comparer = (idx, asc) => (a, b) => {
        const v1 = getCellValue(a, idx);
        const v2 = getCellValue(b, idx);
        
        if (v1.match(/^\d{2}\/\d{2}\/\d{4}$/) && v2.match(/^\d{2}\/\d{2}\/\d{4}$/)) {
            const d1 = v1.split('/').reverse().join('-');
            const d2 = v2.split('/').reverse().join('-');
            return asc ? new Date(d1) - new Date(d2) : new Date(d2) - new Date(d1);
        }
        
        if (!isNaN(v1) && !isNaN(v2)) {
            return asc ? v1 - v2 : v2 - v1;
        }
        
        return asc ? v1.localeCompare(v2) : v2.localeCompare(v1);
    };

    document.querySelectorAll('th').forEach(th => {
        const headerIndex = Array.from(th.parentElement.children).indexOf(th);
        
        if (['ID', 'Título', 'Status', 'Data de Solicitação', 'Data de Entrega'].includes(th.textContent.trim())) {
            th.classList.add('sortable');
            th.style.cursor = 'pointer';
            
            const icon = document.createElement('span');
            icon.className = 'sort-icon';
            icon.textContent = '↕';
            th.appendChild(icon);
            
            th.addEventListener('click', () => {
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));
                
                document.querySelectorAll('th').forEach(header => {
                    if (header !== th) {
                        header.classList.remove('asc', 'desc');
                        const otherIcon = header.querySelector('.sort-icon');
                        if (otherIcon) otherIcon.textContent = '↕';
                    }
                });
                
                const isAsc = !th.classList.contains('asc');
                th.classList.toggle('asc', isAsc);
                th.classList.toggle('desc', !isAsc);
                
                const icon = th.querySelector('.sort-icon');
                icon.textContent = isAsc ? '↑' : '↓';
                
                rows.sort(comparer(headerIndex, isAsc));
                tbody.append(...rows);
            });
        }
    });
}); 