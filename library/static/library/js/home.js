// Update the slide position
let currentSlide = 0;

function moveSlide(direction) {
  const items = document.querySelectorAll(".slide-item");
  const totalSlides = items.length;

  currentSlide += direction;

  if (currentSlide >= totalSlides) {
    currentSlide = 0;
  } else if (currentSlide < 0) {
    currentSlide = totalSlides - 1;
  }

  const slidesContent = document.querySelector(".slides-content");
  slidesContent.style.transform = `translateX(-${currentSlide * 100}%)`;
}

