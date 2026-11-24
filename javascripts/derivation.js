/* 式変形ステッパー。<div class="deriv" markdown> の直下の div を1ステップとして送る。 */
(function () {
  function prefersReduced() {
    return window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function build(root) {
    if (root.dataset.derivReady === "1") return;
    var steps = Array.prototype.filter.call(root.children, function (el) {
      return el.tagName === "DIV" && !el.classList.contains("deriv-bar");
    });
    if (steps.length < 2) return;
    root.dataset.derivReady = "1";

    var bar = document.createElement("div");
    bar.className = "deriv-bar";
    bar.innerHTML =
      '<button type="button" class="deriv-btn deriv-ghost" data-act="prev">◀ 戻る</button>' +
      '<span class="deriv-count" role="status" aria-live="polite"></span>' +
      '<button type="button" class="deriv-btn" data-act="next">次の式へ ▶</button>' +
      '<button type="button" class="deriv-btn deriv-ghost" data-act="all">すべて表示</button>' +
      '<button type="button" class="deriv-btn deriv-ghost" data-act="reset">最初から</button>' +
      '<span class="deriv-done" hidden>できあがり</span>';
    root.appendChild(bar);

    var cur = 1;
    var count = bar.querySelector(".deriv-count");
    var done = bar.querySelector(".deriv-done");
    var btnPrev = bar.querySelector('[data-act="prev"]');
    var btnNext = bar.querySelector('[data-act="next"]');

    function render() {
      for (var i = 0; i < steps.length; i++) {
        steps[i].classList.toggle("is-on", i < cur);
        steps[i].classList.toggle("is-new", i === cur - 1 && cur > 1);
      }
      count.textContent = cur + " / " + steps.length;
      btnPrev.disabled = cur <= 1;
      btnNext.disabled = cur >= steps.length;
      done.hidden = cur < steps.length;
    }

    function go(n, scroll) {
      var next = Math.min(Math.max(n, 1), steps.length);
      if (next === cur) return;
      cur = next;
      render();
      if (scroll) {
        steps[cur - 1].scrollIntoView({
          block: "nearest",
          behavior: prefersReduced() ? "auto" : "smooth"
        });
      }
    }

    bar.addEventListener("click", function (e) {
      var b = e.target.closest ? e.target.closest("button") : null;
      if (!b) return;
      var a = b.dataset.act;
      if (a === "next") go(cur + 1, true);
      else if (a === "prev") go(cur - 1, false);
      else if (a === "all") go(steps.length, false);
      else if (a === "reset") go(1, false);
    });

    bar.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); go(cur + 1, true); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); go(cur - 1, false); }
    });

    render();
  }

  function init() {
    var list = document.querySelectorAll(".deriv");
    for (var i = 0; i < list.length; i++) build(list[i]);
  }

  if (window.document$ && window.document$.subscribe) {
    window.document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
