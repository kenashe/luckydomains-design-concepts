/* ---------------------------------------------------------------- 3. footer year, contact form, article contents list */
(function () {
  "use strict";

/*FORM*/

  // Article contents list: mark the section being read. The list works as plain links without this.
  var toc = document.querySelector(".art-toc");
  if (toc && "IntersectionObserver" in window) {
    var links = {};
    toc.querySelectorAll("a").forEach(function (a) { links[a.getAttribute("href").slice(1)] = a; });
    var mark = function (id) {
      Object.keys(links).forEach(function (k) { links[k].removeAttribute("aria-current"); });
      if (links[id]) links[id].setAttribute("aria-current", "true");
    };
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) mark(e.target.id); });
    }, { rootMargin: "-12% 0px -72% 0px" });
    Object.keys(links).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) spy.observe(el.tagName === "SECTION" ? (el.querySelector("h2") || el) : el);
    });
  }
})();
