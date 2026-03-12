"""Fix usWeightClass and related metadata in built TTF files."""
from fontTools.ttLib import TTFont
import glob, os, sys

WEIGHT_MAP = {
    "Thin": 100,
    "ExtraLight": 200,
    "Light": 300,
    "Regular": 400,
    "Medium": 500,
    "SemiBold": 600,
    "Bold": 700,
    "ExtraBold": 800,
    "Black": 900,
}

for f in sorted(glob.glob("output/Tomorrow-*.ttf")):
    basename = os.path.basename(f).replace("Tomorrow-", "").replace(".ttf", "")
    # Strip "Italic" to get the weight name
    weight_name = basename.replace("Italic", "").strip()
    if not weight_name:
        # Pure "Italic" means Regular weight
        weight_name = "Regular"

    weight_class = WEIGHT_MAP.get(weight_name)
    if weight_class is None:
        print(f"WARNING: Unknown weight '{weight_name}' for {f}", file=sys.stderr)
        continue

    tt = TTFont(f)
    old_wc = tt["OS/2"].usWeightClass
    tt["OS/2"].usWeightClass = weight_class

    # Fix macStyle and fsSelection for bold variants
    is_bold = weight_class >= 700
    is_italic = "Italic" in basename

    # macStyle: bit 0 = bold, bit 1 = italic
    mac_style = 0
    if is_bold:
        mac_style |= 0x0001
    if is_italic:
        mac_style |= 0x0002
    tt["head"].macStyle = mac_style

    # fsSelection: bit 0 = ITALIC, bit 5 = BOLD, bit 6 = REGULAR
    fs = 0
    if is_italic:
        fs |= 0x0001
    if is_bold:
        fs |= 0x0020
    if not is_bold and not is_italic:
        fs |= 0x0040
    # bit 7 = USE_TYPO_METRICS
    fs |= 0x0080
    tt["OS/2"].fsSelection = fs

    tt.save(f)
    print(f"{os.path.basename(f):40s}  usWeightClass: {old_wc} -> {weight_class}")
    tt.close()
