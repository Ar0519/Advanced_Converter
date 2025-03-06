document.addEventListener('DOMContentLoaded', () => {
    const uploadBox = document.getElementById('uploadBox');
    const fileInput = document.getElementById('fileInput');
    const convertBtn = document.getElementById('convertBtn');
    const conversionType = document.getElementById('conversionType');
    const statusMessage = document.getElementById('statusMessage');
    const downloadLink = document.getElementById('downloadLink');
    const downloadAnchor = document.getElementById('downloadAnchor');

    uploadBox.addEventListener('click', () => fileInput.click());
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.style.background = 'rgba(255, 255, 255, 0.2)';
    });
    uploadBox.addEventListener('dragleave', () => {
        uploadBox.style.background = 'rgba(255, 255, 255, 0.1)';
    });
    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.style.background = 'rgba(255, 255, 255, 0.1)';
        fileInput.files = e.dataTransfer.files;
        statusMessage.textContent = `${fileInput.files.length} file(s) selected`;
    });

    fileInput.addEventListener('change', () => {
        statusMessage.textContent = `${fileInput.files.length} file(s) selected`;
    });

    convertBtn.addEventListener('click', async () => {
        const files = fileInput.files;
        const type = conversionType.value;

        if (files.length === 0) {
            statusMessage.textContent = 'Please upload files first.';
            return;
        }

        const formData = new FormData();
        for (const file of files) {
            if (type === 'images_to_pdf') {
                formData.append('images', file);
            } else if (type === 'pdf_to_docx') {
                formData.append('pdf', file);
            } else if (type === 'docx_to_pdf') {
                formData.append('docx', file);
            }
        }
        formData.append('conversion_type', type);

        try {
            statusMessage.textContent = 'Converting...';
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();
            if (response.ok) {
                statusMessage.textContent = result.message;
                downloadAnchor.href = `/download/${result.filename}`;
                downloadAnchor.textContent = `Download ${result.filename}`;
                downloadLink.classList.remove('hidden');
            } else {
                statusMessage.textContent = result.error;
            }
        } catch (error) {
            statusMessage.textContent = 'Conversion failed. Please try again.';
        }
    });
});