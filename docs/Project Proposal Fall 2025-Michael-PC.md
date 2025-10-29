# **Topological Geomorphometry: A Physics-Aware Framework for Structural and Process Analysis**

**Author:** Michael Kerr\
**Date:** October 23, 2025

## Executive Summary

This research establishes a new paradigm in quantitative terrain analysis, **Topological Geomorphometry**, by developing and rigorously validating a novel computational framework. Current geomorphometry is descriptive, while standard Topological Data Analysis (TDA) is isotropic—blind to the directional processes (e.g., water flow) and anisotropic structures (e.g., tectonic fabric) that define landscapes.

This project overcomes this critical flaw by implementing two physics-aware TDA methods:
1.  **Non-Isotropic Persistent Homology (NIPH):** To quantify and extract anisotropic structural fabric (e.g., fold axes, fault lines).
2.  **Persistent Path Homology (PPH):** To quantify the directional signatures of surface processes (e.g., fluvial erosion networks).

The "landmark" contribution of this work is its **two-phase validation and application design**.
* **Phase 1 (Validation):** We first validate this framework on a terrestrial "ground truth"—the **Appalachian physiographic provinces**. Using **high-resolution USGS 3DEP (10m and 1m) LiDAR data**, we prove that NIPH/PPH can (a) discriminate between structurally distinct landscapes, (b) recover known structural fabric, and (c) are **methodologically robust and stable across different data resolutions (1m vs. 10m)**.
* **Phase 2 (Application):** With the methodology validated, we apply this "Rosetta Stone" to a frontier scientific problem: **discriminating Martian lithologies from topography alone**, benchmarking it against traditional and isotropic TDA methods.

**Impact:** This work moves beyond simple landscape description to genuine geophysical inference. It delivers a validated, open-source toolkit for decoding geological processes and structures from topography, with immediate applications in terrestrial hazard assessment, resource exploration, and planetary science.

---

## 1. Introduction: From Isotropic Description to Anisotropic Inference

### 1.1 The Limits of Current Terrain Analysis

The study of planetary and terrestrial surfaces has been revolutionized by high-resolution Digital Elevation Models (DEMs), from Earth-based LiDAR to Martian HiRISE data. However, our analytical tools, collectively known as Digital Terrain Analysis (DTA), remain limited. Standard metrics (e.g., slope, curvature) are descriptive, local, and scale-dependent. They fail to capture the multiscale, hierarchical, and interconnected nature of the geomorphic systems that sculpt landscapes, creating a fundamental disconnect between landscape *form* and formative *process*.

### 1.2 The Promise of Standard TDA (Persistent Homology)

Topological Data Analysis (TDA), particularly **Persistent Homology (PH)**, offers a new language by quantifying the intrinsic "shape" of a landscape across all scales simultaneously.

We achieve this through a **filtration**, most intuitively a "flooding" of the landscape (a *sublevel set filtration*). As the "water level" rises, PH tracks the "birth" and "death" of topological features:
* **$H_0$ (Components):** New islands are "born." When they merge, the shorter one "dies."
* **$H_1$ (Loops):** Lakes (basins) are "born." When the water overtops the surrounding ridge (a saddle), the lake "dies" (is filled).

The output is a **Persistence Diagram**, a 2D scatter plot showing the (birth, death) coordinates of every feature. The distance of a point from the diagonal (its "persistence") is a measure of its robustness, which allows us to separate large-scale geological structure from small-scale noise.

### 1.3 The "Isotropy Flaw": A Fundamental Disconnect

This standard PH method, however, suffers from a **critical flaw**: it is fundamentally *isotropic* (direction-blind). The standard **Vietoris-Rips filtration**, which builds a shape from a point cloud, uses a symmetric Euclidean distance metric. It can measure the *size* of a ridge but not its *orientation*.

This mathematical convenience is fundamentally at odds with the nature of geology:
* **Processes are Directional:** Fluvial erosion, aeolian transport, and glacial flow are governed by asymmetric, downslope, or downwind forces.
* **Structures are Anisotropic:** Tectonic stresses, folded strata, and fault systems create a preferred orientation or "grain" in the landscape.

Applying an isotropic tool to an anisotropic system risks obscuring or completely missing the most important geological information.

### 1.4 Bridging the Gap: Directional & Anisotropic Topology

Early attempts to solve this, such as the **Euler Characteristic Transform (ECT)**, demonstrated the power of a *directional* approach. The ECT builds a shape signature by "probing" it from many different directions, demonstrating that directional analysis can capture information that standard, non-directional PH misses.

However, the ECT (which uses a simpler topological summary) and its PH-based cousins are still *probing* the shape "as-is." They do not account for the fact that the landscape itself has been *plastically deformed* by geological forces.

A truly physics-aware framework must go one step further. It must not only *probe* directionality (to capture process) but also *solve for* the underlying structural anisotropy (to capture fabric). This project develops and validates that framework.

---

## 2. A Physics-Aware TDA Framework

This research develops and integrates two advanced topological methods tailored for the geosciences.

### 2.1 Method 1: Persistent Path Homology (PPH) for Directional Processes

To capture directional processes, we move beyond standard homology to **Path Homology**. This foundational method models the DEM as a *directed graph* (digraph), where each edge explicitly points downslope along the elevation gradient.

We then apply **Persistent Path Homology (PPH)**, a framework for analyzing directed networks. Using a **Dowker complex filtration**, which respects the asymmetry of the flow network, PPH quantifies directional topological features, which allows us to capture the unique, asymmetric signatures of process-dominated systems, such as dendritic fluvial networks, distinguishing them from landscapes shaped by non-directional processes (e.g., impact cratering or isotropic Karst dissolution).

### 2.2 Method 2: Non-Isotropic Persistent Homology (NIPH) for Structural Fabric

To quantify anisotropy, we implement NIPH. Instead of using a fixed metric (like standard PH), NIPH systematically deforms the DEM point cloud by applying directional scaling transformations (i.e., "stretching" and "compressing" the landscape in different orientations).

By computing PH for each scaled version and analyzing the resulting shifts in the persistence diagram, NIPH solves an optimization problem to extract the landscape's dominant orientation, scaling factor, and orientational variance, which provides a direct, quantitative measure of the geological "grain" (e.g., the NE-SW trend of the Appalachian Valley & Ridge).

---

## 3. Core Research Questions & Hypotheses

We will structure this project as a logical progression from methodological validation on Earth to scientific application on Mars.

### Phase 1: Methodological Validation (Earth)

**RQ1: Structural Fabric Recovery:** Can NIPH robustly extract known structural fabric from terrain alone?
* **H₁ (Alternative):** NIPH-derived anisotropy direction will strongly correlate ($r > 0.8$) with the known NE-SW fold axes in the Valley & Ridge province.
* **H₁ (Control):** NIPH will show no dominant fabric (Anisotropy Index $\approx 0$) in the isotropic Karst "negative control" landscape.

**RQ2: Landscape Discrimination:** Can NIPH and PPH features, derived from 10m DEMs, discriminate between landscapes with distinct structural and process controls?
* **H₂ (Alternative):** A Random Forest classifier using NIPH/PPH features will achieve >85% accuracy in distinguishing the six Appalachian provinces (e.g., *structure-dominated* Valley & Ridge vs. *process-dominated* Plateau vs. *isotropic* Karst).

**RQ3: Methodological Robustness (The "Unimpeachable" Test):** Are NIPH/PPH signatures geologically meaningful, or just artifacts of data resolution?
* **H₃ (Alternative):** Topological features are robust to data resolution.
    * **Stability:** NIPH anisotropy *direction* and PPH/NIPH persistence landscape *shapes* computed from 1m and 10m 3DEP data for the same sites will be strongly correlated ($r > 0.8$).
    * **Prediction:** 10m TDA features will significantly improve the prediction of 1m-scale terrain roughness (improve $R^2$ by $\geq 0.15$ over baseline models), proving they encode real, hierarchical information.

### Phase 2: Scientific Application (Mars)

**RQ4: Lithological Discrimination:** Following successful validation on Earth, can this TDA framework discriminate between Martian lithologies with higher accuracy than baseline methods?
* **H₄ (Alternative):** A classifier trained on NIPH/PPH features will distinguish Martian lithologies (e.g., basalts vs. sedimentary deposits) with significantly higher accuracy than classifiers trained on (a) traditional geomorphometry or (b) standard isotropic PH.

---

## 4. Study Design & Data (Two-Phase)

### 4.1 Phase 1: Validation on a Terrestrial "Ground Truth" (Earth)

We use the six Appalachian physiographic provinces as a perfect, well-understood natural laboratory.

* **Study Areas:**
    1.  **Valley and Ridge:** (Positive Control for NIPH). Strong NE-SW anisotropic fabric.
    2.  **Appalachian Plateau:** (Test Case for PPH). High-relief, process-dominated dendritic dissection.
    3.  **Karst Landscape (WV):** (Negative Control for NIPH). Isotropic, solution-dominated terrain.
    4.  **Blue Ridge:** High-relief, folded metamorphic structure.
    5.  **Piedmont:** Rolling, deeply weathered crystalline rock.
    6.  **Coastal Plain:** Low-relief, featureless sedimentary deposits.
* **Data:**
    * **Primary (RQ1, RQ2):** **USGS 3DEP 10m DEMs.** Tiled into ~300 (10x10 km) analysis windows.
    * **Validation (RQ3):** **USGS 3DEP 1m DEMs.** Paired 1x1 km sites (1m vs. 10m) to test cross-scale robustness.

### 4.2 Phase 2: Application to a Planetary Frontier (Mars)

* **Rationale:** On Mars, topography is often the only high-resolution data available. We test whether our validated framework can decode lithology from DEMs alone.
* **Study Areas:** Sites with well-characterized lithologies (e.g., basalts, sedimentary deposits, cratered highlands) confirmed by independent data.
* **Data:**
    * **Topography:** High-resolution DEMs from **HiRISE** (~1 m/pixel) and **CTX** (~6 m/pixel).
    * **"Ground Truth":** Lithological maps derived from **CRISM** spectral data and in-situ rover investigations.

---

## 5. Methodology & Analysis

### 5.1 Computational Pipeline

1.  **Data Curation:** Acquire and tile all Earth (3DEP) and Mars (PDS) DEMs.
2.  **Filtration Construction:** For each window, generate:
    * **Baseline 1 (Standard PH):** Isotropic Vietoris-Rips filtration.
    * **Novel 1 (NIPH):** A set of directionally-scaled point clouds.
    * **Novel 2 (PPH):** A directed graph (flow network) and its Dowker complex filtration.
3.  **Persistence Calculation:** Compute $H_0$ and $H_1$ persistent homology for all filtrations using high-performance libraries (e.g., Gudhi, **Ripser**).
4.  **Vectorization:** Convert all persistence diagrams into stable, fixed-length vectors. We will use **Persistence Images (PIs)**, an optimal-grade method that is computationally efficient and well-suited for machine learning, thereby avoiding the computational overhead of alternatives such as Persistence Landscapes.

### 5.2 Statistical Analysis Framework

* **Analysis 1 (Fabric, RQ1):** Angular correlation between $\theta_{\text{NIPH}}$ and $\theta_{\text{map}}$ (known fold axes).
* **Analysis 2 (Discrimination, RQ2):** MANOVA and Random Forest classification on PI vectors to separate the 6 Appalachian provinces.
* **Analysis 3 (Robustness, RQ3):**
    * **Stability:** Pearson correlation ($r$) on PI vectors and angular correlation on $\theta_{\text{NIPH}}$ from paired 1m vs. 10m sites.
    * **Prediction:** Nested regression models to test if 10m TDA features predict 1m terrain roughness.
* **Analysis 4 (Application, RQ4):** Train RF/SVM classifiers on Mars data. Rigorously benchmark NIPH/PPH feature accuracy against (a) Traditional DTA features (slope, etc.) and (b) Standard PH features.

### 5.3 The "Rosetta Stone": Geological Interpretation

This framework translates abstract topological features into tangible geological meaning.

| TDA Feature | Geological Interpretation (Hypothesized) | Example Landscape |
| :--- | :--- | :--- |
| **High NIPH Anisotropy** | Strong, uniform structural control (folds, faults). | Valley and Ridge |
| **Low NIPH Anisotropy** | Isotropic structure or process (e.g., dissolution, impacts). | Karst, Impact Craters |
| **Strong PPH Signature** | Directionally-dominant process, organized flow network. | Dissected Plateau (fluvial) |
| **High $H_0$ Persistence** | A few, deep, and/or wide basins. | Large sinkholes, grabens. |
| **High $H_1$ Persistence** | A few, tall, and/or wide peaks. | Monadnocks, horsts. |
| **Low Persistence (all)** | Low relief, featureless, homogenous surface. | Coastal Plain, Martian plains. |

---

## 7. Intellectual Merit & Broader Impacts

### 7.1 Intellectual Merit

1.  **Methodological Creation:** Pioneers a new sub-field of **Topological Geomorphometry** by tailoring advanced TDA (PPH, NIPH) to the physical realities of geology (anisotropy and directionality).
2.  **Unimpeachable Validation:** Establishes the *first* rigorous, multiscale (1m vs. 10m) validation of these methods on a terrestrial "ground truth," proving they are robust and geologically real.
3.  **Landmark Application:** Delivers a *validated* (not just proposed) framework for planetary science, enabling new quantitative methods for automated geologic mapping from topography alone.

### 7.2 Broader Impacts

1.  **Direct Terrestrial Applications:** The validated framework is immediately transferable to pressing Earth-based challenges, including **natural hazard assessment** (automated landslide scarp detection) and **resource management** (characterizing fracture networks for groundwater or geothermal energy).
2.  **Open Science:** We will package all algorithms into a user-friendly, open-source Python library. All derived datasets and results will be published with open access, ensuring reproducibility and community adoption.
3.  **Education & Outreach:** This project provides compelling material at the intersection of planetary exploration, mathematics, and AI, creating engaging tutorials for inspiring the next generation of interdisciplinary scientists.

---

## 8. References (Combined)

* Bauer, U. (2021). **Ripser**: Efficient computation of Vietoris-Rips persistence barcodes. *Journal of Applied and Computational Topology*.
* Bubenik, P. (2015). Statistical topological data analysis using persistence landscapes. *Journal of Machine Learning Research*.
* Carlsson, G. (2009). Topology and data. *Bulletin of the American Mathematical Society*.
* Chowdhury, S., & Mémoli, F. (2018). Persistent path homology of directed networks. *Proceedings of the 29th ACM-SIAM Symposium on Discrete Algorithms*.
* Edelsbruner, H., & Harer, J. (2010). *Computational Topology: An Introduction*. AMS.
* Grande, T., et al. (2024). Non-isotropic Persistent Homology. *Proceedings of the 41st International Conference on Machine learning (PMLR)*.
* Mander, L., et al. (2020). Refining the uplift history of the Patagonian Andes using topological data analysis. *Earth and Planetary Science Letters*.
* Pérez, A., et al. (2020). The shape of landslides: Persistent homology analysis of topographic change. *Geomorphology*.
* U.S. Geological Survey. (n.d.). *The National Map - 3DEP*. Retrieved October 23, 2025.
* Wilson, J. P., & Gallant, J. C. (2000). *Terrain Analysis: Principles and Applications*. Wiley.
* *(Additional references to be added for Euler Characteristic Transform (Turner, et al.) and Persistence Images (Adams, et al.))*
