#!/bin/bash
# uso: mix.sh out.wav music.wav dur vX@t ...
V=$(dirname $0)/../vo; out=$1; music=$2; dur=$3; shift 3; ins=""; fl=""; i=1; labs=""
for spec in "$@"; do f=${spec%@*}; t=${spec#*@}; ins="$ins -i $V/$f.wav"; ms=$(python3 -c "print(int($t*1000))"); fl="$fl[$i:a]aresample=48000,adelay=${ms}|${ms},apad[d$i];"; labs="$labs[d$i]"; i=$((i+1)); done
ffmpeg -nostdin -y -v error -i $music $ins -filter_complex "[0:a]aresample=48000,volume=0.20,atrim=0:$dur[m];${fl}${labs}amix=inputs=$#:normalize=0,atrim=0:$dur,asplit=2[vo][sc];[m][sc]sidechaincompress=threshold=0.015:ratio=8:attack=15:release=400:makeup=1[md];[md][vo]amix=inputs=2:normalize=0,afade=t=out:st=$(python3 -c "print($dur-0.6)"):d=0.6,aresample=48000" -ac 2 -ar 48000 -c:a pcm_f32le tmp_$out
I=$(ffmpeg -nostdin -hide_banner -i tmp_$out -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}')
G=$(python3 -c "print(-14.0-($I))")
ffmpeg -nostdin -y -v error -i tmp_$out -af "volume=${G}dB,alimiter=limit=0.84:attack=3:release=60:level=disabled" -c:a pcm_s16le $out; rm tmp_$out
