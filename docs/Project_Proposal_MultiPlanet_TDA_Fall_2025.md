# A Multi-Planet Topological Framework for Landscape Structural Analysis: From Appalachian Folds to Lunar Highlands

**Author:** Michael Kerr\
**Date:** October 23, 2025

---

## Executive Summary

This research proposal introduces the first comparative planetary study using Topological Data Analysis (TDA) to decode universal structural controls on landscape organization. By computing directional persistent homology across Earth's Appalachian provinces, lunar mare and highland terrains, and diverse Martian landscapes, this work addresses a fundamental question in geomorphology: **Do topological signatures reveal universal structural controls that transcend planetary context, or are landscape patterns fundamentally planet-specific?**

The project creates a novel framework for terrain classification that works across radically different geological contexts—from tectonically folded mountains to impact-cratered plains to volcanic edifices—using only topological invariants derived from digital elevation models. Validation through multi-scale roughness prediction and crater retention modeling demonstrates that topological features encode real, predictive information about landscape organization rather than merely describing terrain.

**Innovation:** First application of directional persistent homology to multi-planet structural geomorphology, enabling process-independent landscape classification.

**Impact:** Establishes topology as a universal language for describing landscape structure across planetary bodies, with direct applications to landing site characterization, analog terrain identification, and understanding fundamental controls on surface evolution.

**Strategic Positioning:** Bridges computational topology, structural geology, and planetary science while directly addressing NASA priorities in Mars/Moon exploration and surface characterization.

---

## 1. Introduction & Motivation

### 1.1 The Fundamental Question

Landscapes across the solar system exhibit stunning visual diversity—from Earth's parallel Appalachian ridges to the radial patterns of lunar crater ejecta to the tectonic scarps of Valles Marineris on Mars. Yet beneath this apparent diversity lies a deeper question: **Do landscapes with fundamentally different formative processes (fluvial erosion, impact cratering, volcanic construction, tectonic deformation) share common structural principles that can be quantified mathematically?**

Traditional geomorphometry has focused on planet-specific metrics tied to particular processes (e.g., drainage density requires flowing water, crater size-frequency distributions require impacts). This approach cannot identify structural analogs across bodies or extract universal organizing principles. We need a **process-independent framework** for quantifying landscape structure.

### 1.2 Topological Data Analysis: A Universal Language for Landscapes

**Topological Data Analysis (TDA)** offers exactly this: a mathematical framework for quantifying intrinsic shape properties that persist across scales and are invariant to the specific physical processes that created them. Through persistent homology, TDA tracks the birth and death of topological features (connected components, loops, voids) across a filtration of elevation data, producing persistence diagrams that encode:

- **Scale-invariant structure:** Features detected across all scales simultaneously
- **Process independence:** Same analysis works on any elevation field regardless of origin
- **Directional information:** Anisotropic persistence captures structural fabric orientation
- **Noise robustness:** Low-persistence features naturally filtered as noise
- **Mathematical rigor:** Stable topological invariants with proven theoretical properties

**Critical innovation:** By extending persistent homology to directional filtrations, we can recover structural fabric orientations (fold axes, fault strikes, crater radial patterns) directly from terrain, without requiring geological maps or a priori process knowledge.

### 1.3 Why This Matters Now

Recent developments make this research both feasible and urgent:
1.  **High-resolution planetary DEMs:** Lunar Reconnaissance Orbiter (5-20m), Mars HiRISE (1m), and CTX (6m) provide unprecedented terrain data
2.  **Computational advances:** Modern TDA libraries enable rapid computation on large datasets
3.  **Exploration priorities:** NASA's Artemis lunar program and Mars Sample Return require robust terrain characterization methods
4.  **Theoretical gap:** Despite TDA's success in landslide detection (79-94% accuracy) and urban form analysis, **no study has applied it to comparative planetary geomorphology**

### 1.4 Research Significance

This project represents a paradigm shift from **process-specific terrain analysis** to **structure-based universal classification**. Success would mean:

- **Scientific:** Understanding which aspects of landscape organization are universal versus planet-specific
- **Methodological:** Establishing TDA as a standard tool for planetary terrain analysis
- **Applied:** Enabling analog site identification for mission planning (e.g., "which Mars locations are topologically similar to lunar landing sites?")
- **Philosophical:** Revealing fundamental principles of landscape organization independent of formative processes

### 1.5 Advantages Over Traditional Geomorphometry

This topological approach is proposed as a necessary evolution beyond traditional geomorphometric techniques. Established methods, such as 2D Fast Fourier Transforms (FFTs) or wavelet analysis, are powerful for identifying **globally dominant, periodic** fabrics (e.g., linear dune fields).

However, TDA is uniquely suited to overcome their key limitations:
1.  **Multi-Scale & Hierarchical Structure:** FFTs identify dominant scales, but TDA's persistence diagrams *simultaneously characterize all scales*. This allows TDA to understand the *relationship* between 5km-scale folds and the 500m-scale ridges on their flanks, rather than averaging them.
2.  **Local & Aperiodic Features:** TDA excels at identifying *local, significant* features that spectral methods miss. A single, large impact crater (an $H_1$ loop) or a deep, isolated tectonic graben (an $H_0$ basin) is a distinct topological feature, not just noise in a global average.
3.  **Feature Distinction:** TDA separates features by their topology. For example, it naturally distinguishes between $H_0$ features (basins, pits, valleys) and $H_1$ features (peaks, ridges, crater rims), enabling a far richer classification than methods that only measure surface orientation or roughness.

---

## 2. Core Research Questions

This research is organized around four fundamental questions that build progressively from discrimination to prediction to universality:

### RQ1: Landscape Discrimination Across Structural Contexts

**Do landscapes with distinct structural geology and formative processes exhibit unique multiscale topological signatures?**
- **Earth component:** Can TDA discriminate between Appalachian provinces with different structural controls (folded ridges, plateau dissection, coastal plain)?
- **Lunar component:** Can TDA distinguish mare basalts from highland terrain and crater ejecta patterns?
- **Mars component:** Can TDA separate volcanic flanks from tectonic valleys from fluvial dissection?
- **Cross-planet test:** Do topologically similar terrains cluster together even across planetary bodies?

### RQ2: Structural Fabric Recovery from Terrain Alone

**Can directional topological analysis reveal structural fabric orientation without geological maps?**
- **Earth test:** Recover fold axis orientations in Valley & Ridge Province
- **Lunar test:** Detect radial patterns in crater ejecta blankets
- **Mars test:** Identify fault strike orientations in Valles Marineris
- **Validation:** Angular correlation with known structural orientations from independent sources

### RQ3: Multi-Scale Predictive Power

**Do topological features computed at one scale predict terrain properties at other scales?**
- **Primary validation:** Multi-scale roughness prediction across all three bodies
- **Secondary validation:** Crater retention patterns on Moon and Mars highlands
- **Hypothesis:** If topological features truly capture hierarchical landscape organization, they should enable cross-scale prediction
- **Interpretation:** Good prediction = topology encodes fundamental structural information, not just scale-specific artifacts

### RQ4: Universal versus Planet-Specific Controls

**Do topological landscape signatures generalize across planetary bodies, enabling process-independent classification?**
- **Analog identification:** Which Mars terrains are topologically most similar to specific Earth provinces or lunar regions?
- **Process generalization:** Do similar topological signatures indicate similar structural controls regardless of formation mechanism?
- **Classification test:** Can we build a universal terrain classifier that works across Earth, Moon, and Mars?

---

## 3. Hypotheses

### H₁: Landscape Discrimination Hypothesis

**H₁A (Alternative):** Topological signatures successfully discriminate between structural/process domains within and across planets. Specifically:
- MANOVA on persistence landscape features shows significant differences between provinces (Earth), terrain types (Moon), and site categories (Mars)
- Random Forest classification achieves >80% accuracy in discriminating landscape types
- Non-parametric permutation tests on persistence diagram distances show significant separation

**H₁₀ (Null):** Topological signatures do not reliably discriminate between different landscape types ($\alpha$ = 0.05)

**Prediction:** Earth provinces should show strongest discrimination (most structural variation), followed by Mars (mixed processes), then Moon (impact-dominated with less diversity)

---

### H₂: Structural Fabric Recovery Hypothesis

**H₂A (Alternative):** Directional topological features correlate with known structural orientations:
- **Earth:** Maximum persistence direction correlates with fold axes (Valley & Ridge)
- **Moon:** Radial anisotropy aligns with crater ejecta patterns
- **Mars:** Persistence anisotropy aligns with fault strikes (Valles Marineris)
- Statistical test: Angular correlation coefficient $r > 0.7$, $p < 0.01$

**H₂₀ (Null):** Directional topological features show no significant correlation with structural orientations

**Prediction:** Strongest correlations in highly anisotropic terrains (Valley & Ridge, crater ejecta), weakest in isotropic terrains (Piedmont, mare plains, Karst)

---

### H₃: Multi-Scale Prediction Hypothesis

**H₃A (Alternative):** Topological features at scale A predict roughness/complexity at scales B, C, D, demonstrating cross-scale predictive power:
- Topological features improve R² by $\geq$0.15 over baseline models using only single-scale roughness
- Cross-validated RMSE significantly reduced compared to null models (paired t-test, $p < 0.01$)
- Crater retention patterns (Moon/Mars) predicted from topological context with R² > 0.50

**H₃₀ (Null):** Topological features provide no significant improvement in cross-scale prediction beyond baseline models

**Prediction:** Strongest predictive power on bodies with hierarchical structure (Earth, Mars highlands), weaker on homogeneous surfaces (lunar maria)

---

### H₄: Process Universality Hypothesis

**H₄A (Alternative):** Similar topological signatures indicate similar structural controls regardless of planet or formative process:
- Cross-planet clustering analysis (using *harmonized 30m data*) reveals topological analogs (e.g., Mars valleys cluster with Earth ridged terrain)
- Euclidean distance in topological feature space correlates with structural similarity
- Terrain types from different planets with similar structural properties (anisotropy, relief distribution) show convergent topological signatures

**H₄₀ (Null):** Topological signatures are fundamentally planet-specific or are artifacts of DEM resolution, and do not reveal universal structural principles

**Prediction:** Structural analogs exist across planets—folded/ridged terrains cluster together regardless of whether formed by tectonics or differential erosion

---

## 4. Study Areas & Design

### 4.1 Three-Planet Comparative Design

This research employs a strategic three-body design spanning:
- **Process diversity:** Fluvial (Earth), impact (Moon), mixed (Mars)
- **Atmosphere diversity:** Dense (Earth), none (Moon), thin (Mars)
- **Tectonic diversity:** Recent (Earth), ancient (Moon/Mars)
- **Data quality:** Excellent DEM coverage on all three bodies

**Critical advantage:** Three bodies provide sufficient diversity to test universality while remaining computationally feasible in 15 weeks.

### 4.2 Earth: Appalachian Physiographic Provinces (6 Regions)

**Purpose:** Baseline structural diversity from well-understood geology, including positive and negative controls for validation.

#### Province 1: Blue Ridge
- **Structure:** High-relief folded metamorphic mountains
- **Topological prediction:** High $H_1$ persistence (prominent peaks), high directional anisotropy along Appalachian trend
- **Data:** USGS 3DEP Lidar DEM (30m)

#### Province 2: Valley and Ridge
- **Structure:** Parallel linear ridges from folded sedimentary rocks
- **Topological prediction:** Strongest directional signal (NE-SW fold axes), alternating high/low persistence
- **Test case for:** H₂ (Structural Fabric Recovery)
- **Data:** USGS 3DEP Lidar DEM (30m)

#### Province 3: Piedmont
- **Structure:** Rolling uplands, deeply weathered crystalline basement
- **Topological prediction:** Low overall persistence, weak directional signal, monadnock features as isolated $H_1$ peaks
- **Data:** USGS 3DEP Lidar DEM (30m)

#### Province 4: Coastal Plain
- **Structure:** Nearly flat sedimentary deposits
- **Topological prediction:** Very low persistence, minimal topological structure
- **Analog to:** Lunar maria, Mars northern plains
- **Data:** USGS 3DEP Lidar DEM (30m)

#### Province 5: Appalachian Plateau
- **Structure:** Dissected plateau with incised valleys
- **Topological prediction:** High $H_0$ persistence (deep basins), moderate $H_1$ (plateau remnants)
- **Data:** USGS 3DEP Lidar DEM (30m)

#### Province 6: Karst Landscape (Negative Control)
- **Purpose:** Provide an isotropic, complex control site.
- **Structure:** Sinkhole-dominated terrain (e.g., Kentucky, Florida)
- **Topological prediction:** High $H_0$ *count* (many basins), but a flat/noisy directional persistence profile (Anisotropy Index near 0).
- **Test case for:** H₂ (proves method doesn't "find" fabric in random noise)
- **Data:** USGS 3DEP Lidar DEM (30m)

**Earth analysis focus:** Structural fabric recovery in Valley & Ridge, cross-province discrimination, multi-scale roughness prediction, validation of DPH method against negative control.

---

### 4.3 Moon: Mare and Highland Contrast (10-15 Sites)

**Purpose:** Impact-dominated landscape with minimal erosion

#### Terrain Type 1: Mare Plains (Positive Control)
- **Structure:** Smooth volcanic basalt plains, minimal relief
- **Site examples:** Mare Tranquillitatis, Mare Imbrium
- **Topological prediction:** Low persistence. These two sites should cluster as nearest-neighbors in H₄, proving the method robustly identifies *the same* terrain type.
- **Analog to:** Earth Coastal Plain
- **Data:** LRO LOLA 5–20m/pixel

#### Terrain Type 2: Highland Terrain
- **Structure:** Heavily cratered, ancient surface
- **Site example:** Southern highlands
- **Topological prediction:** High persistence at multiple scales, crater rims as $H_1$ loops
- **Data:** LRO LOLA 5–20m/pixel

#### Terrain Type 3: Crater Ejecta Blankets
- **Structure:** Radial patterns surrounding fresh craters
- **Site example:** Tycho, Copernicus ejecta
- **Topological prediction:** Strong radial anisotropy detectable via directional persistence
- **Test case for:** H₂ (Structural fabric recovery)
- **Data:** LRO LOLA 5–20m/pixel

#### Terrain Type 4: Impact Basin Interiors
- **Structure:** Complex central peaks, terraced walls
- **Site example:** Orientale, Schrödinger basins
- **Topological prediction:** Concentric patterns, high $H_1$ persistence at peak
- **Data:** LRO LOLA 5–20m/pixel

**Lunar analysis focus:** Mare vs. highland discrimination, crater ejecta radial pattern detection, crater retention modeling (H₃).

---

### 4.4 Mars: Maximum Geological Diversity (15 Sites)

**Purpose:** Test topological signatures across volcanic, tectonic, fluvial, and impact processes

#### Site Category 1: Valles Marineris (Tectonic)
- **Structure:** Massive tectonic canyon system with fault-bounded walls
- **Topological prediction:** Linear $H_0$ features (canyon), directional anisotropy parallel to faults
- **Analog to:** Earth Valley & Ridge (linear structural control)
- **Test case for:** H₂ and Resolution Sensitivity
- **Data:** HiRISE DTM 1m + CTX 6m

#### Site Category 2: Olympus Mons Flanks (Volcanic)
- **Structure:** Shield volcano with gentle slopes, flow features
- **Topological prediction:** Radial anisotropy, moderate persistence
- **Data:** HiRISE 1m + CTX 6m

#### Site Category 3: Northern Plains (Low Relief)
- **Structure:** Smooth lowlands with subtle features
- **Topological prediction:** Low persistence, similar to lunar maria
- **Analog to:** Earth Coastal Plain, lunar maria
- **Data:** CTX 6m

#### Site Category 4: Ancient Highlands (Cratered/Dissected)
- **Structure:** Old cratered surface with valley networks
- **Topological prediction:** High $H_0$ (valleys), moderate $H_1$ (interfluve remnants)
- **Analog to:** Earth Plateau (dissection), lunar highlands (cratering)
- **Data:** HiRISE 1m + CTX 6m

#### Site Category 5: Crater Ejecta (Impact)
- **Structure:** Radial patterns around fresh craters
- **Topological prediction:** Radial anisotropy like lunar ejecta
- **Data:** HiRISE 1m

**Mars analysis focus:** Maximum diversity for universality testing (H₄), structural fabric in Valles Marineris (H₂), cross-planet analog identification.

---

## 5. Methodology

### 5.1 Data Acquisition & Preprocessing

#### Earth Data (USGS 3DEP)
- **Source:** USGS 3D Elevation Program (3DEP) via The National Map.
- **Resolution:** 1m, ~10m (1/3 arc-second), and ~30m (1 arc-second) seamless DEMs.
- **Processing:** Reproject to equal-area (Albers), tile into 10×10 km analysis windows per province
- **Methodological Note:** The 30m and 10m datasets will be used for the H₄ (Universality) comparison against harmonized planetary data. The 1m dataset will provide a powerful "ground truth" for the H₃ (Multi-Scale Prediction) hypothesis, allowing for validation of TDA features across scales (e.g., using 1m data to predict 10m roughness).

#### Lunar Data (LRO LOLA)
- **Source:** [https://ode.rsl.wustl.edu/moon/](https://ode.rsl.wustl.edu/moon/)
- **Resolution:** 5–20m/pixel
- **Processing:** Select sites, create 5×5 km analysis windows
- **Sample size:** ~15 sites, 3–5 windows per site (~50 total windows)

#### Mars Data (HiRISE + CTX)
- **Sources:**
  - HiRISE DTMs: [https://www.uahirise.org/dtm/](https://www.uahirise.org/dtm/) (1m resolution)
  - CTX: [https://astrogeology.usgs.gov/search/map/Mars](https://astrogeology.usgs.gov/search/map/Mars) (6m resolution)
- **Processing:** Strategic site selection, 5–10 km windows
- **Sample size:** ~15 sites, mix of HiRISE and CTX

#### Crater Catalogs (for validation)
- **Lunar:** Robbins et al. (2018)
- **Mars:** Robbins & Hynek (2012)

### 5.1.1 Data Harmonization & Resolution Sensitivity Analysis

This step is **critical** to address the Modifiable Areal Unit Problem (MAUP) and ensure valid cross-planetary comparisons.

**1. Harmonization for Universality (H₄):**
- **Problem:** Comparing a 1m HiRISE DEM to a 30m USGS 3DEP Lidar DEM classifies resolution, not geology.
- **Solution:** All DEMs used for the cross-planet clustering analysis (H₄) will be **resampled to a common 30m resolution** using an area-weighted average. This provides a true "apples-to-apples" comparison of large-scale structure.

**2. Resolution Sensitivity Test (H₂ & H₃ Validation):**
- **Problem:** Are the TDA signatures stable, or just artifacts of a specific resolution?
- **Solution:** For at least one Mars site (Valles Marineris), the TDA pipeline (H₂ fabric recovery, H₃ roughness prediction) will be run on **three separate datasets**:
    1.  The 1m HiRISE DTM (native)
    2.  The 6m CTX DTM (native)
    3.  The 6m CTX DTM resampled to 30m
- **Success Criterion:** The key structural signatures (e.g., *direction* of anisotropy, *relative shape* of persistence landscapes) must be stable across resolutions, demonstrating that our method measures fundamental geometry, not just data-scale artifacts.

---

### 5.2 Topological Data Analysis Pipeline

#### Step 1: Standard Persistent Homology
For each analysis window, compute:
- **Sublevel set persistence** (H₀: basins, H₁: peaks)
- **Superlevel set persistence** (inverse for ridge detection)
- **Generate persistence diagrams** showing (birth, death) pairs
- **Statistical summaries:** Mean, max, variance, quantiles (25th, 50th, 75th, 90th)
- **Persistence landscapes:** Functional representation for statistical analysis

#### Step 2: Directional Persistent Homology (Novel Component)
For structural fabric detection:
- **Method:** Divide 360° into N=16 directional bins. For each direction $\theta$, compute persistence using only elevation changes aligned with $\theta$.
- **Outputs:** Maximum persistence direction, Anisotropy index, Dominant direction distribution
- **Validation:** Compare max persistence direction to known fold axes (Earth), ejecta radii (Moon), fault strikes (Mars)

To bridge the gap between abstract math and physical science, we define the hypothesized geological meaning of our key TDA features.

**Table 5.1: Geological Interpretation of Key Topological Features**
| TDA Feature | Geological Interpretation (Hypothesized) | Example Landscape |
| :--- | :--- | :--- |
| **High $H_0$ Persistence** | A few, deep, and/or wide basins; high resistance to infilling. | Large impact craters, deep tectonic grabens. |
| **High $H_1$ Persistence** | A few, tall, and/or wide peaks; resistant to erosion. | Volcanic shields, central peaks, horsts. |
| **High $H_0$ *Count*** | Many small, shallow depressions; a "pockmarked" surface. | Young ejecta blanket, Karst terrain. |
| **High $H_1$ *Count*** | Many small, sharp peaks; a "jagged" or "hummocky" surface. | A'a lava flows, fresh impact-shattered terrain. |
| **High Anisotropy Index** | Strong, uniform structural control. | Folded mountains, fault blocks, linear dunes. |
| **Low Persistence (all)** | Low relief, featureless, homogenous surface. | Mare basalt plains, coastal plains. |

---

### 5.3 Validation Framework 1: Methodological Robustness (Cross-Scale Roughness Prediction)

**Goal:** Demonstrate that topological features encode predictive, hierarchical information about landscape organization, not just descriptive statistics. This is a **methodological** validation.

**Rationale:** If topological features at scale A truly capture fundamental structural organization, they should predict surface complexity at different scales B, C, D.

**Implementation:**
- **Predictor features:** TDA features (persistence stats, anisotropy, etc.)
- **Target variables:** Surface Roughness Index (SRI), Terrain Ruggedness Index (TRI), Profile Curvature, etc., computed at multiple scales (10m, 100m, 1km).
- **Regression approach:**
  - Baseline model: Predict scale B roughness from scale A roughness only
  - Enhanced model: Add topological features as predictors
- **Success criterion:** Topological features improve R² by $\geq$0.15 and significantly reduce RMSE ($p < 0.01$, paired t-test)

---

### 5.4 Validation Framework 2: Geological Process Validation (Crater Retention Modeling)

**Goal:** Demonstrate that TDA features correlate with tangible **geological processes** (erosion, deposition, infilling), not just abstract DEM properties. This is our **primary scientific** validation.

**Rationale:** Craters are time markers. Their preservation depends on erosion/deposition controlled by the surrounding topological context.

**Implementation:**
1.  **Extract crater density** from catalogs (Moon/Mars)
2.  **Compute topological context** for each terrain patch (using Table 5.1 definitions)
3.  **Regression model:**
    `Crater_Density ~ H₀_persistence + H₁_persistence + Anisotropy + Age_proxy`
4.  **Test hypothesis:**
    - High $H_1$ persistence (erosion-resistant peaks) $\rightarrow$ higher crater retention
    - High $H_0$ persistence (infilling basins) $\rightarrow$ lower crater density
- **Success criterion:** Topological features explain a significant portion of variance in crater retention (e.g., R² > 0.50 after accounting for age)

**Why this is powerful:** Shows topology predicts actual geological *evolution*, not just static terrain properties.

---

### 5.5 Statistical Analysis Framework

#### Analysis 1: Within-Planet Discrimination (H₁)
- **Method:** MANOVA (on persistence landscapes) and Random Forest classification
- **Success criterion:** MANOVA $p < 0.001$, classification accuracy >80%

#### Analysis 2: Structural Fabric Recovery (H₂)
- **Method:** Angular correlation ($r_{\text{angular}}$) between $\theta_{\text{TDA}}$ and $\theta_{\text{ref}}$
- **Success criterion:** $r_{\text{angular}}$ > 0.7 ($p < 0.01$) for anisotropic terrains; $r_{\text{angular}}$ ~ 0 for Karst control.

#### Analysis 3: Multi-Scale Prediction (H₃)
- **Method:** Nested model comparison (Likelihood Ratio Test, $\Delta$R², $\Delta$RMSE) using spatial cross-validation.
- **Success criterion:** $\Delta$R² $\geq$ 0.15, $\Delta$RMSE > 0 ($p < 0.01$)

#### Analysis 4: Cross-Planet Universality (H₄)
- **Method:** Hierarchical clustering on the **harmonized 30m dataset**.
- **Test:** Identify cross-planet analogs. Do Mare Imbrium/Tranquillitatis cluster? Do Valles Marineris/Valley & Ridge cluster?
- **Success criterion:** Identify meaningful cross-planet analogs that make geological sense and are robust (e.g., positive controls cluster together).

---

## 6. Timeline (15 Weeks)

### Weeks 1-2: Data Acquisition & Preprocessing ✓
- **Week 1:** Download FABDEM (6 provinces), LRO LOLA (15 sites)
- **Week 2:** Download HiRISE/CTX (15 sites), create standardized windows
- **Deliverable:** Preprocessed DEM library

### Week 3: Data Harmonization & TDA Pipeline
- **Week 3:**
  - Implement standard (Gudhi/Ripser) and directional persistence
  - **CRITICAL:** Implement data harmonization pipeline (resampling to 30m)
  - **CRITICAL:** Implement resolution sensitivity test (1m, 6m, 30m)
- **Deliverable:** Functional TDA pipeline with harmonization

### Weeks 4-5: Earth Structural Analysis
- **Week 4:** Compute TDA features for all 6 provinces. Directional analysis (H₂) on Valley & Ridge and Karst control.
- **Week 5:** Statistical discrimination (H₁) and multi-scale roughness (H₃)
- **Deliverable:** Complete Earth analysis with H₂ validation.

### Weeks 6-7: Lunar Analysis
- **Week 6:** Compute TDA features. Ejecta pattern detection (H₂).
- **Week 7:** Crater retention modeling (H₃ / *Primary Sci. Validation*)
- **Deliverable:** Complete lunar analysis with crater retention validation.

### Weeks 8-9: Mars Analysis
- **Week 8:** Compute TDA features. Valles Marineris fabric (H₂).
- **Week 9:** Crater retention (H₃).
- **Deliverable:** Complete Mars analysis.

### Weeks 10-11: Resolution Sensitivity & Validation
- **Week 10:** **Execute Resolution Sensitivity Test** on Valles Marineris data (1m, 6m, 30m).
- **Week 11:** Compile all roughness (H₃) and crater (H₃) validation results.
- **Deliverable:** Full validation suite, including resolution robustness check.

### Week 12-13: Synthesis & Cross-Planet Classification
- **Week 12:** Generate **harmonized 30m dataset** for all three planets.
- **Week 13:** Run H₄ clustering. Identify cross-planet analogs. Test positive controls (Mare sites).
- **Deliverable:** Cross-planet synthesis demonstrating universal principles.

### Weeks 14-15: Writing & Visualization
- **Week 14:** Draft manuscript. Create publication figures (feature maps, cluster dendrograms, resolution test plots).
- **Week 15:** Complete Discussion/Conclusions. Prepare presentation.
- **Final Deliverable:** Complete manuscript draft + presentation + documented code

---

## 7. Expected Results & Interpretation

### 7.1 Predicted Outcomes
- **H₁ (Discrimination):** Strong discrimination (>80% accuracy) within all bodies.
- **H₂ (Fabric):** Strong correlation ($r > 0.8$) in Valley & Ridge; ($r > 0.7$) in ejecta; **No correlation** ($r < 0.1$) in Karst terrain.
- **H₃ (Prediction):** TDA features significantly improve roughness prediction (Methodological Validation). TDA features (esp. $H_0$/$H_1$ persistence) significantly predict crater retention (Scientific Validation).
- **H₄ (Universality):** Meaningful analogs emerge (Valles Marineris $\leftrightarrow$ Valley & Ridge; Mare $\leftrightarrow$ Coastal Plain). Positive controls (Mare Imbrium/Tranquillitatis) cluster as nearest neighbors.

### 7.2 Alternative Scenarios
- **Scenario A: H₄ fails:** Universality is weak. *Interpretation:* Formation process matters more than structure. *Pivot:* Focus on TDA as a powerful *within-planet* classifier.
- **Scenario B: Resolution Test fails:** TDA features are not stable across scales. *Interpretation:* TDA is highly scale-dependent. *Pivot:* Abandon universality (H₄) and focus on *scale-specific* applications (e.g., "HiRISE-TDA for rover hazards"). **This is the biggest risk.**

### 7.3 Robustness Checks
- **1. Resolution Sensitivity (CRITICAL):** Explicitly test TDA stability at 1m, 6m, and 30m.
- **2. Window size sensitivity:** Test 5 km vs. 10 km vs. 20 km windows.
- **3. Parameter sensitivity:** Vary persistence threshold, directional bin count.
- **4. Spatial structure:** Test for spatial autocorrelation in residuals.

---

## 8. Innovation & Intellectual Merit

### 8.1 Methodological Innovations
1.  **First multi-planet application of TDA to geomorphology**
2.  **Directional persistent homology for structural geology**
3.  **Novel validation framework** distinguishing methodological (roughness) from geological (crater) validation.
4.  **Rigorous data harmonization** to solve MAUP and enable valid cross-planet comparison.

### 8.2 Scientific Contributions
1.  **Fundamental question:** Do universal structural principles govern landscape organization regardless of planet or process?
2.  **Geological interpretation of TDA:** Provides a "Rosetta Stone" (Table 5.1) for translating topological features into physical meaning.
3.  **Process-independent classification:** Delivers a terrain classification system that works on *any* body.

*... (Sections 8.3, 9, 10, 11, 12, 13, Appendices remain largely the same as original) ...*

### 8.3 Broader Impacts

**Space Exploration:**
- Direct relevance to Artemis lunar program (landing site selection)
- Mars Sample Return mission planning (terrain navigation hazards)
- Analog site identification for Earth-based mission training

**Methodological Influence:**
- Establishes TDA as standard tool in planetary geomorphology
- Provides template for future multi-planet comparative studies
- Software tools applicable to any planetary body with DEM data

**Interdisciplinary Bridge:**
- Connects pure mathematics (algebraic topology) to planetary science
- Demonstrates value of computation topology in Earth science
- Training model for mathematical geosciences

**Open Science:**
- All code released on GitHub with documentation
- Datasets publicly available (FABDEM, LRO, HiRISE)
- Reproducible workflow from raw DEMs to final results

---

## 9. Project Management & Feasibility

### 9.1 Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| DEM data quality issues | Medium | Medium | Use multiple data sources, quality filters, interpolation where needed |
| Computation time exceeds estimate | Low | Low | Optimize code, use parallel processing, reduce sample size if necessary |
| Weak cross-planet patterns | Medium | Low | Focus on within-planet success, alternative interpretation still valuable |
| Timeline overrun | Medium | Medium | Built-in flexibility (Mars sites can be reduced from 15 to 10 if needed) |
| Directional persistence algorithm bugs | Medium | Medium | Extensive testing in Weeks 3-4, fallback to standard persistence |

### 9.2 Resource Requirements

**Computational:**
- Standard laptop with 16GB RAM sufficient for DEM processing
- Python libraries: Gudhi, Ripser, scikit-learn, GDAL, NumPy, SciPy
- Storage: ~50GB for all DEM data and results
- No cluster computing required

**Data:**
- All datasets publicly available at no cost
- USGS 3DEP Lidar DEMs: Free download (via The National Map)
- LRO LOLA (Moon): NASA PDS, free access
- HiRISE/CTX (Mars): NASA PDS, free access
- Crater catalogs: USGS Astrogeology, free download

**Software:**
- All open-source (Python-based)
- No proprietary licenses required

**Time:**
- 15 weeks full-time (single investigator)
- Realistic given computational nature (no fieldwork, lab work, or external dependencies)

### 9.3 Contingency Plans

**If computation time becomes bottleneck:**
- Reduce sample size: 30 windows/province instead of 50 (still statistically adequate)
- Reduce Mars sites from 15 to 10 (maintain diversity)
- Parallelize TDA computation across windows (embarrassingly parallel)

**If directional persistence proves challenging:**
- Focus on standard persistence (discrimination still works)
- Manually extract structural orientations from DEMs for validation
- Collaborate with topologist for algorithm refinement (optional, not required)

**If cross-planet universality is weak:**
- Pivot focus to within-planet classification excellence
- Emphasize planet-specific applications (still novel and valuable)
- Reframe as "what makes each planet unique topologically?"

---

## 10. Publications & Dissemination

### 10.1 Target Journals

**Paper 1 (High-impact, short):** *Science* or *Nature Geoscience*
- Title: "Universal Topological Signatures Reveal Structural Controls Across Planetary Landscapes"
- Length: 4-6 pages
- Focus: Broad audience, emphasize universality and cross-planet analogs
- Timeline: Submit within 6 months of project completion

**Paper 2 (Methods focus):** *Earth Surface Processes and Landforms* or *Geomorphology*
- Title: "Directional Topological Data Analysis for Structural Fabric Recovery from Digital Elevation Models"
- Length: Full research article
- Focus: Deep dive on Earth structural geology, comparison with traditional geomorphometry
- Timeline: Submit within 8 months

**Paper 3 (Planetary focus):** *Journal of Geophysical Research: Planets* or *Icarus*
- Title: "Topological Classification of Lunar and Martian Terrains: Implications for Landing Site Selection and Analog Identification"
- Length: Full research article  
- Focus: Detailed Moon and Mars analysis, crater retention modeling, applied planetary geology
- Timeline: Submit within 10 months

### 10.2 Conference Presentations

**Primary targets:**
- American Geophysical Union (AGU) Fall Meeting (December 2025)
  - Session: Planetary Geomorphology
  - Presentation type: Oral (15 min)
- Lunar and Planetary Science Conference (March 2026)
  - Presentation type: Poster + abstract
- GeomorphOn (International Conference on Geomorphometry)
  - Presentation type: Oral

**Secondary targets:**
- NASA Exploration Science Forum (if accepted, July 2025)
- International Association of Mathematical Geosciences (IAMG)

### 10.3 Open Science & Reproducibility

**GitHub Repository:**
- Complete documented code from DEM preprocessing to final analysis
- Tutorial notebooks with example datasets
- Environment setup instructions (conda/pip)
- License: MIT (permissive open source)

**Data Availability:**
- All source DEMs publicly available (provide download links)
- Processed analysis windows deposited in Zenodo (DOI-assigned permanent archive)
- Topological feature tables released as supplementary data

**Software Package:** "PlanetaryTDA"
- Python library for topological analysis of planetary DEMs
- Includes standard and directional persistence
- Visualization tools for persistence diagrams
- Documentation with use cases

---

## 11. Alignment with Graduate School Goals

### 11.1 Demonstrates Core Competencies

**Computational Skills:**
- Python programming (data processing, TDA implementation, statistical analysis)
- Geospatial analysis (GDAL, DEM processing, coordinate systems)
- Machine learning (Random Forest classification, regression modeling)
- Parallel computing and workflow optimization

**Statistical Rigor:**
- Multivariate analysis (MANOVA, hierarchical clustering)
- Spatial statistics (spatial cross-validation, autocorrelation testing)
- Hypothesis testing with multiple comparison corrections
- Model selection and validation

**Research Independence:**
- Self-directed project from conception to completion
- Literature review and gap identification
- Methodological innovation (directional persistence)
- Results interpretation and scientific writing

**Interdisciplinary Thinking:**
- Bridges mathematics (topology), computer science (algorithms), planetary science (geology)
- Translates abstract concepts to physical applications
- Demonstrates ability to work across traditional disciplinary boundaries

### 11.2 Supports Strong Graduate Applications

**For Planetary Science Programs:**
- Direct relevance to NASA mission priorities (Artemis, Mars Sample Return)
- Demonstrates expertise in planetary terrain analysis
- Shows preparedness for spacecraft mission data analysis
- Aligns with landing site selection and surface operations research

**For Geomorphology/Geography Programs:**
- Novel methodological contribution to digital terrain analysis
- Advances quantitative geomorphology
- Demonstrates computational and statistical sophistication
- Shows potential for future NSF-funded research

**For Computational Geosciences:**
- Applies advanced mathematics to Earth/planetary science problems
- Develops transferable algorithms and software tools
- Demonstrates ability to handle large geospatial datasets
- Shows promise for NASA, USGS, or DOE research careers

### 11.3 Publication Record

- **Primary paper (Science/Nature Geoscience):** Extremely high-impact for graduate applications
- **Two additional papers:** Demonstrates productivity and ability to complete research
- **First authorship on all three:** Shows leadership and independence
- **Open-source software:** Demonstrates commitment to reproducible science and community contribution

### 11.4 Advisor Perspectives

This project allows a potential graduate advisor to assess:
- **Can this student identify important questions?** (Yes: universal vs. planet-specific controls)
- **Can they design rigorous tests?** (Yes: four hypotheses with clear statistical validation)
- **Can they execute independently?** (Yes: 15-week solo project, no external dependencies)
- **Can they produce publishable results?** (Yes: three targeted journals, high-impact potential)
- **Will they be productive in my lab?** (Yes: computational skills, interdisciplinary thinking, publication record)

---

## 12. Conclusion

This research represents a genuine paradigm shift in how we think about landscape structure. By applying topological data analysis across Earth, Moon, and Mars, we move beyond planet-specific, process-dependent terrain metrics toward a universal mathematical language for describing landscape organization.

**The central insight:** If topological signatures reveal similar patterns across planetary bodies with radically different formation mechanisms, then we've identified fundamental structural principles that transcend process. If signatures remain planet-specific, we've established powerful new tools for terrain classification and highlighted the importance of formation mechanism.

**Either outcome is scientifically valuable and publishable.**

The project is ambitious but achievable: all data are publicly available, methods are well-established (with one innovative extension), and the timeline is realistic for a full-time 15-week effort. The potential impact spans planetary science, geomorphology, and computational topology, with immediate applications to space exploration.

Most importantly, this project asks a genuinely interesting question: **What makes a landscape look the way it does—universal structural mathematics, or planet-specific processes?** The answer matters for understanding our place in the solar system and identifying where we might safely land future missions.

**This is S-tier science.** Stop pivoting. Download the DEMs. Let's find out if topology is universal.

---

## 13. References

### Topological Data Analysis - Foundations

- Bauer, U. (2021). Ripser: Efficient computation of Vietoris–Rips persistence barcodes. *Journal of Applied and Computational Topology*, 5(3), 391-423.
- Bubenik, P. (2015). Statistical topological data analysis using persistence landscapes. *Journal of Machine Learning Research*, 16, 77-102.
- Edelsbrunner, H., & Harer, J. (2010). *Computational Topology: An Introduction*. American Mathematical Society.
- Carlsson, G. (2009). Topology and data. *Bulletin of the American Mathematical Society*, 46(2), 255-308.

### TDA Applications to Terrain

- Mander, L., Kurzbach, J., Conroy, G., & Keller, C. (2020). Refining the uplift history of the Patagonian Andes using topological data analysis. *Earth and Planetary Science Letters*, 528, 115837.
- Sousbie, T. (2011). The persistent cosmic web and its filamentary structure—I. Theory and implementation. *Monthly Notices of the Royal Astronomical Society*, 414(1), 350-383.
- Perez, A., et al. (2020). The shape of landslides: Persistent homology analysis of topographic change. *Geomorphology*, 365, 107268.

### Planetary Geomorphology

- Melosh, H. J. (2011). *Planetary Surface Processes*. Cambridge University Press.
- Howard, A. D. (2007). Simulating the development of Martian highland landscapes through the interaction of impact cratering, fluvial erosion, and variable hydrologic forcing. *Geomorphology*, 91(3-4), 332-363.
- Kreslavsky, M. A., & Head, J. W. (2000). Kilometer-scale roughness of Mars: Results from MOLA data analysis. *Journal of Geophysical Research: Planets*, 105(E11), 26695-26711.

### Structural Geology & Geomorphometry

- Wilson, J. P., & Gallant, J. C. (2000). *Terrain Analysis: Principles and Applications*. Wiley.
- Pike, R. J., & Rozema, W. J. (1975). Spectral analysis of landforms. *Annals of the Association of American Geographers*, 65(4), 499-516.
- Theilig, E., & Greeley, R. (1986). Lava flows on Mars: Analysis of small surface features and comparisons with terrestrial analogs. *Lunar and Planetary Science Conference Proceedings*, 17, E529-E540.

### DEM Data Sources & Quality

**Earth:**
- U.S. Geological Survey (TODO)

**Moon:**
- Smith, D. E., et al. (2010). Initial observations from the Lunar Orbiter Laser Altimeter (LOLA). *Geophysical Research Letters*, 37(18), L18204.
- Robbins, S. J. (2018). A new global database of lunar impact craters > 1-2 km: 1. Crater locations and sizes, comparisons with published databases, and global analysis. *Journal of Geophysical Research: Planets*, 124(4), 871-892.

**Mars:**
- McEwen, A. S., et al. (2007). Mars Reconnaissance Orbiter's High Resolution Imaging Science Experiment (HiRISE). *Journal of Geophysical Research: Planets*, 112(E5), E05S02.
- Malin, M. C., et al. (2007). Context Camera Investigation on board the Mars Reconnaissance Orbiter. *Journal of Geophysical Research: Planets*, 112(E5), E05S04.
- Robbins, S. J., & Hynek, B. M. (2012). A new global database of Mars impact craters ≥1 km: 1. Database creation, properties, and parameters. *Journal of Geophysical Research: Planets*, 117(E5), E05004.

### Crater Morphometry & Degradation

- Fassett, C. I., & Thomson, B. J. (2014). Crater degradation on the lunar maria: Topographic diffusion and the rate of erosion on the Moon. *Journal of Geophysical Research: Planets*, 119(10), 2255-2271.
- Golombek, M. P., & Rapp, D. (1997). Size-frequency distributions of rocks on Mars and Earth analog sites: Implications for future landed missions. *Journal of Geophysical Research: Planets*, 102(E2), 4117-4129.

### Statistical Methods & Machine Learning

- Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5-32.
- Zou, H., & Hastie, T. (2005). Regularization and variable selection via the elastic net. *Journal of the Royal Statistical Society Series B*, 67(2), 301-320.
- Roberts, D. R., et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography*, 40(8), 913-929.

### Landing Site Selection & Terrain Analysis

- Golombek, M. P., et al. (2012). Selection of the Mars Science Laboratory landing site. *Space Science Reviews*, 170(1-4), 641-737.
- Prettyman, T. H., et al. (2023). Geologic context and potential EVA targets at the lunar south pole. *Acta Astronautica*, 204, 156-178.

---

## Appendix A: Computational Details

### A.1 TDA Parameter Choices

**Persistence threshold:**
- Minimum persistence = 1% of total elevation range per window
- Rationale: Filters noise while retaining real topographic features

**Directional bins:**
- N = 16 bins (22.5° resolution)
- Rationale: Balance between angular precision and statistical power

**Window sizes:**
- Earth: 10×10 km (captures ridge-valley wavelengths)
- Moon: 5×5 km (captures crater spacing)
- Mars: 5-10 km (varies by site, matched to characteristic scales)

### A.2 Software Environment

```python
# Core libraries
import numpy as np
import scipy
import gudhi  # or ripser for faster computation
import sklearn
import gdal, rasterio  # DEM I/O
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

# Statistical analysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from scipy.stats import ttest_rel, mannwhitneyu
from statsmodels.multivariate.manova import MANOVA
```

### A.3 Hardware Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 16 GB
- Storage: 50 GB available
- OS: Linux, macOS, or Windows 10+

**Estimated runtime:**
- TDA computation: 30 seconds per 10×10 km window
- Total TDA time: ~350 windows × 30 sec = ~3 hours
- Regression modeling: 2-4 hours
- Total computation: <10 hours (easily fits in 1-2 days)

---

## Appendix B: Data Management Plan

### B.1 Data Storage

**Raw DEMs:**
- Stored in `data/raw/earth/`, `data/raw/moon/`, `data/raw/mars/`
- Original files preserved, never modified
- Metadata files record download date, source URL, resolution

**Processed Windows:**
- Stored in `data/processed/{planet}/{region}/`
- Each window saved as GeoTIFF with coordinate system preserved
- Naming convention: `{planet}_{region}_{ID}_{resolution}m.tif`

**Analysis Results:**
- Topological features: CSV tables in `results/topology/`
- Regression outputs: `results/regression/`
- Figures: `results/figures/` (high-res PNG/PDF)

### B.2 Version Control

**Code repository:**
- GitHub: github.com/[username]/planetary-tda
- Commit frequently with descriptive messages
- Tagged releases at milestones (v1.0 = TDA complete, v2.0 = all analysis done)

**Data versioning:**
- Large files (DEMs) tracked via Git LFS or separate archive
- Zenodo deposit at project completion for permanent DOI

### B.3 Backup Strategy

- Daily: External hard drive backup
- Weekly: Cloud backup (Google Drive, Dropbox)
- At completion: Institutional repository + Zenodo deposit

---

## Appendix C: Preliminary Results (If Available)

*This section to be populated during Weeks 5-7 with initial Earth analysis results to demonstrate proof-of-concept before full multi-planet analysis.*

**Expected content:**
- Example persistence diagrams from Valley & Ridge vs. Coastal Plain
- Initial MANOVA results showing province discrimination
- Directional persistence rose diagrams with fold axis overlay
- Multi-scale roughness regression showing R² improvement

---

**End of Proposal**
