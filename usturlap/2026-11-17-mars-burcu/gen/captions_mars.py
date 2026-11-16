import json, sys
words = json.load(open(sys.argv[1]))
out = sys.argv[2]
OFF = float(sys.argv[3]) if len(sys.argv) > 3 else 0.3
W = [{"id": f"w{i}", "text": t, "start": round(s + OFF, 3), "end": round(e + OFF, 3)} for i, (t, s, e) in enumerate(words)]
# groups by word index ranges; the closing question (words 57-62) is on screen verbatim, so it is not captioned.
GROUPS = json.load(open(sys.argv[4]))
groups_html, js = [], []
for g,(a,b) in enumerate(GROUPS):
    ws = W[a:b+1]
    start = round(ws[0]["start"] - 0.06, 3)
    nxt = W[GROUPS[g+1][0]]["start"] - 0.06 if g+1 < len(GROUPS) else ws[-1]["end"] + 0.4
    end = round(min(ws[-1]["end"] + 0.35, nxt), 3)
    spans = " ".join(f'<span id="cap-{w["id"]}" class="cw">{w["text"]}</span>' for w in ws)
    groups_html.append(f'<div id="cap-g{g}" class="clip cap" data-start="{start}" data-duration="{round(end-start,3)}" data-track-index="0"><div id="cap-g{g}-in" class="cap-in">{spans}</div></div>')
    js.append(f'tl.fromTo("#cap-g{g}-in", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1, ease: "power2.out" }}, {start});')
    for w in ws:
        js.append(f'tl.fromTo("#cap-{w["id"]}", {{ color: "#F2EDE3" }}, {{ color: "#E8D3A0", duration: 0.06 }}, {w["start"]});')
        js.append(f'tl.to("#cap-{w["id"]}", {{ color: "#F2EDE3", duration: 0.12 }}, {w["end"]});')
    js.append(f'tl.to("#cap-g{g}-in", {{ opacity: 0, duration: 0.1, ease: "power2.in" }}, {round(end-0.1,3)});')
html = f'''<template>
  <style>
    @font-face {{ font-family: "Usturlap Sans"; font-weight: 500; src: url("assets/fonts/poppins-500-latin.woff2") format("woff2"); unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD; }}
    @font-face {{ font-family: "Usturlap Sans"; font-weight: 500; src: url("assets/fonts/poppins-500-latin-ext.woff2") format("woff2"); unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF; }}
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    /* one rail line: under the dial, inside the Reels safe band (ends above 1248 px) */
    .cap {{ position: absolute; left: 0; top: 1126px; width: 1080px; overflow: visible; }}
    .cap-in {{ width: 1080px; text-align: center; font-family: "Usturlap Sans", sans-serif; font-weight: 500; font-size: 58px; line-height: 1.2; color: #F2EDE3; text-shadow: 0 2px 10px rgba(11, 13, 18, 0.95), 0 0 2px rgba(11, 13, 18, 0.9); }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
    {"".join(groups_html)}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join("      "+l for l in js).lstrip()}
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
'''
open(out, "w").write(html)
json.dump(W, open(out.replace("compositions/captions.html", "assets/transcript.json"), "w"), ensure_ascii=False, indent=0)
print(len(GROUPS), "groups")
