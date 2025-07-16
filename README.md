# ecoli-code

## Run Jupyter Notebook

```sh
uv run --with jupyter jupyter lab
```

> NOTE: This repo uses **uv**. Use `uv run python` instead of `python` to run Python scripts, and `uv add` instead of `pip install` when adding new packages.

# Project Vision: Flue‑to‑Jet Sustainable Aviation Fuel (SAF)

## 1  Purpose

Develop a modular, electricity‑driven platform that converts **CO₂/CO‑rich flue gas** into drop‑in SAF at **≤ US \$ 700 t⁻¹** while achieving an overall **space‑time yield (STY) ≥ 30 g L⁻¹ h⁻¹**.

## 2  Process Architecture

```mermaid
flowchart LR
    A[Flue gas (CO₂ + CO)] -->|Gas capture & drying| B(Electrocatalytic<br>formate reactor)
    B -->|Liquid HCOO⁻/HCOOH| C(Cell‑free<br>Formate→Acetyl‑CoA)
    C -->|Acetyl‑CoA pool| D(Cell‑free<br>reverse β‑oxidation)
    D -->|C₄–C₁₆ acyl‑CoA / acids| E{Chain‑length<br>decision}
    E -- C₈–C₁₆ --> F(Zeolite ZSM‑5<br>dehydration / oligomerisation)
    E -- C₄–C₈ --> G(Single‑step ATJ‑type<br>oligomerisation)
    F & G --> H(Hydroprocessing & distillation)
    H --> I(SAF blend stock – ASTM D1655/D7566)
```

* **Distributed front‑end (A → B):** skid‑mounted gas‑diffusion MEA stacks at point sources (cement, steel, refinery). Formate solution (≈ 35 wt %) transported to the biocatalysis hub.
* **Central back‑end (C → I):** nitrogen‑blanketed continuous stirred‑tank reactors (CSTRs) running PURE/iPROBE cell‑free systems at 25–35 °C, followed by fixed‑bed solid‑acid upgrading.

## 3  Scientific Benchmarks

| Module                        | Technology                             | 2025 best‑in‑class result             | STY (g L⁻¹ h⁻¹) | Comment                          |
| ----------------------------- | -------------------------------------- | ------------------------------------- | --------------- | -------------------------------- |
| CO₂/CO → Formate              | Rh‑doped In₂O₃ gas‑diffusion MEA       | 1.2 A cm⁻², 90 % FE, 15 mmol cm⁻² h⁻¹ | 1.0             | Stable > 100 h \[1]              |
| Formate → Acetyl‑CoA (ReForm) | 9‑enzyme synthetic pathway (cell‑free) | 606 µM malate proxy @ 24 h            | 0.08            | ATP‑neutral via PPK loop \[2]    |
| Acetyl‑CoA → C₆ acids (r‑BOX) | In‑vitro r‑BOX (PURE/iPROBE)           | 38 mM hexanoate @ 10 h                | 0.44            | Chain length tunable C₄–C₁₆ \[3] |
| C₈–C₁₆ upgrading              | ZSM‑5 dehydration/oligomerisation      | 92 % C₈⁺ single‑pass @ 340 °C         | —               | WHSV 2 h⁻¹, 2 % H₂ co‑feed \[4]  |
| One‑step ATJ (C₄–C₈)          | SAPO‑11 solid acid                     | 80–90 % jet‑range @ 280–320 °C        | —               | Basis of Twelve E‑Jet® \[5]      |

### Key Enabling Principles

1. **Electro‑enzymatic cofactor recycling** (NADH, ATP) minimises OPEX.
2. **Enzyme immobilisation** on conductive supports extends half‑life (> 200 h).
3. **Heat integration:** zeolite reactor exhaust (340 °C) pre‑heats MEA catholyte.
4. **Distributed capture:** limits CO₂ transport and leverages low‑cost renewable power.

## 4  Techno‑Economic Snapshot

| Parameter               | 2026 pilot (100 L h⁻¹) | 2030 target       |
| ----------------------- | ---------------------- | ----------------- |
| Overall STY (CO₂ → SAF) | 4 g L⁻¹ h⁻¹            | ≥ 30 g L⁻¹ h⁻¹    |
| Electricity demand      | 21 kWh kg⁻¹ SAF        | ≤ 12 kWh kg⁻¹ SAF |
| Enzyme half‑life        | 120 h                  | ≥ 500 h           |
| Minimum selling price   | €1 350 t⁻¹             | ≤ US \$ 700 t⁻¹   |

Dominant cost drivers are renewable electricity (≈ 55 %), capital depreciation (≈ 25 %), and enzymes (≈ 10 %). Meeting the price target requires PV electricity ≤ 2 ¢ kWh⁻¹ (Chile, MENA, India) and long‑lived enzymes.

## 5  Integrated Development Roadmap (2025‑2030)

| Phase                      | Scale & Timing                           | Critical Deliverables                                                                                                                      |
| -------------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| \*\*Bench (α)\*\*Weeks 1–4 | 5–50 mL batch reactions                  | Reproduce ReForm malate 606 µM @ 24 h; calibrate r‑BOX hexanoate 38 mM @ 10 h; build kinetic model with CatPred priors; validate via LC‑MS |
| \*\*Flow (β)\*\*Months 2–4 | 1 L h⁻¹ skid, enzyme‑immobilised columns | Continuous formate→Ac‑CoA (τ≈3 h) and r‑BOX (τ≈2 h) CSTR trains; inline NADH electro‑recycling; achieve integrated STY ≥ 4 g L⁻¹ h⁻¹       |
| \*\*Pilot (γ)\*\*Year 2    | 100 L h⁻¹ integrated plant               | End‑to‑end SAF conforming to ASTM D7566 Annex A2; overall STY ≥ 10 g L⁻¹ h⁻¹; enzyme half‑life ≥ 120 h                                     |
| \*\*Demo (δ)\*\*Year 5     | 10 m³ h⁻¹ modular unit                   | Dual CSTR trains with immobilised beads (t₁⁄₂ ≥ 500 h); zeolite upgrading; MSP ≤ US \$ 700 t⁻¹ at electricity ≤ 12 kWh kg⁻¹                |

## 6  Risk Register

| Risk                                        | Likelihood | Impact             | Mitigation                                             |
| ------------------------------------------- | ---------- | ------------------ | ------------------------------------------------------ |
| Enzyme thermal drift at 30 °C               | Medium     | Lower yield        | Directed evolution; immobilisation                     |
| MEA flooding above 3 A cm⁻²                 | Medium     | Downtime           | PTFE‑rich foils; ΔP control                            |
| Zeolite coking                              | High       | Selectivity loss   | 500 °C steam‑air regeneration every 24 h               |
| Boltz‑2 k\_cat mis‑prediction (β‑oxidation) | Medium     | Over‑sized reactor | Verify hits with HiTES micro‑assays                    |
| Enzyme bead leaching                        | Medium     | OPEX ↑             | Poly‑Lys/alginate coatings; online fluorescence        |
| Phenol overlay supply                       | Low        | CAPEX / HSE        | Switch to C13 iso‑alkane solvent; closed‑loop recovery |
| Supply of high‑purity KHCO₃                 | Low        | OPEX ↑             | On‑site electrodialytic regeneration                   |

## 7  References

1. Li et al. “Ampere‑level co‑electrosynthesis of formate from CO₂.” *Nat. Commun.* 16, 4850 (2025).
2. Landwehr et al. “A synthetic cell‑free pathway for biocatalytic upgrading of one‑carbon substrates into acetyl‑CoA.” *bioRxiv* (2024).
3. Vögeli et al. “Cell‑free prototyping enables implementation of optimized reverse β‑oxidation pathways.” *Nat. Commun.* 13, 3058 (2022).
4. Xu et al. “Selective dehydration of long‑chain β‑hydroxy acids to alkenes over ZSM‑5.” *Catal. Sci. Technol.* 12, 5678 (2023).
5. Twelve Inc. “E‑Jet® SAF FAQ.” (2025).
6. IATA Press Release 06‑02‑2025. “Airline profitability to strengthen slightly in 2025… Jet fuel expected at \$86 bbl.”

---

# E. coli Codebase for SAF Pathway Design

## 1  Quick‑Start

```bash
# Clone and enter
git clone https://github.com/your‑org/ecoli‑code && cd ecoli‑code

# Set up environment
uv install --dev

# Launch notebooks
uv run --with jupyter jupyter lab
```

## 2  Key Dependencies

| Layer        | Packages                                     | Purpose                                                  |
| ------------ | -------------------------------------------- | -------------------------------------------------------- |
| Genome‑scale | `cobrapy`, `reframed`                        | FBA / dynamic FBA of *E. coli* iML1515 + r‑BOX           |
| Kinetic      | `pydynkin`, `chempy`, `tellurium`            | ODEs with Michaelis–Menten; integrate k\_cat/K\_M priors |
| Reactor      | `pyomo`, `gpkit`                             | CSTR sizing; MILP tank‑farm optimisation                 |
| Process      | `thermosteam`, `biosteam`                    | Economic analysis; Aspen‑ready stream tables             |
| AI models    | `boltz‑2`, `esmfold‑2`, `alphafold‑multimer` | k\_cat prediction, stability ΔΔG, interface design       |
| Utilities    | `polars`, `pydantic`, `rich`, `ipywidgets`   | Fast IO, schema validation, UX                           |

Add new libraries with `uv add <pkg>` to maintain lock‑file integrity.

## 3  Repository Structure

```
.
├── data/            # raw LC‑MS / GC‑FID / bioreactor CSV dumps
├── notebooks/       # ΔESM_screen.ipynb, rBOX_kinetic.ipynb, STY_scaling.ipynb …
├── src/
│   ├── models/      # kinetic + constraint‑based models
│   ├── ai/          # Boltz‑2 wrappers, MPNN, embed‑regressors
│   └── process/     # unit‑ops + CAPEX/OPEX calculators
└── pipelines/       # dvc pipelines for end‑to‑end runs
```

## 4  Workflow Outline

1. **Enzyme scouting** – `src/ai/predict_kcat.py` embeds Alphafold‑multimer structures with Boltz‑2 and applies a LightGBM regressor trained on SABIO‑RK (R² ≈ 0.47). Use predictions as *priors* only.
2. **Pathway pruning** – Import k\_cat/K\_M priors into `notebooks/rBOX_kinetic.ipynb`; Monte‑Carlo sample 500 parameter sets; drop steps with < 1 % flux control.
3. **Stoichiometric optimisation** – Use `cobrapy + optlang` to maximise carbon flux to C₈–C₁₂ acids at ATP ≤ 4 mmol gDW⁻¹ h⁻¹.
4. **CSTR synthesis** – Feed dynamic FBA results to `pyomo`; iterate residence time to meet plant‑level STY targets.
5. **Process integration** – Export stream tables to Aspen Plus® or Thermosteam for utilities and costing.

## 5  Common Gotchas

* Boltz‑2 is sequence‑only; CoA‑thioester kinetics are under‑represented—wet‑lab validation required.
* ML k\_cat regressors can mispredict bifunctional reductases (acr\_f / acr\_g); cross‑check with literature data.
* Thermosteam’s default property package mishandles formate activity > 30 wt %; switch to UNIFAC.
