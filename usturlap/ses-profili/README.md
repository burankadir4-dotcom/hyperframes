# Usturlap anlatıcı sesi (F2) · güncel

VoiceStudio · VoxCPM2 (Apache-2.0, ticari kullanıma açık) · tarifle oluşturulmuş, kimseye ait olmayan kalın erkek sesi (ortalama perde ~141 Hz).

- Referans: `usturlap-anlatici-F2-referans.mp3` (10,6 sn)
- Referans metni: "Bir şeyi gerçekten istediğinde... ilk adımı nasıl atarsın? Cevabın, Mars burcunda saklı. Çünkü Mars, harekete geçme biçimini anlatır."
- Tarif (instruct, İngilizce daha tutarlı): "Deep male voice, low pitch, soft and velvety, speaking slowly and softly as if telling a bedtime story to an adult friend, calm Turkish narrator"
- Ayarlar: language=tr, num_step=24, guidance_scale=2.4
- Yeni metin: `POST /generate` ile `ref_audio` = bu dosya, `ref_text` = yukarıdaki metin, `instruct` = yukarıdaki tarif.
- Not: Türkçe tarifle üretilen eski B sesi erkek için ince çıktı (~175–200 Hz); yeni seslerde perdeyi ölçerek seçin (erkek 85–155 Hz).

---

# Eski ses (B)

VoiceStudio · VoxCPM2 (Apache-2.0, ticari kullanıma açık) · tarifle oluşturulmuş, kimseye ait olmayan ses.

- Referans: `usturlap-anlatici-B-referans.mp3` (13,6 sn)
- Referans metni: "Uzun bir günün sonundasın... Peki seni gerçekten ne rahatlatır? Cevabın bir kısmı, Ay burcunda saklı. Çünkü Ay, duygusal ihtiyaçlarını anlatır."
- Tarif (instruct): "Orta yaşlı, yumuşak ve samimi bir erkek sesi; gece geç saatte bir arkadaşına konuşur gibi alçak tonda, huzur veren, net telaffuz"
- Ayarlar: language=tr, num_step=24, guidance_scale=2.4
- Yeni metin: `POST /generate` ile `ref_audio` = bu dosya, `ref_text` = yukarıdaki metin.
