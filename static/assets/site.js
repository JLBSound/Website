(function () {
  // Mobile menu
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Pause control for the scrolling posters
  var toggle = document.querySelector('[data-poster-toggle]');
  var row = document.querySelector('.posters');
  if (toggle && row) {
    toggle.addEventListener('click', function () {
      var paused = row.classList.toggle('paused');
      toggle.textContent = paused ? 'Play posters' : 'Pause posters';
    });
  }

  // Quote form. Sends through Web3Forms (data-endpoint and the access_key field
  // in src/_form.html) to joe@jlbsound.com. With no endpoint set, it falls back
  // to opening a pre-filled email to Joe.
  var form = document.querySelector('[data-quote]');
  if (form) {
    var status = form.querySelector('.status');
    var say = function (msg, err) {
      status.textContent = msg;
      status.classList.toggle('err', !!err);
    };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = new FormData(form);
      if (data.get('website')) return; // spam trap
      var endpoint = form.getAttribute('data-endpoint');
      if (!endpoint) {
        var labels = { name: 'Name', email: 'Email', project: 'Project', due: 'Due' };
        var body = Object.keys(labels).map(function (k) {
          return labels[k] + ': ' + (data.get(k) || '');
        }).join('\n');
        var subject = 'Quote request: ' + (data.get('project') || 'new project');
        window.location.href = 'mailto:joe@jlbsound.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
        say('Your email app should open with your details filled in. Press send and it goes straight to Joe.');
        return;
      }
      data.delete('website');
      data.set('subject', 'Quote request: ' + (data.get('project') || 'new project'));
      data.set('from_name', 'JLB Studios website');
      say('Sending...');
      fetch(endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          form.reset();
          say('Thanks. Your project details are on their way to Joe.');
        })
        .catch(function () {
          say('That did not send. Please call 801-318-7783 or email joe@jlbsound.com.', true);
        });
    });
  }
})();
