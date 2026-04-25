/**
 * nav.js — Shared navigation component for Canadian Trade Intel
 *
 * Usage: Add to every page <head>:
 *   <script src="/nav.js"></script>
 * And replace any hardcoded <nav> with:
 *   <nav id="main-nav"></nav>
 *
 * This script:
 *  1. Injects canonical nav CSS immediately (no flash of unstyled nav)
 *  2. Injects nav HTML after DOM is ready
 *  3. Auto-highlights the active link by pathname
 *  4. Wires up the mobile hamburger menu
 *
 * To update nav links sitewide: edit this file only.
 */
(function () {
  'use strict';

  // ── Fonts ───────────────────────────────────────────────────────────
  if (!document.getElementById('nav-js-fonts')) {
    var fontLink = document.createElement('link');
    fontLink.id = 'nav-js-fonts';
    fontLink.rel = 'stylesheet';
    fontLink.href = 'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=DM+Mono:wght@400;500&family=Jost:wght@300;400;500;600&display=swap';
    document.head.appendChild(fontLink);
  }

  // ── CSS ────────────────────────────────────────────────────────────
  var css = [
    '/* nav.js — canonical shared nav styles */',
    'nav#main-nav {',
    '  position: sticky; top: 0; z-index: 200;',
    '  background: #1a0505;',
    '  border-bottom: 1px solid rgba(204,0,0,0.2);',
    '  padding: 0 40px; height: 56px;',
    '}',
    '#main-nav .nav-inner {',
    '  max-width: 1200px; margin: 0 auto;',
    '  display: flex; align-items: center; justify-content: space-between;',
    '  height: 100%;',
    '}',
    '#main-nav .nav-brand {',
    '  font-family: "Cormorant Garamond", Georgia, serif;',
    '  font-size: 17px; font-weight: 600; font-style: italic; color: #f0ece4;',
    '  text-decoration: none;',
    '}',
    '#main-nav .nav-links {',
    '  display: flex; gap: 28px; align-items: center;',
    '}',
    '#main-nav .nav-links > a {',
    '  font-family: "DM Mono", monospace;',
    '  font-size: 10px; letter-spacing: 0.12em; text-transform: uppercase;',
    '  color: rgba(255,255,255,0.85); text-decoration: none; transition: color 0.2s;',
    '}',
    '#main-nav .nav-links > a:hover { color: rgba(204,0,0,0.9); }',
    '#main-nav .nav-links > a.active { color: #ffffff; border-bottom: 1px solid rgba(255,255,255,0.5); padding-bottom: 2px; }',
    '#main-nav .nav-dropdown {',
    '  position: relative; display: inline-flex; align-items: center;',
    '}',
    '#main-nav .nav-dropdown-btn {',
    '  font-family: "DM Mono", monospace;',
    '  font-size: 10px; letter-spacing: 0.12em; text-transform: uppercase;',
    '  color: rgba(255,255,255,0.6); background: none; border: none;',
    '  cursor: pointer; padding: 0; transition: color 0.2s;',
    '}',
    '#main-nav .nav-dropdown-btn:hover,',
    '#main-nav .nav-dropdown-btn.active { color: #ffffff; }',
    '#main-nav .nav-dropdown:hover .nav-dropdown-menu { display: block; }',
    '#main-nav .nav-dropdown-menu {',
    '  display: none; position: absolute; top: 100%; right: 0;',
    '  background: #1a0505; border: 1px solid rgba(204,0,0,0.2);',
    '  min-width: 240px; z-index: 400; padding: 8px 0 10px;',
    '  box-shadow: 0 8px 24px rgba(0,0,0,0.4);',
    '}',
    '#main-nav .nav-dropdown-label {',
    '  display: block; padding: 10px 16px 5px;',
    '  font-family: "DM Mono", monospace;',
    '  font-size: 8px; letter-spacing: 0.2em; text-transform: uppercase;',
    '  color: rgba(204,0,0,0.55); pointer-events: none;',
    '}',
    '#main-nav .nav-dropdown-divider {',
    '  height: 1px; background: rgba(255,255,255,0.07);',
    '  margin: 6px 0;',
    '}',
    '#main-nav .nav-dropdown-menu a {',
    '  display: block; padding: 8px 16px;',
    '  font-family: "DM Mono", monospace;',
    '  font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase;',
    '  color: rgba(255,255,255,0.6); text-decoration: none;',
    '  transition: color 0.16s, background 0.16s;',
    '}',
    '#main-nav .nav-dropdown-menu a:hover { color: #fff; background: rgba(204,0,0,0.1); }',
    '#main-nav .nav-dropdown-menu a.active { color: rgba(204,0,0,0.9); }',
    '#main-nav .nav-cta {',
    '  background: #cc0000 !important; color: #fff !important;',
    '  padding: 8px 16px; border-radius: 3px;',
    '  font-family: "DM Mono", monospace;',
    '  font-size: 10px; letter-spacing: 0.12em; text-transform: uppercase;',
    '  text-decoration: none; transition: background 0.2s;',
    '}',
    '#main-nav .nav-cta:hover { background: #aa0000 !important; }',
    '#main-nav .nav-hamburger {',
    '  display: none; flex-direction: column; justify-content: center; gap: 5px;',
    '  background: none; border: none; cursor: pointer; padding: 4px;',
    '}',
    '#main-nav .nav-hamburger span {',
    '  display: block; width: 22px; height: 2px;',
    '  background: rgba(255,255,255,0.6); border-radius: 2px;',
    '  transition: all 0.25s; transform-origin: center;',
    '}',
    '#main-nav .nav-hamburger.open span:nth-child(1) { transform: translateY(7px) rotate(45deg); }',
    '#main-nav .nav-hamburger.open span:nth-child(2) { opacity: 0; }',
    '#main-nav .nav-hamburger.open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }',
    '#main-nav .nav-mobile-menu {',
    '  display: none; flex-direction: column;',
    '  position: absolute; top: 56px; left: 0; right: 0;',
    '  background: #1a0505; border-bottom: 1px solid rgba(204,0,0,0.2);',
    '  padding: 16px 24px 20px; gap: 0; z-index: 300;',
    '}',
    '#main-nav .nav-mobile-menu.open { display: flex; }',
    '#main-nav .nav-mobile-menu a {',
    '  font-family: "DM Mono", monospace;',
    '  font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase;',
    '  color: rgba(255,255,255,0.6); text-decoration: none;',
    '  padding: 11px 0; border-bottom: 1px solid rgba(255,255,255,0.06);',
    '}',
    '#main-nav .nav-mobile-menu a:last-child { border-bottom: none; }',
    '#main-nav .nav-mobile-menu a:hover { color: #fff; }',
    '#main-nav .nav-mobile-menu .nav-mobile-section {',
    '  font-family: "DM Mono", monospace;',
    '  font-size: 8px; letter-spacing: 0.2em; text-transform: uppercase;',
    '  color: rgba(204,0,0,0.5); padding: 14px 0 4px;',
    '  border-bottom: none; pointer-events: none;',
    '}',
    '#main-nav .nav-mobile-menu .nav-cta-mobile {',
    '  color: rgba(204,0,0,0.9) !important; margin-top: 4px;',
    '}',
    '@media (max-width: 768px) {',
    '  nav#main-nav { padding: 0 20px; }',
    '  #main-nav .nav-links { display: none; }',
    '  #main-nav .nav-hamburger { display: flex; }',
    '}'
  ].join('\n');

  var style = document.createElement('style');
  style.id = 'nav-js-styles';
  style.textContent = css;
  document.head.appendChild(style);

  // ── HTML ────────────────────────────────────────────────────────────
  var navHTML = '<div class="nav-inner">' +
    '<a href="/" class="nav-brand">Canadian Trade Intelligence</a>' +
    '<div class="nav-links">' +
      '<a href="/dashboard/">Dashboard</a>' +
      '<a href="/procurement/">Procurement</a>' +
      '<a href="/spotlight/">Spotlight</a>' +
      '<a href="/countries/">Countries</a>' +
      '<a href="/canada-forward/">Canada Forward</a>' +
      '<a href="/reports/">Reports</a>' +
      '<div class="nav-dropdown">' +
        '<button class="nav-dropdown-btn">Resources \u25be</button>' +
        '<div class="nav-dropdown-menu">' +
          '<span class="nav-dropdown-label">Reference</span>' +
          '<a href="/resources/trade-agreements/">Trade Agreements</a>' +
          '<a href="/tariffs/">Tariff Reference</a>' +
          '<a href="/tools/sanctions-check/">Sanctions Screener</a>' +
          '<a href="/guides/">Practical Guides</a>' +
          '<a href="/map/">Business Map \u2192 <small style="opacity:0.55;font-size:0.85em;">(coming soon)</small></a>' +
          '<a href="/methodology/">Methodology</a>' +
          '<div class="nav-dropdown-divider"></div>' +
          '<a href="/about/">About CTI</a>' +
        '</div>' +
      '</div>' +
      '<a href="/pricing/" class="nav-cta">See Plans</a>' +
    '</div>' +
    '<button class="nav-hamburger" id="nav-hamburger" aria-label="Menu">' +
      '<span></span><span></span><span></span>' +
    '</button>' +
  '</div>' +
  '<div class="nav-mobile-menu" id="nav-mobile-menu">' +
    '<a href="/dashboard/">Dashboard</a>' +
    '<a href="/procurement/">Procurement Hub</a>' +
    '<a href="/spotlight/">Canadian Spotlight</a>' +
    '<a href="/countries/">Countries</a>' +
    '<a href="/canada-forward/">Canada Forward</a>' +
    '<a href="/reports/">Reports</a>' +
    '<span class="nav-mobile-section">Resources</span>' +
    '<a href="/resources/trade-agreements/">Trade Agreements</a>' +
    '<a href="/tariffs/">Tariff Reference</a>' +
    '<a href="/tools/sanctions-check/">Sanctions Screener</a>' +
    '<a href="/guides/">Practical Guides</a>' +
    '<a href="/map/">Business Map (coming soon)</a>' +
    '<a href="/methodology/">Methodology</a>' +
    '<a href="/about/">About CTI</a>' +
    '<a href="/pricing/" class="nav-cta-mobile">See Plans</a>' +
  '</div>';

  // ── Init ────────────────────────────────────────────────────────────
  function init() {
    var nav = document.getElementById('main-nav');
    if (!nav) return;

    nav.innerHTML = navHTML;

    // Auto-highlight active link based on pathname
    var rawPath = window.location.pathname;
    var path = rawPath.replace(/\/$/, '') || '/';
    var links = nav.querySelectorAll('a[href]');
    links.forEach(function (a) {
      var href = a.getAttribute('href').replace(/\/$/, '') || '/';
      if (href === '/') return; // never highlight home link
      if (path === href || path.startsWith(href + '/')) {
        if (!a.classList.contains('nav-cta') && !a.classList.contains('nav-cta-mobile')) {
          a.classList.add('active');
        }
      }
    });

    // Highlight Resources dropdown button when on a Resources sub-page
    var resourcePaths = ['/map', '/resources', '/tariffs', '/guides', '/methodology', '/tools', '/about'];
    var btn = nav.querySelector('.nav-dropdown-btn');
    if (btn && resourcePaths.some(function (p) { return path === p || path.startsWith(p + '/'); })) {
      btn.classList.add('active');
    }

    // Mobile menu toggle
    var hamburger = document.getElementById('nav-hamburger');
    var mobileMenu = document.getElementById('nav-mobile-menu');
    if (hamburger && mobileMenu) {
      hamburger.addEventListener('click', function (e) {
        e.stopPropagation();
        hamburger.classList.toggle('open');
        mobileMenu.classList.toggle('open');
      });
    }

    // Close on outside click
    document.addEventListener('click', function (e) {
      if (nav && !nav.contains(e.target)) {
        if (hamburger) hamburger.classList.remove('open');
        if (mobileMenu) mobileMenu.classList.remove('open');
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
