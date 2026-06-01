/* =========================================================
   쓰리 마사지 — shared header / footer / interactions
   Single source of truth for site navigation.
   Pages only need: <div id="site-header"></div> … <div id="site-footer"></div>
   ========================================================= */
(function () {
  "use strict";

  var PHONE_DISPLAY = "0508-202-4717";
  var PHONE_TEL = "tel:05082024717";

  /* ---- Operating regions (single data model) ---- */
  var REGIONS = [
    { key: "suwon-area", name: "수원권", areas: [
      { ko: "수원",   slug: "suwon" },
      { ko: "영통",   slug: "yeongtong" },
      { ko: "수원역", slug: "suwon-station" },
      { ko: "인계동", slug: "ingye-dong" },
      { ko: "구운동", slug: "guun-dong" }
    ]},
    { key: "dongtan-osan", name: "동탄·오산권", areas: [
      { ko: "동탄", slug: "dongtan" },
      { ko: "오산", slug: "osan" },
      { ko: "궐동", slug: "gwol-dong" }
    ]},
    { key: "yongin-area", name: "용인권", areas: [
      { ko: "용인",   slug: "yongin" },
      { ko: "처인구", slug: "cheoin-gu" },
      { ko: "수지",   slug: "suji" },
      { ko: "포곡",   slug: "pogok" },
      { ko: "신갈",   slug: "singal" },
      { ko: "기흥",   slug: "giheung" },
      { ko: "동백",   slug: "dongbaek" }
    ]},
    { key: "bundang-area", name: "분당권", areas: [
      { ko: "분당",   slug: "bundang" },
      { ko: "미금역", slug: "migeum-station" },
      { ko: "수내역", slug: "sunae-station" },
      { ko: "정자역", slug: "jeongja-station" },
      { ko: "서현역", slug: "seohyeon-station" }
    ]}
  ];

  /* ---- Magazine categories ---- */
  var MAG_CATS = [
    { slug: "all",             name: "전체" },
    { slug: "office-fatigue",  name: "직장인 피로 관리" },
    { slug: "family-care",     name: "가족·주거공간 케어" },
    { slug: "regional",        name: "지역별 웰니스 가이드" },
    { slug: "usage-guide",     name: "출장마사지 이용 가이드" },
    { slug: "safety-guide",    name: "서비스 안전 가이드" }
  ];

  /* ---- Top-level menu ---- */
  var MENU = [
    { label: "홈", href: "/" },
    { label: "서비스 안내", children: [
      { label: "출장마사지 안내", href: "/service/massage.html" },
      { label: "프로그램 안내",   href: "/service/program.html" },
      { label: "가격표",          href: "/service/price.html" },
      { label: "이용절차",        href: "/service/process.html" },
      { label: "예약 전 확인사항", href: "/service/checklist.html" }
    ]},
    { label: "지역안내", href: "/areas/", mega: true },
    { label: "매거진", children: MAG_CATS.map(function (c) {
        return { label: c.name, href: c.slug === "all" ? "/magazine/" : "/magazine/?cat=" + c.slug };
      })
    },
    { label: "FAQ", children: [
      { label: "예약 FAQ",        href: "/faq/reservation.html" },
      { label: "지역 FAQ",        href: "/faq/area.html" },
      { label: "이용 전 확인사항", href: "/faq/before-use.html" }
    ]},
    { label: "회사소개", children: [
      { label: "쓰리 마사지 소개", href: "/about/" },
      { label: "사업자 정보",      href: "/about/business.html" },
      { label: "문의",            href: "/about/contact.html" }
    ]}
  ];

  /* ---------- helpers ---------- */
  function el(html) { var t = document.createElement("template"); t.innerHTML = html.trim(); return t.content.firstChild; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]; }); }
  function isActive(href) {
    if (!href) return false;
    var path = location.pathname.replace(/index\.html$/, "");
    var h = href.replace(/index\.html$/, "");
    if (h === "/") return path === "/";
    return path === h || path.indexOf(h.replace(/\.html$/, "")) === 0 && h !== "/";
  }

  /* ---------- Desktop dropdown markup ---------- */
  function megaDropdown() {
    var groups = REGIONS.map(function (r) {
      var links = r.areas.map(function (a) {
        return '<a href="/areas/' + a.slug + '.html">' + esc(a.ko) + '</a>';
      }).join("");
      return '<div class="dd-group"><p>' + esc(r.name) + '</p><div class="dd-areas">' + links + "</div></div>";
    }).join("");
    return '<div class="dropdown dropdown--mega" role="menu">' + groups + "</div>";
  }

  function buildDesktopMenu() {
    return MENU.map(function (m) {
      if (m.mega) {
        return '<li class="nav-item has-dd"><a class="nav-link" href="' + m.href + '"' +
          (isActive(m.href) ? ' aria-current="page"' : "") + ">" + esc(m.label) + "</a>" + megaDropdown() + "</li>";
      }
      if (m.children) {
        var items = m.children.map(function (c) {
          return '<a href="' + c.href + '"' + (isActive(c.href) ? ' aria-current="page"' : "") + ">" + esc(c.label) + "</a>";
        }).join("");
        return '<li class="nav-item has-dd"><a class="nav-link" href="' + (m.children[0].href) + '">' + esc(m.label) +
          '</a><div class="dropdown" role="menu">' + items + "</div></li>";
      }
      return '<li class="nav-item"><a class="nav-link" href="' + m.href + '"' +
        (isActive(m.href) ? ' aria-current="page"' : "") + ">" + esc(m.label) + "</a></li>";
    }).join("");
  }

  /* ---------- Mobile accordion markup ---------- */
  function buildMobileMenu() {
    var html = "";
    MENU.forEach(function (m) {
      if (m.mega) {
        var groups = REGIONS.map(function (r) {
          var links = r.areas.map(function (a) {
            return '<a href="/areas/' + a.slug + '.html">' + esc(a.ko) + "</a>";
          }).join("");
          return '<p class="m-sub-title">' + esc(r.name) + '</p><div class="m-areas">' + links + "</div>";
        }).join("");
        html += '<div class="m-acc"><button class="m-row" type="button">' + esc(m.label) +
          '</button><div class="m-panel"><div class="m-panel-inner">' +
          '<a href="/areas/" style="font-weight:700">지역안내 전체 보기</a>' + groups + "</div></div></div>";
      } else if (m.children) {
        var items = m.children.map(function (c) { return '<a href="' + c.href + '">' + esc(c.label) + "</a>"; }).join("");
        html += '<div class="m-acc"><button class="m-row" type="button">' + esc(m.label) +
          '</button><div class="m-panel"><div class="m-panel-inner">' + items + "</div></div></div>";
      } else {
        html += '<div class="m-acc"><a class="m-row" href="' + m.href + '">' + esc(m.label) + "</a></div>";
      }
    });
    html += '<div class="mobile-cta">' +
      '<a class="btn btn--gold btn--block btn--lg" href="' + PHONE_TEL + '">전화예약 ' + PHONE_DISPLAY + "</a>" +
      '<a class="btn btn--ghost btn--block" href="/service/price.html">가격표 보기</a></div>';
    return html;
  }

  /* ---------- Header ---------- */
  function renderHeader() {
    var mount = document.getElementById("site-header");
    if (!mount) return;
    var header = el(
      '<header class="site-header">' +
        '<div class="container"><nav class="nav" aria-label="주요 메뉴">' +
          '<a class="brand" href="/" aria-label="쓰리 마사지 홈">' +
            '<img class="brand-logo" src="/assets/img/logo.svg" ' +
            'alt="쓰리 마사지" width="320" height="96" decoding="async"></a>' +
          '<ul class="nav-menu">' + buildDesktopMenu() + "</ul>" +
          '<div class="nav-cta">' +
            '<a class="btn btn--ghost" href="/service/price.html">가격표</a>' +
            '<a class="btn btn--gold" href="' + PHONE_TEL + '">전화예약 ' + PHONE_DISPLAY + "</a>" +
            '<button class="nav-toggle" type="button" aria-label="메뉴 열기" aria-expanded="false"><span></span></button>' +
          "</div>" +
        "</nav></div>" +
      "</header>" +
      '<div class="mobile-drawer" aria-label="모바일 메뉴">' + buildMobileMenu() + "</div>"
    );
    mount.replaceWith(header);
    wireInteractions();
  }

  /* ---------- Footer ---------- */
  function renderFooter() {
    var mount = document.getElementById("site-footer");
    if (!mount) return;
    var year = new Date().getFullYear();
    var areaCols = REGIONS.map(function (r) {
      return r.areas.slice(0, 4).map(function (a) {
        return '<a href="/areas/' + a.slug + '.html">' + esc(a.ko) + " 출장마사지</a>";
      }).join("");
    });
    var footer = el(
      '<footer class="site-footer"><div class="container">' +
        '<div class="footer-grid">' +
          '<div class="footer-brand"><b>쓰리 마사지</b>' +
            '<p>수원·동탄·오산·용인·분당 일부 권역을 중심으로 한 출장마사지 예약 안내 서비스입니다. ' +
            '휴식과 컨디션 관리를 위한 케어이며, 의료·치료 목적의 서비스가 아닙니다.</p></div>' +
          '<div><h4>서비스</h4>' +
            '<a href="/service/massage.html">출장마사지 안내</a>' +
            '<a href="/service/program.html">프로그램 안내</a>' +
            '<a href="/service/price.html">가격표</a>' +
            '<a href="/service/process.html">이용절차</a></div>' +
          '<div><h4>지역안내</h4>' + areaCols[0] + areaCols[3] + '<a href="/areas/">전체 지역 보기</a></div>' +
          '<div><h4>고객지원</h4>' +
            '<a href="/faq/reservation.html">예약 FAQ</a>' +
            '<a href="/about/">쓰리 마사지 소개</a>' +
            '<a href="/about/business.html">사업자 정보</a>' +
            '<a href="' + PHONE_TEL + '">전화예약 ' + PHONE_DISPLAY + "</a></div>" +
        "</div>" +
        '<div class="footer-biz">상호 쓰리 마사지 · 운영사 YH LAB · 대표 김유환 · ' +
          '사업자등록번호 815-26-00585 · 경기도 파주시 청석로 268 · 전화예약 ' + PHONE_DISPLAY + '</div>' +
        '<div class="footer-bottom">' +
          "<div>© " + year + ' 쓰리 마사지. All rights reserved.</div>' +
          '<div class="footer-legal">' +
            "<span>운영지역: 수원·동탄·오산·용인·분당 일부</span>" +
            "<span>건전한 휴식 케어 안내</span>" +
          "</div>" +
        "</div>" +
      "</div></footer>"
    );
    mount.replaceWith(footer);
  }

  /* ---------- Interactions ---------- */
  function wireInteractions() {
    var toggle = document.querySelector(".nav-toggle");
    if (toggle) {
      toggle.addEventListener("click", function () {
        var open = document.body.classList.toggle("menu-open");
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
        document.body.style.overflow = open ? "hidden" : "";
      });
    }
    // mobile accordions
    document.querySelectorAll(".mobile-drawer .m-acc > button.m-row").forEach(function (btn) {
      btn.addEventListener("click", function () { btn.parentElement.classList.toggle("open"); });
    });
    // close drawer on navigation
    document.querySelectorAll(".mobile-drawer a").forEach(function (a) {
      a.addEventListener("click", function () {
        document.body.classList.remove("menu-open");
        document.body.style.overflow = "";
      });
    });
  }

  /* ---------- Generic FAQ accordion (any page) ---------- */
  function wireFaq() {
    document.querySelectorAll(".faq-item .faq-q").forEach(function (q) {
      q.addEventListener("click", function () { q.parentElement.classList.toggle("open"); });
    });
  }

  /* ---------- Mobile sticky call bar (전화 전환) ---------- */
  function renderMobileCall() {
    if (document.querySelector(".mobile-call")) return;
    var bar = el('<a class="mobile-call" href="' + PHONE_TEL + '" aria-label="전화예약 ' + PHONE_DISPLAY + '">' +
      '<span class="mobile-call-ico" aria-hidden="true">📞</span> 전화예약 ' + PHONE_DISPLAY + "</a>");
    document.body.appendChild(bar);
  }

  /* ---------- Premium magazine article enhancer ---------- */
  function enhanceArticle() {
    var article = document.querySelector("article.prose");
    if (!article) return;
    if (document.querySelector(".reading-progress")) return;   // already enhanced
    document.body.classList.add("is-article");

    // reading progress bar
    var rp = el('<div class="reading-progress"><i></i></div>');
    document.body.appendChild(rp);
    var fill = rp.firstChild;
    function prog() {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      fill.style.width = (max > 0 ? (h.scrollTop / max * 100) : 0) + "%";
    }
    window.addEventListener("scroll", prog, { passive: true });
    window.addEventListener("resize", prog); prog();

    // byline: avatar + reading time
    var byline = document.querySelector(".page-head .byline");
    if (byline) {
      byline.insertAdjacentHTML("afterbegin",
        '<span class="byline-ava"><img src="/favicon.svg" alt="" width="26" height="26"></span>');
      var chars = (article.textContent || "").replace(/\s/g, "").length;
      var mins = Math.max(2, Math.round(chars / 500));
      byline.insertAdjacentHTML("beforeend",
        '<span class="byline-sep">·</span> 읽는 시간 약 ' + mins + "분");
    }

    // table of contents (section h3) + scrollspy
    var heads = Array.prototype.slice.call(article.querySelectorAll("h3"));
    if (heads.length >= 2) {
      var layout = document.createElement("div");
      layout.className = "article-layout";
      article.parentNode.insertBefore(layout, article);
      layout.appendChild(article);
      var toc = el('<aside class="toc"><p class="toc-title">목차</p><nav class="toc-list"></nav></aside>');
      var list = toc.querySelector(".toc-list");
      var links = heads.map(function (h, i) {
        if (!h.id) h.id = "sec-" + (i + 1);
        var a = document.createElement("a");
        a.href = "#" + h.id; a.textContent = h.textContent;
        list.appendChild(a); return a;
      });
      layout.appendChild(toc);
      var spy = function () {
        var cur = -1;
        heads.forEach(function (h, i) { if (h.getBoundingClientRect().top <= 140) cur = i; });
        links.forEach(function (a, i) { a.classList.toggle("active", i === cur); });
      };
      window.addEventListener("scroll", spy, { passive: true }); spy();
    }

    injectRelatedPosts(article);
  }

  function injectRelatedPosts(article) {
    var container = article.closest(".container");
    if (!container) return;
    var slug = (location.pathname.split("/").pop() || "").replace(".html", "");
    var catName = ((document.querySelector(".page-head .eyebrow") || {}).textContent || "").trim();
    var s = document.createElement("script");
    s.src = "/assets/js/posts.js";
    s.onload = function () {
      if (!window.POSTS || !window.SITE) return;
      var catSlug = (window.SITE.MAG_CATS.filter(function (c) { return c.name === catName; })[0] || {}).slug;
      var others = window.POSTS.filter(function (p) { return p.slug !== slug; });
      var picked = others.filter(function (p) { return p.cat === catSlug; }).slice(0, 3);
      others.forEach(function (p) { if (picked.length < 3 && picked.indexOf(p) < 0) picked.push(p); });
      if (!picked.length) return;
      var cards = picked.map(function (p) {
        var cn = (window.SITE.MAG_CATS.filter(function (c) { return c.slug === p.cat; })[0] || {}).name || "";
        return '<a class="card post-card" href="/magazine/' + p.slug + '.html">' +
          '<span class="post-cat">' + cn + '</span><h3>' + p.title + '</h3>' +
          '<p>' + p.excerpt + '</p>' +
          (p.date ? '<span class="post-date">발행 ' + p.date + '</span>' : '') +
          '<span class="card-link">읽어보기</span></a>';
      }).join("");
      var sec = el('<section class="related-posts"><h2>함께 보면 좋은 글</h2>' +
        '<div class="grid grid-3">' + cards + '</div></section>');
      container.appendChild(sec);
    };
    document.body.appendChild(s);
  }

  /* ---------- expose data for page scripts ---------- */
  window.SITE = { REGIONS: REGIONS, MAG_CATS: MAG_CATS, PHONE_DISPLAY: PHONE_DISPLAY, PHONE_TEL: PHONE_TEL };

  document.addEventListener("DOMContentLoaded", function () {
    renderHeader();
    renderFooter();
    wireFaq();
    renderMobileCall();
    enhanceArticle();
  });
})();
