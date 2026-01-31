# describable-universe-framework
A computational and information-theoretic framework modeling the emergence of stable, redundant macrostructure in describable universes.
# Describable Universe Framework (v2.4)

**Author:** Jesse James Leighty
**Version:** 2.4 — Toy Model Validation + Phase Structure
**Status:** Research framework with computational stress test

---

## Overview

The Describable Universe Framework proposes an information-theoretic selection principle for why certain macroscopic structures in a mathematically consistent universe become stable, redundant, and therefore describable.

The core idea is simple:

Not all coarse-grainings of microstates are equal.
Structures that persist under dynamics and generate redundant environmental records are preferentially describable.

This repository contains:

* The formal framework (PDF + Markdown)
* A computational toy model (spin-chain universe)
* Comparative phase diagrams
* Redundancy growth analysis
* Fully reproducible Python code

---

## Core Functional

The framework evaluates coarse-grainings ( C ) using:

[
F(C) = \alpha S_{\text{info}}(C) + \lambda R_{\text{info}}(C) - \beta L(M)
]

Where:

* ( S_{\text{info}} ) = dynamical stability (negative conditional entropy)
* ( R_{\text{info}} ) = redundancy across environmental fragments
* ( L(M) ) = macrostate complexity penalty
* ( \alpha, \lambda, \beta ) = weighting parameters

The hypothesis:

Coarse-grainings that maximize ( F(C) ) correspond to stable, redundantly encoded macrostructure — the kinds of structures that can be described.

---

## Toy Model Validation

To stress-test the framework, we constructed a minimal universe:

* Microstates: binary spin chain (N = 64)
* Dynamics: independent bit-flip noise
* Coarse-grainings tested:

  * Block-majority (structured)
  * Global majority
  * Random hash (unstructured control)
* Environment: noisy fragment records of macrostates

Results show:

* Structured coarse-grainings retain high ( F(C) ) in defined parameter regions.
* Random coarse-grainings collapse across nearly all regimes.
* A clear describability threshold emerges as dynamical and environmental noise increase.
* Redundancy scales with fragment count in a nonlinear fashion.

This moves the framework from conceptual proposal to computationally validated selection principle.

---

## Repository Structure

```
paper/
    Describable_Universe_Framework_v2_4.pdf
    Describable_Universe_Framework_v2_4.md

figures/
    DU_v24_phase_Block.png
    DU_v24_phase_Global.png
    DU_v24_phase_Hash.png
    DU_v24_redundancy.png

code/
    DU_toy_model.py
    DU_v24_generate.py

data/
    DU_v24_phase_grid_Block.csv
    DU_v24_phase_grid_Global.csv
    DU_v24_phase_grid_Hash.csv
    DU_v24_redundancy.csv
```

---

## Reproducibility (Windows)

1. Install Python 3.10+
2. Open PowerShell in repo folder

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -U pip numpy pandas matplotlib
py .\code\DU_v24_generate.py
```

Outputs are written to `figures/` and `data/`.

---

## Conceptual Positioning

This framework intersects:

* Information theory
* Statistical mechanics
* Renormalization concepts
* Decoherence and redundancy (Quantum Darwinism)
* Emergence and macrostructure stability

It does **not** claim a final cosmological theory.

It proposes a formal selection principle for describability within mathematically consistent structures.

---

## Next Directions

Planned upgrades:

* Critical curve fitting for describability phase boundary
* Scaling analysis
* Formal connection to RG gradient flows
* Higher-dimensional coarse-graining families

---

## Citation (Working Draft)

Leighty, J.J.
*Describable Universe Framework: An Information-Theoretic Selection Principle for Stable Macrostructure.*
Version 2.4 (2026).


