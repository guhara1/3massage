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
          '<a class="brand" href="/"><b>쓰리 마사지</b><span>Three Massage</span></a>' +
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

  /* ---------- expose data for page scripts ---------- */
  window.SITE = { REGIONS: REGIONS, MAG_CATS: MAG_CATS, PHONE_DISPLAY: PHONE_DISPLAY, PHONE_TEL: PHONE_TEL };

  document.addEventListener("DOMContentLoaded", function () {
    renderHeader();
    renderFooter();
    wireFaq();
  });
})();
