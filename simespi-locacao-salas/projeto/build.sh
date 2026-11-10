#!/bin/bash
# Reconstrói as entregas A, B e C a partir das fotos originais do Drive.
# Requisitos: python3 (numpy, Pillow), ffmpeg. Fotos baixadas para projeto/src (não versionadas).
set -e
cd "$(dirname "$0")"
mkdir -p src build
while read id name; do
  [ -f src/$name ] || curl -sSL -o src/$name "https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t"
done <<LIST
1e0cF7dqAjuIrkNZiNPsBkd6CTVEARnC6 S1_9825.jpg
1AAw7SF37zwsvl3WKa3zHZcMMo3SPS4p5 S1_9829.jpg
1a6plb1r0ykK9kERyMserEvTEULTyHyEW S1_9837.jpg
1MQzhJT7FHYPal6ZxsuDtfOjixobi0xAa S1_9832.jpg
1poBl3oFzGb-oQqvfQ6LN80K3si-DMeqr S2_8151.jpg
1XQNoFcdaQrnUfKf17nBaCsgmYPp53u3z S2_8149.jpg
1YIt03AM5740mq3X72YZ4QrZMHwtyF3YU S2_8138.jpg
1LpPxMJq52inH1kgVQuKSED16HmTNusyy S2_8141.jpg
LIST
# render.py usa src/, fonts/, logo/ e vo/*.wav relativos a projeto/
for i in 1 2 3 4 5 6 7 8 9 10 11 12; do ffmpeg -nostdin -v error -y -i vo/v$i.flac vo/v$i.wav; done
cp render.py music.py mix.sh build/ && cd build
python3 music.py main music_main.wav && python3 music.py ad music_ad.wav && python3 music.py tour music_tour.wav
python3 render.py main v_main.mp4 && python3 render.py ad v_ad.mp4 && python3 render.py tour v_tour.mp4 && python3 render.py cover capa.jpg
./mix.sh a_main.wav music_main.wav 39.0 v1@0.5 v2@5.7 v3@12.4 v4@21.6 v5@30.2
./mix.sh a_ad.wav music_ad.wav 15.0 v1@0.15 v6@3.65 v7@8.25
ffmpeg -nostdin -y -v error -i v_main.mp4 -i a_main.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart A_reels_39s.mp4
ffmpeg -nostdin -y -v error -i v_ad.mp4 -i a_ad.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart B_anuncio_15s.mp4
echo "OK: build/A_reels_39s.mp4 build/B_anuncio_15s.mp4 build/capa.jpg"
./mix.sh a_tour.wav music_tour.wav 28.8 v8@0.3 v9@4.6 v10@11.0 v11@17.5 v12@22.9
ffmpeg -nostdin -y -v error -i v_tour.mp4 -i a_tour.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart E_tour_29s.mp4
