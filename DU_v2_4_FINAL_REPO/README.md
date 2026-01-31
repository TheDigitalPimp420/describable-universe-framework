# Describable Universe Framework — v2.4 (Toy Model Validation)

**Author:** Jesse James Leighty  
**Build date:** 2026-01-31

This release packages:
- The v2.4 paper (PDF + Markdown)
- Figures (comparative phase diagrams + redundancy curve)
- Reproducible code to regenerate figures and data
- Data CSVs used for plots

## Repo layout

```
paper/
figures/
code/
data/
README.md
```

## Quick start (Windows)

1. **Download & unzip** this release.
2. Install Python 3.10+ (recommended: Python 3.11).
3. Open **PowerShell** in the repo folder.
4. Create a virtual env (recommended):
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
5. Install dependencies:
   ```powershell
   py -m pip install -U pip numpy pandas matplotlib
   ```
6. Regenerate figures + data:
   ```powershell
   py .\code\DU_v24_generate.py
   ```
   Outputs are written to `figures/` and `data/`.

## GitHub publish steps

1. Create a new repo (or use your existing one).
2. Drag-drop the **contents** of this folder into GitHub Desktop or the web UI.
3. Commit message suggestion:
   - `v2.4 — toy model validation + phase structure`
4. Create a Release/tag:
   - Tag: `v2.4`
   - Attach the zip file you downloaded here.

## Notes

- The toy model is a stress test of the functional selection idea, not a claim about real cosmology.
- The point: structured coarse-grainings retain stability + redundancy in parameter regions where random coarse-graining fails.
