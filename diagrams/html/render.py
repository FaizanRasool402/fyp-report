"""Render each diagram HTML to a cropped high-resolution PNG with headless Edge."""
import glob, os, subprocess, sys
from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
DEST = sys.argv[1]
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
SCALE = 3

for html in sorted(glob.glob(os.path.join(HERE, "fig_*.html"))):
    name = os.path.splitext(os.path.basename(html))[0]
    raw = os.path.join(HERE, name + "_raw.png")
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={SCALE}", "--window-size=1100,1700",
                    "--virtual-time-budget=2000", f"--screenshot={raw}",
                    "file:///" + html.replace("\\", "/")], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    im = Image.open(raw).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    box = ImageChops.difference(im, bg).getbbox()
    pad = 12 * SCALE
    box = (max(box[0] - pad, 0), max(box[1] - pad, 0), min(box[2] + pad, im.width), min(box[3] + pad, im.height))
    out = os.path.join(DEST, name + ".png")
    im.crop(box).save(out, dpi=(300, 300))
    print(name, im.crop(box).size, "bottom-touch" if box[3] >= im.height - 1 else "")
