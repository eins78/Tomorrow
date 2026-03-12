#!/bin/bash
set -e

DEPS="--with fontmake --with gftools --with fontbakery --with shaperglot"

rm -rf output/

for src in src/*.glyphs
do
  uv run $DEPS fontmake -g "$src" -o ttf --output-dir output/
done

for font in output/*.ttf
do
  uv run $DEPS gftools fix-nonhinting "$font" "$font"
done

# Cleanup gftools backup files:
rm -f output/*-backup-fonttools-prep-gasp.ttf

cp DESCRIPTION.*.html METADATA.pb OFL.txt output/

uv run $DEPS fontbakery check-googlefonts \
  --no-progress \
  -x googlefonts/glyphsets/shape_languages \
  --loglevel INFO \
  --ghmarkdown Tomorrow-fontbakery.md \
  output/*.ttf
