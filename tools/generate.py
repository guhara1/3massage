#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
쓰리 마사지 static site generator.

Produces the area pages and magazine articles from a single data model so that
every page shares the same SEO scaffold while keeping per-page copy distinct.
Run:  python3 tools/generate.py
"""
import os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.3massage.co.kr"   # canonical base — change to the live domain
PHONE_DISPLAY = "0508-202-4717"
PHONE_TEL = "tel:05082024717"


def won(n):
    return f"{n:,}원"


def eun_neun(word):
    """Pick the Korean topic particle 은/는 by final-consonant of the last char."""
    last = word[-1]
    if "가" <= last <= "힣":
        return "은" if (ord(last) - 0xAC00) % 28 else "는"
    return "는"


# ---------------------------------------------------------------------------
# Programs (shared by price page, program page, area pages)
# ---------------------------------------------------------------------------
PROGRAMS = [
    {"name": "타이 건식", "cat": "DRY · 건식", "best": False,
     "desc": "옷 위에서 진행되는 건식 케어. 깊은 압과 관절 가동 범위 중심의 관리로 일상 속 긴장을 완화하는 기본 프로그램.",
     "prices": [("60분", 80000), ("90분", 100000), ("120분", 120000)]},
    {"name": "아로마 오일", "cat": "WET · 오일", "best": False,
     "desc": "아로마 오일을 활용한 부드러운 케어. 편안한 휴식감과 촉촉한 오일 케어를 원하는 고객에게 적합한 프로그램.",
     "prices": [("60분", 90000), ("90분", 110000), ("120분", 130000)]},
    {"name": "시그니처 오일", "cat": "SIGNATURE · 오일", "best": False,
     "desc": "쓰리 마사지의 대표 오일 케어. 강도보다 흐름과 안정감에 집중한 프리미엄 휴식 프로그램.",
     "prices": [("60분", 100000), ("90분", 120000), ("120분", 140000)]},
    {"name": "VVIP 전신케어", "cat": "VVIP · 풀바디", "best": True,
     "desc": "건식과 오일 케어가 함께 구성된 프리미엄 전신 프로그램. 발끝부터 두피까지 여유롭게 관리받고 싶은 고객에게 적합.",
     "prices": [("60분", 110000), ("90분", 130000), ("120분", 150000), ("150분", 180000)]},
    {"name": "한국인 스웨디시", "cat": "KOREAN · 관리사 지정", "best": False,
     "desc": "한국인 관리사 지정 프로그램. 섬세한 강도 조절과 편안한 의사소통을 중요하게 생각하는 고객에게 적합.",
     "prices": [("60분", 150000), ("90분", 190000)]},
    {"name": "남성 스웨디시", "cat": "MEN · 남성 전용", "best": False,
     "desc": "남성 고객을 위한 전용 프로그램. 예약 전 컨디션과 선호 강도를 확인한 뒤 편안한 이용을 돕는 프로그램.",
     "prices": [("60분", 100000), ("90분", 130000), ("120분", 160000)]},
]

CHECKLIST = [
    "위 금액은 프로그램과 이용 시간 기준 안내 금액입니다.",
    "지역별 이동 가능 여부와 예약 가능 시간은 전화예약 시 확인해 주세요.",
    "운영지역은 수원, 동탄, 오산, 용인, 분당 일부 권역으로 한정됩니다.",
    "불건전한 목적의 문의는 받지 않습니다.",
    "의료행위나 치료 목적의 서비스가 아니며, 휴식과 컨디션 관리를 위한 방문 케어 안내입니다.",
]

CATS = {
    "office-fatigue": "직장인 피로 관리",
    "family-care": "가족·주거공간 케어",
    "regional": "지역별 웰니스 가이드",
    "usage-guide": "출장마사지 이용 가이드",
    "safety-guide": "서비스 안전 가이드",
}

# ---------------------------------------------------------------------------
# Areas — each carries bespoke copy so pages are not region-name swaps.
#   region   : display region name
#   life     : life-situation framing
#   landmark : one-line local context (used on the conversion page)
#   reasons  : 3 bullets — who this area's visiting care suits
#   article  : info-purpose magazine piece (title / cat / excerpt / 2-3 paragraphs)
# ---------------------------------------------------------------------------
AREAS = [
 # ---- 수원권 ----
 {"ko":"수원","slug":"suwon","region":"수원권",
  "landmark":"수원 도심과 인계동·영통 일대를 아우르는 넓은 거주·업무 생활권입니다.",
  "reasons":["서울로 장거리 출퇴근해 저녁 시간이 짧은 직장인","집에서 바로 휴식을 이어가고 싶은 분","외출 없이 컨디션을 정리하고 싶은 1인 가구"],
  "article":{"title":"수원에서 서울로 출퇴근하는 직장인의 피로 관리 방법","cat":"office-fatigue",
    "excerpt":"왕복 두세 시간 출퇴근이 쌓이는 어깨·허리 부담을, 퇴근 후 집에서 정리하는 현실적인 루틴을 정리했습니다.",
    "body":["수원에서 서울로 출퇴근하면 이동 시간만 왕복 두세 시간에 이르는 경우가 많습니다. 지하철·버스에서 같은 자세로 오래 버티다 보면 어깨와 허리에 긴장이 쌓이고, 집에 도착할 때쯤이면 이미 외출할 기운이 남지 않습니다.",
      "이럴 때 필요한 건 거창한 관리가 아니라, 짧은 시간이라도 같은 시간에 몸을 풀어 주는 규칙적인 루틴입니다. 샤워 후 가벼운 스트레칭으로 굳은 부위를 먼저 알아차리고, 호흡을 길게 가져가며 긴장을 내려놓는 것만으로도 다음 날 컨디션이 달라집니다.",
      "외출이 부담스러운 날에는 집에서 받는 방문 케어를 활용할 수 있습니다. 이동 시간을 더 쓰지 않고 휴식으로 바로 이어진다는 점이 장거리 출퇴근자에게는 특히 큰 차이를 만듭니다."]}},
 {"ko":"영통","slug":"yeongtong","region":"수원권",
  "landmark":"삼성 디지털시티와 가까운 오피스·주거 밀집 생활권입니다.",
  "reasons":["하루 종일 모니터 앞에 앉아 일하는 사무직","목과 어깨 결림이 잦은 분","퇴근 후 바로 쉬고 싶은 영통 거주자"],
  "article":{"title":"영통 거주 직장인을 위한 퇴근 후 어깨·목 피로 관리","cat":"office-fatigue",
    "excerpt":"장시간 모니터 작업으로 굳기 쉬운 목·어깨를, 퇴근 후 집에서 단계적으로 풀어 주는 방법을 정리했습니다.",
    "body":["영통은 대형 오피스가 밀집해 사무직 비중이 높은 지역입니다. 하루 대부분을 모니터 앞에서 보내면 목이 앞으로 빠지는 자세가 굳어지고, 어깨 위쪽이 묵직하게 뭉치기 쉽습니다.",
      "퇴근 후에는 먼저 목을 천천히 좌우로 돌려 가동 범위를 확인하고, 따뜻한 물로 어깨 위쪽을 데워 주면 긴장이 한결 풀립니다. 자기 전 휴대폰을 멀리 두는 것만으로도 목 부담을 줄일 수 있습니다.",
      "결림이 며칠째 이어진다면 집에서 받는 방문 케어로 굳은 부위를 차분히 정리하는 것도 방법입니다. 다만 통증이 심하거나 지속된다면 먼저 의료기관 상담을 받는 것이 우선입니다."]}},
 {"ko":"수원역","slug":"suwon-station","region":"수원권",
  "landmark":"환승과 상권이 집중된 수원역 일대의 직장·유동 인구 생활권입니다.",
  "reasons":["야근이 잦아 늦게 귀가하는 직장인","불규칙한 일정으로 컨디션 관리가 어려운 분","역 인근에서 빠르게 휴식을 정리하고 싶은 분"],
  "article":{"title":"수원역 인근 직장인을 위한 야근 후 컨디션 회복 가이드","cat":"office-fatigue",
    "excerpt":"늦은 귀가가 반복될 때 수면의 질을 지키며 다음 날 컨디션을 회복하는 순서를 정리했습니다.",
    "body":["수원역 일대는 환승과 상권이 몰려 야근과 늦은 귀가가 잦은 직장인이 많습니다. 늦게 잠들면 다음 날 피로가 그대로 이어지기 쉬워, 회복의 핵심은 결국 수면의 질입니다.",
      "귀가 후에는 강한 빛과 카페인을 피하고, 따뜻한 물로 가볍게 씻으며 몸의 온도를 천천히 낮추는 것이 도움이 됩니다. 굳은 종아리와 발을 가볍게 눌러 주면 잠들기 전 긴장이 풀립니다.",
      "야근이 며칠 이어진 주에는 집에서 받는 방문 케어로 누적된 피로를 한 번 정리해 주는 것도 방법입니다. 이동 없이 휴식으로 바로 이어진다는 점이 늦은 시간대에는 특히 편안합니다."]}},
 {"ko":"인계동","slug":"ingye-dong","region":"수원권",
  "landmark":"수원 대표 오피스·상권이 모인 인계동 업무 생활권입니다.",
  "reasons":["방문 케어를 처음 이용해 절차가 궁금한 분","예약 전 준비사항을 미리 확인하고 싶은 분","오피스 근처 거주로 짧은 휴식을 자주 찾는 직장인"],
  "article":{"title":"인계동 오피스 근무자를 위한 방문 마사지 이용 전 체크리스트","cat":"usage-guide",
    "excerpt":"처음 방문 케어를 이용할 때 당황하지 않도록, 예약 전 확인할 점과 당일 준비를 순서대로 정리했습니다.",
    "body":["방문 케어를 처음 이용하면 무엇을 준비해야 할지 막막할 수 있습니다. 가장 먼저 확인할 것은 가능 지역과 시간으로, 인계동처럼 오피스와 주거가 섞인 지역은 시간대에 따라 예약 가능 여부가 달라질 수 있어 전화로 먼저 확인하는 편이 좋습니다.",
      "당일에는 샤워 후 편한 복장으로 기다리고, 케어를 받을 공간을 가볍게 정리해 두면 한결 편안합니다. 선호하는 강도나 집중해서 풀고 싶은 부위가 있다면 시작 전에 미리 이야기하는 것이 좋습니다.",
      "이 글은 예약 절차와 준비를 안내하는 정보성 글입니다. 구체적인 가능 시간과 금액은 전화예약 시 확인해 주세요."]}},
 {"ko":"구운동","slug":"guun-dong","region":"수원권",
  "landmark":"오래된 주택가와 아파트가 어우러진 수원 서부의 정주형 주거지입니다.",
  "reasons":["평일에는 바빠 주말에 몰아서 쉬는 분","집에서 가족과 함께 휴식을 정리하고 싶은 분","외출 대신 집에서 컨디션을 챙기고 싶은 분"],
  "article":{"title":"구운동 거주자를 위한 주말 휴식과 방문 케어 준비법","cat":"family-care",
    "excerpt":"평일에 쌓인 피로를 주말에 효율적으로 정리하기 위한 환경 준비와 휴식 순서를 정리했습니다.",
    "body":["구운동처럼 정주형 주거지에 사는 분들은 평일에 바쁘게 일하고 주말에 휴식을 몰아 정리하는 경우가 많습니다. 짧은 주말을 알차게 보내려면 토요일 오전에 충분히 자고, 오후에는 가벼운 활동으로 몸을 깨우는 식의 완급 조절이 도움이 됩니다.",
      "집에서 방문 케어를 받을 계획이라면 미리 공간을 정리하고 조명을 낮춰 두면 더 편안합니다. 따뜻한 차 한 잔과 조용한 음악만 준비해도 휴식의 질이 달라집니다.",
      "주말 휴식의 목표는 무리한 일정이 아니라 다음 주를 가볍게 시작할 수 있는 컨디션을 만드는 것입니다."]}},
 # ---- 동탄·오산권 ----
 {"ko":"동탄","slug":"dongtan","region":"동탄·오산권",
  "landmark":"신도시 아파트 단지가 넓게 조성된 가족 중심 주거 생활권입니다.",
  "reasons":["아이를 돌보느라 외출이 어려운 가정","주말에 가족이 함께 휴식을 정리하고 싶은 분","신축 아파트에서 편안한 환경을 갖춘 분"],
  "article":{"title":"동탄 신도시 가족을 위한 주말 방문 웰니스 안내","cat":"family-care",
    "excerpt":"육아와 살림으로 외출이 어려운 가족이, 집이라는 공간을 활용해 주말 휴식을 정리하는 방법을 담았습니다.",
    "body":["동탄은 어린 자녀를 둔 가족이 많아 주말에도 외출이 쉽지 않은 경우가 많습니다. 아이 일정에 맞추다 보면 정작 부모의 휴식은 뒤로 밀리기 쉽습니다.",
      "이럴 때는 집이라는 익숙한 공간을 휴식의 무대로 활용할 수 있습니다. 아이가 낮잠을 자거나 가족이 함께 쉬는 시간에 맞춰 방문 케어를 예약하면, 외출 준비 없이 컨디션을 정리할 수 있습니다.",
      "신축 아파트는 비교적 케어 환경을 갖추기 쉬운 편입니다. 예약 전 가능 시간과 지역을 전화로 확인해 두면 주말 일정을 한결 여유 있게 잡을 수 있습니다."]}},
 {"ko":"오산","slug":"osan","region":"동탄·오산권",
  "landmark":"산업단지와 주거지가 가까워 통근 직장인이 많은 생활권입니다.",
  "reasons":["교대·장시간 근무로 피로가 누적되는 직장인","퇴근 후 회복 루틴이 필요한 분","집에서 빠르게 휴식을 정리하고 싶은 분"],
  "article":{"title":"오산 직장인을 위한 퇴근 후 피로 관리 루틴","cat":"office-fatigue",
    "excerpt":"장시간·교대 근무가 많은 환경에서, 매일 반복할 수 있는 짧은 회복 루틴을 정리했습니다.",
    "body":["오산은 산업단지가 가까워 장시간 근무나 교대 근무를 하는 분이 많습니다. 근무 패턴이 불규칙하면 피로가 쌓이는 속도도 빨라, 회복 역시 규칙적으로 챙기는 것이 중요합니다.",
      "퇴근 후에는 가장 먼저 다리와 허리의 긴장을 풀어 주는 것이 좋습니다. 따뜻한 물로 하체를 데우고, 발끝부터 천천히 눌러 주면 종일 서거나 앉아 있던 부담이 줄어듭니다.",
      "피로가 며칠째 풀리지 않을 때는 집에서 받는 방문 케어로 한 번 정리해 주는 것도 방법입니다. 매일의 짧은 루틴과 가끔의 집중 휴식을 함께 가져가는 것이 핵심입니다."]}},
 {"ko":"궐동","slug":"gwol-dong","region":"동탄·오산권",
  "landmark":"오산 도심과 가까운 원룸·소형 주거가 많은 1인 가구 생활권입니다.",
  "reasons":["혼자 살아 휴식 환경을 직접 챙기는 1인 가구","처음 방문 케어를 이용해 절차가 궁금한 분","예약 전 확인사항을 미리 알고 싶은 분"],
  "article":{"title":"궐동 1인 가구를 위한 출장마사지 이용 전 확인사항","cat":"usage-guide",
    "excerpt":"혼자 사는 공간에서 방문 케어를 안심하고 이용하기 위해 미리 확인하면 좋은 점들을 정리했습니다.",
    "body":["궐동처럼 원룸·소형 주거가 많은 지역에서는 1인 가구가 방문 케어를 이용하는 경우가 늘고 있습니다. 혼자 사는 공간일수록 예약 전에 몇 가지를 미리 확인해 두면 더 편안하게 이용할 수 있습니다.",
      "먼저 가능 지역과 시간을 전화로 확인하고, 케어를 받을 공간을 가볍게 정리해 두는 것이 좋습니다. 선호하는 강도나 집중하고 싶은 부위는 시작 전에 미리 이야기하면 됩니다.",
      "이 글은 건전한 휴식 케어를 전제로 한 이용 안내입니다. 구체적인 가능 시간과 금액은 전화예약 시 확인해 주세요."]}},
 # ---- 용인권 ----
 {"ko":"용인","slug":"yongin","region":"용인권",
  "landmark":"처인·기흥·수지를 아우르는 넓은 생활권을 가진 지역입니다.",
  "reasons":["평일에는 시간을 내기 어려운 직장인","주말에 집에서 휴식을 정리하고 싶은 분","외출 대신 집에서 컨디션을 챙기고 싶은 분"],
  "article":{"title":"용인 거주자를 위한 주말 방문 마사지 준비 가이드","cat":"usage-guide",
    "excerpt":"생활권이 넓은 용인에서 주말 방문 케어를 효율적으로 준비하는 순서를 정리했습니다.",
    "body":["용인은 처인·기흥·수지에 걸쳐 생활권이 넓어, 같은 용인이라도 지역마다 이동 여건이 다릅니다. 주말에 방문 케어를 계획한다면 가능 지역과 시간을 먼저 전화로 확인하는 것이 가장 확실합니다.",
      "예약이 정해지면 케어를 받을 공간을 정리하고, 편한 복장과 조용한 환경을 준비해 두면 한결 편안합니다. 주말 오전은 비교적 여유로운 시간대라 휴식을 길게 이어 가기 좋습니다.",
      "이 글은 예약 준비를 돕는 정보성 안내입니다. 구체적인 가능 시간과 금액은 전화예약 시 확인해 주세요."]}},
 {"ko":"처인구","slug":"cheoin","region":"용인권",
  "landmark":"용인에서 면적이 가장 넓어 지역별 이동 여건 차이가 큰 생활권입니다.",
  "reasons":["외곽 거주로 이동 가능 여부가 궁금한 분","예약 전 가능 지역을 확실히 확인하고 싶은 분","집에서 휴식을 정리하고 싶은 분"],
  "article":{"title":"처인구 넓은 생활권에서 예약 전 확인해야 할 점","cat":"usage-guide",
    "excerpt":"면적이 넓은 처인구에서 방문 케어를 계획할 때, 가능 지역·시간을 미리 확인하는 방법을 정리했습니다.",
    "body":["처인구는 용인에서 면적이 가장 넓어, 같은 구 안에서도 위치에 따라 이동 여건이 크게 다릅니다. 그래서 방문 케어를 계획할 때는 정확한 주소 기준으로 가능 여부를 먼저 확인하는 것이 중요합니다.",
      "전화로 예약할 때 거주 위치와 희망 시간을 함께 전하면, 이동 가능 여부와 가능한 시간대를 더 빠르게 안내받을 수 있습니다. 외곽 지역일수록 미리 확인해 두는 편이 일정 변동을 줄여 줍니다.",
      "이 글은 예약 전 확인을 돕는 정보성 안내입니다. 운영지역과 가능 시간은 전화예약 시 확인해 주세요."]}},
 {"ko":"수지","slug":"suji","region":"용인권",
  "landmark":"수지·죽전을 중심으로 한 가족 단위 아파트 주거 생활권입니다.",
  "reasons":["주말에 가족과 함께 휴식을 정리하고 싶은 가정","평일 피로를 주말에 몰아 푸는 분","집에서 편안한 환경을 갖춘 분"],
  "article":{"title":"수지·죽전 가족을 위한 주말 홈케어 이용 안내","cat":"family-care",
    "excerpt":"가족 단위 거주가 많은 수지·죽전에서, 집을 휴식 공간으로 활용하는 주말 홈케어 준비법을 담았습니다.",
    "body":["수지·죽전은 가족 단위 아파트 거주가 많은 지역으로, 주말에도 집에서 보내는 시간이 깁니다. 외출 대신 집을 휴식의 공간으로 활용하면 가족 모두의 컨디션을 함께 챙기기 좋습니다.",
      "주말 홈케어를 준비할 때는 가족 일정이 겹치지 않는 시간대를 고르고, 케어를 받을 공간을 미리 정리해 두면 편안합니다. 조명을 낮추고 조용한 환경을 만드는 것만으로도 휴식의 질이 올라갑니다.",
      "이 글은 가족 단위 휴식 환경을 돕는 정보성 안내입니다. 가능 지역과 시간은 전화예약 시 확인해 주세요."]}},
 {"ko":"포곡","slug":"pogok","region":"용인권",
  "landmark":"전원형 주거와 관광지가 어우러진 용인 동부 생활권입니다.",
  "reasons":["외곽 거주로 이동 가능 여부가 궁금한 분","예약 전 체크리스트를 확인하고 싶은 분","집에서 조용히 휴식을 정리하고 싶은 분"],
  "article":{"title":"포곡 거주자를 위한 방문 마사지 예약 전 체크리스트","cat":"usage-guide",
    "excerpt":"전원형 주거가 많은 포곡에서 방문 케어를 계획할 때 미리 점검하면 좋은 항목을 정리했습니다.",
    "body":["포곡은 전원형 주거가 많아 같은 지역 안에서도 위치에 따라 이동 여건이 다릅니다. 방문 케어를 계획한다면 정확한 위치 기준으로 가능 여부를 먼저 확인하는 것이 좋습니다.",
      "예약 전에는 희망 시간과 거주 위치를 함께 전하고, 케어를 받을 공간을 정리해 두면 당일이 한결 수월합니다. 조용한 환경에서 받는 휴식은 전원형 주거의 장점을 잘 살릴 수 있습니다.",
      "이 글은 예약 준비를 돕는 정보성 안내입니다. 가능 지역과 시간은 전화예약 시 확인해 주세요."]}},
 {"ko":"신갈","slug":"singal","region":"용인권",
  "landmark":"교통 요지에 자리해 통근 직장인이 많은 생활권입니다.",
  "reasons":["출퇴근 이동이 많아 피로가 쌓이는 직장인","퇴근 후 회복 루틴이 필요한 분","집에서 빠르게 휴식을 정리하고 싶은 분"],
  "article":{"title":"신갈 직장인을 위한 퇴근 후 피로 관리 가이드","cat":"office-fatigue",
    "excerpt":"교통 요지라 이동이 잦은 신갈 직장인을 위해, 퇴근 후 반복할 수 있는 회복 순서를 정리했습니다.",
    "body":["신갈은 교통 요지에 자리해 출퇴근 이동이 잦은 직장인이 많습니다. 이동이 많을수록 어깨와 허리, 다리에 긴장이 쌓이기 쉬워 퇴근 후 회복이 중요합니다.",
      "집에 도착하면 먼저 다리와 허리를 가볍게 풀어 주고, 따뜻한 물로 긴장을 데워 주면 좋습니다. 자기 전 짧은 스트레칭을 같은 시간에 반복하면 피로가 덜 쌓입니다.",
      "피로가 며칠째 이어진다면 집에서 받는 방문 케어로 한 번 정리해 주는 것도 방법입니다. 다만 통증이 지속된다면 의료기관 상담을 먼저 받는 것이 우선입니다."]}},
 {"ko":"기흥","slug":"giheung","region":"용인권",
  "landmark":"대형 사업장과 오피스가 많은 용인 서부의 업무·주거 생활권입니다.",
  "reasons":["장시간 앉아 일하는 사무직","어깨·허리 결림이 잦은 분","퇴근 후 바로 휴식하고 싶은 기흥 거주자"],
  "article":{"title":"기흥 오피스 근무자를 위한 어깨·허리 피로 관리법","cat":"office-fatigue",
    "excerpt":"오래 앉아 일하는 환경에서 굳기 쉬운 어깨와 허리를 단계적으로 풀어 주는 방법을 정리했습니다.",
    "body":["기흥은 대형 사업장과 오피스가 많아 장시간 앉아 일하는 사무직이 많습니다. 같은 자세가 오래 이어지면 어깨가 말리고 허리 아래쪽이 묵직해지기 쉽습니다.",
      "근무 중에는 한두 시간마다 일어나 가볍게 움직이고, 의자 깊숙이 앉아 허리를 받쳐 주는 것이 도움이 됩니다. 퇴근 후에는 굳은 허리와 어깨를 따뜻하게 데워 주면 긴장이 풀립니다.",
      "결림이 자주 반복된다면 집에서 받는 방문 케어로 굳은 부위를 정리하는 것도 방법입니다. 통증이 심하거나 지속되면 의료기관 상담을 먼저 받는 것이 우선입니다."]}},
 {"ko":"동백","slug":"dongbaek","region":"용인권",
  "landmark":"계획적으로 조성된 아파트 신도시형 주거 생활권입니다.",
  "reasons":["집에서 가족과 휴식을 정리하고 싶은 가정","주말 컨디션 관리가 필요한 분","조용한 주거 환경을 갖춘 분"],
  "article":{"title":"동백 신도시 거주자를 위한 방문 웰니스 케어 안내","cat":"family-care",
    "excerpt":"잘 조성된 주거 환경을 가진 동백에서, 집을 활용해 주말 컨디션을 정리하는 방법을 담았습니다.",
    "body":["동백은 계획적으로 조성된 신도시형 주거지로, 조용하고 정돈된 환경이 장점입니다. 이런 환경은 집에서 휴식을 정리하기에 잘 맞습니다.",
      "주말에 방문 케어를 계획한다면 가족 일정이 겹치지 않는 시간대를 고르고, 케어를 받을 공간을 미리 정리해 두면 편안합니다. 조명을 낮추고 조용한 분위기를 만들면 휴식의 질이 올라갑니다.",
      "이 글은 집을 활용한 휴식 환경을 돕는 정보성 안내입니다. 가능 지역과 시간은 전화예약 시 확인해 주세요."]}},
 # ---- 분당권 ----
 {"ko":"분당","slug":"bundang","region":"분당권",
  "landmark":"판교·정자·서현을 잇는 직주근접 업무·주거 생활권입니다.",
  "reasons":["야근이 잦은 IT·사무직 직장인","퇴근 후 컨디션 관리가 필요한 분","집에서 바로 휴식을 정리하고 싶은 분"],
  "article":{"title":"분당 직장인을 위한 퇴근 후 컨디션 관리 가이드","cat":"office-fatigue",
    "excerpt":"업무 강도가 높은 분당 직장인을 위해, 퇴근 후 컨디션을 회복하는 현실적인 순서를 정리했습니다.",
    "body":["분당은 판교 IT 업무지구와 가까워 업무 강도가 높고 야근이 잦은 직장인이 많습니다. 집중 업무가 이어지면 어깨·목의 긴장과 눈의 피로가 함께 쌓이기 쉽습니다.",
      "퇴근 후에는 화면에서 잠시 멀어져 눈과 목을 쉬게 하고, 따뜻한 물로 어깨 위쪽을 데워 주면 긴장이 풀립니다. 자기 전 호흡을 길게 가져가는 것만으로도 수면의 질이 좋아집니다.",
      "피로가 누적된 주에는 집에서 받는 방문 케어로 한 번 정리해 주는 것도 방법입니다. 이동 없이 휴식으로 바로 이어진다는 점이 바쁜 직장인에게는 큰 차이를 만듭니다."]}},
 {"ko":"미금역","slug":"migeum-station","region":"분당권",
  "landmark":"신분당선·분당선 환승으로 통근 인구가 집중되는 역세권입니다.",
  "reasons":["환승 통근으로 이동이 긴 직장인","야근 후 늦게 귀가하는 분","집에서 빠르게 휴식을 정리하고 싶은 분"],
  "article":{"title":"미금역 인근 직장인을 위한 야근 후 피로 관리법","cat":"office-fatigue",
    "excerpt":"환승 통근이 긴 미금역 생활권에서, 야근 후 누적 피로를 정리하는 방법을 담았습니다.",
    "body":["미금역은 환승 인구가 많아 통근 시간이 긴 직장인이 많습니다. 긴 이동과 야근이 겹치면 다리와 허리에 피로가 빠르게 쌓입니다.",
      "귀가 후에는 종아리와 발을 가볍게 풀어 주고, 따뜻한 물로 하체를 데워 주면 긴장이 줄어듭니다. 늦은 시간일수록 강한 빛과 카페인을 피하는 것이 수면에 도움이 됩니다.",
      "야근이 이어진 주에는 집에서 받는 방문 케어로 누적된 피로를 정리해 주는 것도 방법입니다. 가능 시간은 전화예약 시 확인해 주세요."]}},
 {"ko":"수내역","slug":"sunae-station","region":"분당권",
  "landmark":"오피스와 상권이 밀집한 분당 중심 업무 역세권입니다.",
  "reasons":["오피스 근무로 앉아 있는 시간이 긴 분","점심·퇴근 후 짧은 휴식을 찾는 직장인","집에서 컨디션을 정리하고 싶은 분"],
  "article":{"title":"수내역 오피스 근무자를 위한 방문 마사지 이용 팁","cat":"usage-guide",
    "excerpt":"오피스가 밀집한 수내역 생활권에서 방문 케어를 효율적으로 이용하는 작은 팁들을 정리했습니다.",
    "body":["수내역은 오피스와 상권이 밀집해 앉아 일하는 시간이 긴 직장인이 많습니다. 바쁜 일정 속에서 방문 케어를 이용한다면 몇 가지 팁이 도움이 됩니다.",
      "먼저 원하는 시간대를 여유 있게 잡고, 가능 시간과 지역을 전화로 미리 확인해 두면 일정이 꼬이지 않습니다. 집중해서 풀고 싶은 부위가 있다면 시작 전에 미리 이야기하면 됩니다.",
      "이 글은 이용을 돕는 정보성 안내입니다. 구체적인 가능 시간과 금액은 전화예약 시 확인해 주세요."]}},
 {"ko":"정자역","slug":"jeongja-station","region":"분당권",
  "landmark":"카페거리와 업무지구가 어우러진 분당의 대표 직주근접 역세권입니다.",
  "reasons":["야근 후 회복 루틴이 필요한 직장인","퇴근 후 바로 쉬고 싶은 분","집에서 컨디션을 정리하고 싶은 정자역 거주자"],
  "article":{"title":"정자역 직장인을 위한 퇴근 후 회복 루틴","cat":"office-fatigue",
    "excerpt":"직주근접으로 일과 휴식이 가까운 정자역 생활권에서, 퇴근 후 반복할 수 있는 회복 루틴을 정리했습니다.",
    "body":["정자역은 업무지구와 주거가 가까운 직주근접 지역이라, 일과 휴식의 전환을 잘 만드는 것이 중요합니다. 퇴근 후에도 일 생각이 이어지면 몸은 쉬어도 긴장이 풀리지 않습니다.",
      "집에 도착하면 업무 알림을 잠시 멀리하고, 따뜻한 물로 어깨와 목을 데우며 하루를 정리하는 신호를 주는 것이 좋습니다. 같은 시간에 반복하는 짧은 루틴이 회복의 질을 높입니다.",
      "피로가 쌓인 날에는 집에서 받는 방문 케어로 긴장을 정리해 주는 것도 방법입니다. 가능 시간은 전화예약 시 확인해 주세요."]}},
 {"ko":"서현역","slug":"seohyeon-station","region":"분당권",
  "landmark":"백화점·상권이 모인 분당 동부의 생활·업무 중심 역세권입니다.",
  "reasons":["주중 바빠 주말에 휴식을 정리하는 직장인","가족과 함께 컨디션을 챙기고 싶은 분","집에서 편안한 환경을 갖춘 분"],
  "article":{"title":"서현역 생활권 직장인을 위한 주말 피로 관리 안내","cat":"office-fatigue",
    "excerpt":"평일 업무 강도가 높은 서현역 생활권에서, 주말을 활용해 피로를 정리하는 방법을 담았습니다.",
    "body":["서현역 일대는 상권과 업무지구가 가까워 평일 일정이 빡빡한 직장인이 많습니다. 주중에 충분히 쉬기 어려운 만큼, 주말을 회복의 시간으로 잘 쓰는 것이 중요합니다.",
      "주말에는 늦잠으로 수면 리듬을 무너뜨리기보다, 평소보다 조금 더 자고 낮에는 가벼운 활동으로 몸을 깨우는 편이 좋습니다. 오후에는 집에서 조용한 휴식을 이어 가면 다음 주가 가벼워집니다.",
      "주말 휴식의 목표는 무리한 일정이 아니라 다음 주를 가볍게 시작할 컨디션을 만드는 것입니다. 가능 시간은 전화예약 시 확인해 주세요."]}},
]

# Extra non-area magazine pieces to round out categories
EXTRA_POSTS = [
 {"title":"출장마사지 전화예약 절차와 준비물 한눈에 보기","slug":"reservation-flow","cat":"usage-guide",
  "excerpt":"처음 방문 케어를 이용할 때 헷갈리기 쉬운 전화예약 절차와 당일 준비물을 순서대로 정리했습니다.",
  "body":["방문 케어는 대부분 전화예약으로 진행됩니다. 통화에서는 거주 지역과 희망 시간, 원하는 프로그램과 이용 시간을 함께 전하면 안내가 빠릅니다.",
    "당일에는 샤워 후 편한 복장으로 기다리고, 케어를 받을 공간을 가볍게 정리해 두면 편안합니다. 선호하는 강도나 집중하고 싶은 부위가 있다면 시작 전에 미리 이야기하면 됩니다.",
    "운영지역은 수원·동탄·오산·용인·분당 일부 권역으로 한정되며, 가능 시간과 금액은 전화예약 시 확인해 주세요."]},
 {"title":"방문 케어를 건전하게 이용하기 위한 예약 전 확인사항","slug":"safe-use","cat":"safety-guide",
  "excerpt":"안심하고 휴식 케어를 이용하기 위해 알아 두면 좋은 원칙과 예약 전 확인사항을 정리했습니다.",
  "body":["쓰리 마사지는 휴식과 컨디션 관리를 위한 건전한 방문 케어를 안내합니다. 의료행위나 치료 목적의 서비스가 아니며, 불건전한 목적의 문의는 받지 않습니다.",
    "예약 전에는 가능 지역과 시간, 프로그램과 금액을 전화로 확인하고, 케어를 받을 공간과 편한 복장을 준비해 두면 좋습니다. 개인정보는 예약과 안내 목적에 한해 사용됩니다.",
    "통증이 심하거나 지속되는 경우, 또는 건강상 주의가 필요한 경우에는 먼저 의료기관 상담을 받는 것을 권장합니다."]},
 {"title":"신도시 아파트에서 방문 케어를 받기 전 공간 준비법","slug":"home-setup","cat":"family-care",
  "excerpt":"수원·동탄·용인·분당의 아파트 거주 환경에서 방문 케어를 편안하게 받기 위한 공간 준비를 담았습니다.",
  "body":["아파트 거주 환경에서는 약간의 준비만으로 휴식의 질을 크게 높일 수 있습니다. 케어를 받을 공간을 미리 정리하고, 조명을 낮춰 차분한 분위기를 만드는 것이 좋습니다.",
    "가족이 함께 사는 집이라면 서로의 일정이 겹치지 않는 시간대를 고르면 더 편안합니다. 따뜻한 차 한 잔과 조용한 음악만 준비해도 분위기가 달라집니다.",
    "이 글은 휴식 환경을 돕는 정보성 안내입니다. 가능 지역과 시간은 전화예약 시 확인해 주세요."]},
]


# ---------------------------------------------------------------------------
# HTML scaffold
# ---------------------------------------------------------------------------
def page(path, title, description, body, jsonld=None):
    """path is like 'areas/suwon.html' (relative to repo root)."""
    canonical = BASE + "/" + path.replace("index.html", "")
    jl = ""
    for block in (jsonld or []):
        jl += '\n  <script type="application/ld+json">' + block + "</script>"
    doc = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:locale" content="ko_KR">
  <meta name="theme-color" content="#0c1016">
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
  <link rel="stylesheet" href="/assets/css/styles.css">{jl}
</head>
<body>
  <div id="site-header"></div>
{body}
  <div id="site-footer"></div>
  <script src="/assets/js/site.js"></script>
</body>
</html>
"""
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(doc)


def breadcrumb_ld(items):
    el = []
    for i, (name, url) in enumerate(items, 1):
        el.append('{"@type":"ListItem","position":%d,"name":"%s","item":"%s"}'
                   % (i, name, BASE + url))
    return '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[' + ",".join(el) + "]}"


def crumb_html(items):
    parts = []
    for i, (name, url) in enumerate(items):
        if i < len(items) - 1:
            parts.append(f'<a href="{url}">{html.escape(name)}</a><span class="sep">›</span>')
        else:
            parts.append(f'<span aria-current="page">{html.escape(name)}</span>')
    return '<nav class="breadcrumb" aria-label="현재 위치">' + "".join(parts) + "</nav>"


# ---------------------------------------------------------------------------
# Area page (conversion-focused)
# ---------------------------------------------------------------------------
def area_links_for_region(region):
    out = []
    for a in AREAS:
        if a["region"] == region:
            out.append(f'<a href="/areas/{a["slug"]}.html">{a["ko"]}</a>')
    return "".join(out)


def render_area(a):
    url = f"/areas/{a['slug']}.html"
    reasons = "".join(f"<li>{html.escape(r)}</li>" for r in a["reasons"])
    # representative programs (3)
    cards = ""
    for p in PROGRAMS[:3]:
        rows = "".join(
            f'<div class="price-row"><span class="dur">{d}</span><span class="amt"><b>{won(v)}</b></span></div>'
            for d, v in p["prices"])
        cards += f"""
        <div class="price-card{' is-best' if p['best'] else ''}">
          {'<span class="price-badge">BEST</span>' if p['best'] else ''}
          <span class="price-cat">{html.escape(p['cat'])}</span>
          <h3>{html.escape(p['name'])}</h3>
          <p class="desc">{html.escape(p['desc'])}</p>
          <div class="price-rows">{rows}</div>
        </div>"""
    checklist = "".join(f"<li>{html.escape(c)}</li>" for c in CHECKLIST)
    art = a["article"]
    crumbs = [("홈", "/"), ("지역안내", "/areas/"), (f"{a['ko']} 출장마사지", url)]
    body = f"""  <main>
    <section class="page-head"><div class="container">
      {crumb_html(crumbs)}
      <span class="eyebrow">{html.escape(a['region'])} · 운영지역</span>
      <h1>{html.escape(a['ko'])} 출장마사지 예약 안내</h1>
      <p>{html.escape(a['ko'])}{eun_neun(a['ko'])} {html.escape(a['landmark'])} 쓰리 마사지는 이 지역을 운영권역으로 두고,
         집에서 받는 방문 마사지 예약을 안내합니다. 정확한 가능 지역과 시간은 전화로 확인해 주세요.</p>
      <div class="hero-actions">
        <a class="btn btn--gold btn--lg" href="{PHONE_TEL}">전화예약 {PHONE_DISPLAY}</a>
        <a class="btn btn--ghost btn--lg" href="/service/price.html">가격표 전체보기</a>
      </div>
    </div></section>

    <section class="section"><div class="container">
      <div class="grid grid-2" style="align-items:start">
        <div class="prose">
          <h2>{html.escape(a['ko'])}에서 이런 분께 권합니다</h2>
          <ul>{reasons}</ul>
          <p class="muted">이용 가능 시간과 이동 여부는 당일 상황에 따라 달라질 수 있어, 예약 전 전화로 확인하시는 것이 가장 정확합니다.</p>
        </div>
        <div class="notice">
          <h3>예약 전 확인사항</h3>
          <ul>{checklist}</ul>
        </div>
      </div>
    </div></section>

    <section class="section--tight"><div class="container">
      <div class="section-head"><h2>{html.escape(a['ko'])} 인기 프로그램</h2>
        <p>대표 프로그램 3종입니다. 전체 프로그램과 시간별 금액은 가격표에서 확인하세요.</p></div>
      <div class="price-grid">{cards}</div>
      <div style="margin-top:24px"><a class="btn btn--ghost" href="/service/price.html">가격표 전체보기 →</a></div>
    </div></section>

    <section class="section--tight"><div class="container">
      <div class="cta-band">
        <h2>{html.escape(a['ko'])} 방문 예약 문의</h2>
        <p>가능 지역·시간 확인 후 예약을 도와드립니다. 건전한 휴식 케어만 안내합니다.</p>
        <a class="phone" href="{PHONE_TEL}">{PHONE_DISPLAY}</a>
        <div style="margin-top:18px"><a class="btn btn--gold btn--lg" href="{PHONE_TEL}">바로 전화하기</a></div>
      </div>
    </div></section>

    <section class="section--tight"><div class="container">
      <div class="section-head"><h2>{html.escape(a['ko'])} 생활 정보 읽기</h2>
        <p>예약 정보 외에, {html.escape(a['ko'])} 생활권에 맞춘 피로 관리 이야기도 함께 확인해 보세요.</p></div>
      <div class="grid grid-2">
        <a class="card post-card" href="/magazine/{a['slug']}.html">
          <span class="post-cat">{html.escape(CATS[art['cat']])}</span>
          <h3>{html.escape(art['title'])}</h3>
          <p>{html.escape(art['excerpt'])}</p>
          <span class="card-link">매거진에서 읽기</span>
        </a>
        <div class="region-block card">
          <h3>{html.escape(a['region'])} 다른 지역</h3>
          <p class="region-sub">같은 권역의 운영지역도 함께 확인하세요.</p>
          <div class="area-links">{area_links_for_region(a['region'])}</div>
        </div>
      </div>
    </div></section>
  </main>
"""
    service_ld = ('{"@context":"https://schema.org","@type":"Service","serviceType":"방문 마사지 예약 안내",'
                  '"name":"%s 출장마사지","provider":{"@type":"Organization","name":"쓰리 마사지","telephone":"%s"},'
                  '"areaServed":{"@type":"Place","name":"%s"},"url":"%s"}'
                  % (a['ko'], PHONE_DISPLAY, a['ko'], BASE + url))
    desc = f"{a['ko']} 출장마사지 예약 안내. {a['region']} 운영지역으로 집에서 받는 방문 마사지 프로그램과 가격, 예약 전 확인사항을 안내합니다. 전화예약 {PHONE_DISPLAY}."
    page(f"areas/{a['slug']}.html", f"{a['ko']} 출장마사지 예약 안내 | 쓰리 마사지", desc, body,
         jsonld=[breadcrumb_ld(crumbs), service_ld])


# ---------------------------------------------------------------------------
# Magazine article (info-focused)
# ---------------------------------------------------------------------------
def render_article(slug, title, cat, body_paras, related_area=None):
    url = f"/magazine/{slug}.html"
    paras = "".join(f"<p>{html.escape(p)}</p>" for p in body_paras)
    crumbs = [("홈", "/"), ("매거진", "/magazine/"), (title, url)]
    related = ""
    if related_area:
        related = f"""
      <div class="cta-band" style="text-align:left;margin-top:40px">
        <h2 style="font-size:1.2rem">{html.escape(related_area['ko'])} 방문 예약이 필요하다면</h2>
        <p>이 글은 생활 정보 안내입니다. 실제 예약과 가능 시간은 {html.escape(related_area['ko'])} 지역 페이지에서 확인하세요.</p>
        <div style="display:flex;gap:10px;flex-wrap:wrap">
          <a class="btn btn--gold" href="/areas/{related_area['slug']}.html">{html.escape(related_area['ko'])} 출장마사지 안내</a>
          <a class="btn btn--ghost" href="{PHONE_TEL}">전화예약 {PHONE_DISPLAY}</a>
        </div>
      </div>"""
    body = f"""  <main>
    <section class="page-head"><div class="container">
      {crumb_html(crumbs)}
      <span class="eyebrow">{html.escape(CATS[cat])}</span>
      <h1>{html.escape(title)}</h1>
    </div></section>
    <section class="section"><div class="container">
      <article class="prose">
        {paras}
        <p class="muted">본 콘텐츠는 휴식과 컨디션 관리를 돕기 위한 일반적인 생활 정보이며, 의료적 진단·치료를 대체하지 않습니다.
        통증이 지속되면 의료기관 상담을 권장합니다.</p>
      </article>
      {related}
    </div></section>
  </main>
"""
    desc = (body_paras[0][:110]).strip()
    ld = ('{"@context":"https://schema.org","@type":"Article","headline":"%s",'
          '"articleSection":"%s","inLanguage":"ko-KR",'
          '"publisher":{"@type":"Organization","name":"쓰리 마사지"},"url":"%s"}'
          % (title.replace('"', ''), CATS[cat], BASE + url))
    page(f"magazine/{slug}.html", f"{title} | 쓰리 마사지 매거진", desc, body,
         jsonld=[breadcrumb_ld(crumbs), ld])


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build():
    for a in AREAS:
        render_area(a)
        art = a["article"]
        render_article(a["slug"], art["title"], art["cat"], art["body"], related_area=a)
    for p in EXTRA_POSTS:
        render_article(p["slug"], p["title"], p["cat"], p["body"])
    print(f"Generated {len(AREAS)} area pages, {len(AREAS)+len(EXTRA_POSTS)} magazine articles.")

    # Emit posts manifest for the magazine index (static + JS filter)
    posts = []
    for a in AREAS:
        art = a["article"]
        posts.append({"slug": a["slug"], "title": art["title"], "cat": art["cat"], "excerpt": art["excerpt"]})
    for p in EXTRA_POSTS:
        posts.append({"slug": p["slug"], "title": p["title"], "cat": p["cat"], "excerpt": p["excerpt"]})
    import json
    with open(os.path.join(ROOT, "assets/js/posts.js"), "w", encoding="utf-8") as f:
        f.write("window.POSTS = " + json.dumps(posts, ensure_ascii=False, indent=2) + ";\n")
    print(f"Wrote posts manifest with {len(posts)} entries.")

    write_sitemap()


def write_sitemap():
    """Enumerate every .html page (minus noindex) into sitemap.xml + robots.txt."""
    urls = ["/"]
    static = [
        "service/massage.html", "service/program.html", "service/price.html",
        "service/process.html", "service/checklist.html",
        "areas/", "magazine/",
        "faq/reservation.html", "faq/area.html", "faq/before-use.html",
        "about/", "about/contact.html",
    ]
    urls += ["/" + s for s in static]
    for a in AREAS:
        urls.append(f"/areas/{a['slug']}.html")
    for a in AREAS:
        urls.append(f"/magazine/{a['slug']}.html")
    for p in EXTRA_POSTS:
        urls.append(f"/magazine/{p['slug']}.html")

    items = "\n".join(f"  <url><loc>{BASE}{u}</loc></url>" for u in urls)
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               f"{items}\n</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    robots = ("User-agent: *\nAllow: /\n"
              "Disallow: /about/business.html\n\n"
              f"Sitemap: {BASE}/sitemap.xml\n")
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)
    print(f"Wrote sitemap.xml ({len(urls)} urls) and robots.txt.")


if __name__ == "__main__":
    build()
