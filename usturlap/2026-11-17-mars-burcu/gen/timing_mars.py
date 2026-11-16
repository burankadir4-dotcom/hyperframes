"""Map the script's words onto a Whisper transcript and derive every film cue.
usage: timing.py transcript.json OFFSET out_words.json out_timing.json"""
import json, sys, difflib, re
SCRIPT = ("Bir şeyi gerçekten istediğinde... ilk adımı nasıl atarsın? Cevabın, Mars burcunda saklı. "
          "Çünkü Mars, harekete geçme biçimini anlatır. Mars'ın bir ateş burcundaysa, düşünmeden başlarsın. İlk kıvılcım yeter. "
          "Toprak burcundaysa, önce plan yaparsın, sonra bırakmazsın. Hava burcundaysa, önce konuşursun. Bir fikir seni harekete geçirir. "
          "Su burcundaysa, hissederek ilerlersin. Kalbin ikna olunca durmazsın. Peki senin Mars burcun hangisi? Yorumlara yaz.").split()
tr, OFF, out_w, out_t = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4]
d = json.load(open(tr)); ws = d if isinstance(d, list) else d.get("words", [])
norm = lambda t: re.sub(r"[^a-zçğıöşü]", "", t.lower().replace("İ", "i").replace("I", "ı"))
a, b = [norm(w) for w in SCRIPT], [norm(w["text"]) for w in ws]
m = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
times = [None] * len(SCRIPT)
for tag, i1, i2, j1, j2 in m.get_opcodes():
    if tag in ("equal", "replace") and (i2 - i1) == (j2 - j1):
        for k in range(i2 - i1): times[i1 + k] = (ws[j1 + k]["start"], ws[j1 + k]["end"])
    elif tag == "replace" and j2 > j1:  # spread the span evenly
        s, e = ws[j1]["start"], ws[j2 - 1]["end"]; n = i2 - i1
        for k in range(n): times[i1 + k] = (s + (e - s) * k / n, s + (e - s) * (k + 1) / n)
# fill gaps from neighbours
for i, t in enumerate(times):
    if t is None:
        prev = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), 0.0)
        nxt = next((times[j][0] for j in range(i + 1, len(times)) if times[j]), prev + 0.3)
        times[i] = (prev, max(prev + 0.05, nxt))
missing = sum(1 for k, (tag, *_r) in enumerate(m.get_opcodes()) if tag != "equal")
W = [[SCRIPT[i], round(s, 3), round(e, 3)] for i, (s, e) in enumerate(times)]
json.dump(W, open(out_w, "w"), ensure_ascii=False)
st = lambda i: W[i][1] + OFF; en = lambda i: W[i][2] + OFF
# word indices in SCRIPT
I = {w: i for i, w in enumerate(SCRIPT)}
idx = lambda word, nth=1: [i for i, w in enumerate(SCRIPT) if w == word][nth - 1]
stops = [st(idx("ateş")), st(idx("Toprak")), st(idx("Hava")), st(idx("Su"))]
dial = st(idx("Cevabın,")) + 0.66
exits = [stops[1] - 0.81, stops[2] - 0.81, stops[3] - 0.81, min(en(idx("durmazsın.")) + 0.2, st(idx("Peki")) - 0.35)]
T = {
  "seni": st(idx("ilk")), "rahat": st(idx("nasıl")), "dial": dial,
  "lessonA": st(idx("Mars", 1)), "lessonB": st(idx("Çünkü")), "lessonOut": st(idx("Mars'ın")) - 0.27,
  "sweep": st(idx("harekete")), "stops": stops, "exits": exits, "tEnd": exits[3] + 0.05,
  "ctaA": st(idx("Peki")), "hangisi": st(idx("hangisi?")), "ctaC": st(idx("Yorumlara")),
}
T["lessonA"] = max(T["lessonA"], T["dial"] + 0.25)
T["mark"] = max(en(idx("yaz.")) + 0.15, T["ctaC"] + 0.5)
T["handle"] = T["mark"] + 0.8
T["total"] = round(T["handle"] + 2.6, 2)
T = {k: (round(v, 3) if isinstance(v, float) else [round(x, 3) for x in v] if isinstance(v, list) else v) for k, v in T.items()}
json.dump(T, open(out_t, "w"), indent=1)
print("non-equal opcodes:", missing); print(json.dumps(T))
