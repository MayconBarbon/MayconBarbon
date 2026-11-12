#!/bin/bash
# mktri.sh out.mp4 dur f1 ss1 f2 ss2 f3 ss3   (clipes SDR verticais 1080x1920 já com a logo trocada)
o=$1; t=$2
ffmpeg -v error -y -ss $4 -t $t -i $3 -ss $6 -t $t -i $5 -ss $8 -t $t -i $7 -f lavfi -t $t -i color=0x0a3643:s=1920x1080:r=30 -filter_complex \
"[0:v]scale=632:-2,crop=632:1080,setpts=PTS-STARTPTS[a];[1:v]scale=632:-2,crop=632:1080,setpts=PTS-STARTPTS[b];[2:v]scale=632:-2,crop=632:1080,setpts=PTS-STARTPTS[c];\
[3:v][a]overlay=0:0[p];[p][b]overlay=644:0[q];[q][c]overlay=1288:0,format=yuv420p[v]" -map "[v]" -r 30 -c:v libx264 -crf 14 -t $t $o
