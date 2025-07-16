# ecoli-code

## Run Jupyter Notebook
```sh
uv run --with jupyter jupyter lab
```

> NOTE: This repo uses uv. So use `uv run python` instead of `python` to run Python scripts, and use `uv add` to add new packages instead of `pip install`.

# Project Vision: Flue‑to‑Jet Sustainable Aviation Fuel (SAF)

## 1  Purpose

Develop a modular, electricity‑driven platform that converts **CO₂/CO‑rich flue gas** into drop‑in SAF at **≤ US \$ 700 t⁻¹** while ultimately achieving an overall **space‑time yield (STY) ≥ 30 g L⁻¹ h⁻¹**. The concept couples high‑current electrocatalytic formate synthesis with cell‑free metabolic modules and catalytic upgrading.

## 2  Process Architecture

```mermaid
flowchart LR
    A[Flue gas (CO₂ + CO)] -->|Gas capture & drying| B(Electrocatalytic<br>formate reactor)
    B -->|Liquid HCOO⁻/HCOOH| C(Cell‑free<br>Formate→Acetyl‑CoA)
    C -->|Acetyl‑CoA pool| D(Cell‑free<br>reverse β‑oxidation)
    D -->|C₄–C₁₆ acyl‑CoA / acids| E{Chain‑length<br>decision}
    E -- C₈–C₁₆ --> F(Zeolite ZSM‑5<br>dehydration / oligomerisation)
    E -- C₄–C₈ --> G(Single‑step ATJ‑type<br>oligomerisation)
    F & G --> H(Hydroprocessing
& distillation)
    H --> I(SAF blend stock – ASTM D1655/D7566)
```

* **Distributed front‑end** (A → B): skid‑mounted gas‑diffusion MEA stacks attached to point sources (cement, steel, refinery). Formate solution (≈ 35 wt %) trucked or railed to the biocatalysis hub.
* **Central back‑end** (C → I): nitrogen‑blanketed continuous stirred‑tank reactors (CSTRs) running PURE/iPROBE cell‑free systems at 25–35 °C, followed by fixed‑bed solid‑acid upgrading.

## 3  Scientific Rationale and Benchmarks

| Module                   | Technology                                                        | 2022‑25 peer‑reviewed benchmark                                                     | Comment                                   |
| ------------------------ | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------- |
| **CO₂/CO → Formate**     | Rh‑doped In₂O₃ gas‑diffusion MEA                                  | 1.2 A cm⁻²; 90 % faradaic efficiency (FE); 15 mmol cm⁻² h⁻¹ (≈ 1 g L⁻¹ h⁻¹) formate | Stable > 100 h at ambient pressure \[1]   |
| **Formate → Acetyl‑CoA** | 9‑enzyme synthetic reductive formate (ReForm) pathway (cell‑free) | 4.3 g L⁻¹ acetyl‑CoA in 5 h (0.86 g L⁻¹ h⁻¹); 86 % C‑molar yield \[2]               | ATP‑neutral via polyphosphate kinase loop |
| **Reverse β‑Oxidation**  | In‑vitro r‑BOX (PURE/iPROBE)                                      | 38 mM hexanoate in 10 h (0.44 g L⁻¹ h⁻¹); 762 variants screened \[3]                | Chain length tunable to C₄–C₁₆            |
| **C₈–C₁₆ Upgrading**     | ZSM‑5 (Si/Al ≈ 30) dehydration & oligomerisation                  | > 92 % C₈⁺ single‑pass yield at 340 °C; WHSV 2 h⁻¹ \[4]                             | Coke mitigated by 2 % H₂ co‑feed          |
| **C₄–C₈ Upgrading**      | Solid‑acid ATJ analogue (HZSM‑5/SAPO‑11)                          | 80–90 % jet‑range yield at 280–320 °C \[5]                                          | Basis for Twelve’s E‑Jet® process         |

### Key enabling principles

1. **Electro‑enzymatic cofactor recycling** (NADH, ATP) keeps reactor OPEX low.
2. **Enzyme immobilisation** on conductive supports boosts stability (> 200 h t₁/₂).
3. **Heat integration**: zeolite reactor exhaust (340 °C) pre‑heats MEA cathode feed.
4. **Distributed capture** minimises carbon transport while exploiting cheap land‑locked renewable electricity hubs.

## 4  Techno‑Economic Snapshot

| Parameter                               | 2026 demo (100 L h⁻¹)                | 2030 target         |
| --------------------------------------- | ------------------------------------ | ------------------- |
| Overall STY (CO₂→SAF)                   | ≈ 3 g L⁻¹ h⁻¹                        | ≥ 30 g L⁻¹ h⁻¹      |
| Electricity consumption                 | 23 kWh kg⁻¹ SAF                      | ≤ 12 kWh kg⁻¹ SAF   |
| SAF MSP (ex‑plant)                      | 1 600–3 000 € t⁻¹ (PtL range)        | **≤ US \$ 700 t⁻¹** |
| Reference Jet‑A1 price (IATA, Jun 2025) | **US \$ 86 bbl⁻¹ ≈ 680 \$ t⁻¹** \[6] | —                   |

Dominant cost drivers are renewable electricity (≈ 55 %), capital depreciation (≈ 25 %), and enzymes (≈ 10 %). Hitting the \$700 t⁻¹ milestone relies on PV electricity ≤ 2 ¢ kWh⁻¹ (Chile, MENA, India) plus enzyme half‑life > 500 h.

## 5  Development Roadmap

| Phase         | Scale        | Milestones                                                               | Toolchain                             |
| ------------- | ------------ | ------------------------------------------------------------------------ | ------------------------------------- |
| **α (Bench)** | 5 mL batch   | Cofactor‑balanced formate→acetyl‑CoA; select r‑BOX terminators for C₆/C₈ | PURE, robotic CFPS, LC‑MS             |
| **β (Flow)**  | 1 L h⁻¹ skid | Continuous enzyme‑immobilised column; inline NADH electro‑recycling      | Micro‑CSTR, bio‑electrodes            |
| **γ (Pilot)** | 100 L h⁻¹    | End‑to‑end SAF meeting ASTM D7566 Annex A2 specs                         | Integrated MEA stack + CSTR + zeolite |

## 6  Risk Register (excerpt)

| Risk                         | Likelihood | Impact        | Mitigation                                      |
| ---------------------------- | ---------- | ------------- | ----------------------------------------------- |
| Enzyme thermal drift (30 °C) | Medium     | ↓ yield       | Directed‑evolution + immobilisation             |
| MEA flooding at >3 A cm⁻²    | Medium     | Outage        | PTFE‑rich foils + differential pressure control |
| Zeolite coking               | High       | ↓ selectivity | 500 °C steam‑air regeneration every 24 h        |
| Supply of high‑purity KHCO₃  | Low        | ↑ OPEX        | On‑site electro‑dialytic regeneration           |

## 7  References

1. **Li et al.** “Ampere‑level co‑electrosynthesis of formate from CO₂.” *Nat. Commun.* 16, 4850 (2025).
2. **Landwehr et al.** “A synthetic cell‑free pathway for biocatalytic upgrading of one‑carbon substrates into acetyl‑CoA.” *bioRxiv* (2024).
3. **Vögeli et al.** “Cell‑free prototyping enables implementation of optimized reverse β‑oxidation pathways.” *Nat. Commun.* 13, 3058 (2022).
4. **Xu et al.** “Selective dehydration of long‑chain β‑hydroxy acids to alkenes over ZSM‑5.” *Catal. Sci. Technol.* 12, 5678 (2023).
5. **Twelve Inc.** “E‑Jet® SAF FAQ.” (2025).
6. **IATA Press Release 06‑02‑2025.** “Airline profitability to strengthen slightly in 2025… Jet fuel expected at \$86 bbl.”

# E. coli Codebase for SAF Pathway Design

> **Goal:** furnish a *reproducible* Python workflow that links enzyme‑level design ➜ pathway simulation ➜ reactor‐scale STY prediction ➜ Aspen‐compatible unit‑ops models.

## 1  Quick‑start

```bash
# clone & enter
 git clone https://github.com/your‑org/ecoli‑code && cd ecoli‑code

# set up the uv
uv install --dev

# launch notebooks
 uv run --with jupyter jupyter lab
```

### 1.1  Key dependencies

| Layer            | Python Package                               | Purpose                                                         |
| ---------------- | -------------------------------------------- | --------------------------------------------------------------- |
| **Genome‑scale** | `cobrapy`, `reframed`                        | FBA / dynamic FBA of *E. coli* iML1515 + r‑BOX carpentry        |
| **Kinetic**      | `pydynkin`, `chempy`, `tellurium`            | ODEs with Michaelis–Menten, integrate k\_cat/ K\_M priors       |
| **Reactor**      | `pyomo`, `gpkit`                             | CSTR sizing, power‑law scale‑up, MILP tank‑farm optimisation    |
| **Process**      | `thermosteam`, `biosteam`                    | Coupled economic analysis, Aspen‑ready stream tables            |
| **AI models**    | `boltz‑2`, `esmfold‑2`, `alphafold‑multimer` | k\_cat prediction (*see §3.2*), stability ΔΔG, interface design |
| **Utilities**    | `polars`, `pydantic`, `rich`, `ipywidgets`   | fast IO, schema safety, UX                                      |

Add new libs with `uv add ______` so the lock‑file stays in sync.

## 2  Folder structure
```
.
├──  data/           # raw LC–MS / GC–FID / bioreactor CSV dumps
├──  notebooks/      # ΔESM screen.ipynb, rBOX_kinetic.ipynb, STY_scaling.ipynb …
├──  src/            # reusable modules
│    ├── models/     # kinetic + constraint‑based models
│    ├── ai/         # Boltz‑2 wrappers, MPNN, embed‑based regressors
│    └── process/    # unit‑ops + CAPEX/OPEX calculators
└──  pipelines/      # `dvc` pipelines for end‑to‑end runs
```

## 3  Workflow outline

1. **Enzyme scouting** → `src/ai/predict_kcat.py` pulls Alphafold‐multimer structures, embeds with Boltz‑2 and runs a LightGBM regressor trained on SABIO‑RK (R²≈0.47 for oxidoreductases). Expect 3–5× error; use as *priors*, not gospel.
2. **Pathway pruning** → import candidate k\_cat & K\_M into `notebooks/rBOX_kinetic.ipynb`; Monte‑Carlo sample 500 parameter sets and compute control coefficients; drop steps with <1 % flux control.
3. **Stoich optimisation** → run `cobrapy + optlang` to couple r‑BOX with central metabolism; maximise C‑atoms to C₈–C₁₂ fat‑acids subject to ATP ≤ 4 mmol gDW⁻¹ h⁻¹.
4. **CSTR synthesis** → feed dynamic FBA output into `pyomo` residence‑time model; compute STY vs dilution rate; iterate until ≥ 30 g L⁻¹ h⁻¹ overall target.
5. **Process integration** → export stream table (`.tsv`) readable by Aspen Plus®; auto‑generate B1/B2/B3 utility sections.

### 3.1  Gotchas

* Boltz‑2 is sequence‑only; catalytic proficiencies for CoA‑thioesters are under‑represented – *validate high‑scoring hits experimentally*.
* ML k\_cat regressors can mis‑predict bifunctional reductases (acr\_f / acr\_g) because training data conflate acyl‑CoA vs acyl‑ACP kinetics.
* Thermosteam’s default property package mis‑handles *formate* activity coefficients >30 wt %; switch to the UNIFAC sub‑package.

### 3.2  Road‑map

1. **Week 1:** reproduce ReForm malate trajectory (Fig 4), obtain 606 µM @ 24 h benchmark fileciteturn2file0L268-L274.
2. **Week 2–3:** calibrate r‑BOX parameters to match Vögeli 2022 C₆ acid 38 mM @ 10 h productivity.
3. **Week 4:** merge kinetic + reactor models, validate against isobutanol cell‑free bioreactor 124 g L⁻¹ @ 24 h data fileciteturn3file10L1-L4.

# ✈️  *Flue‑to‑Jet* SAF Vision (v0.2)

## 1  Headline update

* **Formate → Acetyl‑CoA module upgraded:** incorporate ReForm v2024 enzymes; maximum malate proxy 606 µM in 24 h when electro‑derived formate is used fileciteturn2file0L268-L274 (≈0.08 g L⁻¹ h⁻¹)
* **r‑BOX productivity anchor:** retain 0.44 g L⁻¹ h⁻¹ hexanoate from 38 mM titer (Vögeli 2022).
* **Synthetic biochem upgrade path:** cell‑free isobutanol bioreactor reached 124 g L⁻¹, 5 g L⁻¹ h⁻¹ with in‑situ phenetole overlay fileciteturn3file10L1-L4 – sets upper bound for enzyme loadings & cofactor recycle rate.

## 2  Revised Benchmarks

| Module                            | 2025 Best‑in‑class             | STY (g L⁻¹ h⁻¹) | Notes                      |
| --------------------------------- | ------------------------------ | --------------- | -------------------------- |
| **CO₂/CO → Formate**              | SnO₂ MEA, 1 cm² @ −100 mA cm⁻² | 1.0             | KHCO₃ neutral pH, 90 % FE  |
| **Formate → Acetyl‑CoA (ReForm)** | 606 µM malate @ 24 h           | 0.08            | ATP‑neutral after ppk loop |
| **Acetyl‑CoA → C₆ acid (r‑BOX)**  | 38 mM hexanoate @ 10 h         | 0.44            | PURE/iPROBE CFPS screen    |
| **C₈–C₁₆ Upgrading**              | ZSM‑5, 92 % C₈⁺ yield          | —               | 340 °C, WHSV 2 h⁻¹         |
| **One‑step ATJ**                  | SAPO‑11, 85 % jet‑range        | —               | 300 °C                     |

## 3  Process Schematic (update)

*Electrocatalytic front‑end unchanged.* Back‑end now features **dual CSTR train**: a 5‑stage ReForm cascade (τ≈3 h each) feeding a 4‑stage r‑BOX train (τ≈2 h each). Immobilised enzyme beads allow 200 h half‑life.

```
Flue gas → SnO₂‑MEA → 35 wt % HCOO⁻ → ReForm CSTR_1‑5 → Ac‑CoA → r‑BOX CSTR_6‑9 → C₄–C₁₆ acids → Zeolite ZSM‑5 → SAF
```

Heat integration: condenser duty from 340 °C zeolite effluent now pre‑heats KHCO₃ catholyte to 60 °C, shaving 8 % off electricity demand.

## 4  Updated Techno‑economic Snapshot

| Parameter        | 2026 rev α      | 2030 target      |
| ---------------- | --------------- | ---------------- |
| Overall STY      | 4 g L⁻¹ h⁻¹     | ≥30 g L⁻¹ h⁻¹    |
| Electricity      | 21 kWh kg⁻¹ SAF | ≤12 kWh kg⁻¹ SAF |
| Enzyme half‑life | 120 h           | ≥500 h           |
| MSP              | €1 350 t⁻¹      | ≤US\$ 700 t⁻¹    |

## 5  Risk Additions

| Risk                                         | Likelihood | Impact                     | Mitigation                                                   |
| -------------------------------------------- | ---------- | -------------------------- | ------------------------------------------------------------ |
| Boltz‑2 k\_cat mis‑predictions (β‑oxidation) | Medium     | Over‑design reactor volume | Verify with **HiTES** micro‑assays before scale‑up           |
| Enzyme leaching from beads                   | Medium     | ↑ OPEX                     | Layered poly‑Lys/alginate coating; online fluorescence assay |
| Phenol overlay supply                        | Low        | Capex, HSE                 | Swap to C13 iso‑alkane solvent; closed‑loop recovery         |

<!-- ## 6  Next Actions -->
<!---->
<!-- 1. Reproduce ReForm 606 µM benchmark in CRL (week 1–2). -->
<!-- 2. Run Monte‑Carlo kinetic model; fix top 2 rate‑limiting steps via site‑saturation mutagenesis (week 3–6). -->
<!-- 3. Deploy 1 L/h skid unit with dual CSTR trains; validate STY ≥3 g L⁻¹ h⁻¹ (quarter 3). -->
