# Presentation diagram assets

These PNGs match the TikZ figures in the FYP report (Chapters 3–4).
Insert them into methodology / system-design slides of the PowerPoint.

| File | Use on slide | Report figure |
|------|--------------|---------------|
| `01_methodology_pipeline.png` | Methodology overview | Fig. method-pipeline |
| `02_data_unification.png` | Dataset / manifest | Fig. data-unify |
| `03_model_architecture.png` | Architectures + shared head | Fig. model-arch |
| `04_training_phases.png` | Training protocol | Fig. train-phases |
| `05_evaluation_flow.png` | Evaluation + leakage | Fig. eval-flow |
| `06_system_inference.png` | System design / inference | Fig. sys-arch-flow |
| `07_xray_gate.png` | X-ray validation gate | Fig. xray-gate |

**How to rebuild:** from `diagrams/`, run:
```
pdflatex export_diagrams.tex
pdftoppm -png -r 200 export_diagrams.pdf _tmp
```
Then rename pages 1–7 as above.

**Note:** The current PPTX on Desktop was not found (old 3-disease deck).
Share the presentation file and these diagrams can be inserted automatically.
