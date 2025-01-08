let slideIndex = 0;
const slides = document.querySelector('.slides');
const totalSlides = slides.children.length;

function moveSlides(n) {
    slideIndex = (slideIndex + n + totalSlides) % totalSlides;
    slides.style.transform = `translateX(-${slideIndex * 33.33}%)`;
}

function enlargeImage(img) {
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    lightboxImg.src = img.src;
    lightbox.style.display = 'flex';
    lightbox.style.zIndex = '10';
}

function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    lightbox.style.display = 'none';
}

