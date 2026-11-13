#!/bin/bash
# usage: proc_clip.sh DAY TITLE ID SIZE
set -u
S=/tmp/claude-0/-home-user-MayconBarbon/99707c74-1abd-56d4-a68a-c149be73686e/scratchpad
DAY="$1"; TITLE="$2"; ID="$3"; SIZE="$4"
NAME=$(echo "$TITLE" | sed 's/^fx3 gabriel/C/; s/\.MP4$//')
OUT=$S/proc/$DAY/$NAME
[ -f "$OUT/done" ] && exit 0
mkdir -p "$OUT/kf"
TMP=$S/work/${DAY}_${NAME}.mp4
for try in 1 2 3 4 5 6 7 8 9 10; do
  curl -sS -L --retry 3 -o "$TMP" "https://drive.usercontent.google.com/download?id=$ID&export=download&confirm=t"
  [ "$(stat -c %s "$TMP" 2>/dev/null)" = "$SIZE" ] && break
  if head -c 2000 "$TMP" 2>/dev/null | grep -q "Quota exceeded"; then echo "QUOTA $DAY $NAME $(date +%T)" >> $S/proc/quota.log; rm -f "$TMP"; rmdir "$OUT/kf" "$OUT" 2>/dev/null; exit 0; else sleep $((try*5)); fi
done
if [ "$(stat -c %s "$TMP" 2>/dev/null)" != "$SIZE" ]; then echo "FAIL $DAY $TITLE" >> $S/proc/errors.log; rm -f "$TMP"; exit 0; fi
ffprobe -v error -print_format json -show_format -show_streams "$TMP" > "$OUT/probe.json"
ffmpeg -v error -skip_frame nokey -i "$TMP" -map 0:v:0 -vf scale=320:180 -fps_mode vfr -q:v 4 "$OUT/kf/%04d.jpg" -map 0:a:0? -ac 1 -ar 16000 -y "$OUT/audio16k.wav"
rm -f "$TMP"
N=$(ls "$OUT"/kf/*.jpg | wc -l)
# pick 6 evenly spaced keyframes for the sheet
python3 -I -c "
import sys,glob,subprocess
fs=sorted(glob.glob(sys.argv[1]+'/kf/*.jpg')); n=len(fs)
pick=[fs[min(n-1,round(i*(n-1)/5))] for i in range(6)] if n>=6 else fs+[fs[-1]]*(6-n)
args=[]
for p in pick: args+=['-i',p]
subprocess.run(['ffmpeg','-v','error']+args+['-filter_complex',''.join(f'[{i}]' for i in range(6))+'hstack=6','-y',sys.argv[1]+'/sheet.jpg'])
" "$OUT"
ffmpeg -nostats -i "$OUT/audio16k.wav" -af ebur128 -f null - 2>&1 | tail -12 > "$OUT/loud.txt"
touch "$OUT/done"
echo "OK $DAY $NAME $(jq -r .format.duration "$OUT/probe.json")" >> $S/proc/progress.log
