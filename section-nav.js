/**
 * section-nav.js — Shared section navigation component for Canadian Trade Intel
 *
 * Usage:
 *   <script src="/section-nav.js"></script>
 *   <script>
 *     var ctrl = initSectionNav(sections, options);
 *     // ctrl.update(newSections) — swap sections (e.g. on tab switch)
 *     // ctrl.destroy()          — remove the nav
 *   </script>
 *
 * sections: [{id: 'section-id', label: 'Label text'}, ...]
 * options:
 *   mode        — 'horizontal' (default) | 'vertical'
 *   color       — accent hex, e.g. '#cc0000'
 *   topOffset   — px height of sticky elements above (default 56)
 *   scrollOffset — extra px to subtract from scroll target (default 16)
 */
(function (global) {
  'use strict';

  var STYLE_ID = 'section-nav-js-styles';
  var HZ_ID = 'sn-bar';
  var VT_ID = 'sn-side';

  // ── CSS ─────────────────────────────────────────────────────────────────────
  function injectStyles() {
    if (document.getElementById(STYLE_ID)) return;
    var css = [
      '/* section-nav.js */',

      /* ── Horizontal bar ── */
      '#sn-bar {',
      '  position: sticky; z-index: 150;',
      '  background: #f5f4ef; border-bottom: 1px solid #e0e0d8;',
      '  overflow-x: auto; white-space: nowrap;',
      '  scrollbar-width: none;',
      '}',
      '#sn-bar::-webkit-scrollbar { display: none; }',
      '#sn-bar .sn-inner {',
      '  display: inline-flex; gap: 0; padding: 0 40px;',
      '  max-width: 1100px; margin: 0 auto;',
      '}',
      '#sn-bar .sn-link {',
      '  font-family: "DM Mono", monospace;',
      '  font-size: 10px; letter-spacing: 0.11em; text-transform: uppercase;',
      '  color: #888; text-decoration: none;',
      '  padding: 11px 16px; border-bottom: 2px solid transparent;',
      '  margin-bottom: -1px; white-space: nowrap;',
      '  transition: color 0.18s, border-color 0.18s;',
      '  cursor: pointer; background: none; border-top: none; border-left: none; border-right: none;',
      '  display: inline-block;',
      '}',
      '#sn-bar .sn-link:hover { color: #444; }',
      '#sn-bar .sn-link.sn-active { border-bottom-color: var(--sn-color, #cc0000); color: #222; }',

      /* ── Vertical side nav ── */
      '#sn-side {',
      '  position: fixed; right: 28px;',
      '  top: var(--sn-vtop, 140px);',
      '  display: flex; flex-direction: column; gap: 10px;',
      '  z-index: 150;',
      '}',
      '#sn-side .sn-vlink {',
      '  display: flex; align-items: center; gap: 8px;',
      '  font-family: "DM Mono", monospace;',
      '  font-size: 9px; letter-spacing: 0.1em; text-transform: uppercase;',
      '  color: #aaa; text-decoration: none; cursor: pointer;',
      '  background: none; border: none; padding: 0;',
      '  text-align: left; max-width: 140px;',
      '  transition: color 0.18s;',
      '}',
      '#sn-side .sn-vlink::before {',
      '  content: ""; flex-shrink: 0;',
      '  width: 2px; height: 14px; border-radius: 1px;',
      '  background: #ddd;',
      '  transition: background 0.18s, height 0.18s;',
      '}',
      '#sn-side .sn-vlink:hover { color: #555; }',
      '#sn-side .sn-vlink:hover::before { background: #aaa; }',
      '#sn-side .sn-vlink.sn-active { color: var(--sn-color, #cc0000); }',
      '#sn-side .sn-vlink.sn-active::before { background: var(--sn-color, #cc0000); height: 20px; }',

      /* ── Mobile: vertical collapses to horizontal strip ── */
      '@media (max-width: 900px) {',
      '  #sn-side {',
      '    position: sticky; top: var(--sn-top, 56px); right: auto;',
      '    flex-direction: row; flex-wrap: nowrap;',
      '    overflow-x: auto; gap: 0;',
      '    background: #f5f4ef; border-bottom: 1px solid #e0e0d8;',
      '    padding: 0 16px; width: 100%;',
      '    scrollbar-width: none;',
      '  }',
      '  #sn-side::-webkit-scrollbar { display: none; }',
      '  #sn-side .sn-vlink {',
      '    flex-direction: row; max-width: none;',
      '    font-size: 9px; padding: 10px 10px;',
      '    border-bottom: 2px solid transparent;',
      '    white-space: nowrap;',
      '  }',
      '  #sn-side .sn-vlink::before { display: none; }',
      '  #sn-side .sn-vlink.sn-active { border-bottom-color: var(--sn-color, #cc0000); color: #222; }',
      '}',
      '@media (max-width: 768px) {',
      '  #sn-bar .sn-inner { padding: 0 16px; }',
      '}'
    ].join('\n');

    var style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = css;
    (document.head || document.body).appendChild(style);
  }

  // ── Helpers ──────────────────────────────────────────────────────────────────
  function getTopOffset(opts) {
    return (opts && opts.topOffset != null) ? opts.topOffset : 56;
  }

  function getScrollOffset(opts) {
    return (opts && opts.scrollOffset != null) ? opts.scrollOffset : 16;
  }

  function scrollTo(id, opts) {
    var el = document.getElementById(id);
    if (!el) return;
    var top = el.getBoundingClientRect().top + window.pageYOffset
              - getTopOffset(opts) - getScrollOffset(opts);
    window.scrollTo({ top: top, behavior: 'smooth' });
  }

  function setActiveLink(container, id) {
    container.querySelectorAll('[data-sn-id]').forEach(function (el) {
      el.classList.toggle('sn-active', el.getAttribute('data-sn-id') === id);
    });
  }

  // ── IntersectionObserver ─────────────────────────────────────────────────────
  function makeObserver(sections, container, topOffset) {
    var ids = sections.map(function (s) { return s.id; });
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          setActiveLink(container, entry.target.id);
        }
      });
    }, { rootMargin: '-' + (topOffset + 8) + 'px 0px -60% 0px', threshold: 0 });

    ids.forEach(function (id) {
      var el = document.getElementById(id);
      if (el) obs.observe(el);
    });
    return obs;
  }

  // ── Build horizontal bar ──────────────────────────────────────────────────────
  function buildHorizontalBar(sections, opts) {
    var bar = document.createElement('div');
    bar.id = HZ_ID;
    var topOffset = getTopOffset(opts);
    bar.style.top = topOffset + 'px';
    if (opts && opts.color) bar.style.setProperty('--sn-color', opts.color);

    var inner = document.createElement('div');
    inner.className = 'sn-inner';
    sections.forEach(function (s) {
      var a = document.createElement('button');
      a.className = 'sn-link';
      a.setAttribute('data-sn-id', s.id);
      a.textContent = s.label;
      a.addEventListener('click', function () { scrollTo(s.id, opts); });
      inner.appendChild(a);
    });
    bar.appendChild(inner);
    return bar;
  }

  // ── Build vertical side nav ────────────────────────────────────────────────────
  function buildVerticalNav(sections, opts) {
    var side = document.createElement('div');
    side.id = VT_ID;
    var topOffset = getTopOffset(opts);
    side.style.setProperty('--sn-top', topOffset + 'px');
    side.style.setProperty('--sn-vtop', (topOffset + 84) + 'px');
    if (opts && opts.color) side.style.setProperty('--sn-color', opts.color);

    sections.forEach(function (s) {
      var btn = document.createElement('button');
      btn.className = 'sn-vlink';
      btn.setAttribute('data-sn-id', s.id);
      btn.textContent = s.label;
      btn.addEventListener('click', function () { scrollTo(s.id, opts); });
      side.appendChild(btn);
    });
    return side;
  }

  // ── Insert after #main-nav ────────────────────────────────────────────────────
  function insertAfterMainNav(el) {
    var mainNav = document.getElementById('main-nav');
    if (mainNav && mainNav.parentNode) {
      mainNav.parentNode.insertBefore(el, mainNav.nextSibling);
    } else {
      document.body.insertBefore(el, document.body.firstChild);
    }
  }

  // ── Public API ────────────────────────────────────────────────────────────────
  global.initSectionNav = function (sections, opts) {
    injectStyles();

    var mode = (opts && opts.mode) ? opts.mode : 'horizontal';
    var container = null;
    var observer = null;
    var topOffset = getTopOffset(opts);

    function build(secs) {
      if (container) container.remove();
      if (observer) observer.disconnect();

      if (mode === 'vertical') {
        container = buildVerticalNav(secs, opts);
      } else {
        container = buildHorizontalBar(secs, opts);
      }

      function doInsert() {
        insertAfterMainNav(container);
        if (secs.length > 0) setActiveLink(container, secs[0].id);
        observer = makeObserver(secs, container, topOffset);
      }

      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', doInsert);
      } else {
        doInsert();
      }
    }

    build(sections);

    return {
      update: function (newSections) {
        build(newSections);
      },
      destroy: function () {
        if (container) container.remove();
        if (observer) observer.disconnect();
        container = null;
        observer = null;
      }
    };
  };

}(window));
