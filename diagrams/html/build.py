"""Generate the report flowcharts as HTML pages in a draw.io-like style.

Shapes are drawn as stretched SVGs behind centred text; arrows are orthogonal
connectors computed from element positions after layout (see JS below).
Render with render.py.
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# draw.io default palette: (fill, stroke)
PAL = {
    "blue": ("#dae8fc", "#6c8ebf"),
    "green": ("#d5e8d4", "#82b366"),
    "yellow": ("#fff2cc", "#d6b656"),
    "red": ("#f8cecc", "#b85450"),
    "purple": ("#e1d5e7", "#9673a6"),
    "orange": ("#ffe6cc", "#d79b00"),
    "gray": ("#f5f5f5", "#666666"),
    "white": ("#ffffff", "#666666"),
}

CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:Helvetica,Arial,sans-serif;color:#1a1a1a}
.canvas{position:relative;width:WIDTHpx;padding:20px}
svg.wires{position:absolute;left:0;top:0;width:100%;height:100%;overflow:visible;pointer-events:none;z-index:0}
.shape{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;z-index:1;flex:none}
.shape>svg.bg{position:absolute;inset:0;width:100%;height:100%;overflow:visible;z-index:-1}
.lane .shape .t{font-size:16.5px}.lane .shape .s{font-size:14.5px}
.shape .t{font-size:18px;font-weight:700;line-height:1.22}
.shape .s{font-size:15.5px;color:#333;margin-top:3px;line-height:1.3}
.row{display:flex;align-items:center}
.col{display:flex;flex-direction:column}
.cap{font-size:15.5px;color:#333;text-align:center}
.note{font-size:15px;color:#444;font-style:italic;line-height:1.4}
.wlabel{position:absolute;font-size:15px;background:#fff;padding:0 4px;z-index:2;white-space:nowrap}
ul.l{list-style:none;text-align:left;font-size:15.5px;line-height:1.5;margin-top:4px}
ul.l li::before{content:"–";margin-right:6px;color:#666}
.lane{border:1.5px solid #666;background:#fff;flex:none}
.lane .hd{border-bottom:1.5px solid #666;text-align:center;padding:9px 6px}
.lane .hd .n{font-size:19px;font-weight:700}
.lane .hd .d{font-size:14.5px;font-style:italic;color:#333;margin-top:2px}
.lane .bd{padding:16px 14px;display:flex;flex-direction:column;gap:20px;align-items:center}
.lane .ft{text-align:center;font-size:14.5px;color:#333;padding:0 0 12px}
"""

JS = r"""
function anchor(el, side, cv){
  const r = el.getBoundingClientRect(), c = cv.getBoundingClientRect();
  const x = r.left - c.left, y = r.top - c.top;
  return {l:[x, y+r.height/2], r:[x+r.width, y+r.height/2],
          t:[x+r.width/2, y], b:[x+r.width/2, y+r.height]}[side];
}
function wire(cv, svg, w){
  const [a, as, b, bs, o={}] = w;
  const A = anchor(document.getElementById(a), as, cv);
  const B = anchor(document.getElementById(b), bs, cv);
  const f = o.f ?? 0.5; let d;
  const H = s => s==='l'||s==='r';
  if (H(as) && H(bs)) { const xm = A[0] + (B[0]-A[0])*f; d = `M${A} H${xm} V${B[1]} H${B[0]}`; }
  else if (!H(as) && !H(bs)) { const ym = A[1] + (B[1]-A[1])*f; d = `M${A} V${ym} H${B[0]} V${B[1]}`; }
  else if (H(as)) d = `M${A} H${B[0]} V${B[1]}`;
  else d = `M${A} V${B[1]} H${B[0]}`;
  const col = o.color || '#333333';
  const p = document.createElementNS('http://www.w3.org/2000/svg','path');
  p.setAttribute('d', d); p.setAttribute('fill','none'); p.setAttribute('stroke', col);
  p.setAttribute('stroke-width', 1.8); p.setAttribute('stroke-linejoin','miter');
  if (o.dash) p.setAttribute('stroke-dasharray','7 5');
  p.setAttribute('marker-end', `url(#m-${o.mk||'d'})`);
  svg.appendChild(p);
  if (o.label){
    const L = document.createElement('div'); L.className='wlabel'; L.textContent=o.label;
    L.style.color = o.lcolor || '#333'; if (o.bold) L.style.fontWeight = 700; cv.appendChild(L);
    const len = p.getTotalLength(), pt = p.getPointAtLength(len*(o.lt ?? 0.5));
    L.style.left = (pt.x - L.offsetWidth/2 + (o.lx||0)) + 'px';
    L.style.top = (pt.y - L.offsetHeight/2 + (o.ly||0)) + 'px';
  }
}
window.addEventListener('load', () => {
  const cv = document.querySelector('.canvas');
  const svg = document.createElementNS('http://www.w3.org/2000/svg','svg'); svg.classList.add('wires');
  const mk = (id, c) => `<marker id="m-${id}" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="13" markerHeight="13" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 L2.5,5 z" fill="${c}"/></marker>`;
  svg.innerHTML = '<defs>' + mk('d','#333333') + mk('r','#b85450') + mk('o','#d79b00') + '</defs>';
  cv.prepend(svg);
  (window.WIRES || []).forEach(w => wire(cv, svg, w));
});
"""

# Shape outlines in a 100x100 box, stretched to the element (stroke stays 1.6px).
PATHS = {
    "cyl": ('<path d="M0,12 C0,-4 100,-4 100,12 L100,88 C100,104 0,104 0,88 Z"/>'
            '<path d="M0,12 C0,28 100,28 100,12" fill="none"/>'),
    "diamond": '<polygon points="50,0 100,50 50,100 0,50"/>',
    "doc": '<path d="M0,0 H100 V86 C75,72 60,104 30,94 C18,90 8,88 0,92 Z"/>',
    "note": '<path d="M0,0 H88 L100,12 V100 H0 Z"/><path d="M88,0 V12 H100" fill="none"/>',
}


def shape(id_, kind, color, title, sub="", w=220, h=78, pad="0 12px", extra="", style=""):
    fill, stroke = PAL[color]
    if kind in ("rect", "pill"):
        r = h / 2 if kind == "pill" else 8
        body = (f'<svg class="bg" viewBox="0 0 {w} {h}" preserveAspectRatio="none">'
                f'<rect x="0.8" y="0.8" width="{w-1.6}" height="{h-1.6}" rx="{r}" ry="{r}" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="1.6"/></svg>')
    else:
        body = (f'<svg class="bg" viewBox="0 0 100 100" preserveAspectRatio="none" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="1.6" stroke-linejoin="round">'
                + PATHS[kind].replace("<path", '<path vector-effect="non-scaling-stroke"')
                .replace("<polygon", '<polygon vector-effect="non-scaling-stroke"')
                + "</svg>")
    if kind == "cyl":
        pad = "18px 10px 4px"
    if kind == "doc":
        pad = "0 12px 12px"
    t = f'<div class="t">{title}</div>' if title else ""
    s = f'<div class="s">{sub}</div>' if sub else ""
    return (f'<div class="shape" id="{id_}" style="width:{w}px;height:{h}px;padding:{pad};{style}">'
            f'{body}{t}{s}{extra}</div>')


def page(name, width, body, wires):
    html = f"""<!doctype html><html><head><meta charset="utf-8">
<style>{CSS.replace('WIDTH', str(width))}</style></head>
<body><div class="canvas">{body}</div>
<script>window.WIRES = {wires};</script><script>{JS}</script></body></html>"""
    with open(os.path.join(OUT, name + ".html"), "w", encoding="utf-8") as fh:
        fh.write(html)


# ---------------------------------------------------------------- 1. methodology pipeline
B = dict(w=230, h=90)
body = f"""
<div class="row" style="gap:70px">
 {shape('s1','cyl','gray','Public CXR sources',**B)}
 {shape('s2','rect','blue','Build unified manifest','dedupe, patient splits',**B)}
 {shape('s3','rect','blue','Preprocess + augment','model-specific sizes',**B)}
</div>
<div class="row" style="gap:70px;margin-top:60px">
 {shape('s6','pill','green','Flask ensemble deployment','soft voting + X-ray gate',**B)}
 {shape('s5','rect','blue','Evaluate + leakage probe',**B)}
 {shape('s4','rect','blue','Train three architectures',**B)}
</div>"""
page("fig_methodology", 870, body,
     "[['s1','r','s2','l'],['s2','r','s3','l'],['s3','b','s4','t'],['s4','l','s5','r'],['s5','l','s6','r']]")

# ---------------------------------------------------------------- 2. data unification
C = dict(w=200, h=92)
body = f"""
<div class="row" style="gap:62px">
 <div class="col" style="gap:20px">
  {shape('d1','cyl','gray','TB CXR database',**C)}
  {shape('d2','cyl','gray','COVID-19 dataset',**C)}
  {shape('d3','cyl','gray','Pneumonia CXR dataset',**C)}
 </div>
 {shape('m','rect','blue','Merge + hash dedupe',w=180,h=84)}
 {shape('sp','rect','blue','Patient-grouped train/val/test',w=180,h=84)}
 <div class="col" style="gap:10px;align-items:center">
  <div class="cap" style="font-size:14px;white-space:nowrap;visibility:hidden">x</div>
  {shape('mf','doc','green','manifest.csv','4 classes',w=180,h=92)}
  <div class="cap" style="font-size:14px;white-space:nowrap">Normal · TB · COVID-19 · Pneumonia</div>
 </div>
</div>"""
page("fig_data_unification", 960, body,
     "[['d1','r','m','l'],['d2','r','m','l'],['d3','r','m','l'],['m','r','sp','l'],['sp','r','mf','l']]")

# ---------------------------------------------------------------- 3. preprocessing
M = dict(w=250, h=96)
body = f"""
<div class="row" style="align-items:flex-start">
 <div style="width:260px;padding-top:150px">
  {shape('aug','note','yellow','4 · Augmentation','training images only',w=220,h=210,pad='10px 14px',
     extra='<ul class="l"><li>horizontal flip</li><li>rotation ±8%</li><li>zoom ±15%</li><li>translation ±10%</li><li>contrast ±10%</li></ul>')}
 </div>
 <div class="col" style="gap:34px;align-items:center;width:480px">
  {shape('raw','pill','gray','Raw chest X-ray','any size, usually grayscale',w=420,h=76)}
  {shape('dec','rect','blue','1 · Decoding to three channels','a grayscale film is repeated across R, G and B',w=420,h=80)}
  {shape('rs','rect','blue','2 · Bilinear resizing','scaled to each model’s input size',w=420,h=80)}
 </div>
</div>
<div class="row" style="justify-content:space-between;margin-top:66px">
 {shape('e','rect','purple','EfficientNetB3','256 × 256<br>EfficientNet scaling',**M)}
 {shape('dn','rect','purple','DenseNet121','224 × 224<br>DenseNet scaling',**M)}
 {shape('cn','rect','purple','Custom CNN','150 × 150<br>rescale to 0–1',**M)}
</div>
<div class="row" style="justify-content:center;margin-top:48px">
 {shape('ten','pill','green','Model input tensor',w=360,h=64)}
</div>
<div class="note" style="margin-top:16px;text-align:center">Inference repeats the exact decode and resize used in training, so there is no train and serve mismatch.</div>"""
page("fig_preprocessing", 900, body,
     "[['raw','b','dec','t'],['dec','b','rs','t'],"
     "['rs','b','e','t',{label:'3 · model-specific normalisation',lt:0.22}],['rs','b','dn','t'],['rs','b','cn','t'],"
     "['e','b','ten','t'],['dn','b','ten','t'],['cn','b','ten','t'],"
     "['aug','r','rs','l',{dash:1,color:'#d79b00',mk:'o'}]]")

# ---------------------------------------------------------------- 4. model architectures (swimlanes)
K = dict(w=290, h=72, style='font-size:0.92em')


def lane(prefix, name, desc, hdcol, rows, params):
    blocks, wires = [], []
    for i, (t, s, col) in enumerate(rows):
        blocks.append(shape(f"{prefix}{i}", "rect", col, t, s, **K))
        if i:
            wires.append(f"['{prefix}{i-1}','b','{prefix}{i}','t']")
    html = (f'<div class="lane" style="width:322px"><div class="hd" style="background:{PAL[hdcol][0]}">'
            f'<div class="n">{name}</div><div class="d">{desc}</div></div>'
            f'<div class="bd">{"".join(blocks)}</div><div class="ft">{params}</div></div>')
    return html, wires


aug = ("Augmentation", "flip · rotate · zoom · shift", "white")
out4 = ("Dense 4, softmax", "Normal · TB · COVID-19 · Pneumonia", "green")
lanes = [
    ("a", "EfficientNetB3", "transfer learning · frozen then fine-tuned", "blue",
     [("Input 256 × 256 × 3", "", "gray"), aug, ("EfficientNet preprocessing", "", "white"),
      ("EfficientNetB3 base", "ImageNet, 11.2M params", "blue"),
      ("Phase 2: unfreeze from layer 340", "(~43% of weights)", "white"),
      ("Shared head", "GAP > Drop .5 > Dense 256 > Drop .3", "yellow"), out4], "11,178,035 parameters"),
    ("b", "DenseNet121", "transfer learning · frozen then fine-tuned", "blue",
     [("Input 224 × 224 × 3", "", "gray"), aug, ("DenseNet preprocessing", "", "white"),
      ("DenseNet121 base", "ImageNet, 121 layers", "blue"),
      ("Phase 2: unfreeze from layer 300", "(~43% of weights)", "white"),
      ("Shared head", "GAP > Drop .5 > Dense 256 > Drop .3", "yellow"), out4], "7,300,932 parameters"),
    ("c", "Custom CNN", "trained from scratch · no pre-training", "purple",
     [("Input 150 × 150 × 3", "", "gray"), aug, ("Rescale to 0–1", "", "white"),
      ("5 convolution blocks", "32 > 64 > 64 > 128 > 256 filters", "purple"),
      ("Each block", "Conv > BatchNorm > MaxPool (+ Dropout)", "white"),
      ("Own head", "Flatten > Dense 128 > Drop .2", "gray"), out4], "1,247,364 parameters"),
]
htmls, wires = [], []
for l in lanes:
    h, w = lane(*l)
    htmls.append(h)
    wires += w
body = (shape('top', 'rect', 'blue', 'Same unified 4-class dataset, same split, same augmentation, same epoch budget',
              'the two transfer models also share a classification head; the CNN uses its own', w=1006, h=72)
        + '<div class="row" style="justify-content:space-between;align-items:stretch;margin-top:18px">' + "".join(htmls) + "</div>")
page("fig_model_architectures", 1046, body, "[" + ",".join(wires) + "]")

# ---------------------------------------------------------------- 5. training phases
T = dict(w=230, h=96)
body = f"""
<div class="row" style="gap:80px;align-items:flex-start">
 <div class="col" style="gap:10px">{shape('p1','rect','blue','Phase 1','Frozen backbone<br>LR 1×10⁻⁴',**T)}<div class="cap">train head only</div></div>
 <div class="col" style="gap:10px">{shape('p2','rect','blue','Phase 2','Partial unfreeze ~43%<br>LR 1×10⁻⁵',**T)}<div class="cap">BN frozen; Adam</div></div>
 <div class="col" style="gap:10px">{shape('sv','doc','green','Save','4-class .keras',**T)}<div class="cap">seed 1337; class weights</div></div>
</div>"""
page("fig_training_phases", 900, body, "[['p1','r','p2','l'],['p2','r','sv','l']]")

# ---------------------------------------------------------------- 6. evaluation flow
body = f"""
<div class="row" style="gap:56px">
 {shape('ts','cyl','gray','Held-out test set',w=170,h=96)}
 <div class="col" style="gap:18px">
  {shape('m1','rect','purple','EffNetB3',w=150,h=56)}
  {shape('m2','rect','purple','DenseNet',w=150,h=56)}
  {shape('m3','rect','purple','CNN',w=150,h=56)}
 </div>
 {shape('mt','rect','blue','Per-class P / R / F1 + CM',w=190,h=84)}
 {shape('en','pill','green','Soft-vote ensemble',w=190,h=70)}
</div>
<div class="row" style="gap:56px;margin-top:46px">
 <div style="width:170px"></div><div style="width:150px"></div>
 {shape('lk','rect','orange','Leakage probe','(source accuracy)',w=190,h=76)}
</div>"""
page("fig_evaluation", 940, body,
     "[['ts','r','m1','l'],['ts','r','m2','l'],['ts','r','m3','l'],"
     "['m1','r','mt','l'],['m2','r','mt','l'],['m3','r','mt','l'],"
     "['mt','r','en','l'],['mt','b','lk','t']]")

# ---------------------------------------------------------------- 7. system inference
V = dict(w=400, h=78)
body = f"""
<div class="col" style="align-items:center;gap:40px">
 {shape('up','pill','gray','Chest X-ray uploaded','PNG or JPG',w=360,h=72)}
 {shape('gt','rect','yellow','Chest X-ray gate','rejects non radiograph images',**V)}
 {shape('pp','rect','blue','Preprocessing','resized and scaled per model',**V)}
 <div class="row" style="width:100%;justify-content:space-between;margin-top:14px">
  {shape('a','rect','purple','EfficientNetB3','256 × 256',w=240,h=72)}
  {shape('b','rect','purple','DenseNet121','224 × 224',w=240,h=72)}
  {shape('c','rect','purple','Custom CNN','150 × 150',w=240,h=72)}
 </div>
 {shape('ens','rect','green','Three independent verdicts over the same four classes','Normal · Tuberculosis · COVID-19 · Pneumonia',w=560,h=78)}
 {shape('res','pill','gray','Result and agreement shown',w=360,h=64)}
</div>"""
page("fig_system_inference", 860, body,
     "[['up','b','gt','t'],['gt','b','pp','t'],"
     "['pp','b','a','t',{label:'every model scores every image',lt:0.2}],['pp','b','b','t'],['pp','b','c','t'],"
     "['a','b','ens','t'],['b','b','ens','t'],['c','b','ens','t'],['ens','b','res','t']]")

# ---------------------------------------------------------------- 8. x-ray gate (decision diamonds)
D = dict(w=430, h=150, pad="0 70px")
R = dict(w=270, h=78)
red = "{color:'#b85450',mk:'r',label:'fail',lcolor:'#b85450',bold:1}"
grn = "{label:'pass',lcolor:'#2d7a2d',bold:1,lx:30}"
body = f"""
<div class="col" style="gap:34px">
 <div class="row" style="width:430px;justify-content:center">{shape('u','pill','gray','Uploaded image',w=300,h=60)}</div>
 <div class="row" style="gap:90px">
  {shape('g1','diamond','yellow','Stage 1 · Monochrome?','grayscale, or one colour tint',**D)}
  {shape('r1','rect','red','Reject','colour photo, not a radiograph',**R)}
 </div>
 <div class="row" style="gap:90px">
  {shape('g2','diamond','yellow','Stage 2 · Radiograph envelope','7 measures, 1 violation forgiven',**D)}
  {shape('r2','rect','red','Reject','wrong brightness / contrast pattern',**R)}
 </div>
 <div class="row" style="gap:90px">
  {shape('g3','diamond','yellow','Stage 3 · Anatomy present?','bright spine OR symmetry',**D)}
  {shape('r3','rect','red','Reject','no chest structure',**R)}
 </div>
 <div class="row" style="width:430px;justify-content:center">{shape('ok','pill','green','Accepted','sent to all three models',w=300,h=70)}</div>
 <div class="note">Every rejection tells the user why, and offers “Analyse anyway” as an override.</div>
</div>"""
page("fig_xray_gate", 860, body,
     f"[['u','b','g1','t'],['g1','b','g2','t',{grn}],['g2','b','g3','t',{grn}],['g3','b','ok','t',{grn}],"
     f"['g1','r','r1','l',{red}],['g2','r','r2','l',{red}],['g3','r','r3','l',{red}]]")
print("built")
