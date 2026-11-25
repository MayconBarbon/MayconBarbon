#!/bin/bash
# Renderiza todos os quadros: 4 processos em paralelo por vídeo
cd "$(dirname "$0")"
for job in "essencial h" "acabamentos h" "decorado h" "cinematic h" "cinematic v" "essencial v" "acabamentos v" "decorado v"; do
  set -- $job
  echo "== $1 $2 $(date +%T)"
  for w in 0 1 2 3; do node render.js $1 $2 $w 4 > logs/$1_$2_$w.log 2>&1 & done
  wait
  echo "== fim $1 $2 $(date +%T) quadros: $(ls frames/$1_$2 | wc -l)"
done
