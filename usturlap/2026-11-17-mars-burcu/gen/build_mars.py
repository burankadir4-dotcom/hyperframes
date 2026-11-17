import math, sys, json
TM = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else None
out = sys.argv[1]
CX, CY = 540, 810
R_MOON = 130
R_DIAL = 295
S = R_DIAL / R_MOON
SIGNS = ['KOÇ','BOĞA','İKİZLER','YENGEÇ','ASLAN','BAŞAK','TERAZİ','AKREP','YAY','OĞLAK','KOVA','BALIK']
def pt(a, r):
    t = math.radians(a)
    return CX + r*math.cos(t), CY + r*math.sin(t)

# logo crescent (64-unit viewBox, centre 32,32, ring r=22)
CRES = "M29 20a12 12 0 1 0 13 17 9.5 9.5 0 1 1-13-17z"
def cres(scale, idattr):
    return f'<path {idattr} d="{CRES}" transform="translate({CX} {CY}) scale({scale:.4f}) translate(-32 -32)" fill="#C9A75C" />'

# ---------- the match: stick + head; the flame becomes the needle ----------
world = f'''
<svg id="world-svg" viewBox="0 0 1080 1920" width="1080" height="1920" aria-hidden="true">
  <g id="match">
    <rect x="{CX-7}" y="852" width="14" height="210" rx="3" fill="#0B0D12" stroke="#C9A75C" stroke-width="2"/>
    <ellipse cx="{CX}" cy="842" rx="15" ry="21" fill="#C9A75C"/>
  </g>
  <g id="flame">
    <path d="M{CX} 700C{CX+22} 758 {CX+36} 788 {CX+22} 814A26 26 0 0 1 {CX-22} 814C{CX-36} 788 {CX-22} 758 {CX} 700Z" fill="#E8D3A0"/>
    <path d="M{CX} 762C{CX+10} 788 {CX+16} 802 {CX+9} 816A11 11 0 0 1 {CX-9} 816C{CX-16} 802 {CX-10} 788 {CX} 762Z" fill="#F2EDE3"/>
  </g>
</svg>'''

# ---------- night layer: navy sky + skyline that holds the bottom of the frame ----------
def _h(i):  # deterministic pseudo-random in [0,1)
    x = (i * 2654435761) % 4294967296
    return ((x ^ (x >> 13)) % 1000) / 1000.0
night_stars = "".join(f'<circle cx="{int(40 + _h(i*3+1)*1000)}" cy="{int(140 + _h(i*3+2)*1100)}" r="{1.2 + _h(i*3+3)*1.2:.1f}" fill="#F2EDE3" fill-opacity="{0.25 + _h(i*7)*0.35:.2f}"/>' for i in range(26))
SKY_B = [(-20,130,1420),(110,90,1500),(200,150,1380),(350,80,1460),(430,120,1350),(550,100,1440),(650,140,1395),(790,90,1475),(880,120,1370),(1000,110,1455)]
sky_b = "".join(f'<rect x="{x}" y="{t}" width="{w}" height="{1920-t}" fill="#0B0D12"/>' for x,w,t in SKY_B)
sky_l = "".join(f'<path d="M{x} 1920V{t}H{x+w}V1920" fill="none" stroke="#C9A75C" stroke-opacity="0.4" stroke-width="1.5"/>' for x,w,t in SKY_B)
win, unlit = [], []
wi = 0
for bi,(x,w,t) in enumerate(SKY_B):
    cols = max(2, int(w // 34))
    for r in range(7):
        y = t + 30 + r*58
        if y > 1880: break
        for c in range(cols):
            wx = x + 14 + c*((w-28-16)/max(1,cols-1))
            if wx < 0 or wx > 1064: continue
            wi += 1
            if _h(wi*5+bi) < 0.22:
                win.append(f'<rect x="{wx:.0f}" y="{y}" width="16" height="22" fill="#E8D3A0" fill-opacity="0.8"/>')
            else:
                unlit.append((wx, y))
# 12 element lights spread across the skyline (upper rows only, where they read), 3 per element
cand = sorted([u for u in unlit if u[1] < 1640], key=lambda u: (u[0], u[1]))
step = len(cand) / 12
picks = {int(i*step + step/2) for i in range(12)}
el_win = {0: [], 1: [], 2: [], 3: []}
n = 0
for idx,(wx,y) in enumerate(cand):
    if idx in picks:
        k = n % 4; n += 1
        el_win[k].append(f'<rect id="ew{k}-{len(el_win[k])}" class="ew{k}" x="{wx:.0f}" y="{y}" width="16" height="22" fill="#E8D3A0" fill-opacity="0"/>')
    else:
        win.append(f'<rect x="{wx:.0f}" y="{y}" width="16" height="22" fill="#1F2B52" fill-opacity="0.9"/>')
for wx,y in unlit:
    if (wx,y) not in cand:
        win.append(f'<rect x="{wx:.0f}" y="{y}" width="16" height="22" fill="#1F2B52" fill-opacity="0.9"/>')
night = f"""
<svg id="night-svg" viewBox="0 0 1080 1920" width="1080" height="1920" aria-hidden="true">
  <rect x="0" y="0" width="1080" height="1920" fill="#121A33"/>
  <g id="night-stars">{night_stars}</g>
  <g id="skyline">{sky_b}{sky_l}{"".join(win)}{"".join(sum(el_win.values(), []))}</g>
</svg>"""

# ---------- dial ----------
sector_lines = "".join(
    (lambda a: (lambda p,q: f'<line class="sect" x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="#C9A75C" stroke-opacity="0.45" stroke-width="1.2" vector-effect="non-scaling-stroke"/>')(pt(a,268),pt(a,282)))(-105+30*i)
    for i in range(12))
names = []
for i,n in enumerate(SIGNS):
    a = -90 + 30*i
    x,y = pt(a, 247)
    an = ((a+180) % 360) - 180  # -180..180
    rot = a+90 if an <= 0 or an >= 180 else a-90
    if an == 0: rot = 90
    names.append(f'<text id="sg{i}" class="sign" fill="#8B92A8" x="{x:.1f}" y="{y:.1f}" transform="rotate({rot:.1f} {x:.1f} {y:.1f})" text-anchor="middle" dominant-baseline="central">{n}</text>')
names_svg = "".join(names)
tri_pts = " ".join(f"{pt(-90+120*k,212)[0]:.1f},{pt(-90+120*k,212)[1]:.1f}" for k in range(3))
tri_len = 3*212*math.sqrt(3)

dial = f'''
<svg id="dial-svg" viewBox="0 0 1080 1920" width="1080" height="1920" aria-hidden="true">
  <circle id="d-face" cx="{CX}" cy="{CY}" r="{R_DIAL}" fill="#0B0D12" opacity="0"/>
  <circle id="d-ring" cx="{CX}" cy="{CY}" r="{R_DIAL}" fill="none" stroke="#C9A75C" stroke-width="2" stroke-dasharray="{2*math.pi*R_DIAL:.1f}" stroke-dashoffset="{2*math.pi*R_DIAL:.1f}" transform="rotate(-90 {CX} {CY})" vector-effect="non-scaling-stroke"/>
  <g id="d-detail">
    <circle cx="{CX}" cy="{CY}" r="282" fill="none" stroke="#C9A75C" stroke-width="1.2" stroke-opacity="0.45" vector-effect="non-scaling-stroke"/>
    <circle cx="{CX}" cy="{CY}" r="212" fill="none" stroke="#C9A75C" stroke-width="1.2" stroke-opacity="0.45" vector-effect="non-scaling-stroke"/>
    {sector_lines}
    <g id="d-names">{names_svg}</g>
  </g>
  <polygon id="trigon" points="{tri_pts}" fill="none" stroke="#E8D3A0" stroke-width="2" stroke-dasharray="{tri_len:.1f}" stroke-dashoffset="{tri_len:.1f}" vector-effect="non-scaling-stroke"/>
  {cres(R_DIAL/22, 'id="d-cres" opacity="0"')}
  <g id="needle">
    <line x1="{CX}" y1="{CY+204}" x2="{CX}" y2="{CY-204}" stroke="#C9A75C" stroke-width="2.4" vector-effect="non-scaling-stroke"/>
    <path d="M{CX} {CY-226}L{CX-11} {CY-200}H{CX+11}Z" fill="#C9A75C"/>
  </g>
  <circle id="d-pin" cx="{CX}" cy="{CY}" r="9" fill="#0B0D12" stroke="#C9A75C" stroke-width="2" vector-effect="non-scaling-stroke"/>
</svg>'''

ELEM = [
 ("ates","ATEŞ MARS · KOÇ, ASLAN, YAY","Hemen başlamak","İlk kıvılcım yeter",[0,4,8]),
 ("toprak","TOPRAK MARS · BOĞA, BAŞAK, OĞLAK","Plan ve ısrar","Önce plan, sonra bırakmamak",[1,5,9]),
 ("hava","HAVA MARS · İKİZLER, TERAZİ, KOVA","Önce konuşmak","Bir fikir seni harekete geçirir",[2,6,10]),
 ("su","SU MARS · YENGEÇ, AKREP, BALIK","Hissederek ilerlemek","Kalbin ikna olunca durmazsın",[3,7,11]),
]
STOPS = TM["stops"]
TEXIT = TM["exits"]
T_END = TM["tEnd"]
D = TM["dial"]
TOTAL = TM["total"]

def line(id_, cls, start, dur, var, text, extra="", track=3):
    return f'<div id="{id_}" class="clip line {cls}" data-start="{start:.2f}" data-duration="{dur:.2f}" data-track-index="{track}" data-layout-allow-overlap{extra}><span id="{id_}-in" class="in" data-var-text="{var}">{text}</span></div>'

el_html = []
for k,(key,lab,head,sub,_) in enumerate(ELEM):
    st = STOPS[k]
    du = TEXIT[k]+0.25-st
    el_html.append(f'<div class="slot">'
      + line(f"{key}-lab","lab",st,du,f"{key}Label",lab,track=2)
      + line(f"{key}-head","head",st,du,f"{key}Head",head)
      + line(f"{key}-sub","sub",st,du,f"{key}Sub",sub,track=4)
      + '</div>')

wordmark = "".join(f'<span class="wl" id="wl{i}">{c}</span>' for i,c in enumerate("USTURLAP"))

variables = [
 ("hook1","Açılış 1","Bir şeyi istediğinde"),("hook2","Açılış 2","ilk adımı"),("hook3","Açılış vurgu","nasıl atarsın?"),
 ("lesson1","Ders 1","Mars burcun, harekete"),("lesson2","Ders 2","geçme biçimini anlatır"),
]
for key,lab,head,sub,_ in ELEM:
    variables += [(f"{key}Label",f"{key} etiket",lab),(f"{key}Head",f"{key} başlık",head),(f"{key}Sub",f"{key} alt satır",sub)]
variables += [("cta1","Kapanış soru","Senin Mars burcun"),("cta2","Kapanış vurgu","hangisi?"),("cta3","Kapanış çağrı","Yorumlara yaz"),("handle","Hesap","@usturlap.astro")]

html = f'''<template>
  <style>
    @font-face {{ font-family: "Usturlap Serif"; font-weight: 500; src: url("assets/fonts/lora-latin.woff2") format("woff2"); unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }}
    @font-face {{ font-family: "Usturlap Serif"; font-weight: 500; src: url("assets/fonts/lora-latin-ext.woff2") format("woff2"); unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF; }}
    @font-face {{ font-family: "Usturlap Sans"; font-weight: 300; src: url("assets/fonts/poppins-300-latin.woff2") format("woff2"); unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }}
    @font-face {{ font-family: "Usturlap Sans"; font-weight: 300; src: url("assets/fonts/poppins-300-latin-ext.woff2") format("woff2"); unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF; }}
    @font-face {{ font-family: "Usturlap Sans"; font-weight: 500; src: url("assets/fonts/poppins-500-latin.woff2") format("woff2"); unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }}
    @font-face {{ font-family: "Usturlap Sans"; font-weight: 500; src: url("assets/fonts/poppins-500-latin-ext.woff2") format("woff2"); unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; background: var(--night, #0B0D12); color: var(--ivory, #F2EDE3); font-family: "Usturlap Sans", sans-serif; }}
    #world, #night, #dial {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }}
    #world svg, #night svg, #dial svg {{ display: block; }}
    .sign {{ font-family: "Usturlap Sans", sans-serif; font-weight: 500; font-size: 28px; letter-spacing: 0; }}
    .slot {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; pointer-events: none; }}
    .line {{ position: absolute; left: 90px; width: 900px; text-align: center; }}
    .in {{ display: inline-block; }}
    .eyebrow {{ top: 280px; font-weight: 500; font-size: 32px; letter-spacing: 0.18em; color: #C9A75C; }}
    .lab {{ top: 276px; font-weight: 500; font-size: 34px; letter-spacing: 0.16em; color: #C9A75C; }}
    .head, .hook {{ font-family: "Usturlap Serif", serif; font-weight: 500; color: #F2EDE3; line-height: 1.12; }}
    .head {{ top: 324px; font-size: 88px; }}
    .hook {{ font-size: 76px; }}
    .gold {{ color: #E8D3A0; }}
    .sub {{ top: 432px; font-weight: 300; font-size: 48px; color: #F2EDE3; }}
    #wordmark {{ position: absolute; left: 90px; width: 900px; top: 1010px; text-align: center; font-family: "Usturlap Serif", serif; font-weight: 500; font-size: 64px; letter-spacing: 0.22em; color: #E8D3A0; }}
    #handle {{ top: 1100px; font-weight: 300; font-size: 34px; letter-spacing: 0.06em; color: #F2EDE3; }}
  </style>
  <div id="root" data-composition-id="film" data-width="1080" data-height="1920" data-composition-variables='__VARS__'>
    <div id="night" class="clip" data-start="0" data-duration="{TOTAL:.2f}" data-track-index="0" data-layout-allow-overflow>{night}</div>
    <div id="world" class="clip" data-start="0" data-duration="{D+0.4:.2f}" data-track-index="0">{world}</div>
    <div id="dial" class="clip" data-start="{D-0.6:.2f}" data-duration="{TOTAL-D+0.6:.2f}" data-track-index="1">{dial}</div>

    <div class="slot">
      {line("hook-a","hook",0,D-0.2,"hook1","Bir şeyi istediğinde",' style="top:330px"')}
      <div id="hook-b" class="clip line hook" data-start="0" data-duration="{D-0.2:.2f}" data-track-index="3" data-layout-allow-overlap style="top:416px"><span id="hook-b-in" class="in" data-var-text="hook2">ilk adımı</span> <span id="hook-c-in" class="in gold" data-var-text="hook3">nasıl atarsın?</span></div>
    </div>

    <div class="slot">
      {line("lesson-a","hook",D+0.2,TM["lessonOut"]+0.25-(D+0.2),"lesson1","Mars burcun, harekete",' style="top:300px"')}
      {line("lesson-b","hook",D+0.2,TM["lessonOut"]+0.25-(D+0.2),"lesson2","geçme biçimini anlatır",' style="top:386px"')}
    </div>

    {"".join(el_html)}

    <div class="slot">
      <div id="cta-a" class="clip line hook" data-start="{TM["ctaA"]-0.1:.2f}" data-duration="{TOTAL-TM["ctaA"]+0.1:.2f}" data-track-index="3" data-layout-allow-overlap style="top:300px"><span id="cta-a-in" class="in" data-var-text="cta1">Senin Mars burcun</span><br><span id="cta-b-in" class="in gold" data-var-text="cta2">hangisi?</span></div>
      {line("cta-c","sub",TM["ctaC"]-0.1,TOTAL-TM["ctaC"]+0.1,"cta3","Yorumlara yaz",' style="top:500px"')}
      <div id="wordmark" class="clip" data-start="{TM["mark"]-0.1:.2f}" data-duration="{TOTAL-TM["mark"]+0.1:.2f}" data-track-index="3">{wordmark}</div>
      {line("handle","",TM["handle"]-0.1,TOTAL-TM["handle"]+0.1,"handle","@usturlap.astro")}
    </div>
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      const C = "{CX} {CY}";
      const blurIn = (sel, at, d = 0.18) => tl.fromTo(sel, {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: d, ease: "expo.out" }}, at);
      const blurOut = (sel, at) => tl.to(sel, {{ opacity: 0, filter: "blur(8px)", duration: 0.2, ease: "power2.in" }}, at);
      const inkIn = (sel, at) => tl.fromTo(sel, {{ opacity: 0, color: "#8B92A8" }}, {{ opacity: 1, color: "#F2EDE3", duration: 0.3, ease: "power2.out" }}, at);

      // ---- hook: frame 0 already reads; the match strikes on "ilk adımı" ----
      tl.set("#hook-a-in", {{ opacity: 1 }}, 0);
      blurIn(["#hook-b-in", "#hook-c-in"], {TM["seni"]-0.05:.2f});
      tl.fromTo("#hook-c-in", {{ color: "#8B92A8" }}, {{ color: "#E8D3A0", duration: 0.3, ease: "power2.out" }}, {TM["rahat"]:.2f});
      const STRIKE = {TM["seni"]+0.1:.2f};
      tl.set("#flame", {{ scale: 0, svgOrigin: "{CX} 830" }}, 0);
      tl.fromTo("#match", {{ y: 34 }}, {{ y: 0, duration: 0.16, ease: "power4.out" }}, STRIKE);
      tl.to("#flame", {{ scale: 1, svgOrigin: "{CX} 830", duration: 0.4, ease: "expo.out" }}, STRIKE + 0.04);
      blurOut("#hook-a-in", {D-0.5:.2f});
      blurOut(["#hook-b-in", "#hook-c-in"], {D-0.44:.2f});

      // ---- the flame stretches into the needle; the dial draws itself around it ----
      tl.to("#flame", {{ scaleY: 1.9, scaleX: 0.12, svgOrigin: "{CX} 830", duration: 0.5, ease: "power3.in" }}, {D-0.6:.2f});
      tl.fromTo("#needle", {{ opacity: 0, rotation: 0, svgOrigin: C }}, {{ opacity: 1, rotation: 0, svgOrigin: C, duration: 0.12 }}, {D-0.14:.2f});
      tl.fromTo("#d-pin", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {D-0.14:.2f});
      tl.to("#flame", {{ opacity: 0, duration: 0.12 }}, {D-0.1:.2f});
      tl.to("#match", {{ y: 420, opacity: 0, duration: 0.6, ease: "power2.in" }}, {D-0.14:.2f});
      tl.fromTo("#d-face", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "power2.out" }}, {D:.2f});
      tl.to("#d-ring", {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 0.9, ease: "power2.inOut" }}, {D:.2f});
      tl.fromTo("#d-detail", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "power2.out" }}, {D+0.5:.2f});
      tl.fromTo(".sign", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, stagger: 0.04, ease: "power2.out" }}, {D+0.55:.2f});
      tl.set("#trigon", {{ rotation: 0, svgOrigin: C }}, 0);

      blurIn("#lesson-a-in", {TM["lessonA"]:.2f}, 0.2);   // "Mars burcunda"
      blurIn("#lesson-b-in", {TM["lessonB"]:.2f}, 0.2);  // "Çünkü"
      blurOut(["#lesson-a-in", "#lesson-b-in"], {TM["lessonOut"]:.2f});

      // ---- the needle makes a full turn while the voice explains, then lands on Koç on "ateş" ----
      tl.to("#needle", {{ rotation: 360, svgOrigin: C, duration: {STOPS[0]-TM["sweep"]:.2f}, ease: "power2.inOut" }}, {TM["sweep"]:.2f});

      const EL = {[[e[0], e[4]] for e in ELEM]};
      const STOPS = {STOPS};
      const EXITS = {TEXIT};
      EL.forEach(([key, signs], k) => {{
        const stop = STOPS[k];
        if (k > 0) {{
          const rot = k * 150;
          tl.to("#needle", {{ rotation: 360 + rot, svgOrigin: C, duration: 0.8, ease: "power2.inOut" }}, stop - 0.8);
          tl.to("#trigon", {{ rotation: rot, svgOrigin: C, duration: 0.8, ease: "power2.inOut" }}, stop - 0.8);
          tl.to(EL[k - 1][1].map((i) => "#sg" + i), {{ attr: {{ fill: "#8B92A8" }}, duration: 0.2, ease: "power2.out" }}, stop - 0.8);
        }} else {{
          tl.to("#trigon", {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 0.5, ease: "power2.inOut" }}, stop);
        }}
        tl.to(signs.map((i) => "#sg" + i), {{ attr: {{ fill: "#E8D3A0" }}, duration: 0.25, ease: "power2.out" }}, stop);
        tl.to(".ew" + k, {{ attr: {{ "fill-opacity": 0.85 }}, duration: 0.12, stagger: 0.09, ease: "power2.out" }}, stop + 0.05);
        tl.fromTo("#" + key + "-lab-in", {{ opacity: 0, filter: "blur(4px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power2.out" }}, stop + 0.08);
        blurIn("#" + key + "-head-in", stop + 0.18, 0.2);
        inkIn("#" + key + "-sub-in", stop + 0.4);
        blurOut(["#" + key + "-lab-in", "#" + key + "-head-in", "#" + key + "-sub-in"], EXITS[k]);
      }});

      // ---- pull back into the emblem ----
      const tEnd = {T_END};
      tl.to(["#d-detail", "#trigon"], {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, tEnd);
      tl.to("#dial-svg", {{ scale: 0.4, y: -80, transformOrigin: "{CX}px {CY}px", duration: 1.0, ease: "power2.inOut" }}, tEnd);
      tl.to("#needle", {{ rotation: 1131, svgOrigin: C, duration: 1.0, ease: "power2.inOut" }}, tEnd);
      tl.to("#d-cres", {{ opacity: 1, duration: 0.4, ease: "power2.out" }}, tEnd + 0.55);
      blurIn(["#cta-a-in", "#cta-b-in"], {TM["ctaA"]:.2f}, 0.2);
      tl.fromTo("#cta-b-in", {{ color: "#8B92A8" }}, {{ color: "#E8D3A0", duration: 0.3, ease: "power2.out" }}, {TM["hangisi"]:.2f});
      inkIn("#cta-c-in", {TM["ctaC"]:.2f});
      tl.fromTo(".wl", {{ opacity: 0.3, filter: "blur(4px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.25, stagger: 0.1, ease: "power2.out" }}, {TM["mark"]:.2f});
      inkIn("#handle-in", {TM["handle"]:.2f});

      window.__timelines["film"] = tl;
    }})();
  </script>
</template>
'''
html = html.replace('__VARS__', json.dumps([{"id":i,"type":"string","label":l,"default":d} for i,l,d in variables], ensure_ascii=False).replace("'","&#39;"))
open(out, "w").write(html)
import json
open(out + ".vars.json", "w").write(json.dumps([{"id":i,"type":"string","label":l,"default":d} for i,l,d in variables], ensure_ascii=False))
