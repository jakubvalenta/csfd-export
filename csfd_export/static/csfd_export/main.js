(() => {
  function show(el) {
    el.classList.remove(CLASS_HIDDEN);
  }

  function hide(el) {
    el.classList.add(CLASS_HIDDEN);
  }

  function isVisible(el) {
    return !el.classList.contains(CLASS_HIDDEN);
  }

  function setCsv(csv) {
    csvEl.textContent = csv;
    downloadEl.setAttribute(
      'href',
      'data:text/plain;charset=utf-8,' + encodeURIComponent(csv)
    );
    hide(errorEl);
    hide(loadingEl);
    show(doneEl);
  }

  function setErrorMessage(errorMessage) {
    errorMessageEl.textContent = errorMessage;
    hide(doneEl);
    hide(loadingEl);
    show(errorEl);
  }

  const CLASS_HIDDEN = 'hidden';

  const csvEl = document.getElementById('csv');
  const doneEl = document.getElementById('done');
  const downloadEl = document.getElementById('download');
  const errorEl = document.getElementById('error');
  const errorMessageEl = document.getElementById('error-message');
  const loadingEl = document.getElementById('loading');
  const spinnerEl = document.getElementById('spinner');

  const url = document.body.getAttribute('data-user-detail-url');

  document.body.classList.add('js');

  const frames = ['.  ', '.. ', '...', ' ..', '  .', '   '];
  var i = 0;
  const spinnerInterval = setInterval(function () {
    spinnerEl.innerHTML = frames[i];
    i = (i + 1) % frames.length;
  }, 300);

  if (isVisible(doneEl)) {
    return;
  }

  const interval = setInterval(() => {
    fetch(url, { headers: { Accept: 'text/csv' } })
      .then(res => {
        if (res.status === 200) {
          res
            .text()
            .then(csv => setCsv(csv))
            .catch(console.error);
          clearInterval(interval);
          clearInterval(spinnerInterval);
        } else if (res.status === 201) {
          // Retry.
        } else {
          res
            .text()
            .then(errorMessage =>
              setErrorMessage(
                res.headers.get('Content-Type') === 'text/csv'
                  ? errorMessage
                  : 'Unknown error'
              )
            )
            .catch(console.error);
        }
      })
      // In case of connection error, don't show a message to the user, because
      // they could think it's not recoverable and could close the page.
      .catch(console.error);
  }, 3000);
})();
