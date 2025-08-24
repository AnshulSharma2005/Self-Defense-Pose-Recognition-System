// Function to display the uploaded image preview
function loadImage(event) {
    const image = document.getElementById('image-preview');
    const feedback = document.getElementById('feedback-message');
    image.src = URL.createObjectURL(event.target.files[0]);
    image.classList.remove('hidden');
    feedback.textContent = "Image loaded successfully! Click 'Analyze Pose' to start.";
    feedback.className = "feedback success";
}

// Function to send image to Flask backend for pose analysis
function analyzePose() {
    const feedback = document.getElementById('feedback-message');
    const fileInput = document.getElementById('image-upload');
    const file = fileInput.files[0];
    if (!file) {
        feedback.textContent = "Please upload an image first.";
        feedback.className = "feedback error";
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.feedback) {
            feedback.textContent = data.feedback;
            feedback.className = data.feedback.includes("incorrect") ? "feedback error" : "feedback success";
        } else {
            feedback.textContent = "Error analyzing the pose.";
            feedback.className = "feedback error";
        }
    })
    .catch(error => {
        feedback.textContent = "Error uploading the image.";
        feedback.className = "feedback error";
    });
}
