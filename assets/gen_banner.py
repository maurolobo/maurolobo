#!/usr/bin/env python3
"""Gera o banner do perfil (versões clara e escura).

SVG dentro de README passa pelo proxy do GitHub, que serve o arquivo como
imagem: CSS embutido anima, JavaScript não roda. Por isso toda a vida do
banner é keyframe CSS — nada depende de script.
"""
import math
import random

W, H = 1280, 400
SPACING = 26

THEMES = {
    "light": dict(
        bg="#FAFBFF",
        ink="#0A0A0F",
        soft="#4A4A55",
        faint="#8A8A96",
        dot="rgba(12,12,29,0.16)",
        blob_a_op=0.22,
        blob_b_op=0.16,
    ),
    "dark": dict(
        bg="#08080D",
        ink="#F4F4F8",
        soft="#A8A8B4",
        faint="#6E6E7C",
        dot="rgba(255,255,255,0.13)",
        blob_a_op=0.34,
        blob_b_op=0.26,
    ),
}

ACCENT = "#1B4DFF"
VIOLET = "#7B5CFF"


def build(theme_name: str) -> str:
    t = THEMES[theme_name]
    rnd = random.Random(20260806)

    dots = []
    lit = []
    for y in range(SPACING, H, SPACING):
        for x in range(SPACING, W, SPACING):
            # a malha rareia onde o texto vive, para não competir com a leitura
            if x < 640 and 96 < y < 300:
                continue
            dots.append(f'<circle cx="{x}" cy="{y}" r="1.1"/>')
            if rnd.random() < 0.018:
                delay = round(rnd.random() * 6, 2)
                lit.append(
                    f'<circle class="lit" cx="{x}" cy="{y}" r="2.1" '
                    f'style="animation-delay:{delay}s"/>'
                )

    # pulsos que atravessam a linha da direita
    pulses = "".join(
        f'<circle class="pulse" cx="0" cy="{cy}" r="3" style="animation-delay:{d}s"/>'
        for cy, d in ((330, 0), (330, 2.6), (330, 5.2))
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Mauro Lobo — engenheiro de sistemas de IA aplicada">
  <defs>
    <radialGradient id="blobA" cx="50%" cy="50%">
      <stop offset="0%" stop-color="{ACCENT}" stop-opacity="{t['blob_a_op']}"/>
      <stop offset="70%" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="blobB" cx="50%" cy="50%">
      <stop offset="0%" stop-color="{VIOLET}" stop-opacity="{t['blob_b_op']}"/>
      <stop offset="70%" stop-color="{VIOLET}" stop-opacity="0"/>
    </radialGradient>
    <filter id="soften" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>
    <linearGradient id="rule" gradientUnits="userSpaceOnUse" x1="660" y1="330" x2="1208" y2="330">
      <stop offset="0%" stop-color="{ACCENT}" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="{ACCENT}" stop-opacity="0"/>
    </linearGradient>
    <style>
      .dots {{ fill: {t['dot']}; }}
      .lit {{ fill: {ACCENT}; }}
      .eyebrow {{ font: 600 13px 'Inter','Segoe UI',Helvetica,Arial,sans-serif; letter-spacing: 2.6px; fill: {t['faint']}; }}
      .title {{ font: 700 72px 'Inter','Segoe UI',Helvetica,Arial,sans-serif; letter-spacing: -2.4px; fill: {t['ink']}; }}
      .sub {{ font: 400 17px 'Inter','Segoe UI',Helvetica,Arial,sans-serif; fill: {t['soft']}; }}
      .meta {{ font: 500 12px 'Inter','Segoe UI',Helvetica,Arial,sans-serif; letter-spacing: 1.8px; fill: {t['faint']}; }}
      .accent {{ fill: {ACCENT}; }}

      @keyframes breathe {{ 0%,100% {{ transform: none; }} 50% {{ transform: translate(26px,-14px) scale(1.08); }} }}
      @keyframes breathe2 {{ 0%,100% {{ transform: none; }} 50% {{ transform: translate(-22px,12px) scale(1.06); }} }}
      @keyframes blink {{ 0%,100% {{ opacity: .25; }} 50% {{ opacity: 1; }} }}
      @keyframes run {{ from {{ transform: translateX(700px); opacity: 0; }} 12% {{ opacity: 1; }} 88% {{ opacity: 1; }} to {{ transform: translateX(1280px); opacity: 0; }} }}
      @keyframes draw {{ from {{ stroke-dashoffset: 620; }} to {{ stroke-dashoffset: 0; }} }}

      #ba {{ animation: breathe 34s ease-in-out infinite; transform-origin: 200px 120px; }}
      #bb {{ animation: breathe2 44s ease-in-out infinite; transform-origin: 1080px 300px; }}
      .lit {{ animation: blink 7s ease-in-out infinite; }}
      .pulse {{ fill: {ACCENT}; opacity: 0; animation: run 7.8s linear infinite; }}
      .rule {{ stroke-dasharray: 620; animation: draw 2.2s cubic-bezier(.16,1,.3,1) both; }}

      @media (prefers-reduced-motion: reduce) {{
        #ba, #bb, .lit, .pulse, .rule {{ animation: none; }}
        .pulse {{ opacity: 0; }}
      }}
    </style>
  </defs>

  <rect width="{W}" height="{H}" fill="{t['bg']}"/>
  <g filter="url(#soften)">
    <circle id="ba" cx="200" cy="120" r="260" fill="url(#blobA)"/>
    <circle id="bb" cx="1080" cy="300" r="240" fill="url(#blobB)"/>
  </g>

  <g class="dots">{''.join(dots)}</g>
  <g>{''.join(lit)}</g>

  <text class="eyebrow" x="72" y="96">MAURO LOBO · ENGENHEIRO DE SISTEMAS</text>
  <text class="title" x="70" y="188">O óbvio já</text>
  <text class="title" x="70" y="262">foi tentado<tspan class="accent">.</tspan></text>
  <text class="sub" x="72" y="312">CRM comercial · plataformas de dados · agentes autônomos em produção</text>

  <line class="rule" x1="660" y1="330" x2="1208" y2="330" stroke="url(#rule)" stroke-width="1.5"/>
  <g>{pulses}</g>

  <text class="meta" x="72" y="360">CAMPINAS, SP · BRASIL</text>
  <text class="meta" x="1208" y="360" text-anchor="end">MAUROLOBO.VERCEL.APP</text>
</svg>
"""


for name in THEMES:
    path = f"assets/banner-{name}.svg"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(build(name))
    print("ok", path)
