const nav = document.querySelector('.nav');
const menuBtn = document.querySelector('.menu');
const navLinks = document.querySelectorAll('.nav-links a');

export function toggleMenu() {
  nav.classList.toggle('open');
  const expanded = menuBtn.getAttribute('aria-expanded') === 'true';
  menuBtn.setAttribute('aria-expanded', !expanded);
}

if (menuBtn) {
  menuBtn.addEventListener('click', toggleMenu);
}

navLinks.forEach((link) => {
  link.addEventListener('click', () => {
    nav.classList.remove('open');
    menuBtn.setAttribute('aria-expanded', 'false');
  });
});

// Subtle scroll reveal
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  },
  {
    threshold: 0.15,
  }
);

document.querySelectorAll('.project-card, .timeline-item, .stack-card, .highlight').forEach((el) => {
  el.classList.add('reveal');
  observer.observe(el);
});
