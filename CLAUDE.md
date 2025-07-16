# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based scientific computing project for developing sustainable aviation fuel (SAF) from CO₂/CO-rich flue gas using electrocatalytic conversion, cell-free enzymatic biocatalysis, and chemical upgrading processes.

## Development Commands

### Package Management
**Always use `uv` instead of pip**:
```bash
# Install all dependencies
uv install --dev

# Add new packages
uv add <package-name>

# Run Python scripts
uv run python <script.py>

# Run Jupyter notebooks
uv run --with jupyter jupyter lab
```

### Python Version
This project requires Python 3.12 (specified in `.python-version`).

## Project Vision

The goal is to develop a computational framework for sustainable aviation fuel (SAF) production from CO₂/CO-rich flue gas through an integrated bio-electrochemical process.

### Core Technical Vision

**Multi-scale modeling approach**:
1. **Metabolic Layer**: Genome-scale modeling of E. coli for pathway optimization
2. **Kinetic Layer**: Enzyme cascade modeling for cell-free biocatalysis
3. **AI/ML Layer**: Protein engineering using structure prediction and machine learning
4. **Process Layer**: Reactor design and techno-economic optimization

**Key computational workflows**:
- **Flux Balance Analysis (FBA)**: Optimize metabolic fluxes for maximum fatty acid production
- **Kinetic Modeling**: Model enzyme cascades for formate → acetyl-CoA → fatty acids conversion
- **Process Optimization**: Design bioreactor operations and downstream processing
- **Economic Analysis**: Calculate production costs and identify bottlenecks

### Integration Philosophy

The codebase should seamlessly connect:
- Electrochemical CO₂/CO reduction to formate
- Cell-free enzymatic conversion to acetyl-CoA
- Reverse β-oxidation pathway to C₄-C₁₆ fatty acids
- Chemical upgrading to jet fuel specifications

## Critical Technical Challenges

### Primary Bottleneck: Rate Mismatch (Orders of Magnitude)

**Current cell-free systems achieve 0.08–0.44 g L⁻¹ h⁻¹ while targets require ≥ 30 g L⁻¹ h⁻¹**

Rate gaps that must be addressed:
- CO₂→Formate: 1.0 → 30 g L⁻¹ h⁻¹ (× 30 gap)
- Formate→Acetyl-CoA: 0.08 → 30 g L⁻¹ h⁻¹ (× 375 gap)
- Acetyl-CoA→C₆: 0.44 → 30 g L⁻¹ h⁻¹ (× 70 gap)

### Energy Budget Reality Check

**The 12 kWh kg⁻¹ target is thermodynamically aggressive**
- SAF enthalpy: 42–43 MJ kg⁻¹ ≈ 11.6 kWh kg⁻¹ (theoretical minimum)
- Realistic target: 18–22 kWh kg⁻¹ accounting for losses
- Must include: Faradaic losses, ATP/NADH overpotentials, H₂ demand

### High-Priority De-Risking Strategies

1. **Replace PURE/iPROBE with crude lysate systems** (10× protein concentration)
2. **Eliminate Rh catalyst dependency** (Sn/Bi-based MEAs)
3. **Synthetic formate validation** (decouple from electrolysis early)
4. **Thermophilic enzyme mining** (5–10× rate gains)
5. **Cofactor-free cascade development** (reduce NADH/ATP costs)

### Materials & Safety Concerns

**Critical substitutions needed:**
- Phenol extraction → Isododecane/ionic liquids (toxicity/regulations)
- Rh/In₂O₃ catalyst → Sn/Bi alternatives (cost/availability)
- Formic acid transport → On-skid processing (UN Class 8 logistics)

## Scientific Context

The project aims to:
- Convert flue gas (CO₂/CO) to jet fuel at ≤ US$700/ton
- Achieve space-time yield (STY) ≥ 30 g L⁻¹ h⁻¹
- Use cell-free enzymatic systems to avoid cellular maintenance costs
- Produce C₄-C₁₆ fatty acids via reverse β-oxidation

**When implementing features, prioritize:**
- **Rate enhancement strategies** over purity/optimization
- **Crude lysate systems** over purified enzyme approaches
- **Synthetic substrate validation** before MEA integration
- **Alternative catalyst screening** to reduce material costs
- **TRL-gated development** over calendar-based timelines