set -e
shots="4414:5:3.0 2721:2:3.2 42151:1:3.2 42148:1:3.0 42143:1:3.2 51528:1:3.2 51553:3:3.0 4155:6:3.6"
i=1; list=""
for s in $shots; do
  id=${s%%:*}; rest=${s#*:}; ss=${rest%%:*}; d=${rest#*:}
  ffmpeg -v error -y -ss $ss -t $d -i c$id.mp4 -loop 1 -t $d -i ov$i.png -filter_complex \
   "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,eq=saturation=1.08:contrast=1.04[v];[1:v]format=rgba[o];[v][o]overlay=0:0,format=yuv420p[out]" \
   -map "[out]" -an -c:v libx264 -preset medium -crf 20 -r 30 s$i.mp4
  list="$list file 's$i.mp4'\n"; i=$((i+1))
done
ffmpeg -v error -y -loop 1 -t 4 -i fim.png -vf "scale=1080:1920,format=yuv420p,fps=30" -c:v libx264 -preset medium -crf 20 -r 30 s9.mp4
printf "$list file 's9.mp4'\n" > lista.txt
ffmpeg -v error -y -f concat -safe 0 -i lista.txt -c copy video_sem_som.mp4
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 video_sem_som.mp4)
ffmpeg -v error -y -i video_sem_som.mp4 -i m1015.mp3 -filter_complex "[1:a]atrim=0:$D,afade=t=in:d=0.6,afade=t=out:st=$(python3 -c "print(round($D-1.8,2))"):d=1.8,volume=0.85[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 160k -shortest natal-reveillon-30s.mp4
ffprobe -v error -show_entries format=duration,size -of default=nw=1 natal-reveillon-30s.mp4
