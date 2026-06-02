// Galeria — filtros e busca
(function(){
  const grid = document.getElementById('book-grid');
  const cards = grid ? Array.from(grid.querySelectorAll('.book-card')) : [];
  const filterBtns = document.querySelectorAll('.filter-btn');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      cards.forEach(card => {
        const cat = card.dataset.category;
        if (filter === 'all' || cat.toLowerCase().includes(filter.toLowerCase())) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
})();

// Modal de livro
(function(){
  const overlay = document.getElementById('modal-overlay');
  const modal = document.getElementById('modal');
  const closeBtn = document.querySelector('.modal-close');
  const cards = document.querySelectorAll('.book-card');

  const BOOKS = window.LB_BOOKS || {};

  function openBook(vol){
    const book = BOOKS[vol];
    if (!book) return;
    modal.querySelector('.modal-cover').style.background = book.paper;
    modal.querySelector('.modal-cover').style.color = book.ink || '#0E0E0E';
    modal.querySelector('.modal-cover-vol').textContent = 'Vol. ' + book.vol;
    modal.querySelector('.modal-cover-num').textContent = book.vol;
    modal.querySelector('.modal-cover-num').style.color = book.accent + '33';
    modal.querySelector('.modal-cover-cat').textContent = book.category;
    modal.querySelector('.modal-cover-cat').style.color = book.accent;
    modal.querySelector('.modal-cover-title').textContent = book.title;
    modal.querySelector('.modal-cover-author').textContent = book.author;
    modal.querySelector('.modal-eyebrow').textContent = book.category;
    modal.querySelector('.modal-title').textContent = book.title;
    modal.querySelector('.modal-author').textContent = book.author;
    modal.querySelector('.modal-tese').textContent = book.tese;
    const bulletsEl = modal.querySelector('.modal-section ul');
    bulletsEl.innerHTML = book.bullets.map(b => '<li><span>' + b + '</span></li>').join('');
    modal.querySelector('.modal-buy').href = book.cakto;
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeBook(){
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  cards.forEach(card => {
    card.addEventListener('click', () => openBook(card.dataset.vol));
  });
  closeBtn.addEventListener('click', closeBook);
  overlay.addEventListener('click', e => {
    if (e.target === overlay) closeBook();
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeBook();
  });
})();

// Smooth reveal on scroll
(function(){
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.opacity = 1;
        e.target.style.transform = 'translateY(0)';
        observer.unobserve(e.target);
      }
    });
  }, {threshold: 0.1, rootMargin: '0px 0px -50px 0px'});

  document.querySelectorAll('.book-card, .plan-card, .feature, details.faq-item').forEach(el => {
    el.style.opacity = 0;
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity .6s, transform .6s';
    observer.observe(el);
  });
})();
