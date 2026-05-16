window.addEventListener('load', () => {
    setTimeout(() => {
        document.querySelector('.vault-door').classList.add('open');
        }, 100);
    setTimeout(() => {
        document.getElementById('vault-overlay').remove();
        }, 1800);
});

document.addEventListener('DOMContentLoaded', function() {
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    tooltips.forEach(el => new bootstrap.Tooltip(el))
})

let lastScroll = 0;

const navbar = document.querySelector('.custom-navbar');
window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll <= 0) {
        navbar.classList.remove('nav-hidden');
        return;
    }

    if (currentScroll > lastScroll && !navbar.classList.contains('nav-hidden')) {
        navbar.classList.add('nav-hidden');

    } else if (currentScroll < lastScroll && navbar.classList.contains('nav-hidden')) {
        navbar.classList.remove('nav-hidden');
    }

    lastScroll = currentScroll;
});