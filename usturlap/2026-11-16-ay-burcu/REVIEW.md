# REVIEW · Usturlap Reels · 16 Kasım

Render: `renders/usturlap-ay-burcu-16kasim.mp4` (1080×1920, 30 fps, 29 s).

## Creative calls

- Storyline A (Gece 23:47) built. B (Kadran) and C (Dört oda) stay in STORYLINES.md.
- The moon is drawn as the logo emblem (ring + crescent), so the push into the moon lands on the dial and the film ends by pulling the dial back into the same emblem.
- The needle and the element triangle rotate together +150° per element, so each stop points at one sign of the element and the triangle joins its three signs.
- The sky is flooded to the room colour during the push (4.1–4.8 s), so the dial sits on the brand ground with no colour cut.
- Text sits in the Instagram Reels safe band (14–65% of the height). `check --safe-zone reels` is clean.

## Measured

- `check`: 0 errors. Rendered audio: true peak −1.1 dBTP, no clipping, −22 LUFS integrated (SFX only, no music bed). Ticks at 8.405 / 12.43 / 16.405 / 20.43 s, one frame after each needle stop.
- Looked at: frames 0, 2.2, 3.0, 4.0, 4.3–5.1 (the moon→dial seam), 6.5, 8.6, 10.5, 14.5, 18.5, 22.5, 24.2, 25.2, 28.5.
- Not checked: the sound was measured, not heard.

## Weakest shot / next

- No music: the HeyGen catalog needs `npx hyperframes auth login`. With a bed (~70 bpm ambient), land the wordmark on a strong beat at ~25.6 s.
- 4.75–5.0 s shows only the ring for ~0.3 s before the dial draws in; could start the sector lines 0.15 s earlier.
- The bottom third under the dial is empty by design (Instagram caption and buttons sit there).

## Warnings kept

- `timeline_track_too_dense`: one scene on purpose (a continuous take); the text lines share lanes 2–4.
- `rotation_pivot_drift`: the needle and triangle rotate about the dial centre (svgOrigin), not their own box centre. Intended.
