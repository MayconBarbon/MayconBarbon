#!/bin/bash
# Monta os vídeos: quadros JPEG 24 fps + trilha original normalizada em -16 LUFS
# saída: ../../portfolio/construtoras/0N-nivel/  (original de alta qualidade + versão web)
set -e
cd "$(dirname "$0")"
P=../../portfolio/construtoras
declare -A DIR=([essencial]=01-essencial [acabamentos]=02-acabamentos [decorado]=03-decorado [cinematic]=04-cinematic)
for id in "$@"; do
  for o in ${ORIENT:-h v}; do
    F=frames/${id}_$o; [ -d $F ] || continue
    n=$(ls $F | wc -l); dur=$(python3 -c "print({'essencial':25,'acabamentos':30,'decorado':40,'cinematic':60}['$id'])")
    [ "$n" -ge $((dur*24)) ] || { echo "incompleto $id $o: $n"; continue; }
    D=$P/${DIR[$id]}; mkdir -p $D
    tag=$([ $o = h ] && echo 1920x1080 || echo 1080x1920)
    AF="loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=out:st=$((dur-1)):d=1"
    ffmpeg -y -v error -framerate 24 -i $F/%05d.jpg -i audio/$id.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -profile:v high -level 4.2 -c:a aac -b:a 256k -af "$AF" -shortest -movflags +faststart $D/videoimovel-studio3d-${id}-${tag}-original.mp4
    ffmpeg -y -v error -framerate 24 -i $F/%05d.jpg -i audio/$id.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 25 -maxrate 6M -bufsize 12M -pix_fmt yuv420p -profile:v high -level 4.1 -c:a aac -b:a 160k -af "$AF" -shortest -movflags +faststart $D/videoimovel-studio3d-${id}-${tag}-web.mp4
    echo "ok $id $o $(du -h $D/videoimovel-studio3d-${id}-${tag}-original.mp4 | cut -f1) / web $(du -h $D/videoimovel-studio3d-${id}-${tag}-web.mp4 | cut -f1)"
  done
done
