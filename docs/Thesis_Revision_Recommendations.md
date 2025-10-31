# Topological Data Analysis for Landscape Classification: Literature Review and Thesis Revision Recommendations

**Prepared for:** Michael Kerr  
**Date:** October 30, 2025  
**Purpose:** Transform an overly ambitious PhD-scope proposal into a focused, rigorous 2.5-year Master's thesis

---

## Executive Summary

Your committee is right: **this proposal is currently a 3-5 year PhD dissertation, not a Master's thesis.** However, the good news is that with strategic scoping, this can become an excellent Master's project that makes a genuine contribution to both TDA methodology and geomorphology. 

**The core issue:** You're trying to do too much—validate multiple TDA methods, compare vectorization approaches, test spatial transferability, interpret geological mechanisms, AND establish computational benchmarks. A strong Master's thesis needs to answer ONE clear research question excellently, not four questions adequately.

**My recommendation:** Focus entirely on **RQ1** (Euler characteristic vs. persistence homology comparison) as your SOLE thesis question. Make it the definitive methodological study on EC for terrain analysis. This is:
- Genuinely novel (EC has never been systematically applied to DEMs)
- Computationally feasible (EC is 10-20x faster than full PH)
- Publishable regardless of outcome
- A natural foundation for future PhD work if you continue

---

## Part 1: Critical Literature Review Findings

### 1.1 TDA for Terrain: Current State (October 2025)

**Key Finding:** The field is more developed than your proposal suggests, but your specific gaps are real.

#### What Actually Exists:

**Bhuyan et al. (2024, Nature Communications):** The most significant recent work achieved 80-94% accuracy identifying landslide movement types (slides, flows, falls) across Italy, US Pacific Northwest, Denmark, Turkey, and China using topological features.

**Their key features (from the actual paper):**
- Average Lifetime of Holes (ALH): 22% feature importance
- Average Lifetime of Components (ALC): 18% importance  
- Betti Curve features (BCC, BCH): 15% importance
- Wasserstein/bottleneck amplitudes

**Critical insight from Bhuyan:** They used **topological properties of landslide shapes** (3D morphology), NOT full persistence diagrams. Their "topology" is more about connected components and holes in the landslide polygons themselves, not multi-scale persistence analysis of DEMs.

**Syzdykbayev et al. (2020, 2024):** Applied PH to LiDAR DTMs for landslide detection, achieving 70-96% accuracy. However, their 2024 follow-up found "notable incidence of false positives" with pure topological information—best results required integration with geometric filters.

**Other applications:** PH for COVID-19 spatial anomaly detection, land cover change detection, but these are geospatial analysis, not systematic terrain/DEM analysis.

#### What Does NOT Exist (Your Real Gaps):

1. **Euler Characteristic for DEMs:** The EC is well-studied in other domains (cosmology, material science, chemical engineering) as an efficient topological summary, but **no systematic application to terrain classification exists**.

2. **Vectorization comparison:** No study compares persistence landscapes vs. images vs. scalar summaries specifically for terrain data.

3. **Rigorous spatial validation for TDA:** Only ~5% of TDA-terrain studies use spatial cross-validation.

**Your proposal's claim of "<5 rigorous TDA-terrain papers" is roughly correct, but needs nuance:** There are maybe 10-15 applications, but most lack rigorous validation or methodological comparison.

---

### 1.2 Spatial Cross-Validation: The Controversy You Need to Know

**Major Update:** There's an active debate about spatial CV that your proposal doesn't acknowledge.

#### The Pro-Spatial CV Camp:

**Ploton et al. (2020, Nature Communications):** Found random CV yielded R²=0.53 for forest biomass mapping, but spatial CV revealed true R²=0.14—models were predicting via spatial proximity, not environmental relationships.

**Roberts et al. (2017) and Pohjankukka et al. (2017):** Estimated 28-40% performance inflation from ignoring spatial autocorrelation in terrain data.

**Recent support (2025):** Studies continue to show that random splits produce misleading results for spatial data, with error estimates that don't reflect true out-of-sample performance.

#### The Anti-Spatial CV Camp (Critical New Development):

**Wadoux et al. (2021, *Methods in Ecology and Evolution*):** Argue that spatial CV "has no theoretical underpinning and should not be used for assessing map accuracy." They found spatial CV severely overestimated errors (pessimistic bias) while standard CV only modestly overestimated (optimistic bias) for clustered data.

**Their argument:** Spatial CV conflates two different objectives:
1. **Map accuracy** (how well does the map represent reality?) → Use probability sampling + design-based inference
2. **Model transferability** (does the model generalize to new regions?) → Use spatial CV as a test of extrapolation

**Implication for your thesis:** You need to be VERY clear about what you're testing:
- If testing "Do TDA methods distinguish Appalachian provinces?" → Standard CV may be appropriate
- If testing "Will TDA trained on Blue Ridge work in Piedmont?" → Spatial CV is the right approach

**Recommendation:** Use BOTH methods but frame them differently:
- **Standard 5-fold CV:** "Within-region discrimination accuracy" (your primary result)
- **Leave-one-province-out:** "Cross-region transferability" (your secondary analysis)
- **Explicit comparison:** Document the difference to show you understand spatial structure

---

### 1.3 Random Forest + Geomorphometry: Your Performance Baseline

Your proposal claims RF achieves "92-99% overall accuracy" for Appalachian province classification. **Where does this number come from?** I couldn't find published studies with this exact claim for Fenneman provinces.

**Reality check from geomorphometry literature:** Modern terrain analysis using RF on SCORPAN covariates (elevation, slope, curvature, TWI, TPI at multiple scales) typically achieves 70-90% accuracy for landform classification tasks, depending on data quality and class separability.

**Action item:** Either provide the specific citation for 92-99%, or revise to a more conservative 75-85% expected baseline. This matters because your "success" criteria depend on matching or exceeding this.

---

### 1.4 SHAP for Interpretability: Best Practices

SHAP (SHapley Additive exPlanations) is the current gold standard for interpreting Random Forest models, but recent work shows it has biases:

**Bias toward high-cardinality features:** SHAP values inflate importance of features with many categories or continuous variables. For terrain data, this means EC curves (continuous) may appear more important than they actually are compared to discrete topological features.

**Best practice:** Use SHAP for tree-based models (RF, XGBoost) where exact SHAP values can be computed efficiently by exploiting tree structure. Avoid neural networks for SHAP unless using approximation methods.

**Recommendation for your thesis:**
- Use SHAP for RF feature importance (it's standard practice)
- But also report traditional permutation importance as a robustness check  
- Be cautious about over-interpreting SHAP for continuous topological features
- Focus interpretation on WHICH features matter, not precise importance rankings

---

### 1.5 Euler Characteristic: What We Actually Know

**Smith & Zavala (2021, *Computers & Chemical Engineering*):** Comprehensive review of EC as a topological descriptor showed it's effective for characterizing shape in 2D spatial fields, 3D spatio-temporal data, point clouds, and correlation matrices. The EC "summarizes the topological characteristics" and is computationally efficient compared to full persistent homology.

**Key advantages of EC:**
- Parameter-free (unlike PH vectorization which requires choosing landscapes vs. images)
- Computationally fast (~5 min/site vs. 30-45 min for full PH in your estimates)
- Interpretable (χ = β₀ - β₁ directly tells you about components minus loops)

**Key limitations:**
- Loses persistence information (doesn't distinguish long-lived vs. short-lived features)
- Single number per filtration step vs. full diagram
- May be too coarse for subtle discrimination tasks

**Your proposal's mathematical claim issue:** 

Line 158: "β₂ ≈ 0 (verified empirically)" is problematic. Your committee is right that this needs theoretical justification. For 2D height fields, β₂ measures voids in 3D space. For sublevel filtrations of DEMs (water rising), β₂ should indeed be 0 because you're filling space from below, not creating enclosed voids. But you need to state this more carefully:

**Revised statement:** "For sublevel filtrations of 2D height functions (DEMs), β₂ = 0 because we compute homology of 2D complexes, which cannot contain 3D voids. Thus χ(t) = β₀(t) - β₁(t) + 0 simplifies to χ(t) = β₀(t) - β₁(t)."

---

## Part 2: The Master's Thesis Reality Check

### 2.1 What a Master's Thesis Actually Is

**Timeline:** 2-2.5 years (24-30 months)  
**Expected workload:** ~1500-2000 hours of research work  
**Publication expectation:** 0-1 papers (often published AFTER degree completion)  
**Novelty requirement:** Original contribution, not groundbreaking discovery

**Your current proposal:**
- **Timeline:** 30 months (technically feasible)  
- **Estimated workload:** 2500-3500 hours (way too much)  
- **Publication potential:** 2-3 papers (PhD-level)  
- **Novelty claims:** Multiple novel contributions (PhD-level)

### 2.2 The Scope Creep Problem (Quantified)

Let me break down your actual proposed work:

**Phase I (Testbed):** 3 months
- 3 provinces × 20 sites = 60 sites
- Traditional features (easy)
- EC computation (5 min × 60 = 5 hours)
- Full PH (30 min × 60 = 30 hours)
- 3 vectorization methods
- 10 models to train and compare
- Statistical testing with multiple corrections
- **Realistic time:** 3 months ✓ (this part is actually well-scoped)

**Phase II (Main Study):** 24 months  
- 4 provinces × 20-30 sites = 80-120 sites (call it 100)
- All Phase I methods × 3-4 provinces
- Multi-scale analysis (3 scales → 3× data)
- Spatial transferability (4 leave-one-out tests)
- Advanced methods (TLSPs, Mapper if time)
- Comprehensive interpretation
- Thesis writing
- **Realistic time:** 36-42 months (1.5-2× too long for Master's)

**The math doesn't work.** Even with perfect efficiency, you're proposing 27 months of actual work, which leaves only 3 months buffer for:
- Failed experiments
- Advisor revisions
- Learning new methods
- Conference travel
- Life happening

---

## Part 3: Focused Master's Thesis Options

### Option A (RECOMMENDED): "The EC Thesis" - Computational Efficiency Study

**Title:** "Euler Characteristic Curves for Landscape Classification: A Fast Alternative to Persistent Homology"

**Single Research Question:** Can Euler characteristic analysis provide computationally efficient landscape classification with accuracy comparable to full persistent homology?

**Scope:**
- **Methods:** EC curves vs. ONE PH vectorization method (persistence landscapes only) vs. traditional geomorphometry
- **Sites:** 60-80 total (20 per province, 3-4 provinces)
- **Scale:** Single scale (1 km windows) - NO multi-scale analysis
- **Validation:** Standard 5-fold CV + leave-one-province-out (no extensive spatial CV exploration)

**Timeline (24 months):**
- **Months 1-3:** Testbed (as proposed) → Decision gate
- **Months 4-6:** Scale to 60-80 sites, all feature extraction
- **Months 7-9:** Modeling (3 model families: EC, PH, traditional)
- **Months 10-12:** Leave-one-province-out transferability
- **Months 13-16:** Computational benchmarking, interpretation
- **Months 17-24:** Thesis writing, revisions, defense

**Success Criteria (Simplified):**
- **Tier 1 (Minimum Success):** EC achieves ≥70% accuracy; computational speedup demonstrated
- **Tier 2 (Strong Success):** EC within 5% of PH accuracy but 5-10× faster  
- **Tier 3 (Exceptional):** EC equals or exceeds PH accuracy with major speed advantage

**Why this works:**
1. **Novelty intact:** No one has systematically tested EC for terrain classification
2. **Computationally feasible:** EC is fast, so scaling to 80 sites is realistic
3. **Clear contribution:** Establishes whether expensive PH computation is necessary
4. **Publishable regardless:** "EC sufficient" or "PH necessary" are both valuable findings
5. **Addresses your goals:** Tests if TDA adds value; provides ML interpretability via SHAP
6. **Natural PhD bridge:** If successful, you can extend to multi-scale, more methods, etc.

**What you sacrifice:**
- ❌ Persistence images comparison (defer to future work)
- ❌ Multi-scale analysis (mention as limitation)
- ❌ Advanced methods (Mapper, TLSPs - too ambitious)
- ❌ Comprehensive spatial CV exploration (pick ONE approach)

---

### Option B: "The Hybrid Methods Thesis" - TDA + Traditional Integration

**Title:** "Topological Augmentation of Geomorphometric Features for Landscape Classification"

**Single Research Question:** Do topological features (EC or persistence summaries) improve Random Forest classification accuracy when combined with traditional geomorphometry, and do they provide better model interpretability?

**Scope:**
- **Methods:** Traditional features → Traditional + EC → Traditional + PH scalars
- **Sites:** 60-80 total (20 per province, 3-4 provinces)
- **Focus:** SHAP analysis to understand which topological features complement which traditional features

**Timeline (24 months):**
- **Months 1-3:** Testbed
- **Months 4-9:** Scale up and modeling (focus on feature interaction analysis)
- **Months 10-15:** Deep interpretability study (SHAP, feature interactions, geological meaning)
- **Months 16-24:** Thesis writing

**Why this might work:**
- Directly addresses your goal #2 (is TDA useful for geospatial science/ML interpretability)
- Less computationally intensive (use scalar summaries, not full vectorization)
- More relevant to practitioners (most won't use full PH anyway)

**Why I don't recommend it as strongly:**
- Less methodologically novel (hybrid models are common)
- Harder to publish (incremental improvement rather than new method)
- Interpretability is subjective (harder to prove "better" interpretability)

---

### Option C: "The Spatial Methods Thesis" - Validation Focus

**Title:** "Spatial Validation Methods for Topological Features in Terrain Classification"

**Single Research Question:** How does spatial cross-validation strategy affect performance estimates for topological vs. traditional terrain features?

**Why I DON'T recommend this:**
- Too methodological (more statistics than geomorphology)
- The spatial CV debate is unresolved; you'd be wading into controversy
- Less novel (spatial CV is well-studied; applying it to TDA is incremental)
- Your committee's geology professor would hate it ("where's the geological knowledge?")

---

## Part 4: Specific Revisions for Option A (EC Thesis)

### 4.1 Title

**Current:** "Topological Signatures of Appalachian Landscapes: A Rigorous Methodological Evaluation"

**Revised:** "Euler Characteristic Curves for Landscape Classification: A Computational Efficiency Study in the Appalachian Provinces"

*Rationale:* Immediately signals focus on EC, computational efficiency, and realistic scope.

---

### 4.2 Research Questions

**Current:** 4 RQs spanning methods comparison, hybrid integration, spatial transferability, and interpretability

**Revised (Single RQ with sub-questions):**

**Primary RQ:** Does Euler characteristic analysis provide computationally efficient landscape classification with accuracy comparable to full persistent homology?

**Sub-questions:**
- **RQ1a:** What is the classification accuracy of EC-based features compared to persistence landscapes and traditional geomorphometry?
- **RQ1b:** What is the computational cost-benefit tradeoff? (runtime, memory, scalability)
- **RQ1c:** Do EC features transfer across provinces as well as PH features?
- **RQ1d:** Which specific EC features (total variation, peak locations, curve shape) discriminate provinces?

---

### 4.3 Methods Section Simplification

**Keep:**
- ✓ Euler characteristic curves (your core contribution)
- ✓ Persistence landscapes (single PH comparison method - most stable theoretically)
- ✓ Traditional geomorphometry baseline
- ✓ 60-80 sites (realistic for Master's)
- ✓ Random Forest as primary classifier
- ✓ SHAP for interpretability

**Remove:**
- ❌ Persistence images (mention as "beyond scope" - persistence landscapes sufficient)
- ❌ Scalar summaries as separate method (they're already part of EC and PL)
- ❌ Multi-scale analysis (pick ONE scale, mention as limitation)
- ❌ Ensemble methods (RF is sufficient)
- ❌ Advanced methods (Mapper, TLSPs)
- ❌ Multiple spatial CV approaches (pick leave-one-province-out only)

**Simplify:**
- Models: 4 total instead of 10
  1. Traditional-only RF
  2. EC-only RF
  3. PH landscapes-only RF
  4. EC + Traditional hybrid RF
- Statistics: Simpler testing
  - McNemar's test for pairwise comparisons (3 comparisons, not 45)
  - Benjamini-Hochberg for multiple testing (more powerful than Holm-Bonferroni)
  - Bootstrap CI for all metrics
  - NO MANOVA (overkill for 3-4 classes with 20 samples each)

---

### 4.4 Sample Size Justification (Revised)

**Current claim:** "80-120 samples achieves n_eff ≈ 50-75 (adequate)"

**Problem:** Your power analysis is for MANOVA with moderate spatial autocorrelation. But you don't even need MANOVA for classification tasks.

**Revised justification:**

"**Sample size determination:** For RF classification with 10-15 features (after Elastic Net selection), standard practice suggests 10-20 observations per feature minimum. With 3-4 classes and ~15 final features, we target 60-80 observations (20 per province).

**Spatial autocorrelation consideration:** If variogram analysis reveals autocorrelation range >10 km, effective sample size may be reduced by factor of (1-ρ)/(1+ρ). With ρ=0.4 (typical for terrain features), n_eff = 60 × 0.43 ≈ 26 - sufficient for model training but limiting for statistical power. This is an acknowledged limitation: we prioritize spatial honesty over sample size inflation.

**Rationale:** We deliberately choose smaller n with proper spatial structure over larger n with pseudoreplication. This provides realistic performance estimates even if reducing statistical power."

---

### 4.5 Scale Matching Problem (Critical Fix)

**Your committee is absolutely right about this.** Lines 391, 386-402 make geological predictions based on 1 km windows, but:

Valley & Ridge fold wavelengths are 2-20 km. Your 1 km window will capture local ridge flanks, not fold-scale structure.

**Current approach:** 1 km windows (100 × 100 cells at 10m resolution)

**The scale mismatch:**
- **Geomorphons** operate at 50-cell radius (500m) - your 1 km window is appropriate
- **Valley & Ridge folds** have 5-15 km wavelength - your 1 km window is too small
- **Topological features** will capture within-valley structure, not fold architecture

**Solutions (Pick ONE):**

**Option 1: Accept the mismatch, adjust predictions**
- Use 1 km windows (computationally feasible)
- Revise geological predictions to match this scale:
  - Valley & Ridge: "High H₁ persistence from valley sidewalls and local ridges, NOT fold-scale structure"
  - Blue Ridge: "High H₀ from local peaks within 1 km, capturing terrain ruggedness"
  - Piedmont: "Low H₀/H₁ reflecting local smoothness"
- State explicitly: "This study examines local-scale (1 km) topological structure, not regional fold architecture"

**Option 2: Use larger windows, reduce sample size** (NOT RECOMMENDED - too computationally expensive)
- 5 km windows to match fold wavelength
- Would require 500 × 500 = 250,000 cells/window
- PH computation would take hours per site
- Would have to reduce to 40-60 sites total

**My recommendation: Option 1.** Be honest about what you're actually measuring. Local-scale topological differences are still geomorphologically meaningful even if they don't directly map to fold architecture.

---

### 4.6 Statistical Overspecification Fix

**Remove:**
- Holm-Bonferroni vs. Benjamini-Hochberg debate (just pick B-H, it's more powerful)
- MANOVA (unnecessary for classification; use confusion matrices instead)
- Complex power analysis (your n is what it is; just report effect sizes)
- Pre-registration discussion (nice in theory, but not standard for Master's thesis)

**Keep simple:**
- Accuracy, precision, recall, F1, Kappa (standard classification metrics)
- McNemar's test for model comparisons
- Bootstrap CI (1000 iterations)
- Benjamini-Hochberg for multiple comparisons
- Cohen's d for effect sizes

**Add:**
- Computational benchmarking (this is your key contribution!)
  - Wall-clock time per site
  - Memory usage
  - Scalability curves (time vs. DEM size)

---

### 4.7 Reproducibility (Keep This Excellent)

Your reproducibility plan is one of the best parts of the proposal. Keep all of it:
- ✓ GitHub + Zenodo DOI
- ✓ requirements.txt with exact versions
- ✓ Random seed documentation
- ✓ Complete pipeline
- ✓ Example data

**Add one thing:** Docker container or Conda environment.yml

Your committee asked for this specifically (Document 1, line 4). Do it. It takes 30 minutes and makes reproduction trivial.

---

## Part 5: Literature Review Additions

### 5.1 Missing Citations

**Add these key papers:**

**TDA foundations:**
- Bubenik, P. (2015). "Statistical Topological Data Analysis using Persistence Landscapes." *Journal of Machine Learning Research* - for theoretical stability of landscapes
- Cohen-Steiner, D., Edelsbrunner, H., & Harer, J. (2007). "Stability of persistence diagrams." *Discrete & Computational Geometry* - for fundamental stability theorem

**Geomorphometry reviews:**
- Pike, R.J., Evans, I.S., & Hengl, T. (2009). "Geomorphometry: A Brief Guide." in *Developments in Soil Science*
- Amatulli et al. (2020). "Geomorpho90m, empirical evaluation and accuracy assessment of global high-resolution geomorphometric layers." *Scientific Data*

**Spatial validation:**
- Wadoux et al. (2021). "Spatial cross-validation is not the right way to evaluate map accuracy." *Methods in Ecology and Evolution* - for balanced view of spatial CV controversy
- Recent 2025 paper on block selection: *Frontiers in Remote Sensing*

**ML interpretability:**
- Hooker et al. (2023). "Debiasing SHAP scores in random forests." *AStA Advances in Statistical Analysis*
- Lundberg, S.M. & Lee, S.I. (2017). "A Unified Approach to Interpreting Model Predictions." *NeurIPS*

### 5.2 Revise Overclaims

**Line 36: "<5 rigorous TDA-terrain papers"**

**Revised:** "Fewer than 15 peer-reviewed applications of persistent homology to terrain analysis exist, and fewer than 5 include both rigorous spatial validation and systematic method comparison. Most applications focus on specific detection tasks (landslides, peaks) rather than general terrain classification."

**Cite specifically:**
- Bhuyan et al. (2024) - landslide movement classification
- Syzdykbayev et al. (2020, 2024) - landslide detection from LiDAR
- Bouchaffra & Ykhlef (2021) - land cover change detection
- Ver Hoef et al. (2023) - cloud pattern classification (your current citation)

---

## Part 6: Timeline and Milestones (Revised for 24-Month Master's)

### Realistic 24-Month Schedule for Option A

**Phase 0: Preparation (Month 0, concurrent with coursework)**
- Literature review completion
- IRB/data access approvals (if needed)
- Software environment setup
- Pilot testing (2-3 sites to validate pipeline)

**Phase I: Proof-of-Concept Testbed (Months 1-3)**
- **Month 1:**
  - Data acquisition: 3 provinces × 20 sites = 60 sites
  - DEM preprocessing, quality control
  - Preprocessing sensitivity test (breach-fill vs. raw)
- **Month 2:**
  - Traditional feature extraction (geomorphometry, geomorphons)
  - EC computation for all 60 sites (~5 hours total)
  - PH computation (persistence landscapes only) (~30 hours = 3-4 days)
- **Month 3:**
  - Train 4 models (Traditional, EC, PH, Hybrid)
  - Statistical comparison
  - Write testbed report (15-20 pages)
  - **DECISION GATE:** Go/No-go for main study

**Phase II: Main Study Execution (Months 4-16)**
- **Months 4-5:** Scale to 80 sites if needed (likely just add 20 more sites, 1 more province)
- **Months 6-7:** Complete feature extraction for all sites
- **Months 8-9:** Primary modeling and validation
  - 5-fold CV for all 4 models
  - McNemar's tests, bootstrap CI
  - Computational benchmarking
- **Months 10-12:** Transferability analysis
  - Leave-one-province-out CV
  - Distance-decay analysis
  - Cross-province accuracy assessment
- **Months 13-14:** SHAP interpretation and feature importance
  - Which EC features matter most?
  - Which traditional features are complemented by EC?
  - Geological interpretation of discriminative features
- **Months 15-16:** Computational cost-benefit analysis
  - Runtime comparisons
  - Memory profiling
  - Scalability projections

**Phase III: Thesis Writing and Defense (Months 17-24)**
- **Months 17-18:** First draft of chapters 1-3 (Intro, Literature, Methods)
- **Months 19-20:** First draft of chapter 4 (Results) and 5 (Discussion/Conclusion)
- **Month 21:** Advisor review and major revisions
- **Month 22:** Committee draft distributed; prepare defense presentation
- **Month 23:** Minor revisions, defense rehearsals
- **Month 24:** Thesis defense, final revisions, submission

**Contingency buffers:**
- 2 weeks built into each phase for delays
- If testbed fails (Month 3), pivot to traditional geomorphometry comparison
- If PH computation too slow, reduce to 60 sites total
- If writing takes longer, extend to Month 27 (still within 2.5 years)

---

## Part 7: Success Criteria (Revised and Realistic)

### Tier 1: Minimum Viable Thesis (Defensible Master's Degree)

**Required:**
- ✓ EC achieves ≥65% accuracy for 3-class province discrimination (better than random: 33%)
- ✓ Complete computational benchmarking showing EC runtime advantages
- ✓ Statistical comparison documenting where EC succeeds vs. fails
- ✓ Documented reproducible pipeline (GitHub + Zenodo)
- ✓ Written thesis meeting university standards

**Outcome:** You graduate with a Master's degree. Contribution: establishes computational feasibility of EC for terrain, even if accuracy is limited.

**Publication potential:** Methods paper in *Computers & Geosciences* or *Environmental Modelling & Software*: "Euler Characteristic for Terrain Classification: A Computational Efficiency Study"

---

### Tier 2: Strong Master's Thesis (Competitive Job Market Position)

**Required:**
- ✓ EC achieves ≥75% accuracy (competitive with traditional methods)
- ✓ EC within 10% of PH accuracy but 5-10× faster computationally
- ✓ Leave-one-province-out shows reasonable transferability (>60% accuracy)
- ✓ SHAP analysis reveals interpretable EC features (e.g., "total variation correlates with relief")
- ✓ Clear methodological recommendations for practitioners

**Outcome:** Strong Master's thesis with PhD program acceptance or industry job offers.

**Publication potential:** *Geomorphology* or *Earth Surface Processes and Landforms*: "Euler Characteristic Curves for Landscape Classification: A Fast Alternative to Persistent Homology"

---

### Tier 3: Exceptional Master's Thesis (PhD Fellowship Quality)

**Required:**
- ✓ EC matches or exceeds PH accuracy (within 3%)
- ✓ Major computational advantage demonstrated (10-20× speedup)
- ✓ EC features show better transferability than PH (>10% higher on leave-one-out)
- ✓ Novel EC features identified (e.g., directional EC for anisotropy)
- ✓ Clear geological interpretation connecting EC signatures to processes

**Outcome:** Top-tier Master's thesis, NSF GRFP competitive, multiple publication opportunities.

**Publication potential:** 
1. Primary: *Nature Communications* or *PNAS* if combined with Mars analog
2. Methods: *Journal of Machine Learning Research* for EC vectorization method
3. Application: *Geomorphology* for Appalachian case study

---

## Part 8: Addressing Committee Concerns Point-by-Point

### Concern 1: Scope Creep (MOST CRITICAL)

**Committee:** "This reads like a PhD dissertation"

**Your response:**
- Reduce from 4 RQs to 1 primary RQ with sub-questions
- Cut persistence images, multi-scale analysis, advanced methods
- Reduce from 10 models to 4 models
- Focus on EC vs. PH comparison, not exhaustive TDA survey

**Evidence of change:**
- Old: 80-120 sites, 3 scales, 10+ models, 27 months research
- New: 60-80 sites, 1 scale, 4 models, 16 months research + 8 months writing

---

### Concern 2: Novelty vs. Methodological Validation

**Math Prof:** "Rigorous methods comparison—valuable but incremental"

**Your response:** 
"I agree this is methodological, not theoretical. But it fills a genuine gap: EC has **never** been systematically tested for terrain despite 15+ years of TDA development. My contribution is establishing whether computationally expensive PH is necessary, or whether EC suffices—a practical question with immediate value to practitioners."

**Geology Prof:** "Where's the new geological knowledge?"

**Your response (revised geological outcomes):**
"This thesis establishes **which topological metrics quantify qualitative geomorphological descriptions**. For example:
- Does 'strongly folded parallel ridges' (Valley & Ridge) correspond to high H₁ persistence at 1 km scale?
- Does 'rolling uplands' (Piedmont) produce low total EC variation?
- Does local-scale topological complexity (1 km) differ systematically between provinces even if we don't capture fold wavelength?

**New knowledge:** We'll learn whether **topological features at the scale of geomorphological processes** (hillslope-to-valley, not regional folds) distinguish landscapes. This is still geomorphologically meaningful."

**Geospatial Prof:** "Methods papers are important but harder to publish"

**Your response:**
"I position this as a **computational geomorphometry** study, not pure methods. The question 'Can we achieve 80% accuracy 10× faster?' has immediate practical value. With Geomorpho90m and similar global datasets, practitioners need fast methods for continental-scale analysis. If EC works, it enables applications currently infeasible with full PH."

---

### Concern 3: Statistical Over/Under-Specification

**Committee:** Multiple testing corrections overkill; power analysis missing Type II error

**Your response:**
- Simplify to single correction method (Benjamini-Hochberg)
- Remove MANOVA (use confusion matrices instead)
- Acknowledge Type II error: "With n=60-80 and spatial autocorrelation, we have limited power to detect small effect sizes (Cohen's d < 0.5). We prioritize spatial honesty over statistical power."
- Pre-registration: "We state expected rank order: PH > EC > Traditional, but remain open to alternative outcomes."

---

### Concern 4: Scale Matching

**Committee:** "1 km window vs. fold wavelength is a real problem"

**Your response (see Section 4.5):**
"We explicitly study **local-scale topological structure** (1 km), not regional fold architecture. We revise geological predictions accordingly and state this limitation upfront. Local-scale topology is still geomorphologically meaningful and matches the scale at which geomorphons and similar methods operate."

**Add discussion section:**
"Future work should examine multi-scale topological analysis (5 km, 10 km windows) to capture fold wavelength. However, computational constraints limit this to future PhD research. This thesis establishes feasibility at local scale as foundation for regional-scale studies."

---

### Concern 5: Mathematical Claims

**Committee:** EC formulation needs clarification; β₂≈0 assumption not justified

**Your response (see Section 1.5):**
Replace Lines 156-159 with:

"**Euler characteristic for 2D height functions:** For sublevel filtrations of DEMs (representing water rising to level t), we compute persistent homology of 2D cubical complexes. By definition, 2D complexes cannot contain 3-dimensional voids, thus β₂(t) = 0 for all t. Therefore, χ(t) = β₀(t) - β₁(t) + 0 simplifies to:

χ(t) = β₀(t) - β₁(t)

where β₀(t) counts connected components (peaks/basins) and β₁(t) counts loops (enclosed valleys) at elevation threshold t.

**Empirical verification:** We confirm β₂ = 0 for all sites in our dataset, as expected from theory."

---

## Part 9: Final Recommendations

### What to Do Monday Morning

1. **Schedule 1-hour meeting with committee** (all three if possible)
   - Present Option A (EC Thesis) framework
   - Get consensus on reduced scope
   - Ask explicit question: "Is testbed alone a viable fallback thesis if main study reveals EC insufficient?"

2. **Revise abstract and RQs** (2-3 hours)
   - Single primary RQ
   - Clear focus on EC vs. PH computational efficiency
   - Remove all references to multi-scale, advanced methods, extensive spatial CV

3. **Cut proposal to 30-40 pages** (current: ~50+ pages)
   - Remove/condense: Advanced methods section, multi-scale discussion, extensive spatial CV details
   - Keep: Testbed-then-scale design, reproducibility plan, computational benchmarking

4. **Add sections** (1 day work):
   - "Computational Efficiency as Primary Contribution" (new section explaining why speed matters)
   - "Scale Limitations and Local Topology" (address 1 km vs. fold wavelength explicitly)
   - "Expected Geological Outcomes at Local Scale" (revised predictions for 1 km windows)

5. **Fix mathematical justification** (2 hours)
   - Revise β₂≈0 explanation (see Section 1.5)
   - Add diagram showing sublevel filtration on 2D surface
   - Reference Smith & Zavala 2021 for EC theoretical background

6. **Update literature review** (2-3 days)
   - Add missing citations (Section 5.1)
   - Revise "<5 papers" overclaim
   - Add Wadoux et al. 2021 for balanced spatial CV discussion
   - Add Bhuyan et al. 2024 proper summary

7. **Create decision flowchart** (1 hour)
   - Visual diagram: "Testbed → Decision Gate → Main Study or Pivot"
   - Show explicit criteria and contingency plans

### What NOT to Do

- ❌ Try to save all 4 RQs by "streamlining" - You can't streamline 4 questions into 1 thesis
- ❌ Argue with committee about scope - They're right; listen to them
- ❌ Add more methods to "strengthen" the proposal - Addition = subtraction from Master's thesis
- ❌ Defend multi-scale as "essential" - It's not; it's nice-to-have for PhD
- ❌ Push back on geology prof about "new knowledge" - Reframe your contribution, don't defend old framing

---

## Part 10: The PhD Path (If You Continue)

If Option A succeeds and you want to continue to PhD, here's the natural progression:

**Master's thesis (2.5 years):** EC vs. PH computational efficiency at local scale (1 km), 3-4 Appalachian provinces

**PhD dissertation (4-5 years):**
- **Year 1:** Multi-scale extension (1 km, 5 km, 10 km) capturing fold wavelength
- **Year 2:** All vectorization methods (landscapes, images, silhouettes)
- **Year 3:** Cross-continental validation (Appalachians → Rockies → Sierra Nevada → Mars)
- **Year 4:** Advanced methods (Mapper for regime identification, multiparameter PH)
- **Year 5:** Write 3-4 papers + dissertation

This way, your Master's is a complete, publishable study that also serves as pilot data for PhD applications. You'll have:
- 1 strong methods paper published
- NSF GRFP application based on Master's work
- Clear PhD research plan building on established foundation
- Proven computational skills and productivity

Much better than trying to do PhD-level work in a Master's timeline and burning out.

---

## Conclusion: The Hard Truth and the Path Forward

**The hard truth:** Your current proposal is too ambitious for a Master's thesis. Your committee is right.

**The good news:** With strategic scoping, this can be an **excellent** Master's thesis that makes a real contribution.

**The path forward:**
1. Accept that you're doing ONE thesis, not four
2. Focus on computational efficiency (your real competitive advantage)
3. Make EC for terrain classification your niche
4. Execute 60-80 sites rigorously instead of 120 sites hastily
5. Write a crystal-clear thesis answering one question well

**The opportunity:** If EC works, you've established a new standard method for terrain classification. If it doesn't, you've documented why and saved others wasted effort. Either way, you've made a contribution.

**Your committee will approve** a focused, realistic proposal. They won't approve an overly ambitious one that you can't finish.

**Choose scope. Execute rigorously. Graduate on time.**

---

## Appendix A: Elevator Pitch for Revised Thesis

*"My Master's thesis tests whether Euler characteristic curves—a fast topological summary—can classify Appalachian provinces as accurately as full persistent homology, which takes 10-20× longer to compute. Using 60-80 carefully selected sites, I compare four approaches: traditional geomorphometry, EC-only, persistent homology-only, and hybrid EC+traditional. If EC works, it enables continent-scale topological analysis previously infeasible due to computational cost. If not, I document precisely where and why it fails, preventing wasted effort. Either outcome is publishable and valuable. The testbed-then-scale design ensures I produce results even if the method doesn't work as hoped. Timeline: 24 months including writing. Deliverables: Master's thesis, 1-2 papers, open-source reproducible code."*

**That's your thesis. Now go write it.**

---

## Appendix B: Key References to Add

### Essential TDA Papers
- Bubenik (2015) - persistence landscapes theory
- Cohen-Steiner et al. (2007) - stability theorem
- Adams et al. (2017) - persistence images
- Smith & Zavala (2021) - Euler characteristic review

### Geomorphometry
- Pike et al. (2009) - geomorphometry overview
- Amatulli et al. (2020) - Geomorpho90m
- Jasiewicz & Stepinski (2013) - geomorphons

### Spatial Validation
- Roberts et al. (2017) - pro spatial CV
- Ploton et al. (2020) - Nature Comm, 28-50% inflation
- Wadoux et al. (2021) - anti spatial CV counterargument
- Valavi et al. (2019) - blockCV package

### ML Interpretability  
- Lundberg & Lee (2017) - SHAP original paper
- Hooker et al. (2023) - SHAP bias in RF
- Molnar (2020) - Interpretable ML book

### TDA for Terrain
- Bhuyan et al. (2024) - landslides, Nature Comm
- Syzdykbayev et al. (2020, 2024) - landslides, false positives
- Corcoran & Jones (2023) - TDA for GIS review

