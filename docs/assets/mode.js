/* DIVE-PL — Diver / Engineer mode switch
   - Persists choice in localStorage ('dive-pl-mode')
   - Sets [data-mode] on <html> (the dark theme reads this)
   - Injects the toggle control into nav.site, no per-page markup needed
   Pair with the dark assets/style.css. To avoid a flash on load, also add to each
   page's <head>, before the stylesheet:
     <script>try{var m=localStorage.getItem('dive-pl-mode');if(m)document.documentElement.setAttribute('data-mode',m);}catch(e){}</script>
*/
(function () {
  var KEY = 'dive-pl-mode';
  var MODES = ['diver', 'engineer'];
  var LABELS = { diver: '\u25C8 Diver', engineer: '\u2317 Engineer' };

  function current() {
    var m;
    try { m = localStorage.getItem(KEY); } catch (e) {}
    return MODES.indexOf(m) >= 0 ? m : 'diver';
  }

  function apply(mode) {
    document.documentElement.setAttribute('data-mode', mode);
    var btns = document.querySelectorAll('.modes .seg');
    for (var i = 0; i < btns.length; i++) {
      btns[i].setAttribute('aria-pressed', String(btns[i].getAttribute('data-mode') === mode));
    }
  }

  function set(mode) {
    try { localStorage.setItem(KEY, mode); } catch (e) {}
    apply(mode);
  }

  function build() {
    var nav = document.querySelector('nav.site');
    if (!nav || nav.querySelector('.modes')) { apply(current()); return; }
    var group = document.createElement('div');
    group.className = 'modes';
    group.setAttribute('role', 'group');
    group.setAttribute('aria-label', 'Visual mode');
    MODES.forEach(function (mode) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'seg';
      b.setAttribute('data-mode', mode);
      b.textContent = LABELS[mode];
      b.addEventListener('click', function () { set(mode); });
      group.appendChild(b);
    });
    nav.appendChild(group);
    apply(current());
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
