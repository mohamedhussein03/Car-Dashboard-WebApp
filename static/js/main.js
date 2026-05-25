/* Dashly AI — main.js */

/* ── Mobile navigation toggle ──────────────────────────────── */
const navToggle = document.getElementById('navToggle');
const navLinks  = document.getElementById('navLinks');

if (navToggle && navLinks) {
  navToggle.addEventListener('click', function () {
    const isOpen = navLinks.classList.toggle('open');
    navToggle.classList.toggle('open', isOpen);
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });

  document.addEventListener('click', function (e) {
    if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
      navLinks.classList.remove('open');
      navToggle.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
    }
  });
}

/* ── Image preview on file select ──────────────────────────── */
const imageInput     = document.getElementById('imageInput');
const previewImage   = document.getElementById('previewImage');
const previewWrapper = document.getElementById('previewWrapper');

if (imageInput && previewImage && previewWrapper) {
  imageInput.addEventListener('change', function () {
    const file = this.files[0];
    if (!file) {
      previewWrapper.classList.remove('visible');
      previewImage.src = '';
      return;
    }
    const reader = new FileReader();
    reader.onload = function (e) {
      previewImage.src = e.target.result;
      previewWrapper.classList.add('visible');
    };
    reader.readAsDataURL(file);
  });
}

/* ── Drag-and-drop visual feedback ─────────────────────────── */
const uploadZone = document.getElementById('uploadZone');

if (uploadZone) {
  ['dragenter', 'dragover'].forEach(function (evt) {
    uploadZone.addEventListener(evt, function (e) {
      e.preventDefault();
      uploadZone.classList.add('drag-over');
    });
  });
  ['dragleave', 'drop'].forEach(function (evt) {
    uploadZone.addEventListener(evt, function () {
      uploadZone.classList.remove('drag-over');
    });
  });
}

/* ── Show loading overlay on form submit ────────────────────── */
const detectForm     = document.getElementById('detectForm');
const loadingOverlay = document.getElementById('loadingOverlay');
const submitButton   = document.getElementById('submitButton');

if (detectForm && loadingOverlay && submitButton) {
  detectForm.addEventListener('submit', function () {
    loadingOverlay.classList.add('active');
    submitButton.disabled = true;
    submitButton.textContent = '…';
  });
}

/* ── Icon library expand/collapse ───────────────────────────── */
function toggleIconDetails(index) {
  const details = document.getElementById('icon-details-' + index);
  const card    = details ? details.closest('.icon-card') : null;
  if (!details || !card) return;

  const isOpen = details.classList.contains('open');

  document.querySelectorAll('.icon-details.open').forEach(function (el) {
    el.classList.remove('open');
    const parentCard = el.closest('.icon-card');
    if (parentCard) {
      parentCard.classList.remove('expanded');
      parentCard.setAttribute('aria-expanded', 'false');
    }
  });

  if (!isOpen) {
    details.classList.add('open');
    card.classList.add('expanded');
    card.setAttribute('aria-expanded', 'true');
    card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}
