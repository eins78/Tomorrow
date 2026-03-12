#!/bin/bash
set -e

rm -rf output/

for src in src/*.glyphs
do
  fontmake -g "$src" -o ttf --output-dir output/
done

for font in output/*.ttf
do
  gftools fix-nonhinting "$font" "$font"
done

# Cleanup gftools backup files:
rm -f output/*-backup-fonttools-prep-gasp.ttf

cp DESCRIPTION.*.html METADATA.pb OFL.txt output/

fontbakery check-googlefonts \
  --no-progress \
  -x googlefonts/glyphsets/shape_languages \
  --loglevel INFO \
  --ghmarkdown Tomorrow-fontbakery.md \
  output/*.ttf
