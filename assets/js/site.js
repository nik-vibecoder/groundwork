/* Groundwork. Vanilla JS, no dependencies, no build step. */
(function () {
  'use strict';

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ------------------------------------------------- sidebar drawer */

  var side = $('[data-side]');
  var scrim = $('[data-scrim]');
  var burger = $('[data-burger]');

  function closeSide() {
    if (!side) return;
    side.classList.remove('is-open');
    if (scrim) scrim.classList.remove('is-on');
    if (burger) burger.setAttribute('aria-expanded', 'false');
  }

  if (burger && side) {
    burger.addEventListener('click', function () {
      var open = side.classList.toggle('is-open');
      if (scrim) scrim.classList.toggle('is-on', open);
      burger.setAttribute('aria-expanded', String(open));
    });
  }
  if (scrim) scrim.addEventListener('click', closeSide);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeSide(); });
  $$('.side a').forEach(function (a) { a.addEventListener('click', closeSide); });

  /* --------------------------------------------- active nav marking */

  (function markNav() {
    var here = location.pathname.split('/').pop() || 'index.html';
    var exact = null;
    $$('.side a[href]').forEach(function (a) {
      var href = a.getAttribute('href');
      if (href.charAt(0) === '#' || href.indexOf('http') === 0) return;
      var file = href.split('#')[0];
      if (file !== here) return;
      if (!href.split('#')[1]) exact = a;
      var grp = a.closest('.navgroup');
      if (grp) grp.open = true;
    });
    if (exact) exact.setAttribute('aria-current', 'page');
  })();

  /* ------------------------------------- highlight section in sidebar */

  var sectionLinks = $$('.side a[href*="#"]').filter(function (a) {
    var href = a.getAttribute('href');
    var file = href.split('#')[0];
    return file === (location.pathname.split('/').pop() || 'index.html');
  });

  if (sectionLinks.length && 'IntersectionObserver' in window) {
    var byId = {};
    var targets = [];
    sectionLinks.forEach(function (a) {
      var id = a.getAttribute('href').split('#')[1];
      var el = id && document.getElementById(id);
      if (el) { byId[id] = a; targets.push(el); }
    });
    var seen = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { seen[en.target.id] = en.isIntersecting; });
      var first = targets.filter(function (t) { return seen[t.id]; })[0];
      sectionLinks.forEach(function (a) { a.classList.remove('is-active'); });
      if (first && byId[first.id]) byId[first.id].classList.add('is-active');
    }, { rootMargin: '-80px 0px -65% 0px' });
    targets.forEach(function (t) { io.observe(t); });
  }

  /* ---------------------------------------------------- pyramid tiers */

  $$('[data-tier]').forEach(function (btn) {
    var panel = document.getElementById(btn.getAttribute('aria-controls'));
    if (!panel) return;
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      panel.hidden = open;
    });
  });

  /* -------------------------------------------------------- filtering */

  $$('[data-filter-group]').forEach(function (group) {
    var scope = document.getElementById(group.getAttribute('data-filter-group'));
    if (!scope) return;
    var items = $$('[data-tags]', scope);
    group.addEventListener('click', function (e) {
      var chip = e.target.closest('[data-filter]');
      if (!chip) return;
      $$('[data-filter]', group).forEach(function (c) {
        c.setAttribute('aria-pressed', String(c === chip));
      });
      var want = chip.getAttribute('data-filter');
      items.forEach(function (el) {
        var tags = (el.getAttribute('data-tags') || '').split(/\s+/);
        el.hidden = !(want === 'all' || tags.indexOf(want) > -1);
      });
    });
  });

  /* ------------------------------------------------ energy calculator */

  var calc = $('[data-calc]');
  if (calc) initEnergy(calc);

  function initEnergy(form) {
    var unit = 'metric';
    try { if (localStorage.getItem('gw-unit') === 'imperial') unit = 'imperial'; } catch (e) {}

    var el = {
      sex: $('#sex', form), age: $('#age', form),
      weight: $('#weight', form), height: $('#height', form),
      activity: $('#activity', form), goal: $('#goal', form),
      wLab: $('[data-w-label]', form), hLab: $('[data-h-label]', form)
    };
    var out = {};
    ['target', 'tdee', 'bmr', 'protein', 'fat', 'carb', 'rate', 'note'].forEach(function (k) {
      out[k] = $('[data-out="' + k + '"]');
    });

    function paintUnits() {
      $$('[data-unit]', form).forEach(function (b) {
        b.setAttribute('aria-pressed', String(b.getAttribute('data-unit') === unit));
      });
      if (el.wLab) el.wLab.textContent = unit === 'metric' ? 'kg' : 'lb';
      if (el.hLab) el.hLab.textContent = unit === 'metric' ? 'cm' : 'in';
    }

    $$('[data-unit]', form).forEach(function (b) {
      b.addEventListener('click', function () {
        var next = b.getAttribute('data-unit');
        if (next === unit) return;
        var w = parseFloat(el.weight.value), h = parseFloat(el.height.value);
        if (!isNaN(w)) el.weight.value = Math.round(next === 'imperial' ? w * 2.20462 : w / 2.20462);
        if (!isNaN(h)) el.height.value = Math.round(next === 'imperial' ? h / 2.54 : h * 2.54);
        unit = next;
        try { localStorage.setItem('gw-unit', unit); } catch (e) {}
        paintUnits();
        run();
      });
    });

    function run() {
      var age = parseFloat(el.age.value);
      var wv = parseFloat(el.weight.value);
      var hv = parseFloat(el.height.value);
      if (!age || !wv || !hv) return;

      var kg = unit === 'metric' ? wv : wv / 2.20462;
      var cm = unit === 'metric' ? hv : hv * 2.54;

      var bmr = 10 * kg + 6.25 * cm - 5 * age + (el.sex.value === 'female' ? -161 : 5);
      var tdee = bmr * parseFloat(el.activity.value);

      var goal = el.goal.value;
      var pct = { cut: -0.20, lean: -0.10, maintain: 0, gain: 0.10 }[goal];
      var target = tdee * (1 + pct);

      var perKg = goal === 'cut' ? 2.2 : goal === 'lean' ? 2.0 : 1.8;
      var protein = kg * perKg;
      var fat = Math.max(kg * 0.7, target * 0.22 / 9);
      var carb = Math.max((target - protein * 4 - fat * 9) / 4, 50);

      var weeklyKg = (target - tdee) * 7 / 7700;
      var ratePct = (weeklyKg / kg) * 100;
      var shown = unit === 'metric' ? weeklyKg : weeklyKg * 2.20462;
      var wu = unit === 'metric' ? 'kg' : 'lb';

      put(out.target, Math.round(target / 10) * 10);
      put(out.tdee, Math.round(tdee / 10) * 10);
      put(out.bmr, Math.round(bmr / 10) * 10);
      put(out.protein, Math.round(protein) + ' g');
      put(out.fat, Math.round(fat) + ' g');
      put(out.carb, Math.round(carb) + ' g');

      if (out.rate) {
        out.rate.textContent = goal === 'maintain'
          ? 'Weight stays flat'
          : (shown > 0 ? '+' : '') + shown.toFixed(2) + ' ' + wu + ' per week, or ' +
            (ratePct > 0 ? '+' : '') + ratePct.toFixed(2) + '% of bodyweight';
      }
      if (out.note) {
        out.note.textContent = {
          cut: 'A 20% deficit is aggressive. Workable for 8 to 12 weeks, then take a break at maintenance. If your strength drops sharply or sleep suffers, switch to the slower option.',
          lean: 'The sustainable default. Slow enough that you keep your lifts and your social life.',
          maintain: 'Use this while you learn to hit protein and train consistently. If you are new or returning after a break, you can gain muscle and lose fat here at the same time.',
          gain: 'Roughly 0.25 to 0.5% of bodyweight per week. Anything faster is mostly fat.'
        }[goal];
      }
    }

    function put(node, v) { if (node) node.textContent = v; }

    $$('input, select', form).forEach(function (n) {
      n.addEventListener('input', run);
      n.addEventListener('change', run);
    });
    form.addEventListener('submit', function (e) { e.preventDefault(); });

    paintUnits();
    run();
  }

  /* ------------------------------------------------ volume calculator */

  var vol = $('[data-volume]');
  if (vol) {
    var days = $('#days', vol), lvl = $('#level', vol);
    var vOut = $('[data-out="sets"]'), pOut = $('[data-out="per-session"]');
    var nOut = $('[data-out="per-session-note"]'), sOut = $('[data-out="split"]');

    var freqFor = { 2: 2, 3: 3, 4: 2, 5: 2, 6: 2 };
    var splits = {
      2: 'Full body twice. Every muscle on both days.',
      3: 'Full body three times, or Push / Pull / Legs if you prefer shorter sessions.',
      4: 'Upper / Lower / Upper / Lower. The best return per hour for most people.',
      5: 'Upper / Lower / Push / Pull / Legs.',
      6: 'Push / Pull / Legs twice. Only worth it if sleep and food are already solid.'
    };

    var volRun = function () {
      var d = parseInt(days.value, 10);
      var band = { new: [10, 12], some: [14, 16], years: [16, 20] }[lvl.value];
      var f = freqFor[d];
      if (vOut) vOut.textContent = band[0] + ' to ' + band[1];
      if (pOut) pOut.textContent = Math.round(band[0] / f) + ' to ' + Math.round(band[1] / f);
      if (nOut) nOut.textContent = 'sets per session, each muscle ' + f + 'x per week';
      if (sOut) sOut.textContent = splits[d];
    };
    [days, lvl].forEach(function (n) { if (n) n.addEventListener('change', volRun); });
    volRun();
  }

  /* --------------------------------------------------- 1RM calculator */

  var orm = $('[data-orm]');
  if (orm) {
    var wIn = $('#lift-weight', orm), rIn = $('#lift-reps', orm);
    var ormOut = $('[data-out="orm"]'), tblOut = $('[data-out="orm-table"]');
    var uLab = $('[data-orm-unit]', orm);
    var ormUnit = 'kg';

    $$('[data-orm-u]', orm).forEach(function (b) {
      b.addEventListener('click', function () {
        ormUnit = b.getAttribute('data-orm-u');
        $$('[data-orm-u]', orm).forEach(function (x) {
          x.setAttribute('aria-pressed', String(x === b));
        });
        if (uLab) uLab.textContent = ormUnit;
        ormRun();
      });
    });

    var ormRun = function () {
      var w = parseFloat(wIn.value), r = parseInt(rIn.value, 10);
      if (!w || !r || r < 1 || r > 12) return;
      // Epley and Brzycki averaged; they diverge above ~10 reps
      var epley = w * (1 + r / 30);
      var brzycki = w * 36 / (37 - r);
      var max = (epley + brzycki) / 2;

      if (ormOut) ormOut.textContent = Math.round(max * 2) / 2 + ' ' + ormUnit;
      if (tblOut) {
        var rows = [[1, 100], [2, 95], [3, 92], [5, 87], [6, 85], [8, 80], [10, 75], [12, 70], [15, 65]];
        tblOut.innerHTML = rows.map(function (row) {
          var kgv = Math.round(max * row[1] / 100 * 2) / 2;
          return '<tr><td>' + row[0] + ' reps</td><td class="mono">' + row[1] + '%</td>' +
                 '<td class="mono">' + kgv + ' ' + ormUnit + '</td></tr>';
        }).join('');
      }
    };
    [wIn, rIn].forEach(function (n) {
      if (n) { n.addEventListener('input', ormRun); n.addEventListener('change', ormRun); }
    });
    ormRun();
  }
})();
