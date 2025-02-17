document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('arquivo');
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const removeFile = document.getElementById('removeFile');
    const form = document.querySelector('form');

    window.handleFormReset = function(e) {
        e.preventDefault();
        
        form.reset();
        
        document.getElementById('titulo').value = '';
        document.getElementById('quantidade_copias').value = '';
        document.getElementById('data_entrega').value = '';
        document.getElementById('grampos').selectedIndex = 1;
        document.getElementById('tipo_entrega').selectedIndex = 0;
        document.getElementById('tipo_atividade').selectedIndex = 0;
        document.getElementById('tipo_impressao').selectedIndex = 1;
        
        handleFileRemove();
        
        const errorMessages = document.querySelectorAll('.error-message');
        errorMessages.forEach(msg => msg.remove());
        
        const successMessages = document.querySelectorAll('.messages');
        successMessages.forEach(msg => msg.remove());
        
        form.querySelector('#titulo').focus();
    };

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, unhighlight, false);
    });

    uploadArea.addEventListener('drop', handleDrop, false);
    
    fileInput.addEventListener('change', handleFileSelect, false);
    
    removeFile.addEventListener('click', handleFileRemove, false);
    
    form.addEventListener('reset', handleFileRemove, false);

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight(e) {
        uploadArea.classList.add('dragover');
    }

    function unhighlight(e) {
        uploadArea.classList.remove('dragover');
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    function handleFileSelect(e) {
        const files = e.target.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            
            if (file.size > 10 * 1024 * 1024) {
                showError('O arquivo não pode ter mais de 10MB.');
                return;
            }

            const ext = file.name.split('.').pop().toLowerCase();
            const allowedExtensions = ['pdf', 'doc', 'docx', 'odt'];
            
            if (!allowedExtensions.includes(ext)) {
                showError('Formato de arquivo não permitido. Use: PDF, DOC, DOCX ou ODT.');
                return;
            }

            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            fileInput.files = dataTransfer.files;

            fileName.textContent = file.name;
            fileInfo.style.display = 'flex';
            uploadArea.querySelector('.upload-content').style.display = 'none';
        }
    }

    function handleFileRemove() {
        fileInput.value = '';
        fileInfo.style.display = 'none';
        uploadArea.querySelector('.upload-content').style.display = 'flex';
        fileName.textContent = '';
    }

    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = message;
        
        uploadArea.parentNode.insertBefore(errorDiv, uploadArea.nextSibling);
        
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
        
        handleFileRemove();
    }
}); 