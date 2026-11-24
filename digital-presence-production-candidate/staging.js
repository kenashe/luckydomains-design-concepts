/* Staging only. Blocks the contact form before the site script can send anything. */
document.addEventListener('submit', function (e) {
  e.preventDefault(); e.stopImmediatePropagation();
  var s = document.getElementById('form-status');
  if (s) { s.textContent = 'Review environment. This form is disabled here and nothing was collected, stored, or sent.'; s.className = 'form-status show err'; }
}, true);
