# 쓰리 마사지 (Three Massage)

수원·동탄·오산·용인·분당 일부 운영지역을 중심으로 한 **출장마사지 예약 안내** 정적 사이트입니다.
빌드 도구·의존성 없이 순수 HTML/CSS/바닐라 JS로 동작하며, 도메인 루트에 그대로 배포하면 됩니다.

## 구조

```
/
├─ index.html                 홈
├─ service/
│  ├─ massage.html            출장마사지 안내
│  ├─ program.html            프로그램 안내
│  ├─ price.html              가격표 (다크 프리미엄 카드 + 구조화 데이터)
│  ├─ process.html            이용절차
│  └─ checklist.html          예약 전 확인사항
├─ areas/
│  ├─ index.html              지역안내 (권역별)
│  └─ <slug>.html             20개 지역 상세 페이지(예약 전환용)
├─ magazine/
│  ├─ index.html              매거진 목록 (카테고리 필터)
│  └─ <slug>.html             매거진 글(생활정보 제공용)
├─ faq/
│  ├─ reservation.html        예약 FAQ
│  ├─ area.html               지역 FAQ
│  └─ before-use.html         이용 전 확인사항
├─ about/
│  ├─ index.html              쓰리 마사지 소개
│  ├─ business.html           사업자 정보 (운영자가 실제 값 입력 필요)
│  └─ contact.html            문의
├─ assets/
│  ├─ css/styles.css          디자인 시스템 (다크 + 웜골드)
│  └─ js/
│     ├─ site.js              상단 메뉴/모바일 아코디언/푸터 (단일 소스)
│     └─ posts.js             매거진 글 목록(생성물)
├─ sitemap.xml / robots.txt   (생성물)
├─ 404.html
└─ tools/generate.py          지역/매거진 페이지·사이트맵 생성 스크립트
```

## 네비게이션 / 콘텐츠 수정

- 상단 메뉴·운영지역·매거진 카테고리는 **`assets/js/site.js`** 의 `MENU` / `REGIONS` / `MAG_CATS` 데이터가 단일 소스입니다.
  데스크톱 드롭다운(지역안내는 권역별 메가 드롭다운)과 모바일 아코디언이 이 데이터로 자동 생성됩니다.
- 지역 상세 페이지와 매거진 글은 **`tools/generate.py`** 의 `AREAS` / `EXTRA_POSTS` 데이터에서 생성합니다.
  지역명만 바꾼 복붙형 양산을 피하기 위해 각 지역마다 생활상황·대상 중심의 개별 문구를 두었습니다.
  데이터 수정 후 재생성:

  ```bash
  python3 tools/generate.py
  ```

  > `site.js`(메뉴용 지역 목록)와 `generate.py`(지역 페이지 생성)의 지역 slug는 동일하게 유지하세요.

## 콘텐츠 정책

- **지역 페이지 = 예약 전환용**, **매거진 글 = 생활정보 제공용** 으로 역할을 분리해 중복을 피했습니다.
- 운영지역(수원·동탄·오산·용인·분당 일부)만 노출하며, 강남·송파·홍대·광교·영등포 등 비운영지역은 포함하지 않습니다.
- 휴식·컨디션 관리를 위한 건전한 케어 안내이며, 의료·치료 목적이 아님을 전 페이지에 명시했습니다.

## 배포 전 확인

- 도메인은 `https://3massage.netlify.app` 기준으로 설정되어 있습니다. 변경 시 `tools/generate.py`의 `BASE`와
  각 페이지 `canonical`/`og`/구조화 데이터 값을 함께 바꾸세요.
- 사업자 정보(`about/business.html` 및 메인 신뢰 섹션)는 실제 값(YH LAB · 김유환 · 815-26-00585 · 파주 청석로 268)으로 반영되어 있습니다.
- 루트 도메인 배포 기준의 절대경로(`/...`)를 사용합니다. 하위 경로 배포 시 경로 조정이 필요합니다.

## 이미지 / 로고

- 헤더 로고는 경량 SVG(`assets/img/logo.svg`, 약 1KB · 무손실 확대)로 전 페이지에 사용됩니다.
- schema.org `logo`는 `assets/img/logo-512.png`(원본 로고를 512px로 리사이즈·여백 트림, 약 67KB)를 참조합니다.
- 소셜 공유 이미지는 `assets/img/og-default.png`(1200×630, 약 100KB)입니다. 전 페이지 `og:image`/`twitter:image`에 적용됩니다.
- 위 두 래스터는 `tools/make_images.py`로 원본 로고에서 재생성할 수 있습니다(Pillow + 나눔고딕 필요).
  원본 고해상도 로고가 필요하면 별도 보관하세요(리포에서는 용량 절감을 위해 512px 버전만 유지).

## 로컬 미리보기

```bash
python3 -m http.server 8000
# http://localhost:8000
```

## 배포 (Cloudflare Pages)

정적 사이트라 **빌드 명령 없이** 그대로 배포됩니다.

1. Cloudflare Pages → **Create a project** → Git 저장소(`guhara1/3massage`) 연결
2. 빌드 설정:
   - Framework preset: **None**
   - Build command: *(비움)*
   - Build output directory: **`/`** (루트)
   - (콘텐츠 수정 시 `python3 tools/generate.py`로 재생성 후 커밋 — Pages 빌드 단계에서 파이썬을 돌리지 않음)
3. 배포 후 **Custom domains** 에 `3massage.netlify.app` 연결(루트 도메인). www는 아래 리다이렉트로 흡수.
4. 도메인 정규화는 리포의 **`_redirects`** 가 처리:
   - `www.3massage.netlify.app/*` → `3massage.netlify.app/*` (301)
   - `*.pages.dev/*` → `3massage.netlify.app/*` (301)
5. 캐싱·보안 헤더는 **`_headers`** 가 처리(정적 자산 장기 캐시, 사이트맵·RSS 짧은 캐시).

> 사이트 전체 canonical이 **non-www(`https://3massage.netlify.app`)** 기준입니다.
> 서치콘솔/네이버 속성도 `https://3massage.netlify.app` 으로 등록하고 사이트맵·RSS를 제출하세요.

