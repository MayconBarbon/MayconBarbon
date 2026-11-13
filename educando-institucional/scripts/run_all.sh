#!/bin/bash
cat /tmp/claude-0/-home-user-MayconBarbon/99707c74-1abd-56d4-a68a-c149be73686e/scratchpad/jobs2.tsv | tr '\t\n' '\0\0' | xargs -0 -n4 -P2 /tmp/claude-0/-home-user-MayconBarbon/99707c74-1abd-56d4-a68a-c149be73686e/scratchpad/bin/proc_clip.sh
echo ALLDONE >> /tmp/claude-0/-home-user-MayconBarbon/99707c74-1abd-56d4-a68a-c149be73686e/scratchpad/proc/progress.log
