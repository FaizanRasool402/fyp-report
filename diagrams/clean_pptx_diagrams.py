"""Clean methodology diagrams extracted from the original PPTX."""
from PIL import Image
import os

SRC = r"c:\Users\Dell\Desktop\fyp-report\diagrams\from_pptx"
DST = r"c:\Users\Dell\Desktop\fyp-report\diagrams\cleaned"
IMG = r"c:\Users\Dell\Desktop\fyp-report\images\diagrams"
os.makedirs(DST, exist_ok=True)
os.makedirs(IMG, exist_ok=True)

TARGETS = {
    "slide15_1_Preprocessing_Pipeline.png": "preprocessing_pipeline.png",
    "slide16_1_Overall_System_Architecture.png": "system_architecture.png",
    "slide19_1_Methodology__Model_Architectures.png": "model_architectures.png",
    "slide22_1_Methodology__EfficientNetB3.png": "efficientnetb3_method.png",
    "slide26_1_Methodology__DenseNet121.png": "densenet121_method.png",
    "slide28_1_Methodology__Custom_CNN.png": "custom_cnn_method.png",
    "slide32_1_Input_Validation_Pipeline.png": "xray_gate_pipeline.png",
}


def trim_whitespace(im: Image.Image, threshold: int = 245, pad: int = 12) -> Image.Image:
    """Crop near-white / transparent borders, keep a small pad."""
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    # Flatten onto white for bounding-box detection
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    flat = Image.alpha_composite(bg, im)
    rgb = flat.convert("RGB")
    w, h = rgb.size
    px = rgb.load()

    def is_bg(x, y):
        r, g, b = px[x, y]
        return r >= threshold and g >= threshold and b >= threshold

    top = 0
    while top < h and all(is_bg(x, top) for x in range(w)):
        top += 1
    bottom = h - 1
    while bottom > top and all(is_bg(x, bottom) for x in range(w)):
        bottom -= 1
    left = 0
    while left < w and all(is_bg(left, y) for y in range(top, bottom + 1)):
        left += 1
    right = w - 1
    while right > left and all(is_bg(right, y) for y in range(top, bottom + 1)):
        right -= 1

    left = max(0, left - pad)
    top = max(0, top - pad)
    right = min(w - 1, right + pad)
    bottom = min(h - 1, bottom + pad)
    cropped = flat.crop((left, top, right + 1, bottom + 1))
    # Opaque white background for LaTeX/PPT reliability
    out = Image.new("RGB", cropped.size, (255, 255, 255))
    out.paste(cropped, mask=cropped.split()[-1])
    return out


for src_name, dst_name in TARGETS.items():
    src_path = os.path.join(SRC, src_name)
    im = Image.open(src_path)
    cleaned = trim_whitespace(im)
    # Mild sharpen via slightly larger canvas? keep native res
    out1 = os.path.join(DST, dst_name)
    out2 = os.path.join(IMG, dst_name)
    cleaned.save(out1, "PNG", optimize=True)
    cleaned.save(out2, "PNG", optimize=True)
    print(f"{src_name} -> {dst_name} {cleaned.size}")

print("done")
