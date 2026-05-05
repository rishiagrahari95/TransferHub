document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const statusMessage = document.getElementById('status-message');
    const fileList = document.getElementById('file-list');
    const pinInput = document.getElementById('pin-input');

    dropZone.addEventListener('click', () => fileInput.click());

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    });

    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length === 0) return;
        
        const pin = pinInput.value.trim();
        if (!pin) {
            showStatus('Please enter the Access PIN first.', 'var(--error)');
            return;
        }

        uploadFiles(files, pin);
    }

    function uploadFiles(files, pin) {
        const formData = new FormData();
        formData.append('pin', pin);
        
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }

        progressContainer.style.display = 'block';
        statusMessage.textContent = '';
        
        const xhr = new XMLHttpRequest();
        
        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percentComplete = Math.round((e.loaded / e.total) * 100);
                progressBar.style.width = percentComplete + '%';
                progressText.textContent = percentComplete + '%';
            }
        });

        xhr.onload = function() {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                showStatus('Upload complete!', 'var(--success)');
                updateFileList(response.files);
            } else {
                let errorMsg = 'Upload failed.';
                try {
                    errorMsg = JSON.parse(xhr.responseText).error;
                } catch(e) {}
                showStatus(errorMsg, 'var(--error)');
            }
            setTimeout(() => { progressContainer.style.display = 'none'; progressBar.style.width = '0%'; }, 3000);
            fileInput.value = ''; 
        };

        xhr.onerror = function() {
            showStatus('Network error occurred.', 'var(--error)');
            progressContainer.style.display = 'none';
        };

        xhr.open('POST', '/upload', true);
        xhr.send(formData);
    }

    function showStatus(message, color) {
        statusMessage.textContent = message;
        statusMessage.style.color = color;
    }

    function updateFileList(files) {
        files.forEach(file => {
            const li = document.createElement('li');
            const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            li.innerHTML = `<span>${file.name}</span> <span style="color: #6B7280; font-size: 12px;">${file.size} MB • ${time}</span>`;
            fileList.prepend(li);
        });
    }
});
