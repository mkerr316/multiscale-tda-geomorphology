# A Multiscale Topological Framework for Landscape Characterization and Process Prediction

* **Author:** Michael Kerr
* **Date:** September 26, 2025
* **Timeline:** 15 Weeks (Fall 2025)

### Introduction & Objective

The quantitative science of geomorphometry has progressed through distinct generations of analytical techniques. The first generation focused on local, fixed-scale metrics, such as slope and curvature. The second developed compound indices, such as TWI and SPI, to model specific processes. However, both generations are constrained by a fundamental dependency on analytical scale and, in the case of curvature, a well-documented "implementation crisis" that undermines reproducibility.

This project introduces and validates a third-generation paradigm for geomorphometry. We will develop a novel framework that moves beyond measuring local form to quantifying multiscale shape. The core innovation is the creation of Topological Land-Surface Parameters (TLSPs), a new suite of continuous data layers derived from a sliding-window Topological Data Analysis (TDA) pipeline.

The objective is to demonstrate that this framework provides a more fundamental, robust, and physically meaningful language for describing landscapes. We will validate its utility in two coequal domains:
1.  **Landscape Characterization:** To prove that TLSPs can capture the essential structural signatures that distinguish geomorphic provinces.
2.  **Process Prediction:** To show that these topological signatures are potent predictors of environmental processes, offering more explanatory power than traditional metrics.

The outcome will be a methodologically transparent, computationally scalable, and fully reproducible pipeline that bridges the gap between abstract shape analysis and applied predictive modeling, with direct applications in soil conservation, water resource management, and climate adaptation.

### Core Hypotheses

To provide a rigorous statistical structure, we reverse the original project's logical flow. We will first establish that TLSPs are effective descriptors of landscape structure, and then demonstrate their utility in a predictive context. We define the alternative and null hypotheses as follows:

* **$H_1$ (Landscape Characterization Hypothesis):**
    * **$H_{A1}$:** Geomorphic provinces exhibit statistically distinct multiscale topological signatures.
    * **$H_{01}$:** There is no statistically significant difference in the multiscale topological signatures between geomorphic provinces.

* **$H_2$ (Process Prediction Hypothesis):**
    * **$H_{A2}$:** Multiscale topological signatures are significant predictors of erosion potential, providing more explanatory power than a baseline model using only traditional land-surface parameters.
    * **$H_{02}$:** The inclusion of multiscale topological signatures does not significantly improve the predictive performance of a model for erosion potential compared to a baseline model.

### Methods and Implementation

#### Computational Framework

We will execute all analyses within a Docker container to guarantee full reproducibility. The core pipeline is built on a parallel processing architecture using Dask to analyze larger-than-memory DEMs.

This project will implement the Dynamic Resource Allocation Framework outlined in our literature review, which is a key methodological contribution that ensures portability and scalability. The framework programmatically interrogates system resources (`psutil`) at runtime to dynamically calculate optimal data chunk sizes and configure Dask worker parameters (core count, memory limits). This principled approach avoids static, hard-coded configurations, allowing the pipeline to perform efficiently on any available hardware without manual tuning.

#### TDA Implementation and Justification

The TDA workflow will be implemented in Python using the `scikit-tda` ecosystem.

* **Filtration Method:** We will primarily use sublevel and superlevel set filtrations directly on DEM elevation values. We chose this method for its direct geomorphic interpretability: the "birth" and "death" of topological features correspond to specific elevation thresholds, directly linking the analysis to topographic features like peaks, pits, and passes. While the Vietoris-Rips filtration is robust, sublevel sets provide a more natural and computationally efficient framework for grid-based elevation data.

* **Homology Computation:** The high-performance `ripser.py` library will compute persistent homology for dimensions 0 ($H_0$, connectivity of components) and 1 ($H_1$, loops/enclosures). We will analyze both the raw DEM (for pits and basins) and the inverted DEM (for peaks and ridges).

* **Feature Vectorization:** To ensure methodological robustness, we will generate two distinct vector representations of the persistence diagrams:
    1.  **Persistence Landscapes (`persim`):** A stable, functional representation suitable for statistical analysis.
    2.  **Persistence Images:** A grid-based representation that integrates seamlessly with machine learning workflows and provides a complementary view of the diagram's feature distribution.

#### Sampling Design

We will use a stratified, doubly balanced sampling design to ensure a statistically powerful and efficient test of the core hypotheses. We will define strata by equal-area elevation quantiles within each geomorphic province. The Local Cube method (via the `BalancedSampling` package) is chosen over alternatives like BAS because it guarantees strong, often exact, balance on covariates, which is critical for minimizing variance in both the classification and regression models, maximizing statistical power.

#### Target Process Metric Justification

For the predictive track ($H_2$), we will use the Revised Universal Soil Loss Equation (RUSLE) to model erosion potential. We select RUSLE as the initial target variable for this 15-week proof-of-concept due to its straightforward implementation, relying on readily available DEM, soil, and precipitation data.

However, we explicitly acknowledge the limitations of this empirical model, as detailed in our literature review. A key future direction for this work, and a natural next step for a graduate-level project, will be to validate the TLSP framework against the outputs of a fully process-based model, such as the Water Erosion Prediction Project (WEPP), which will test the link between fundamental structure and fundamental physics, a more scientifically rigorous endeavor.

### 15-Week Project Plan

#### Section I: Foundational Research & Statistical Design (Weeks 1-4)

* **Week 1: Scoping & Finalizing Covariates**
    * [x] Finalize study area polygons and hold-out validation area.
    * [ ] **Finalize Toolchain:** Formally document primary Python libraries: `ripser.py`/`persim` (TDA), `whitebox` (Geomorphometry), `BalancedSampling` (Sampling).
    * [ ] **Define Covariate Layers:** Finalize balancing covariates, explicitly including wavelet-based roughness as a robust replacement for standard curvature to address the "curvature crisis". Acquire data for the RUSLE model (DEM, K-factor, R-factor).
* **Week 2: Pilot Study Design & Data Collection**
    * [ ] Define equal-area elevation strata for each province.
    * [ ] **Pilot Rationale:** Estimate variance for both topological features ($H_1$) and RUSLE values ($H_2$) to inform power analysis.
    * [ ] **Implement Pilot Sampling:** Generate 15 pilot locations per stratum using a simple spatially balanced sample.
    * [ ] Download pilot DEMs and extract all covariates.
* **Week 3: Pilot Analysis & Characteristic Scale Determination**
    * [ ] Run TDA pipeline on pilot data.
    * [ ] **Determine Analysis Scales:** Use semi-variogram and local variance analysis on pilot DEMs to identify the characteristic scales of topographic variation. These data-driven scales (e.g., local, hillslope, catchment) will define the window sizes for the sliding-window analysis, replacing arbitrary fixed sizes.
    * [ ] **Covariate Correlation Analysis:** Identify covariates most strongly correlated with variance in TDA metrics and RUSLE values.
* **Week 4: Power Analysis & Final Sampling**
    * [ ] **Perform A Priori Power Analysis** for both MANOVA ($H_1$) and regression ($H_2$).
    * [ ] **Design and Execute Final Sample Draw:** Implement the stratified, doubly balanced sample using the Local Cube method.
    * [ ] Generate formal oversample and replacement protocol.

#### Section II: TDA Pipeline Development & Feature Engineering (Weeks 5-10)

* **Week 5: Final Data Acquisition & Reproducible Environment**
    * [ ] Download all primary and oversample DEMs.
    * [ ] Generate wall-to-wall RUSLE raster layer.
    * [ ] Finalize Docker container with dynamic Dask parallel processing setup.
* **Weeks 6-7: Core Pipeline Validation on Synthetic Landscapes**
    * [ ] Develop the core sliding-window TDA function (serial implementation).
    * [ ] **Methodological Validation:** Test the serial pipeline exhaustively on synthetic landscapes (e.g., fractal surfaces, sinusoidal fields) to confirm the recovery of known topological ground truths. This "validate-then-scale" approach de-risks the project by ensuring the core logic is correct before parallelization.
* **Weeks 8-9: Parallelization & TLSP Raster Generation**
    * [ ] Wrap the validated serial function using Dask for parallel execution.
    * [ ] Conduct incremental scaling and resource profiling using the Dask dashboard to optimize performance.
    * [ ] **Generate TLSP Rasters:** Apply the final parallel pipeline to generate the full suite of TLSP raster layers.
* **Week 10: Data Extraction & Final Dataset Assembly**
    * [ ] Extract values from all generated TLSP and process-based rasters at the final sample locations.
    * [ ] Assemble and clean the master dataset for modeling.

#### Section III: Analysis, Validation, & Interpretation (Weeks 11-13)

* **Week 11: Track A - Landscape Characterization & Classification ($H_1$)**
    * [ ] Apply PCA/UMAP to the TLSP feature set for dimensionality reduction and visualization.
    * [ ] **Perform MANOVA** to formally test $H_1$.
    * [ ] Train a Random Forest classifier.
    * [ ] **Validation:** Compare TDA-based classification accuracy against a baseline model using Geomorphon landform classifications as predictors.
* **Week 12: Track B - Environmental Process Prediction ($H_2$)**
    * [ ] Train a Gradient Boosting regressor to predict RUSLE values using TLSPs.
    * [ ] **Physical Interpretation:** Use SHAP to identify the most predictive topological features. Correlate these key features with process-based indices (TWI, SPI) to provide a physical grounding for their predictive power.
    * [ ] Compare model performance against a baseline using only traditional metrics (slope, relief, wavelet-roughness).
* **Week 13: Final Validation & Synthesis**
    * [ ] **External Validation:** Apply both final models to the independent, held-out validation dataset to obtain an honest measure of generalizability.
    * [ ] **Synthesize & Visualize:** Create plots, maps, and figures that weave all results into a coherent geomorphic narrative, linking the classification and prediction outcomes.

#### Section IV: Documentation & Final Deliverables (Weeks 14-15)

* **Week 14: Final Report & Presentation**
    * [ ] Write final report, framing the work as a foundational "3rd Generation" geomorphometry.
    * [ ] Prepare a presentation for both technical and general audiences.
* **Week 15: Code Publication & Project Archiving**
    * [ ] Finalize GitHub repository with all commented scripts, Dockerfile, and a replication notebook.
    * [ ] **Project Debrief & Future Work:** Explicitly plan for a methods-focused paper on the TLSP framework and an application-focused paper on erosion prediction, including the proposed extension to WEPP.

### Future Directions & Project Enhancements

While the 15-week plan outlines a complete and impactful project, this framework opens several avenues for future graduate-level research:

* **Methodological Expansions:**
    * **Mapper Algorithm:** Use the Mapper algorithm for exploratory visualization of the final TLSP feature space to reveal higher-order structural relationships between geomorphic provinces.
    * **Higher Homology Dimensions ($H_2$):** Compute the second homology group to capture large-scale volumetric features (voids), such as enclosed basins, which may be a key differentiator in provinces like the Basin and Range or karst landscapes.
* **Validation & Sensitivity Deep Dives:**
    * **DEM Error Propagation:** Conduct a formal Monte Carlo simulation to quantify how uncertainty in the source DEM (e.g., from LiDAR) propagates through the TDA pipeline to the final predictions and classifications.
* **Computational Optimization:**
    * **GPU Acceleration:** For very large-scale or near-real-time deployments, explore GPU-accelerated TDA libraries (e.g., `CuPy`, `GUDHI`) for the filtration step to reduce computation time dramatically.
* **Process-Based Model Integration:**
    * **WEPP Validation:** Execute the plan to validate the TLSP framework against the process-based WEPP model, providing a more rigorous test of the process-topology link.