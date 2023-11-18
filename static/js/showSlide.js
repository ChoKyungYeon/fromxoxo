function showSlide(slideNumber) {
    for (let i = 1; i <= 6; i++) {
        const btn = document.querySelector(`#btn-slide${i}`);
        const slide = document.querySelector(`#slide${i}`);

        if (i === slideNumber) {
            btn.classList.add('btn-touched');
            btn.classList.remove('btn-untouched');
            slide.style.display = 'flex';
        } else {
            btn.classList.add('btn-untouched');
            btn.classList.remove('btn-touched');
            slide.style.display = 'none';
        }
    }
}
showSlide(1);