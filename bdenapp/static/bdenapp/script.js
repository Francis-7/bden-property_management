const modal = document.getElementById('fullscreenModal');
    const fullscreenImage = document.getElementById('fullscreenImage');
    const closeBtn = document.getElementById('closeFullscreen');
    const prevBtn = document.getElementById('prevImage');
    const nextBtn = document.getElementById('nextImage');

    const images = document.querySelectorAll('.gallery__img');
    let currentIndex = 0;

    // Show the full-screen image when an image is clicked
    images.forEach((img, index) => {
        img.addEventListener('click', () => {
            modal.style.display = 'flex';
            fullscreenImage.src = img.src;
            currentIndex = index;
        });
    });

    // Close the full-screen modal when clicking the close button or pressing ESC
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Close the modal if clicking anywhere outside the image
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Listen for ESC key to close modal
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            modal.style.display = 'none';
        }
    });

    // Go to the previous image
    prevBtn.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        fullscreenImage.src = images[currentIndex].src;
    });

    // Go to the next image
    nextBtn.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % images.length;
        fullscreenImage.src = images[currentIndex].src;
    });