# SPEC · Usturlap Reels · "Ay burcuna göre seni ne rahatlatır?"

GOAL: The viewer recognises their own end-of-day state, learns which element their Moon sign belongs to, and comments their Moon sign.
OUTPUT: HyperFrames, 1080 × 1920, 30 fps. Instagram Reels, 20:00 TSİ, 16 Nov 2026.
TIME: 29 s × 30 = 870 frames. No music source available (not signed in), so the clock is the picture; SFX only.
LOOK: The Usturlap brand system, nothing else.
Ground #0B0D12 (room); window sky #121A33 flat, no gradient; ink #F2EDE3; quiet text #8B92A8.
Accent #C9A75C (lines, the dial) / #E8D3A0 (one word per frame, lit sign names, lit windows).
Display: Lora 500 (self-hosted, "Usturlap Serif"), 70–88 px, tracking 0.
Body: Poppins 300/500 (self-hosted, "Usturlap Sans"), 40 px body; labels 30 px, 500, tracking 0.18 em.
The medium is the brand's line drawing: every structure is a 2 px gold hairline (non-scaling), no fills except the moon crescent and the skyline.
No grain, no vignette, no shadow, no glow.
OBJECTS: An arched window (double hairline, sill), a skyline silhouette with a few lit windows, the moon drawn exactly as the logo emblem (ring + crescent),
the astrolabe dial: outer ring + notch ring, 12 sector lines, 12 Turkish sign names, inner ring, alidade (needle), centre pin,
the element triangle (trigon) joining the three signs of one element.
MOTION: Camera push: power3.inOut, 3.6 s, one tween, scale 1 → 2.769 about the moon centre (moon r 130 → dial r 360).
Needle + trigon: rotate together +150° per element, power2.inOut 0.8 s, always clockwise.
Text in: whole-line blur 8 → 0 px + opacity, 0.18 s, expo.out; sub-lines grey → ink 0.3 s, no translate.
Text out: blur 0 → 8 px + opacity → 0, 0.2 s, power2.in. Titles never move after they land.
End: dial pull-back (scale 1 → 0.33, power2.inOut 1.0 s) into the logo emblem; wordmark letters 0.3 → 1, 0.1 s apart.
SHOTS: f0–96 (0–3.2 s) hook: "23:47 / Zor bir günün sonunda" on screen at frame 0; "seni ne rahatlatır?" blurs in at 0.35/0.6 s; skyline lights go out at 1.2, 1.9, 2.6 s.
f36–144 (1.2–4.8 s) push into the moon; hook text exits at 3.0 s; whoosh peak on the fastest frame (~3.0 s).
f144–228 (4.8–7.6 s) moon ring becomes the dial; sign names draw in; lesson "Ay burcun, sana neyin / iyi geldiğini anlatır".
f228–708 (7.6–23.6 s) four 4 s beats (Ateş, Toprak, Hava, Su): needle turns 0.8 s → tick on the stop → three names light, trigon (drawn on beat 1) → label, headline, sub-line.
f708–870 (23.6–29 s) pull back into the emblem; "Senin Ay burcun hangisi?" / "Yorumlara yaz"; USTURLAP letter by letter, riser peak 25.6 s; @usturlap.astro; hold ≥ 2 s.
BANNED: dark void with small floating things (the window and the dial fill ≥ 70% of the width); glow, particles, gradients;
every element fading and sliding up; text moving while read; idle breathing/floating; corner labels; the docked logo;
tarot, crystal ball, neon galaxy (brand rule); chimes or synthesised tones.
QA: t=0 (thumbnail reads without sound), 3.0 (fastest push frame), 4.8 (moon → dial swap invisible), 8.4/12.4/16.4/20.4 (needle on the right sign, trigon on the 3 named signs),
10.5/14.5/18.5/22.5 (each element card readable at 360 px), 24.6 (emblem = logo), 28.5 (end card).
