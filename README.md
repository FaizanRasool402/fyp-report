# AI Agent for Lung Disease Detection — LaTeX FYP Report

LaTeX source for the Final Project Report: **AI Agent for Lung Disease Detection**.

## Project Structure

```
fyp-report/
├── main.tex              # Main document — compile this file
├── preamble.tex          # Packages and formatting
├── frontmatter.tex       # Title page, abstract, table of contents
├── references.tex        # Bibliography
├── appendices.tex        # Appendices A–C
├── chapters/
│   ├── chapter01.tex     # Introduction
│   ├── chapter02.tex     # Literature Review
│   ├── chapter03.tex     # System Architecture
│   ├── chapter04.tex     # COVID-19 Model (DenseNet121)
│   ├── chapter05.tex     # TB Model (EfficientNetB3)
│   ├── chapter06.tex     # Pneumonia Model (Custom CNN)
│   ├── chapter07.tex     # Flask Web Application
│   ├── chapter08.tex     # System Integration
│   ├── chapter09.tex     # Tools and Technologies
│   ├── chapter10.tex     # Results and Discussion
│   ├── chapter11.tex     # Challenges and Solutions
│   └── chapter12.tex     # Conclusion and Future Work
└── README.md
```

## Prerequisites (MiKTeX — you are downloading this)

1. Finish installing **MiKTeX** (`basic-miktex-25.12-x64.exe` from your screenshot).
2. During setup, choose **"Install missing packages on-the-fly: Yes"** so LaTeX can auto-download any extra packages.
3. Optional: install **TeXstudio** or use VS Code with the **LaTeX Workshop** extension for easier editing.

## How to Compile (Windows)

### Option A — Command line (PowerShell)

Open PowerShell in this folder and run:

```powershell
cd C:\Users\Dell\Desktop\fyp-report
pdflatex main.tex
pdflatex main.tex
```

Run `pdflatex` **twice** so the table of contents and cross-references resolve correctly.

Output: `main.pdf`

### Option B — TeXstudio

1. Open `main.tex` in TeXstudio.
2. Set **Options → Configure TeXstudio → Build → Default Compiler** to `pdfLaTeX`.
3. Press **F5** (Build & View) twice.

### Option C — VS Code + LaTeX Workshop

1. Install the **LaTeX Workshop** extension.
2. Open the `fyp-report` folder.
3. Open `main.tex` and save — it should build automatically, or use **Build LaTeX project**.

## Customization

Edit these before submission:

| What to change | File |
|----------------|------|
| Your name / student ID | `frontmatter.tex` (add after title block) |
| University logo | `frontmatter.tex` — add `\includegraphics{logo.png}` |
| Supervisor name | `frontmatter.tex` |
| Exact accuracy numbers | `chapters/chapter10.tex` |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `pdflatex` not recognized | Restart terminal after MiKTeX install, or add MiKTeX `bin` to PATH |
| Missing package error | Allow MiKTeX to install it when prompted |
| Table of contents empty | Run `pdflatex` a second time |
| `%` symbols in tables | Already escaped as `\%` in the source |

## Notes

- This report matches your provided content: 12 chapters, references, and 3 appendices.
- Figures are not included yet — add images to an `images/` folder and use `\includegraphics{images/yourfile.png}` where needed.
- For official university formatting (margins, cover page template), adjust `preamble.tex` and `frontmatter.tex` to match your department guidelines.
