# REVIEW · Usturlap Reels · 17 Kasım · Mars burcu

Render: `renders/usturlap-mars-burcu-17kasim.mp4` (1080×1920, 30 fps, 31.8 s; not tracked in git).

- Storyline A (Kıvılcım): a match strikes on "ilk adımı", the flame stretches into the astrolabe needle, the dial draws itself around it; needle stops on Ateş / Toprak / Hava / Su, then pulls back into the logo emblem.
- Voice: VoiceStudio · VoxCPM2 · Usturlap Anlatıcı (B), one take, 27.98 s, normalised to -16 LUFS (`assets/vo/vo-mars.mp3`).
- Timing: local Whisper (small, tr) aligned to the script (`gen/timing_mars.py`); stops 9.41 / 13.54 / 17.26 / 21.18 s. Regenerate with `gen/build_mars.py`, `gen/captions_mars.py`.
- Whisper heard "Mars burcun" as "Mars Burcu'nun" (same as the Ay video): needs a human listen.
- `check`: 0 errors; kept warnings: track density, needle rotation pivot (intended).
- Mix: -13.4 LUFS integrated, peak -1.0 dBFS. Measured, not heard. No music bed.
