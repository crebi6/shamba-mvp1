
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('fileInput');

// Trigger file input when clicking the drop zone
dropZone.addEventListener('click', () => {
    fileInput.click();
});

// Handle file upload
fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) {
        uploadFile(file);
    }
});

// Drag-and-drop functionality
dropZone.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (event) => {
    event.preventDefault();
    dropZone.classList.remove('dragover');

    const file = event.dataTransfer.files[0];
    if (file) {
        uploadFile(file);
    }
});

// Upload file to backend
function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`Error: ${data.error}`);
            } else {
                alert(`Prediction: ${data.class}\nConfidence: ${data.confidence}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
