 // Smooth Scrolling to Hash Anchors
 document.addEventListener("DOMContentLoaded", function() {
    const hash = window.location.hash;
    if (hash) {
        const target = document.querySelector(hash);
        if (target) {
            setTimeout(() => {
                target.scrollIntoView({ behavior: "smooth", block: "start" });
            }, 150);
        }
    }
});
 
 // Auto-fade alerts
setTimeout(() => {
    document.querySelectorAll('.mi-alert').forEach(el => {
        el.style.transition = "opacity 0.5s ease";
        el.style.opacity = "0";
        setTimeout(() => el.remove(), 500);
    });
}, 3000);

// Collect all gallery images
const galleryImages = document.querySelectorAll('.gallery-thumb');
const modalImage = document.querySelector('#modalImage');
const galleryModal = new bootstrap.Modal(document.querySelector('#galleryModal'));

let currentIndex = 0;

// Open modal when clicking a thumbnail
galleryImages.forEach(img => {
    img.addEventListener('click', () => {
        currentIndex = parseInt(img.dataset.index);
        modalImage.src = img.src;
        galleryModal.show();
    });
});

// Next image
document.querySelector('#nextBtn').addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % galleryImages.length;
    modalImage.src = galleryImages[currentIndex].src;
});

// Previous image
document.querySelector('#prevBtn').addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + galleryImages.length) % galleryImages.length;
    modalImage.src = galleryImages[currentIndex].src;
});

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (!document.querySelector('#galleryModal').classList.contains('show')) return;

    if (e.key === 'ArrowRight') {
        currentIndex = (currentIndex + 1) % galleryImages.length;
        modalImage.src = galleryImages[currentIndex].src;
    }

    if (e.key === 'ArrowLeft') {
        currentIndex = (currentIndex - 1 + galleryImages.length) % galleryImages.length;
        modalImage.src = galleryImages[currentIndex].src;
    }
});
