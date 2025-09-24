# A Multiscale TDA Framework for Geomorphology
- **Author:** Michael Kerr
- **Timeline:** 15 Weeks (Fall 2025)

---

### **Objective**
To develop and validate a novel multiscale framework for classifying geomorphic provinces using a state-of-the-art, probability-based sampling design and a fully reproducible Topological Data Analysis (TDA) pipeline. This project is designed to produce a methodologically transparent, statistically robust, and fully replicable classification of landscapes, validated against both external data and known geomorphic processes.

### **Core Hypotheses**
- **H₀ (Null Hypothesis):** There are no statistically significant differences in the multiscale topological feature distributions among the six geomorphic provinces.
- **Hₐ (Alternative Hypothesis):** The geomorphic provinces exhibit unique and statistically significant topological signatures that vary characteristically with spatial scale, and the distinctiveness of these signatures can be quantified and validated.

---
## 15-Week Project Plan

### Section I: Foundational Research & Statistical Design (Weeks 1-4)

- **Week 1: Scoping & Advanced Literature Review**
    - [x] **Define Study Areas & Control Province:** Finalize and acquire boundary polygons for all six primary provinces.
    - [x] **Define External Validation Area:** Delineate a smaller, spatially separate hold-out area in a geologically similar province (e.g., a portion of the North Carolina Piedmont) that will be used *only* for final model validation.
    - [ ] **Literature Review (Zotero):**
        - **Core Topics:** Geomorphology, TDA, Multiscale Analysis (Wavelets, Scale-Space Theory).
        - **Advanced Spatial Statistics:** Doubly Balanced Sampling (Local Cube / BAS), covariate selection for variance reduction.
    - [ ] **Define & Justify Covariate & Process Layers:** Identify and acquire wall-to-wall raster data for:
        - **Balancing Covariates:** (e.g., slope, relief, curvature). Justify selection based on potential variance reduction and geomorphic interpretability.
        - **Process-Based Metrics:** (e.g., Topographic Wetness Index, Stream Power Index).

- **Week 2: Pilot Study Design & Data Collection**
    - [ ] **Define Strata:** Generate three equal-area elevation strata (Low, Medium, High) for each province.
    - [ ] **Pilot Study Rationale:** The pilot study has three explicit deliverables: (1) Robustly estimate variance to inform power analysis, (2) Validate the range of scales for the multiscale analysis, and (3) Identify the most effective terrain covariates for balancing.
    - [ ] **Implement Pilot Sampling:** Generate **10-15 pilot locations per stratum (Total N=180-270)** using a simple spatially balanced sample (GRTS).
    - [ ] **Download Pilot Data & Extract Covariates:** For all pilot locations, download large DEM tiles and extract corresponding covariate and process-metric values.

- **Week 3: Pilot Analysis & QA/QC**
    - [ ] **Run TDA Pipeline on Pilot Data:** Process all pilot plots to generate preliminary topological feature vectors.
    - [ ] **Validate Analysis Scales:** Perform Variogram/LV analysis to confirm the appropriate range of plot sizes for the multiscale analysis.
    - [ ] **Covariate Correlation Analysis:** Identify the 2-4 terrain covariates most strongly correlated with variance in the pilot TDA metrics.
    - [ ] **QA/QC - Variance Stabilization Analysis:** Plot variance estimates against the number of cumulative samples (N) to document that the pilot study was sufficiently large.

- **Week 4: Power Analysis & Final "Platinum-Standard" Sampling**
    - [ ] **Perform A Priori Power Analysis:**
        - **Metric:** Use a specified effect size metric (e.g., MANOVA Pillai’s trace).
        - **Variance:** Use covariate-adjusted variance estimates to calculate the required sample size (N).
        - **Contingency:** Define a contingency plan if the pilot effect size is smaller than expected.
    - [ ] **Design and Execute Final Sample Draw:**
        - **Method:** Use `BalancedSampling` or `BAS` or something similar to implement a stratified, doubly balanced sample.
        - **Covariate Sensitivity Test:** Briefly rerun the sample draw with different covariate subsets to ensure robustness.
    - [ ] **Generate Formal Oversample & Replacement Protocol:** Generate a randomized, ordered replacement list for each stratum and document the full nonresponse framework.

---
### Section II: TDA Pipeline Development & Data Processing (Weeks 5-10)

- **Week 5: Final Data Acquisition & Reproducible Environment**
    - [ ] **Download Primary Data:** Acquire final DEMs for all primary, oversample, and external validation locations.
    - [ ] **Download/Calculate Process-Based Metrics:** For all final sample locations, download or calculate rasters for TWI, SPI, etc.
    - [ ] **Containerize Environment (Docker/Singularity):** Build a container with the exact versions of all software and libraries. All subsequent analyses will be executed within this container.

- **Weeks 6-9: TDA Core Pipeline Construction & Automation**
    - [ ] **Core Function:** Write a Python function that takes a DEM file path as input and is robust to varying dimensions.
    - [ ] **Filtration & Persistent Homology:** Implement functions to compute persistence diagrams for H₀ and H₁.
    - [ ] **Vectorization:** Implement methods to convert persistence diagrams into machine-learning-ready vectors (e.g., persistence images).
    - [ ] **Batch Processing Script:** Write a master script to automate the full pipeline from DEM to feature vector for all samples.

- **Week 10: Buffer, Debugging & Code Refinement**
    - [ ] Conduct a full test run of the batch processing script within the container.
    - [ ] Debug any issues with file paths, data formats, or library compatibility.
    - [ ] Refactor code for clarity, efficiency, and reproducibility.

---
### Section III: Multiscale Analysis, Validation, & Interpretation (Weeks 11-13)

- **Week 11: Multiscale TDA Processing & Dimensionality Reduction**
    - [ ] **Run Multiscale TDA Pipeline:** For each sample location, run the TDA pipeline in a loop across a range of pre-defined spatial scales (e.g., 800m, 1200m, 1600m, 2000m). The output for each location is now a *set* of topological vectors, one for each scale.
    - [ ] **Dimensionality Reduction (PCA):** Apply PCA to the concatenated multiscale feature vectors. Analyze loadings to understand how topological features at different scales contribute to variance.

- **Week 12: Hypothesis Testing & Uncertainty Quantification**
    - [ ] **Primary Test (MANOVA):** Perform MANOVA on significant PCs.
    - [ ] **Post-Hoc Analysis:** Perform pairwise tests, controlling for multiple comparisons (e.g., FDR).
    - [ ] **Quantify Fingerprint Distinctiveness & Uncertainty:**
        - **Cross-Validation:** Train a classification model (e.g., Random Forest) on the multiscale feature vectors.
        - **Bootstrapping:** Run the cross-validation process hundreds of times on resampled data to generate **bootstrap confidence intervals** for classification accuracy and other key metrics.

- **Week 13: Final Validation & Synthesis**
    - [ ] **External Validation:** Use your final, trained classification model to predict the province labels for the completely independent, held-out validation dataset. The accuracy on this set is your most honest measure of real-world performance.
    - [ ] **Process-Based Validation:** Correlate your TDA-derived principal components with the process-based metrics (TWI, SPI). A strong correlation provides a physical grounding for your abstract topological findings.
    - [ ] **Synthesize & Visualize:** Create plots, maps, and figures to weave all validation results into a coherent geomorphic narrative.

---
### Section IV: Documentation & Final Deliverables (Weeks 14-15)

- **Week 14: Final Report & Presentation**
    - [ ] **Write Final Report:** Structure the report in a standard scientific format. The Methods section will be a central pillar, detailing the entire landmark workflow.
    - [ ] **Prepare Presentation:** Create a slide deck summarizing the project's motivation, methods, key findings, and future directions.

- **Week 15: Code Publication & Project Archiving**
    - [ ] **Finalize GitHub Repository & Data Management Plan:** Upload all commented scripts, the Dockerfile, and a formal Data Management Plan.
    - [ ] **NEW: Create Final Replication Package:** Develop a single RMarkdown or Jupyter Notebook that reproduces the entire analysis on a subset of the data.
    - [ ] **Project Debrief:** Write a final reflection on lessons learned and explicitly plan for a **methods note submission** and future papers based on the "Side Quests" below.

---
## Project Enhancements
These are high-value enhancements to explore if time permits during the 15 weeks or to serve as a roadmap for future research.

### **Methodological Expansions**
- **TDA Method Diversification:** Compare persistence homology against other TDA methods.
  - **Mapper Algorithm:** Use for an alternative, cluster-based view of your high-dimensional feature space.
  - **Alternative Distances:** Calculate Wasserstein or Bottleneck distances between persistence diagrams for a more topologically faithful comparison than vector-based methods.
  - **Higher Homology Dimensions:** Compute H₂ (voids) to capture large-scale basin and enclosure structures, which may be a key differentiator in provinces like the Coastal Plain or Basin and Range.

### **Advanced Statistical Modeling**
- **Hierarchical Modeling:** Use a hierarchical (multilevel) model to explicitly account for the nested structure of your data (samples within strata within provinces), which may yield more accurate estimates of variance.
- **Functional Data Analysis (FDA):** Instead of vectorizing persistence diagrams, treat them as functions. FDA methods can analyze the full shape and form of the diagrams, potentially capturing information lost during vectorization.
- **Formal Topological Inference:** Move beyond descriptive statistics to use formal inference methods for topological features, such as calculating confidence bands for persistence diagrams.

### **Validation & Sensitivity Deep Dives**
- **Synthetic Landscape Testing:** Test the entire pipeline on synthetic landscapes with known theoretical properties (e.g., fractal surfaces with a specific Hurst exponent) to see how well it recovers known ground truths.
- **DEM Error Propagation:** If using a DEM with a known error surface, run a Monte Carlo simulation to see how that uncertainty propagates through to your final TDA metrics.

### **Computational Optimization**
- **Parallel Processing:** Refactor the batch processing script to run on multiple cores, dramatically speeding up the analysis of hundreds of samples across multiple scales.
- **GPU Acceleration:** For very large DEM plots, explore using GPU-accelerated libraries for the filtration step, which can offer an order-of-magnitude speed increase.
