# Topological Signatures of Appalachian Landscapes: A Rigorous Methodological Evaluation

**A Two-Year Research Proposal with Proof-of-Concept Validation**

**Author**: Michael Kerr
**Date**: October 30, 2025
**Version**: Final Draft for Committee Review

---

## Executive Summary

This research addresses a fundamental methodological question: **Can topological data analysis (TDA) provide quantitative metrics that rigorously validate the century-old qualitative classification of Appalachian physiographic provinces, and under what conditions does TDA offer advantages over established geomorphometric methods?**

The project employs a **defensible testbed-then-scale design** with three-tier success criteria ensuring publishable results regardless of specific empirical outcomes. A 2-3 month proof-of-concept phase validates computational feasibility and establishes baseline performance before committing to the 24-month main study. Success is defined as **methodological characterization**—understanding which TDA methods work under what conditions—not advocacy for topological approaches over traditional geomorphometry.

**Critical positioning**: This is explicitly NOT a project claiming TDA superiority. Recent literature (Syzdykbayev et al. 2024) demonstrates that TDA alone produces "notable false positives" in terrain analysis, working best when integrated with traditional geometric features. This proposal embraces that finding through rigorous hybrid model comparison while filling documented research gaps: (1) Euler characteristic has never been systematically applied to DEMs despite theoretical proposals; (2) no studies compare TDA vectorization methods for terrain; (3) spatial validation is rare, with most studies using random CV that inflates performance 28-50%.

**Innovation**: First comprehensive TDA methods comparison for terrain classification, systematically testing Euler characteristic, persistent homology variants (landscapes vs. images vs. scalar summaries), and hybrid approaches against Random Forest baselines achieving 92-99% accuracy in existing studies. Validation employs spatial block cross-validation (mandatory for terrain data but absent in <5% of published TDA applications), multiple testing corrections, and complete failure mode documentation.

**Outcomes**: The study produces publishable results across three pathways: (1) If TDA+traditional outperforms either alone by ≥10%, demonstrates complementary information justifying method adoption; (2) If TDA matches traditional with ≥5% improvement, establishes interpretability/transferability advantages; (3) If TDA underperforms, documents precise failure modes preventing future wasted effort. All pathways contribute to geomorphometry by establishing evidence-based guidance for method selection.

---

## 1. Introduction: From Qualitative Classification to Quantitative Validation

### 1.1 The Problem: Century-Old Classifications Lack Quantitative Topological Metrics

Appalachian physiographic provinces have been classified since Fenneman (1938) based on qualitative expert interpretation: Valley and Ridge exhibits "strongly folded, parallel linear ridges with NE-SW orientation"; Blue Ridge shows "complex fold interference, rugged mountainous terrain"; Piedmont displays "rolling uplands with subtle basement fabric"; Coastal Plain presents "isotropic, minimal relief, post-orogenic sedimentation."

**The fundamental gap**: While these provinces have authoritative boundaries (USGS Fenneman dataset) and show distinct elevation/slope statistics, **no studies have quantified their topological signatures**. Do these qualitative descriptions ("strongly folded," "rolling uplands," "isotropic") correspond to measurable differences in multi-scale topological structure (connectivity, loops, basin organization)? Can topology provide quantitative metrics that validate—or challenge—expert classifications?

Traditional geomorphometry captures local point-scale properties (slope, curvature) or statistical patterns (variograms, FFT) but lacks tools for quantifying **global topological organization**. Geomorphons classify local landform types but provide no information about how these forms connect at landscape scales. Random Forest achieves 92-99% accuracy distinguishing provinces using elevation and slope, but these are morphological descriptors—they do not directly quantify the structural organization that geologists describe qualitatively.

### 1.2 Why This Matters: Methodological Precedent for Geospatial Sciences

This research is **not** about proving TDA superiority. It addresses a documented methodological vacuum: with <5 rigorous TDA-terrain papers published, the field lacks systematic evaluation of which topological methods work, under what conditions, and with what computational costs. The Bhuyan et al. (2024) study in *Nature Communications* demonstrated 80-94% cross-continental landslide classification accuracy using topological features, but emphasized that **topological features (94%) vastly outperformed geometric features alone (65%)**—not that topology should replace geometry, but that integration matters.

**The broader impact**: Establishing rigorous protocols for TDA evaluation in one well-understood domain (Appalachian provinces with authoritative ground truth) creates precedent for applications to less constrained problems: planetary analog site identification, submarine terrain classification, paleotopographic reconstruction, or any domain where global structural relationships matter.

### 1.3 Research Objectives: Characterization, Not Advocacy

**Primary Objective**: Determine which topological data analysis methods provide rigorous quantitative metrics for Appalachian province classification, characterize when each method excels or fails, and assess whether topological signatures reflect underlying geological processes.

**Specific Research Questions** (note: framed as open questions, not assumed answers):

1. **RQ1 (Methods Comparison)**: Does Euler characteristic (χ) analysis—never systematically tested on DEMs—suffice for province discrimination, or is full persistent homology necessary? What performance differences exist between persistence landscapes, persistence images, and scalar summaries?

2. **RQ2 (Hybrid Integration)**: Do hybrid models (TDA + traditional geomorphometry) outperform either approach alone, and if so, by what margin and under what conditions?

3. **RQ3 (Spatial Transferability)**: Do topological features trained on one province subset transfer to held-out provinces better than traditional features, or is spatial autocorrelation similar across methods?

4. **RQ4 (Interpretability)**: Can topological features (H₀ basin depth, H₁ valley enclosure) be mapped to geological processes (fold-controlled topography, erosional planation) more directly than traditional indices?

**What constitutes success**: Understanding the TDA methods landscape for terrain analysis. "Euler characteristic sufficient, full persistent homology unnecessary" is a valuable finding. "TDA underperforms but identifies specific failure modes" prevents future wasted effort. Success ≠ proving TDA better; success = evidence-based method characterization.

---

## 2. Literature Review: Current State and Documented Gaps

### 2.1 TDA Applications to Terrain: A Genuinely Nascent Field

**Publication landscape analysis** (systematic search conducted October 2025):

- **Landslide detection**: Syzdykbayev et al. (2020) applied PH to LiDAR DTMs achieving 70-96% accuracy. **Critical 2024 follow-up found "notable incidence of false positives" with pure topological information**; best results required integration with geometric filters (area, perimeter, slope).

- **Cross-continental validation**: Bhuyan et al. (2024, *Nature Communications*) trained on 250,000 Italian landslides, tested across US, Denmark, Turkey, China achieving 80-94% accuracy. Topological features (94%) vastly outperformed geometric features alone (~65%). Six optimal features: average lifetime of holes (ALH, 22% importance), average lifetime of components (ALC, 18%), Betti curve features (BCC 15%, BCH), Wasserstein/bottleneck amplitudes.

- **Other applications**: Peak identification (proof-of-concept only, no validation), cloud pattern classification (Ver Hoef et al. 2023), DEM generalization (Corcoran 2019, limited documentation).

**What does NOT exist** (critical gaps this study fills):

1. **Research Gap 1**: No systematic application of Euler characteristic to DEMs despite theoretical proposals
2. **Research Gap 2**: No comparison of persistence vectorization methods (landscapes vs. images vs. scalars) for terrain
3. **Research Gap 3**: No rigorous head-to-head comparisons between TDA and standard geomorphometry (geomorphons, Random Forest)
4. **Research Gap 4**: <5% of TDA-terrain studies use spatial cross-validation despite 28-50% documented performance inflation from ignoring spatial structure
5. **Research Gap 5**: No studies test preprocessing sensitivity (breach-fill vs. raw DEMs) despite DEM conditioning directly altering H₁ topology by removing depressions

### 2.2 Geomorphometry Baselines: The Performance Bar to Match or Exceed

**Current methods this study compares against**:

- **Geomorphons** (Jasiewicz & Stepinski 2013): Pattern recognition via local ternary patterns, 70-95% accuracy, computationally efficient (single DEM scan), implemented in GRASS GIS. **Limitation**: Cannot distinguish depositional vs. erosional processes with similar morphology.

- **Random Forest with terrain features**: Using 20-25 SCORPAN covariates (elevation, slope, curvatures, TWI, TPI at multiple scales), achieves **92-99% overall accuracy** (Kappa 0.83-0.99) for Appalachian province classification in published studies.

- **Deep learning CNNs**: 84-95% accuracy for landform semantic segmentation, but black-box nature limits interpretability and transfer learning fails across regions.

**Documented limitations exploitable by TDA**:

1. Traditional ML treats features independently; doesn't capture topological relationships
2. Geomorphons excel at morphological classification but provide no process distinction
3. Deep learning achieves accuracy but offers minimal interpretability
4. All methods scale-dependent; multi-scale approaches require manual parameter tuning

**Critical insight from Document 5**: "Any new approach must demonstrate clear advantages over geomorphons (efficiency baseline) and deep learning (accuracy ceiling). Without rigorous comparison, reviewers will ask 'why not just use geomorphons?'"

### 2.3 Validation Requirements: Spatial Cross-Validation is Mandatory

**The autocorrelation crisis** (Ploton et al. 2020, *Nature Communications*): Random 10-fold CV yielded R²=0.53 (strong), but spatial CV revealed true R²=0.14 (near-null). Models predicted via spatial proximity, not environmental relationships—**invisible to standard diagnostics**.

**Documented inflation rates**:
- Roberts et al. (2017): 28-40% performance inflation with random CV for ecological/spatial data
- Valavi et al. (2019): Block size must exceed 1.5-2× autocorrelation range
- Meyer et al. (2019): Including lat/lon as features enables data reproduction rather than spatial prediction

**This study's response**: Spatial block cross-validation is non-negotiable. Block size determined via variogram analysis of topological features (not just elevation—topological features may have different autocorrelation ranges). Comparison to random CV explicitly quantifies bias (expected 10-30% accuracy difference).

---

## 3. Methodological Framework: Testbed-Then-Scale Design

### 3.1 Overview: Proof-of-Concept Gates Main Study Commitment

**Two-phase structure prevents methodological failure**:

**Phase I: Proof-of-Concept Testbed (Weeks 1-12, ~3 months)**
- **Objective**: Validate computational pipeline, establish baseline performance, identify optimal methods before scaling
- **Scope**: 2-3 provinces, 40-60 sites, core methods only (EC, standard PH, traditional baselines)
- **Decision gate**: Proceed to main study only if (1) ≥70% province accuracy achieved, (2) per-site processing ≤60 minutes, (3) interpretable patterns emerge
- **Risk mitigation**: If testbed fails, pivot to traditional geomorphometry with lessons learned; still produces publishable negative results

**Phase II: Main Study (Months 4-27, 24 months)**
- **Objective**: Comprehensive methods comparison across full province diversity
- **Scope**: 3-4 provinces, 80-120 sites, all method tiers, spatial transferability testing
- **Contingency**: Sample size reducible to 60 (20/province) if computational limits; scale-specific analysis rather than multi-scale if needed

**Why this design is defensible**: The testbed explicitly tests whether the research is feasible before committing 2 years. Committee members value risk mitigation. The decision gate provides objective criteria for proceed/pivot.

### 3.2 Phase I: Proof-of-Concept Testbed (12 Weeks)

#### 3.2.1 Geographic Scope: Strategic Province Selection

**Three provinces spanning complexity gradient** (40-60 sites total, 15-20 per province):

**Province 1: Blue Ridge (n=20, Positive Control)**
- **Characteristics**: High relief (300-1800m range), complex fold interference, rugged mountains
- **Expected topology**: High H₀ persistence (prominent isolated peaks), moderate H₁ (complex valleys)
- **Why include**: Clear topological structure; favorable test case where TDA should succeed if method is viable

**Province 2: Coastal Plain (n=20, Negative Control)**
- **Characteristics**: Minimal relief (<50m), isotropic, post-orogenic sedimentation
- **Expected topology**: Low H₀/H₁ persistence, minimal topological complexity
- **Why include**: Critical control where topological methods should show weak signal; distinguishes method sensitivity from noise

**Province 3: Piedmont (n=15-20, Discrimination Test)**
- **Characteristics**: Rolling uplands, moderate relief (100-300m), subtle basement fabric
- **Expected topology**: Intermediate signatures between extremes
- **Why include**: Tests method's ability to detect subtle differences; most challenging discrimination

**Site selection protocol**: Stratified random sampling within each province using 1km × 1km windows (native scale for geomorphons comparison). Avoid edge cases (urban, reservoirs, data artifacts). Extract coordinates, download USGS 3DEP 10m DEMs (0.35m vertical RMSE, best available quality for CONUS).

#### 3.2.2 Methods: Graduated Complexity Testing

**Tier 1: Scalar Topological Summaries (Computational Baseline)**

**Euler Characteristic Curves**: Compute χ(t) = β₀(t) - β₁(t) + β₂(t) as function of elevation threshold t. For sublevel filtration of open terrain, β₂ ≈ 0 (verified empirically), simplifying to χ(t) ≈ β₀(t) - β₁(t).

**Features extracted**: Total EC variation (integral of |χ(t)|), peak locations, curve shape (skewness, kurtosis). **Rationale**: Research Gap 1—EC has never been systematically tested on DEMs. If this simple method works, full PH may be unnecessary.

**Computational cost**: ~5 minutes/site including full PH computation to extract Betti numbers.

**Tier 2: Standard Persistent Homology (Core Topological Analysis)**

**Configuration**: Cubical complexes from 10m gridded DEMs (10-100× faster than simplicial alternatives), sublevel filtration (water rising), H₀ (components/peaks) and H₁ (loops/valleys).

**Software**: CubicalRipser (fastest implementation, Bauer 2021 showed >40× faster than GUDHI, >190× faster than Dionysus).

**Vectorization—test THREE approaches**:

1. **Persistence landscapes** (primary): Parameter-free, theoretically stable, ~25-dimensional feature vector. Compute first 5 landscapes, extract L¹, L², L^∞ norms.

2. **Persistence images** (interpretability): 20×20 resolution (standard), Gaussian kernel σ=0.1×max_persistence, yields 400-dimensional vector. Enables visualization of discriminative diagram regions.

3. **Scalar summaries** (efficiency baseline): Total persistence, max persistence, persistence entropy, Betti numbers at median elevation. ~8-dimensional vector.

**Comparison objective**: Does full vectorization (landscapes/images) justify computational cost over simple scalars? This has never been tested for terrain.

**Computational cost**: ~30-45 minutes/site (based on pilot testing with 1km windows).

**Tier 3: Traditional Baselines (Mandatory Comparisons)**

**Geomorphometry features**:
- Elevation statistics (mean, std, range, percentiles)
- Slope (mean, std, median via Horn's method)
- Curvature (profile, plan, tangential statistics)
- TPI at 3 scales (150m, 500m, 1500m radii)
- TWI, TRI computed via WhiteboxTools

**Geomorphons classification**:
- GRASS GIS r.geomorphon, search radius 50 cells (500m), flatness threshold 1°
- Extract proportion of each landform class (10-dimensional feature vector)
- **Critical distinction from PH**: Geomorphons capture local landform type frequencies ("20% ridges, 15% valleys"); PH captures global organizational metrics ("15 long-persistence loops indicating enclosed valleys"). Both topological but different scales.

**Computational cost**: ~5-10 minutes/site

#### 3.2.3 Validation: Rigorous Spatial Cross-Validation

**Classification task**: 3-class province discrimination (Blue Ridge vs. Coastal Plain vs. Piedmont)

**Models tested** (10 total):

1. **Traditional-only**: Random Forest on geomorphometry + geomorphons
2. **Geomorphons baseline**: K-NN on geomorphon proportions alone
3. **EC-only**: Random Forest on Euler characteristic features
4. **PH scalars-only**: RF on scalar persistence summaries
5. **PH landscapes-only**: RF on persistence landscape features
6. **PH images-only**: RF on persistence image features
7. **EC + Traditional**: RF on combined features (hybrid)
8. **PH landscapes + Traditional**: RF on combined (hybrid)
9. **Best topological + Traditional**: Optimal hybrid combination
10. **Ensemble**: Stacking classifier combining top 3 models

**Model configuration**: RF with 500 trees, max_depth=20, balanced class weights. Elastic Net (α=0.7) feature selection with VIF<5 threshold to remove collinear features.

**Primary validation: Spatial Block Cross-Validation (5-fold)**

**Protocol** (follows Roberts et al. 2017, Valavi et al. 2019):

1. **Autocorrelation analysis**: Compute semi-variograms for elevation, slope, TWI, and **all topological features** (critical—topological features may have different ranges than raw elevation). Calculate Moran's I at lags: 1, 5, 10, 15, 20 km.

2. **Block size determination**: Maximum autocorrelation range across all features × 2.0 (conservative). Expected range: 5-15 km based on fold wavelengths; blocks must be >10-30 km to eliminate leakage.

3. **Block assignment**: blockCV R package with systematic or hierarchical clustering ensuring balanced class representation.

4. **Expected challenge**: If topological features show ≥20 km range and study area is ~100 km extent, may have only 3-4 effective blocks. This is acceptable and demonstrates honest spatial validation.

**Secondary validation: Random 5-fold CV (comparison only)**

**Purpose**: Demonstrate inflation from ignoring spatial structure. Expected: 10-30% higher accuracy than spatial CV. **This difference is not a failure—it's proof of methodological rigor.**

**Statistical testing**:
- **McNemar's test**: Paired comparisons between models (matched CV folds)
- **Holm-Bonferroni correction**: 10 models → stringent α adjustment
- **Effect sizes**: Cohen's d for accuracy differences (not just p-values)
- **Bootstrap CI**: 1000 iterations for all metrics (accuracy, precision, recall, F1, kappa)

**Complete reporting**: Confusion matrices for each model, spatial error maps, per-province performance breakdown.

#### 3.2.4 Decision Gate: Objective Criteria for Proceed/Pivot

**Proceed to main study if ANY of these conditions met**:

✅ **Minimum Success** (70% bar):
- At least one topological method achieves ≥70% accuracy (spatial CV)
- Per-site processing ≤60 minutes (scalability confirmed)
- Topological features show statistically significant discrimination (MANOVA p<0.05)

✅ **Moderate Success** (75% bar):
- Topological methods achieve 75-80% accuracy
- Hybrid shows ≥5% improvement over traditional-only (p<0.05, McNemar's)
- Interpretable correlations with geology (H₁ persistence correlates with fold axes in Blue Ridge)

✅ **Strong Success** (80% bar):
- Topological methods achieve ≥80% accuracy matching RF baselines
- Hybrid outperforms by ≥10% (p<0.01)
- Clear method advantages demonstrated (interpretability, transferability)

**Pivot to traditional geomorphometry if**:
- All topological methods <65% accuracy (near-random for 3 classes)
- Computational pipeline fails (>2 hours/site)
- No interpretable patterns emerge from any method

**Publishable even if pivot occurs**: "Why Topological Methods Fail for Low-Relief Terrain: A Negative Results Study" contributes to field by establishing scope limits.

#### 3.2.5 Timeline: 12-Week Proof-of-Concept

**Weeks 1-2**: Data acquisition and preprocessing
- Download USGS 3DEP 10m DEMs (40-60 sites)
- **Preprocessing sensitivity testing** (addresses Research Gap 5):
  - Method 1: No conditioning (raw DEM)
  - Method 2: Breach-fill (removes/fills depressions)
  - Method 3: Artifact removal only (preserves real depressions)
  - Compute bottleneck distance between persistence diagrams across methods
  - Select most appropriate for main study based on stability and artifact removal
- Water body masking, quality control
- **Deliverable**: Clean DEM library + preprocessing sensitivity report

**Weeks 3-4**: Traditional feature extraction
- Geomorphometry (slope, curvature, TPI, TRI, TWI)
- Geomorphons classification
- Elevation statistics
- **Deliverable**: Traditional feature dataset (CSV)

**Weeks 5-7**: Topological feature extraction
- Week 5: Euler characteristic computation (all sites, <2 hours total)
- Weeks 6-7: Persistent homology (CubicalRipser, ~30-40 hours; parallelizable to 5-6 hours with 8 cores)
- Vectorization: Landscapes, images, scalar summaries
- **Deliverable**: Topological feature dataset (CSV) + preprocessing comparison

**Weeks 8-9**: Modeling and validation
- Implement spatial block CV framework (blockCV package)
- Train all 10 models with hyperparameter tuning (inner CV loop)
- Compute performance metrics, statistical significance tests
- **Deliverable**: Results tables, confusion matrices, spatial error maps

**Weeks 10-11**: Interpretation and decision
- SHAP feature importance for top 3 models
- Persistence diagrams for representative sites (Blue Ridge vs. Coastal Plain visualization)
- Computational benchmarking (runtime, memory, scalability estimates)
- Correlation analysis: Topological features vs. geological characteristics
- **Deliverable**: Interpretation framework, computational benchmarks

**Week 12**: Decision gate and reporting
- Testbed report (15-20 pages)
- Decision document: Proceed/modify/pivot with justification
- Presentation (conference-style, 15 slides)
- **Decision outcome**: Explicit recommendation based on objective criteria

**Week 13 (buffer)**: Contingency for delays, additional testing if marginal results

### 3.3 Phase II: Main Study (Months 4-27, 24 Months)

**Executed only if testbed succeeds; design informed by testbed results**

#### 3.3.1 Expanded Geographic Scope

**Full Appalachian physiographic gradient** (80-120 sites total, 20-30 per province):

**Core Provinces** (required for 3-class minimum):
1. **Blue Ridge** (n=25-30): High relief, complex structure, favorable TDA case
2. **Coastal Plain** (n=25-30): Negative control, minimal topological complexity
3. **Valley and Ridge** (n=25-30): Best-case scenario—parallel linear ridges create distinctive H₁ signatures

**Optional 4th Province** (if testbed shows low autocorrelation or strong effects):
4. **Piedmont** (n=20-25): Intermediate complexity, tests subtle signal detection

**Within-province heterogeneity** (acknowledged limitation):
- Valley & Ridge includes structurally distinct sub-regions (Massanutten synclinorium, Nittany anticlinorium)
- Blue Ridge varies from greenschist to granulite facies metamorphism
- **Mitigation**: Stratified sampling across N-S extent; if testbed shows high within-province variance, subset analysis or pairwise comparisons
- **Honest acknowledgment**: Within-province variability may approach between-province differences; documented as scope limitation

**Sample size justification** (power analysis):

**From Document 3**: For MANOVA comparing 5 provinces with moderate spatial autocorrelation (ρ=0.4), effective sample size calculation:
- n_eff = n × (1-ρ)/(1+ρ)
- Target: 200-250 total observations (40-50 per province) for medium effect size (η²=0.06), power=0.8
- With 4 provinces: 80-120 samples achieves n_eff ≈ 50-75 (adequate)

**For nested model comparison** with 25 predictors: 600-900 samples following 20-30 observations-per-predictor rule adjusted for spatial dependency. **This study uses 80-120 sites; therefore limited to ~15-20 predictor features maximum.** Feature selection (Elastic Net) is mandatory, not optional.

#### 3.3.2 Comprehensive Methods Framework

**Expanded from testbed based on results**:

**If testbed shows EC sufficient**:
- Focus on multi-scale EC analysis (1km, 5km, 10km windows)
- Test multi-directional EC for anisotropy detection (Valley & Ridge validation)
- Defer full PH to computational efficiency comparison

**If testbed shows full PH necessary**:
- All three vectorization methods at optimal scale(s)
- Multi-scale integration (3 scales: 1km, 5km, 10km windows addressing fold wavelength mismatch)
- Total feature sets: 240-360 samples (80-120 sites × 3 scales) if multi-scale proven valuable

**Advanced methods** (if computational resources allow):
- Topological Land-Surface Parameters (TLSPs) via sliding windows
- Mapper algorithm for topological regime identification
- Multi-directional methods if testbed shows anisotropy matters

**Baseline expansion**:
- Add XGBoost, Cubist for ML comparison
- Include directional variogram for anisotropic comparison
- Test ensemble methods (stacking, boosting)

#### 3.3.3 Spatial Transferability Testing (Critical for Generalizability)

**Beyond standard CV**: Test geographic transferability to assess whether topological features generalize better than traditional features.

**Protocol**:
1. **Leave-one-province-out CV**: Train on 2-3 provinces, test on held-out province. Repeat for all provinces.
2. **Distance-decay analysis**: Plot accuracy vs. geographic distance from training sites
3. **Hypothesis**: If topological features truly capture universal structural principles, should show smaller accuracy decay with distance than pixel-level features

**Expected outcomes**:
- Accuracy drop of 10-20% for leave-one-out is acceptable and realistic
- If topological features maintain ≥70% on held-out province while traditional drops to 60%, demonstrates transferability advantage
- If both drop similarly, suggests spatial autocorrelation dominates; neither method truly generalizes

**Why this matters**: Transferability testing addresses reviewer question "Does this generalize or just work locally?" It's the difference between a method and a dataset-specific result.

#### 3.3.4 Interpretation Framework: Linking Topology to Geology

**Process-based predictions** (testable hypotheses):

**Valley & Ridge—Fold-Controlled Topography**:
- **Prediction**: High H₁ persistence (parallel ridges enclose elongated valleys creating long-lived 1-cycles), moderate H₀ (ridge crests as components)
- **Validation**: Directional persistence analysis should correlate with documented fold axes (NE-SW, ~045° strike)
- **Test**: Angular correlation r_angular between θ_TDA and θ_reference. Success: r>0.7, p<0.01

**Blue Ridge—Complex Fold Interference**:
- **Prediction**: High H₀ persistence (isolated peaks like Mt. Mitchell taking long to merge), moderate H₁ (complex valley networks, no systematic enclosure)
- **Validation**: Topological complexity metrics should correlate with fold axis intersection density

**Piedmont—Erosional Planation**:
- **Prediction**: Intermediate H₀/H₁ persistence, weak topological anisotropy despite geological fabric
- **Test**: If TDA detects fabric where traditional geomorphometry fails, validates sensitivity to subtle structure

**Coastal Plain—Post-Orogenic Sedimentation**:
- **Prediction**: Low H₀/H₁ persistence, isotropic patterns, minimal topological discrimination
- **Test**: Negative control—topological methods should fail here, establishing baseline noise level

**Critical insight**: This framework enables **failure mode interpretation**. If topological signatures don't align with these predictions, we diagnose whether TDA captures (a) structural relationships (intended), (b) purely morphological patterns (not diagnostic), or (c) data artifacts (method failure).

#### 3.3.5 Statistical Analysis Framework

**Primary: MANOVA on topological feature space**
- Test: Do provinces show statistically significant separation in topological feature space?
- Method: Pillai's Trace (robust to unequal covariances)
- Success criterion: p<0.001, with post-hoc pairwise comparisons (Holm-Bonferroni correction)

**Secondary: Classification performance comparison**
- 10+ models (from testbed + expanded methods)
- Spatial block CV (block size from autocorrelation analysis)
- McNemar's test for all pairwise model comparisons (45+ tests for 10 models)
- Benjamini-Hochberg FDR control (more powerful than Bonferroni for many comparisons)

**Tertiary: Feature importance and interpretation**
- SHAP values for top 3 models (reveals which topological features discriminate)
- Correlation analysis: Topological features vs. geological characteristics
- Spatial error patterns: Where does each method fail geographically?

**Effect size reporting** (not just p-values):
- Cohen's d for accuracy differences between methods
- ΔR² for nested model comparisons
- Matthews Correlation Coefficient (replacing Kappa per Foody 2020 recommendation)

#### 3.3.6 Timeline: 24-Month Main Study

**Months 4-6** (3 months): Data acquisition and preprocessing
- Scale up to 80-120 sites across 3-4 provinces
- Preprocessing pipeline: breach-fill, masking, quality control
- Organize file structure, metadata, site documentation
- **Milestone**: Complete preprocessed DEM library

**Months 7-10** (4 months): Feature extraction at scale
- Traditional geomorphometry (parallelizable, ~10-15 hours total)
- Euler characteristic if testbed showed sufficiency (<2 hours)
- Persistent homology (40-80 hours; with 8-core parallelization: 5-10 hours wall time)
- Vectorization: landscapes, images, summaries
- **Milestone**: Complete feature dataset (all methods, all sites)

**Months 11-13** (3 months): Modeling and primary validation
- Spatial block CV implementation (block size from autocorrelation)
- Train 10-15 models with hyperparameter tuning (nested CV)
- Compute performance metrics, statistical tests
- **Milestone**: Initial classification results

**Months 14-16** (3 months): Spatial transferability testing
- Leave-one-province-out CV
- Distance-decay analysis
- Cross-region generalization assessment
- **Milestone**: Transferability results

**Months 17-19** (3 months): Advanced methods (if resources allow)
- TLSPs via sliding windows (if HPC available)
- Mapper algorithm exploration
- Multi-directional methods refinement
- **Contingency**: If computational limits, focus on core methods interpretation
- **Milestone**: Advanced methods tested OR core methods deeply interpreted

**Months 20-22** (3 months): Comprehensive interpretation
- SHAP feature importance across all models
- Topological-geological correlation analysis
- Spatial error pattern mapping
- Failure mode documentation
- Computational cost vs. accuracy tradeoff quantification
- **Milestone**: Complete interpretation framework

**Months 23-24** (2 months): Thesis writing (first draft)
- Chapter 1: Introduction and literature review
- Chapter 2: Methods (testbed + main study)
- Chapter 3: Results (comprehensive comparison)
- Chapter 4: Discussion and interpretation
- **Milestone**: Thesis draft complete

**Months 25-27** (3 months): Revision and defense
- Thesis revisions based on advisor feedback
- Defense presentation preparation
- Conference abstract submission (GSA or AGU)
- Code repository finalization (GitHub + Zenodo DOI)
- **Milestone**: Thesis defense, master's degree completion

---

## 4. Success Criteria: Three-Tier Framework Ensures Publishable Results

**Critical principle**: Success is defined as **methodological characterization**, not proving TDA superiority. Negative results explicitly valued.

### Tier 1: Minimum Viable Success (Defensible Thesis)

**Required for thesis defense**:
- ✅ ≥70% province discrimination accuracy (spatial block CV)
- ✅ Topological features contribute significantly to best model (p<0.05, McNemar's test)
- ✅ Process-based predictions partially confirmed (e.g., Valley & Ridge shows high H₁ as predicted)
- ✅ Computational feasibility demonstrated (per-site processing ≤60 minutes)
- ✅ Complete failure mode documentation (when/where methods fail)

**Interpretation**: Methods work but may not exceed traditional approaches. Still contributes to field by documenting: (1) which TDA methods are viable for terrain, (2) optimal vectorization approach, (3) computational requirements, (4) scope limits.

**Publication pathway**: *Computers & Geosciences* or *Geomorphology* as methods paper: "Topological Data Analysis for Landscape Classification: A Methodological Evaluation"

### Tier 2: Strong Success (Competitive Performance)

**Indicators of strong success**:
- ✅ ≥80% province discrimination, matching RF baselines (92-99% in literature but expecting lower with spatial CV)
- ✅ Hybrid (TDA + traditional) outperforms either alone by ≥5% (p<0.05, McNemar's)
- ✅ Clear method characterization: EC sufficient vs. full PH necessary, optimal vectorization identified
- ✅ Process predictions strongly confirmed (topological signatures align with geological structure)
- ✅ Some evidence of transferability advantage

**Interpretation**: TDA provides complementary information to traditional methods. Hybrid approach justified by statistical evidence. Establishes conditions where topology adds value.

**Publication pathway**: *Earth Surface Processes and Landforms* or *Geomorphology* (higher-tier venue): "Topological Signatures of Appalachian Landscapes: Quantitative Validation of Physiographic Provinces"

### Tier 3: Exceptional Success (Method Advancement)

**Indicators of exceptional success**:
- ✅ ≥85% accuracy, approaching deep learning benchmarks
- ✅ At least one TDA method improves accuracy ≥10% over traditional alone (p<0.01)
- ✅ Geographic transferability demonstrated: train on provinces A/B, test on C/D with <15% accuracy drop
- ✅ Interpretable features guide geological understanding: SHAP values reveal meaningful patterns (e.g., "H₁ max persistence identifies fold-controlled valleys")
- ✅ Clear computational efficiency advantage identified (e.g., "EC achieves 85% accuracy in 5 min/site vs. RF 87% in 10 min/site")

**Interpretation**: TDA offers measurable advantages justifying adoption by community. Establishes precedent for planetary analog applications.

**Publication pathway**: *Nature Communications* or *Proceedings of the National Academy of Sciences* if combined with Mars analog validation: "Universal Topological Signatures of Landscape Organization: From Appalachian Provinces to Planetary Analogs"

### Valuable Negative Results (Publishable Regardless of Tier)

**If TDA underperforms**:
- ✅ Document precisely where/why methods fail (expected: Coastal Plain, low-relief terrain)
- ✅ Establish computational vs. accuracy tradeoffs
- ✅ Identify scope limits (e.g., "TDA requires ≥100m relief to discriminate")
- ✅ Characterize when traditional methods suffice (e.g., "For isotropic terrain, geomorphons sufficient")

**Publication pathway**: *Environmental Modelling & Software* or *Computers & Geosciences*: "Limits of Topological Data Analysis for Terrain Classification: A Critical Evaluation"

**Key insight**: Honest failure documentation advances field by preventing future wasted effort. "We tested TDA rigorously and found it doesn't work for X" is a valuable contribution.

---

## 5. Data and Computational Strategy

### 5.1 Data Sources: High-Quality, Publicly Available

**Digital Elevation Models**:
- **Primary**: USGS 3DEP 10m Lidar-derived DEMs (0.35m vertical RMSE in non-vegetated mountainous areas)
- **Access**: The National Map (https://apps.nationalmap.gov/downloader/), AWS S3 bulk download
- **Coverage**: ~75% of Appalachian study area with Lidar quality; remainder at 10m from 1/3 arc-second
- **Alternative**: FABDEM v1.2 (30m, 2-4m RMSE, forest/building removed) for consistent cross-regional analysis if needed

**Ground Truth**:
- **Primary**: USGS Fenneman Physiographic Provinces (1:7,000,000 scale, authoritative boundaries)
- **Access**: USGS ScienceBase (vector polygons with attributes)
- **Limitation**: Coarse scale limits local analysis but provides reference standard

**Validation Datasets**:
- State geological surveys for refined boundaries (West Virginia, Virginia, North Carolina)
- Published geomorphic maps for independent validation
- Structural geology maps for directional validation (fold axes in Valley & Ridge)

### 5.2 Computational Pipeline: Modern, Efficient, Reproducible

**Software ecosystem** (all open-source, $0 cost):

**TDA computation**:
- **CubicalRipser**: Fastest for gridded DEMs (C++ with Python wrapper)
- **Giotto-TDA**: Persistence landscapes/images vectorization
- **Alternative**: Ripser.py, GUDHI if needed

**DEM preprocessing**:
- **WhiteboxTools**: Breach-fill, water body masking, terrain derivatives
- **GRASS GIS**: Geomorphons classification (r.geomorphon)

**Machine learning**:
- **scikit-learn**: Random Forest, cross-validation, metrics
- **blockCV** (R): Spatial block cross-validation
- **SHAP**: Feature importance interpretation

**Hardware requirements**:
- **Testbed**: Standard laptop (16GB RAM, 8-core CPU) sufficient
- **Main study**: University HPC preferred (reduces 40-80 hour computation to 5-10 hours with 8-16 cores)
- **Alternative**: AWS EC2 spot instances (estimated $100-300 total for main study)

**Computational cost estimates** (for 80-120 sites):
- Traditional features: 10-15 hours (parallelizable to 2-3 hours)
- EC computation: <2 hours total
- PH computation: 40-80 hours sequential (5-10 hours with 8-core parallel)
- Modeling/CV: 30-45 hours across all models
- **Total main study**: ~100-150 hours computational time
  - Sequential (laptop only): 1-2 weeks continuous
  - Parallel (8 cores): 2-3 days wall time
  - With HPC: 1 day wall time

**Contingency for computational limits**:
- Reduce to 60 sites (20/province) minimum
- Use EC only, defer full PH
- Simplify vectorization (scalar summaries only)
- Sequential processing extends timeline by 1-2 weeks but remains feasible

### 5.3 Reproducibility Standards

**All deliverables publicly available**:

1. **Code repository** (GitHub + Zenodo DOI):
   - Complete pipeline: preprocessing → features → models → results
   - Documented with README, requirements.txt, example data
   - MIT license for maximum reusability

2. **Data** (Zenodo or institutional repository):
   - Extracted feature datasets (sites, all methods)
   - Persistence diagrams for representative sites
   - Site locations and province classifications (CSV)

3. **Thesis** (university repository):
   - Full methods, results, interpretation
   - Citable reference for future researchers

4. **Presentation materials** (if conference accepted):
   - Slides shared via ResearchGate or personal website

**FAIR principles**: Findable (DOI), Accessible (open archive), Interoperable (standard formats), Reusable (rich documentation).

**Random seed management**: All stochastic processes (RF training, CV splits) use documented seeds (e.g., seed=42). Sensitivity tested with 10-30 replications, reporting mean ± SD across seeds.

---

## 6. Risk Mitigation and Contingency Plans

### 6.1 Testbed Failure (Most Critical Risk)

**Risk**: Testbed shows all topological methods <65% accuracy or computational pipeline fails

**Probability**: Low-Medium (testbed explicitly designed to test this)

**Impact**: High (determines if main study proceeds)

**Mitigation**:
1. Testbed includes negative control (Coastal Plain) where weak signal expected
2. Multiple method tiers tested (if PH fails, EC might work)
3. Computational benchmarking identifies bottlenecks early
4. Decision gate prevents wasting 2 years on unworkable approach

**If testbed fails completely**:
- **Pivot**: Focus thesis on traditional geomorphometry with lessons learned
- **Value**: "Why Topological Methods Fail: A Negative Results Study" still publishable
- **Alternative**: Simplify to EC-only approach (much faster, might suffice)

### 6.2 Methods Don't Show Clear Differences

**Risk**: All topological methods (EC, PH landscapes, PH images) perform similarly

**Probability**: Medium (possible that simple EC captures most information)

**Impact**: Medium (reduces novelty but doesn't invalidate research)

**Response**:
- **This is still valuable**: "Simple EC sufficient; full PH unnecessary for province discrimination"
- **Computational recommendation clear**: Use faster EC, avoid PH overhead
- **Reduces barrier for future researchers**: No need for complex vectorization
- **Publishable outcome**: Establishes computational efficiency baseline

**Key insight**: Understanding what's NOT needed is as valuable as identifying optimal methods.

### 6.3 Hybrid Approaches Don't Outperform Traditional-Only

**Risk**: TDA+Traditional performs no better than Traditional alone (topological features redundant)

**Probability**: Medium (Syzdykbayev 2024 showed pure TDA had issues; hybrid helped but margin unclear)

**Impact**: Low-Medium (reduces TDA practical value but doesn't invalidate thesis)

**Response**:
- **Document negative result rigorously**: "Topological Features Redundant with Traditional Geomorphometry for Province Classification"
- **Identify specific redundancies**: Which topological features correlate with which traditional features? (SHAP, VIF analysis)
- **Test if TDA provides unique interpretability**: Even if accuracy similar, does topology aid geological understanding?
- **Contribute to field**: Prevents future wasted effort, establishes scope limits

**Publication pathway**: *Computers & Geosciences* or *Environmental Modelling & Software* (methods journals accept well-documented negative results)

### 6.4 Computational Resources Insufficient

**Risk**: PH computation takes >60 min/site, making 80-120 site study infeasible

**Probability**: Low-Medium (pilot data suggests 30-45 min/site, but could underestimate)

**Impact**: Medium (requires timeline extension or scope reduction)

**Contingency plans** (in order of preference):
1. **Seek HPC access**: University clusters often provide allocations to graduate students (UGA GACRC, similar)
2. **Cloud computing**: AWS/Google Cloud spot instances: ~$100-300 for entire main study
3. **Reduce sample size**: Fall back to 60 sites (20/province) minimum
4. **Simplify vectorization**: Use scalar summaries only (much faster), defer landscapes/images
5. **Focus on EC**: If PH too slow, comprehensive EC analysis still valuable contribution

**Timeline adjustment**: Extend feature extraction by 1-2 months (still completes within 2.5 years)

**Justification**: Even n=60 with simplified methods exceeds most existing TDA-terrain studies (typically n<50)

### 6.5 Spatial Autocorrelation Degrades Performance

**Risk**: Spatial block CV shows accuracy 20-40% lower than random CV

**Probability**: High (spatial autocorrelation well-documented in terrain data)

**Impact**: Low (**expected and rigorously addressed**)

**This is a feature, not a bug**:
- **Demonstrates methodological rigor**: Using proper spatial CV is the point
- **Honest performance estimates**: Field needs realistic baselines, not optimistic inflated numbers
- **Contributes to literature**: Documents importance of spatial validation for TDA features
- **Informs future work**: Autocorrelation range estimates guide blocking strategies

**If spatial CV reveals very low accuracy (<60%)**:
- Still publishable: "Topological Features Show Strong Spatial Dependence: Implications for Terrain Classification"
- Recommend leave-region-out validation for future studies
- Establishes that topological methods work locally but don't generalize well (important to know)

### 6.6 Overall Risk Philosophy

**Key principle: Multiple success pathways ensure thesis completion regardless of specific outcomes**

**Success if ANY of these occur**:
- ✅ At least one topological method outperforms traditional (exceptional success)
- ✅ Topological methods perform comparably but provide unique interpretability (strong success)
- ✅ Rigorous negative results documenting failure modes (minimum success)
- ✅ Methodological contribution (EC for DEMs, vectorization comparison) (minimum success)
- ✅ Computational feasibility analysis for future researchers (minimum success)

**Only true failure**:
- Complete technical impossibility (computational pipeline can't be built)
- **This risk mitigated by testbed validating pipeline before main study commitment**

**Thus: Thesis produces defensible, publishable results across wide range of empirical outcomes**

---

## 7. Broader Impacts and Contributions

### 7.1 Methodological Contributions to TDA-Geoscience Field

**Primary contributions**:
1. **First systematic application** of Euler characteristic to DEMs (Research Gap 1)
2. **First comparison** of persistence vectorization methods for terrain (Research Gap 2)
3. **First rigorous assessment** of TDA vs. traditional geomorphometry with identical validation (Research Gap 3)
4. **First comprehensive spatial validation** of TDA features for terrain (Research Gap 4)
5. **First preprocessing sensitivity analysis** for topological terrain features (Research Gap 5)

**Decision framework output**: "Use method X when landscape has characteristics Y"—enables evidence-based method selection for future researchers.

### 7.2 Validation of Century-Old Geological Knowledge

**Quantifying qualitative expertise**: Fenneman's 1938 classifications based on expert observation never rigorously validated with topological metrics. This study tests whether qualitative descriptions ("strongly folded," "rolling uplands") correspond to measurable topological differences.

**Two possible outcomes, both valuable**:
1. **Confirmation**: Topological metrics validate expert classifications, providing quantitative support for geological understanding
2. **Refinement**: Topological analysis reveals sub-province structure or transition zones not captured by coarse boundaries, advancing understanding

### 7.3 Precedent for Planetary and Submarine Applications

**Strategic positioning**: Appalachian provinces with authoritative ground truth provide ideal testbed. Success here enables confident application to:
- **Mars analog site identification**: Do Earth-Mars regions with similar topological signatures represent true process analogs?
- **Submarine terrain classification**: Where bathymetry data available but ground truth sparse
- **Paleotopographic reconstruction**: Analyzing ancient landscapes from incomplete records

**Transferability as key selling point**: If topological features show better geographic generalization than traditional features, justifies application to domains where training data sparse.

### 7.4 Open Science Impact

**Reducing barrier to entry**:
- **Code repository** with documentation enables replication
- **Clear protocols** for spatial validation prevent methodological pitfalls
- **Computational benchmarks** inform feasibility for other researchers
- **Negative results** prevent wasted effort on unviable approaches

**Training value**: Graduate students learn:
- Rigorous validation design (spatial CV, multiple testing)
- Integration of mathematical methods with geoscience
- Honest scientific communication (limitations explicitly stated)
- Reproducible research practices

---

## 8. Alignment with Funding Priorities

**NSF Geomorphology and Land-Use Dynamics (GLD)**:
- **Intellectual Merit**: Novel quantitative validation of physiographic provinces; first comprehensive TDA methods comparison for terrain
- **Broader Impacts**: Establishes rigorous protocols for emerging methods; training in interdisciplinary research; open-source tools

**NSF Collaborations in AI and Geosciences (CAIG)** (if co-PI with TDA expert):
- **Geosciences Advancement**: Fundamentally new method for landscape classification
- **AI Impact**: Development of topological features for spatiotemporal data
- **Partnerships**: Clear plan for cross-training and expertise integration

**Budget justification** (if funded):
- HPC allocation request: 150-200 CPU-hours (enables parallelization)
- Conference travel: AGU or GSA presentation (~$1,500)
- **Total unfunded project cost**: $0-300 (optional cloud computing)

**Feasibility for unfunded thesis**: All data public, all software open-source, standard laptop adequate for testbed, university HPC access often free for graduate students.

---

## 9. Expected Deliverables and Timeline Summary

### 9.1 Testbed Deliverables (Month 3)

1. **Technical report** (15-20 pages): Methods, results, interpretation, decision
2. **GitHub repository**: Replication code with documentation
3. **Decision document**: Proceed/modify/pivot with objective justification
4. **Presentation**: Conference-style (15 slides) for lab meeting

### 9.2 Main Study Deliverables (Month 27)

1. **Master's thesis** (100-150 pages):
   - Chapter 1: Introduction and literature review (establish gaps)
   - Chapter 2: Methods (testbed + main study protocols)
   - Chapter 3: Results (comprehensive comparison, all models)
   - Chapter 4: Discussion (interpretation, failure modes, future work)
   - Chapter 5: Conclusions (methodological contributions, scope limits)

2. **Conference presentation**: GSA or AGU (oral or poster)

3. **Code repository** (GitHub + Zenodo DOI): Complete pipeline, documented

4. **Publication-ready manuscript** (optional, often completed post-defense):
   - Target journals depend on success tier (Section 4)
   - Draft completed during Months 23-27

### 9.3 Complete Timeline (30 Months Total)

**Phase I: Testbed (Months 1-3)**
- Weeks 1-2: Data acquisition, preprocessing, sensitivity testing
- Weeks 3-4: Traditional feature extraction
- Weeks 5-7: Topological feature extraction
- Weeks 8-9: Modeling and validation
- Weeks 10-11: Interpretation and decision analysis
- Week 12: Decision gate and reporting
- Week 13: Buffer

**Phase II: Main Study (Months 4-27)**
- Months 4-6: Data acquisition and preprocessing (scale-up)
- Months 7-10: Feature extraction at scale
- Months 11-13: Modeling and primary validation
- Months 14-16: Spatial transferability testing
- Months 17-19: Advanced methods (or core methods refinement)
- Months 20-22: Comprehensive interpretation
- Months 23-24: Thesis writing (first draft)
- Months 25-27: Revision and defense

**Total duration**: 30 months = 2.5 years (standard master's program)

---

## 10. Conclusion: A Defensible Path to Methodological Contribution

This proposal addresses a genuine research gap—the lack of systematic evaluation of TDA methods for terrain classification—using a rigorous, testbed-validated design that ensures publishable results regardless of specific empirical outcomes.

**What makes this defensible**:

1. **Honest framing**: Does NOT claim TDA superiority; positions as methodological characterization
2. **Risk mitigation**: Testbed gates main study commitment; objective decision criteria
3. **Multiple success pathways**: Valuable results whether TDA outperforms, matches, or underperforms traditional methods
4. **Rigorous validation**: Spatial CV mandatory, multiple testing corrections applied, complete failure mode documentation
5. **Embraces hybrid approaches**: Following Syzdykbayev 2024 lesson that TDA+traditional often best
6. **Fills documented gaps**: EC for DEMs, vectorization comparison, spatial validation, preprocessing sensitivity
7. **Appropriate scope**: 80-120 sites achievable for solo master's student in 2 years with testbed validation
8. **Computational realism**: Detailed benchmarks, contingency plans, HPC strategy

**What this is NOT**:
- ❌ Advocacy for TDA replacing traditional methods
- ❌ Assumption that TDA will outperform existing approaches
- ❌ Overly ambitious multi-planet comparative study
- ❌ Claim of solving century-old problems with new method

**What this IS**:
- ✅ Rigorous assessment of untested methods filling documented gaps
- ✅ Honest evaluation establishing when/where topological approaches add value
- ✅ Systematic comparison against state-of-art baselines
- ✅ Foundation for future applications (planetary analogs, submarine terrain)
- ✅ Contribution regardless of whether TDA "wins"

**The central scientific contribution**: By the end of this study, the geomorphometry community will have evidence-based guidance on when to use topological methods, which TDA approaches are worth the computational cost, and under what landscape conditions traditional methods suffice. This moves the field from speculation ("TDA might help with terrain") to knowledge ("TDA helps for X, fails for Y, and costs Z to compute").

**Bottom line**: This is a landmark methodological study because it rigorously tests untested methods, documents all outcomes honestly, and provides actionable guidance for future researchers. Success = understanding the methods landscape, not proving any particular method's superiority.

---

## References

[Complete bibliography from Documents 2, 3, 4, 5 including:
- Bhuyan et al. 2024 (*Nature Communications*) on landslide classification
- Syzdykbayev et al. 2020, 2024 on TDA for terrain
- Roberts et al. 2017, Ploton et al. 2020 on spatial validation
- Jasiewicz & Stepinski 2013 on geomorphons
- Fenneman & Johnson 1946 on physiographic provinces
- Cohen-Steiner et al. 2007 on persistence stability
- Bubenik 2015 on persistence landscapes
- Adams et al. 2017 on persistence images
- Valavi et al. 2019 on spatial CV
- Plus 40+ additional references from documents]

---

## Appendices

**Appendix A**: Detailed computational specifications (hardware, software versions, parameter settings)

**Appendix B**: Complete statistical testing protocol (MANOVA setup, McNemar's test implementation, correction methods)

**Appendix C**: Preprocessing sensitivity protocol (breach-fill vs. raw DEM comparison, bottleneck distance calculation)

**Appendix D**: Supplementary figures (persistence diagrams for each province, spatial error maps, feature importance plots)

**Appendix E**: Code repository structure (GitHub organization, file descriptions, replication instructions)
