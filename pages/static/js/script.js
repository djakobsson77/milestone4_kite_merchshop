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
const modalElement = document.querySelector('#galleryModal');
if (modalElement) {
    const galleryModal = new bootstrap.Modal(modalElement);
}

let currentIndex = 0;

// Open modal when clicking a thumbnail
if (galleryImages.length > 0) {
    galleryImages.forEach(img => {
        img.addEventListener('click', () => {
            currentIndex = parseInt(img.dataset.index);
            modalImage.src = img.src;
            galleryModal.show();
        });
    });
}


// Next image
const nextBtn = document.querySelector('#nextBtn');
if (nextBtn) {
    nextBtn.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % galleryImages.length;
        modalImage.src = galleryImages[currentIndex].src;
    });
}


// Previous image
const prevBtn = document.querySelector('#prevBtn');
if (prevBtn) {
    prevBtn.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + galleryImages.length) % galleryImages.length;
        modalImage.src = galleryImages[currentIndex].src;
    });
}


// Keyboard navigation
const modalEl = document.querySelector('#galleryModal');
if (modalEl) {
    document.addEventListener('keydown', (e) => {
        if (!modalEl.classList.contains('show')) return;

        if (e.key === 'ArrowRight') {
            currentIndex = (currentIndex + 1) % galleryImages.length;
            modalImage.src = galleryImages[currentIndex].src;
        }

        if (e.key === 'ArrowLeft') {
            currentIndex = (currentIndex - 1 + galleryImages.length) % galleryImages.length;
            modalImage.src = galleryImages[currentIndex].src;
        }
    });
}


// Auto-fade messages
window.onload = () => {
    setTimeout(() => {
        const msgs = document.querySelectorAll('.messages');
        msgs.forEach(msg => {
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 500);
        });
    }, 2500);
};

