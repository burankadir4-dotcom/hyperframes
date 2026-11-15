# Usturlap anlatıcı sesi (B)

VoiceStudio · VoxCPM2 (Apache-2.0, ticari kullanıma açık) · tarifle oluşturulmuş, kimseye ait olmayan ses.

- Referans: `usturlap-anlatici-B-referans.mp3` (13,6 sn)
- Referans metni: "Uzun bir günün sonundasın... Peki seni gerçekten ne rahatlatır? Cevabın bir kısmı, Ay burcunda saklı. Çünkü Ay, duygusal ihtiyaçlarını anlatır."
- Tarif (instruct): "Orta yaşlı, yumuşak ve samimi bir erkek sesi; gece geç saatte bir arkadaşına konuşur gibi alçak tonda, huzur veren, net telaffuz"
- Ayarlar: language=tr, num_step=24, guidance_scale=2.4
- Yeni metin: `POST /generate` ile `ref_audio` = bu dosya, `ref_text` = yukarıdaki metin.
