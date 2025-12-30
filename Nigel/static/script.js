const track = document.querySelector('.carousel-track');
const slides = document.querySelectorAll('.carousel-track img');
const nextBtn = document.querySelector('.carousel-btn.next');
const prevBtn = document.querySelector('.carousel-btn.prev');
let index = 0;
const slideWidth = slides[0].clientWidth;
function updateCarousel() {
  track.style.transform = `translateX(-${index * slideWidth}px)`;
}
function nextSlide() {
  index = (index + 1) % slides.length;
  updateCarousel();
}
function prevSlide() {
  index = (index - 1 + slides.length) % slides.length;
  updateCarousel();
}
nextBtn.addEventListener('click', nextSlide);
prevBtn.addEventListener('click', prevSlide);
// Auto-slide every 4 seconds
setInterval(nextSlide, 4000);