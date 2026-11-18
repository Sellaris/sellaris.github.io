// Keep language changes in the same section; both pages work without JavaScript.
(() => {
  const options = document.querySelectorAll('.language-option');
  function updateLinks() {
    for (const option of options) {
      const destination = new URL(option.getAttribute('href'), location.href);
      destination.hash = location.hash;
      option.href = destination.href;
    }
  }
  updateLinks();
  window.addEventListener('hashchange', updateLinks);
  for (const option of options) {
    option.addEventListener('click', event => {
      if (option.getAttribute('aria-current') === 'page') {
        event.preventDefault();
        return;
      }
      // Prefer an explicit anchor, including while its scroll is still settling.
      const sections = [...document.querySelectorAll('main > section')];
      const visible = sections.find(section => {
        const rect = section.getBoundingClientRect();
        return rect.bottom > 80 && rect.top < innerHeight;
      });
      const destination = new URL(option.href);
      destination.hash = location.hash || (visible ? '#' + visible.id : '');
      option.href = destination.href;
    });
  }
})();
