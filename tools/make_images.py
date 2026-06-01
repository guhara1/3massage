#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
브랜드 래스터 이미지 생성기.
원본 로고(assets/img/source-logo.png 또는 인자로 받은 파일)에서
  - assets/img/logo-512.png   : schema.org logo 용 (512px, 여백 트림)
  - assets/img/og-default.png : 1200x630 소셜 공유 이미지
를 만든다.

필요: Pillow, 한글 폰트(나눔고딕). 실행:
  python3 tools/make_images.py [원본로고.png]
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets/img")
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(IMG, "source-logo.png")

FONT_DIR = "/usr/share/fonts/truetype/nanum"
F  = os.path.join(FONT_DIR, "NanumGothic.ttf")
FB = os.path.join(FONT_DIR, "NanumGothicBold.ttf")
EB = os.path.join(FONT_DIR, "NanumGothicExtraBold.ttf")
EBf = EB if os.path.exists(EB) else FB

GOLD=(201,168,106); GOLDS=(227,201,143); TEXT=(238,242,247); SUB=(184,194,208)
BG=(12,16,22); BG2=(20,29,43)


def make_logo_512(src):
    im = Image.open(src).convert("RGBA")
    bbox = im.split()[3].getbbox()
    if bbox:
        im = im.crop(bbox)
    nw = 512
    nh = round(im.height * nw / im.width)
    im.resize((nw, nh), Image.LANCZOS).save(os.path.join(IMG, "logo-512.png"), optimize=True)
    return os.path.join(IMG, "logo-512.png")


def make_og(logo512):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), BG); px = img.load()
    for y in range(H):
        t = y / H
        row = (int(BG[0]+(BG2[0]-BG[0])*t), int(BG[1]+(BG2[1]-BG[1])*t), int(BG[2]+(BG2[2]-BG[2])*t))
        for x in range(W):
            px[x, y] = row
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([W-520, -260, W+160, 360], fill=(201, 168, 106, 46))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([28, 28, W-28, H-28], radius=26, outline=(36, 48, 67), width=2)
    f_eyebrow = ImageFont.truetype(FB, 25)
    f_h1 = ImageFont.truetype(EBf, 72)
    f_sub = ImageFont.truetype(F, 30)
    f_phone = ImageFont.truetype(FB, 40)
    logo = Image.open(logo512).convert("RGBA")
    lw = 330; lh = round(logo.height * lw / logo.width)
    logo = logo.resize((lw, lh), Image.LANCZOS)
    img.paste(logo, (84, 58), logo)
    d = ImageDraw.Draw(img, "RGBA")
    y = 58 + lh + 22
    d.text((88, y), "THREE MASSAGE · 출장마사지 예약 안내", font=f_eyebrow, fill=GOLD); y += 46
    d.text((84, y), "수원·동탄·오산·용인·분당", font=f_h1, fill=TEXT)
    d.text((84, y+86), "출장마사지 예약 안내", font=f_h1, fill=GOLDS)
    d.text((86, y+86+104), "전화예약 가능한 방문 마사지 · 가능지역과 시간은 전화로 확인", font=f_sub, fill=SUB)
    d.text((84, H-92), "전화예약  0508-202-4717", font=f_phone, fill=GOLDS)
    img.save(os.path.join(IMG, "og-default.png"), optimize=True)


if __name__ == "__main__":
    if not os.path.exists(SRC):
        sys.exit("원본 로고를 찾을 수 없습니다: %s (인자로 경로를 전달하세요)" % SRC)
    logo512 = make_logo_512(SRC)
    make_og(logo512)
    print("생성 완료: assets/img/logo-512.png, assets/img/og-default.png")
