# Project Memory — FYP Report & System

**Last updated:** 2026-09-14  
**Report repo:** `c:\Users\Dell\Desktop\fyp-report`  
**Code repo:** `c:\Users\Dell\Desktop\FYP\fyp`  
**Purpose of this file:** Persistent memory of what we built, changed, and decided so future sessions stay consistent.

---

## 1. Project identity

| Field | Value |
|-------|--------|
| Report title | AI Agent for Lung Disease Detection |
| Longer description | Unified four-class multi-architecture chest X-ray benchmark with ensemble web deployment |
| Students | Muhammad Ehtisham Hanif (ECI-IT-21-064), Humair Hayat (ECI-IT-21-058), Faizan Rasool (ECI-IT-21-057) |
| Supervisor | Miss Aisha Shafique |
| Examiners | Dr Muhammad Shaheer; Sir Usman Javed |
| Chairman | Dr Tahir Saleem |
| Associate Dean | Dr Hassan Raza |
| University | Hamdard University Islamabad Campus — FEST / Department of Computing |

---

## 2. What the system is NOW (post-2026 conversion)

**Before:** Three separate single-disease apps/models  
- TB → EfficientNetB3 (binary)  
- COVID → DenseNet121 (historically 2/3-class)  
- Pneumonia → Custom CNN (binary)  

**After (current truth for the report):**  
- **One label space:** Normal · Tuberculosis · COVID-19 · Pneumonia (fixed order)  
- **Three architectures** trained on the **same** `training/manifest.csv`  
- **Flask app:** no model picker — every upload runs all models + **soft-voting ensemble**  
- **Weights:** `weights/*_4class.keras` (not legacy `.h5`)  
- Viral Pneumonia (COVID source) **merged into Pneumonia**

### Models

| Model | Init | Input | Weights |
|-------|------|-------|---------|
| EfficientNetB3 | ImageNet | 256×256 | `efficientnetb3_4class.keras` |
| DenseNet121 | ImageNet | 224×224 | `densenet121_4class.keras` |
| Custom CNN | Scratch | 150×150 | `cnn_4class.keras` |

Shared transfer head: GAP → Dropout(0.5) → Dense(256, ReLU) → Dropout(0.3) → Softmax(4)  
Fine-tune: DenseNet from layer 300, EfficientNet from 340 (~43% weights); BatchNorm frozen in phase 2.

---

## 3. Verified 4-class results (Chapter 5 — do not invent)

**Manifest:** 3,227 images · train/val/test = 2,260 / 485 / 482 · seed 1337 · cap 1,200  
**COVID after dedupe:** 130 · Test COVID support: 19  

| Model | Accuracy | Balanced Acc. | Macro F1 |
|-------|----------|---------------|----------|
| EfficientNetB3 | 82.99% | 83.00% | 0.745 |
| DenseNet121 | 90.87% | 89.14% | 0.864 |
| Custom CNN | 90.25% | 88.36% | 0.835 |
| Ensemble | 92.32% | 93.07% | 0.867 |

**Leakage probe:** 88.17% source accuracy vs 49.79% majority baseline → **moderate** source signal.  
**Gate study:** 351 real / 106 non-X-ray → 100% real accepted; ~77% non-X-ray rejected (old ~21%).

**Training Mac env:** macOS 15.7.9, i9-9980HK, 32 GB, CPU-only TF 2.16.2 / Keras 3.15.0 / Python 3.11.15.

**Historical only (not comparable to 4-class):**  
- TB EfficientNetB3 test 95.63% (val 93.82%)  
- Pneumonia CNN 92% on 624-image test  
- Old COVID DenseNet validation ~0% (severe overfit)

---

## 4. Report structure (`fyp-report`)

### Front matter
Title pages (×4) → Abstract → Acknowledgement → Project in Brief → TOC → List of Figures → List of Tables

### Chapters
1. **Introduction** — Motivation, Problem, Aim & Objectives (5), Organization  
2. **Literature Review** — CNNs, COVID/TB/Pneumonia, transfer learning, gaps, related-works table  
3. **Methodology** — Unified manifest, honest splits, shared head, training, eval, leakage, app workflow  
4. **System Design** — Architecture, FR1–7, NFR1–6, X-ray gate, UI, train/serve consistency  
5. **Results and Discussion** — Manifest, metrics, confusion matrices, leakage, UI demos, historical prior work  
6. **Future Recommendations** — Conclusion, recommendations, future work, contributions  

### Back matter
References → Appendix A Dataset → Appendix B Architectures → Appendix C SDGs

### Key LaTeX files
- `main.tex`, `preamble.tex`, `frontmatter.tex`, `references.tex`, `appendices.tex`  
- `chapters/chapter01.tex` … `chapter06.tex`  
- UI images: `images/ui_*.png`  
- Confusion matrices: `images/results/confusion_*.png`  
- Logo: `images/hu.png`

### Formatting conventions (current)
- Font: newtx (Times-like), 12 pt, **one-half spacing** body; single spacing in tables/title pages  
- Chapter opener pages via `\chaptertitlepage{...}`  
- Tables: booktabs + `adjustbox` where needed; ragged `P{}` columns  
- Honesty rule: never invent metrics; label historical binary results clearly  

---

## 5. Work done in this Cursor conversation (high level)

1. Expanded early chapter text; applied Hamdard thesis-style formatting  
2. Title pages / certificate names / Project in Brief bordered table  
3. Removed “viral pneumonia as COVID model output” framing → later restored as **merge-into-Pneumonia** in unified design  
4. Full rewrite to **unified 4-class** design per `PROJECT_STATUS.md` + user handoff notes  
5. Replaced old UI screenshots with new 4-class Flask UI (`ui_upload`, `ui_gate_reject`, TB/COVID/pneumonia results)  
6. Validated methodology against detailed HTML methodology draft  
7. Finalized report from `FYP_Report_Generation_Brief.doc`  
8. Filled Chapter 5 from complete metrics pack (manifest, comparison, ensemble, leakage, runs)  
9. Formatting polish pass + this `memory.md` file  

---

## 6. Important paths outside the report repo

| Path | Role |
|------|------|
| `c:\Users\Dell\Desktop\FYP\fyp\` | Source code, training, weights, metrics |
| `...\training\manifest.csv` | Shared splits |
| `...\training\results\` | comparison.md, results.json, ensemble.json, leakage, confusion PNGs |
| `...\training\runs\*.json` | Train histories |
| `...\weights\*_4class.keras` | Deployed models |
| `...\xray-classifier-portable\` | Portable inference bundle |
| `c:\Users\Dell\Desktop\AI Agent For Lungs Diseases Detection.pptx` | Old 3-disease presentation (historical only) |

---

## 7. Rules for future edits

1. **Do not invent** Accuracy / P / R / F1 — use `training/results/` only.  
2. **Do not mix** historical binary TB/COVID/pneumonia scores into 4-class result tables.  
3. Prefer **balanced accuracy** as headline (COVID test n=19).  
4. Always note **research demo / not a clinical device**.  
5. Keep label order: Normal, Tuberculosis, COVID-19, Pneumonia.  
6. Cap used in reported run was **1200**, not the code default 400.  
7. Ensemble numbers are from offline `ensemble.json` (soft voting) — UI also shows consensus.  

---

## 8. Formatting polish (2026-09-14)

Completed:
- Fixed `\pagestyle{mainmatter}` before `\fancypagestyle` (caused `\undefinedpagestyle`).
- Removed `AtBeginEnvironment{tabular}` singlespace hook (broke nested `adjustbox`).
- Added `xurl` / `\path{...}` for breakable file paths.
- Project in Brief → `tabularx`; related-works table → `tabularx`.
- Body uses one-half spacing; chapter title pages unchanged.

### Table design system (same day)
- Slate header rows (`TableHead` + white `\Head{...}`)
- Alternating zebra body rows (`TableZebra`)
- Accent highlight for totals / ensemble / “this project” (`TableAccent`)
- Project in Brief: dark label column + soft gray rules
- Shared `\arraystretch{1.35}` and wider `\tabcolsep`

---

## 9. Optional remaining polish (not blocking)

- Physical certificate signatures on print  
- Fresh UI screenshots if app chrome changes  
- Final human proofread / viva Q&A sheet  
- Windows local TB + pneumonia folders only needed if regenerating eval from scratch  
- **Presentation:** share updated PPTX so methodology PNG diagrams can be inserted into slides  

### Presentation diagrams (cleaned, 2026-09-15)
- Extracted original PPT methodology images, trimmed whitespace, flattened to RGB
- Rebuilt deck from original (45 slides) with aspect-preserving placement
- Report now uses: `images/diagrams/preprocessing_pipeline.png`, `system_architecture.png`, `model_architectures.png`, `xray_gate_pipeline.png`
- Output: Desktop `AI_Lung_Disease_Detection_with_diagrams.pptx`

---

*End of memory file. Update this document whenever the system design, metrics, or report structure changes.*
