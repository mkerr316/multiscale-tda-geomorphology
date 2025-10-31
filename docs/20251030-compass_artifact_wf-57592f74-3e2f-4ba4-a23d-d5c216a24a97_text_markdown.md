# TDA for Landscape Classification: A Defensible Research Proposal Guide

## Executive Assessment: What You're Walking Into

**The reality check first**: TDA applications to terrain analysis represent an **extremely nascent frontier** with fewer than 5 directly relevant papers published in the last 3-5 years. This is simultaneously good news (genuine novelty opportunity) and challenging news (you'll need exceptional justification). One 2024 study explicitly found that **TDA alone produced "notable incidence of false positives"** and worked best when combined with traditional geometric features. You're not entering a crowded field—you're genuinely pioneering—but that means your defensibility bar is high.

Meanwhile, landscape classification itself is **mature and competitive**, with established methods achieving 73-91% accuracy. Any new approach must demonstrate clear advantages over geomorphons (computationally efficient, widely used) and deep learning methods (current accuracy leaders). The Earth-Mars comparative angle is **well-established and feasible**, particularly for specific landforms like dunes and valleys, but requires careful attention to dimensionless parameters and physical constraints.

**Bottom line**: This is achievable and exciting, but success requires proving necessity (not just novelty), rigorous baseline comparisons, and honest acknowledgment of where TDA helps versus where traditional methods suffice.

## Section 1: Current State of TDA in Geomorphometry

### What Actually Exists (Not Speculation)

The TDA-terrain literature is **remarkably sparse**. Extensive search revealed only these direct applications:

**Landslide Detection** (Syzdykbayev et al. 2020, 2024): Applied persistent homology to LiDAR-derived DTMs. The critical 2024 follow-up found that **pure topological information resulted in notable false positives**. Best results came from combining PH with traditional geometric filters (area, length-to-width ratio, slope). RMSE reduction of 8-50% after error elimination, but this is error detection, not landslide classification accuracy. The key lesson: **TDA supplements rather than replaces traditional methods**.

**Peak Identification** (Wilkinscaruana): Proof-of-concept using SRTM data west of Sydney. Used persistence to rank 66 peaks quantitatively. No comparison with traditional peak-finding algorithms. Identified boundary effects as limitation. Status: interesting demonstration, not validated method.

**DEM Generalization** (Corcoran 2019): Height-based filtration for DEM simplification. Quantitative performance metrics not detailed in available sources. Limited documentation.

**Adjacent Field Applications**: Ver Hoef et al. (2023) successfully classified cloud patterns using persistent homology + SVM with "good results" (no specific accuracy reported). Ofori-Boateng et al. (2021) compared aerosol optical depth maps at multiple resolutions using PH. These show TDA works for 2D spatial patterns but don't establish terrain classification capability.

### Methods Actually Tested

**Persistent homology dominates**—essentially the only TDA method applied. Specifically: standard PH with height-based filtration, computing 0-dimensional (connected components/peaks) and 1-dimensional (loops/valleys) features. Persistence diagrams and barcodes for visualization. Persistence landscapes used in cloud classification (Ver Hoef 2023).

**Not found**: Euler characteristic curves for terrain, Mapper algorithm for landscape analysis, multi-parameter persistence applications, or any advanced TDA methods beyond basic PH.

### Actual Performance vs. Traditional Methods

**Here's the gap that matters for your proposal**: Virtually no papers provide quantitative head-to-head comparisons between TDA and standard geomorphometric methods. The Syzdykbayev 2024 study is the only one with comparative results, and it found **hybrid approaches outperform pure TDA**. 

**Missing from literature**:
- TDA vs. geomorphons for landform classification
- TDA vs. traditional slope/curvature analysis  
- TDA performance on standard geomorphometry benchmarks
- TDA vs. Random Forest with terrain features
- Any demonstration that TDA outperforms existing methods

**Critical implication**: You have opportunity to be first to do rigorous comparative testing, but you MUST design these comparisons into your study. Without them, reviewers will ask "why not just use geomorphons?"

### Field Maturity: Definitively New Frontier

**Evidence for nascent status**:
- Publication timeline: 2019-2024 (3-5 years old)
- Volume: ~4-5 direct terrain papers, ~10-15 adjacent geospatial
- No TDA sessions at geomorphometry conferences
- No integration with standard GIS software
- No textbook coverage
- Geomorphometry community has not embraced these methods

**Key researchers**: Hassan Karimi group (U Pittsburgh) on landslides; Padraig Corcoran (Cardiff) on GIS applications; Imme Ebert-Uphoff (Colorado State) on environmental imagery. This is a small, emerging community, not an established subfield.

### The Research Gap You Can Fill

**Standard geomorphometric variables**: Slope, aspect, curvatures (profile, plan, tangential), roughness indices (TRI, VRM), topographic indices (TPI, TWI, CTI), and geomorphons. **TDA has not been tested against ANY of these**. No published applications comparing TDA-derived features to these 26+ standard parameters. This represents a major opportunity but also a major validation requirement.

## Section 2: Landscape Classification Baselines You Must Beat

### Current State-of-the-Art Methods

Your new method needs to demonstrate advantages over these established approaches:

**Geomorphons** (Jasiewicz & Stepinski 2013): Pattern recognition using local ternary patterns. Identifies 10 common landform types (flat, summit, ridge, shoulder, spur, slope, hollow, footslope, valley, depression). **Key strengths**: Unprecedented computational efficiency (single DEM scan), scale-adaptive, no training data required, implemented in GRASS GIS. **Limitation**: Cannot distinguish depositional from erosional landforms; may miss narrow features. **Your baseline to beat for efficiency and practicality**.

**Topographic Position Index (TPI)** (Weiss 2001): Compares each cell to mean neighborhood elevation. Creates 10 landform classes using multi-scale TPI. **Strengths**: Simple, interpretable, widely implemented. **Limitations**: Highly sensitive to neighborhood size selection; fails in heterogeneous landscapes (De Reu et al. 2013 documented erroneous classifications). **Your opportunity**: Show TDA handles heterogeneous terrain better.

**Iwahashi-Pike Unsupervised** (2007, 2018): Uses slope gradient, local convexity, and surface texture with k-means clustering. Applied globally at 280m resolution using MERIT DEM. **Strengths**: No training data, globally applicable, objective. Successfully cross-tabulated with geological maps. **Limitation**: ~62% accuracy in heterogeneous areas; mixes depositional and erosional features. **Your baseline for unsupervised global classification**.

**Random Forest with Terrain Features**: Using slope, aspect, curvature, TWI, TRI, multi-scale TPI. **Typical accuracy: 73-87%** overall accuracy depending on feature set and complexity. Himalayan mountain classification achieved 87.33%. **Your supervised learning baseline**.

**Deep Learning (CNNs)**: U-Net and FCN-ResNet architectures for semantic segmentation. **Accuracy: 79-91%** depending on study. Yang et al. (2023) used FCN-ResNet with AW3D30 DEM against 1:1,000,000 Chinese landform map. Semi-supervised Mars terrain achieved 91.1% with only 1% training data. **Your accuracy ceiling**—if you can't beat or match this, you need other compelling advantages (interpretability, transferability, efficiency).

### What These Methods Get Wrong (Your Opening)

**The gaps you can exploit**:

1. **Geomorphons fail at process distinction**: Cannot differentiate alluvial fans from pediplains from lava plains with similar topographic form. Purely morphological, not genetic.

2. **TPI sensitivity to parameters**: No clear guidelines for optimal neighborhood size selection across regions. User expertise required.

3. **Traditional ML lacks spatial context**: Random Forest treats features independently; doesn't capture topological relationships between landforms.

4. **Deep learning black boxes**: CNNs achieve high accuracy but offer minimal interpretability. What topological features discriminate classes? Unknown. Also poor transfer learning across geographic regions.

5. **All methods are scale-dependent in problematic ways**: Multi-scale approaches exist but require manual parameter tuning.

**Your potential TDA advantages**:
- **Multi-scale by design**: Persistence captures features across scales simultaneously
- **Topological invariance**: Robust to rotation, translation, small deformations
- **Interpretable features**: Persistence diagrams show what topological structures (peaks, basins, ridges) distinguish landscapes
- **Transferability hypothesis**: Topological signatures may generalize better across regions than pixel-level features

**Critical caveat**: These are hypotheses until proven. Your study must test whether these theoretical advantages materialize in practice.

### Accuracy Levels You're Competing Against

**Minimum acceptable performance**: If you fall below ~70% accuracy, the method is likely not viable unless you have extraordinary other advantages (computational speed, interpretability, transferability).

**Competitive range**: 75-85% puts you in the Random Forest/traditional ML tier. Defensible if you show clear advantages in interpretability or efficiency.

**Excellence threshold**: 85-90% matches or exceeds current best methods. At this level, TDA becomes compelling even if computationally expensive.

**State-of-art**: 90%+ approaches best deep learning results. Unlikely for first TDA application, but possible with hybrid approaches.

**Your realistic target**: Aim for 80-85% with clear interpretability advantages, or demonstrate that TDA+traditional features exceeds either alone (hybrid approach following Syzdykbayev 2024 lesson).

### Known Limitations You Can Address

**Fundamental challenge**: Continuous terrain vs. discrete classification. Real landscapes exist on continua; classification into discrete types is inherently artificial and scale-dependent. All methods struggle here.

**Ground truth scarcity**: Creating reliable landform ground truth is subjective, expensive, time-consuming. Different geomorphologists may classify identically. No "ImageNet for landforms" exists.

**Class imbalance**: Rare but important landforms (volcanic features, karst, specific glacial forms) underrepresented in training data.

**Transfer learning failure**: Models trained in one geographic/geologic setting perform poorly in others. CNN-based methods especially affected.

**Your TDA opportunity**: If you can demonstrate better transfer learning (topology more universal than pixel patterns?) or provide interpretable features that help geomorphologists understand misclassifications, you have a defensibility argument even at moderate accuracy levels.

## Section 3: Earth-Mars Comparative Geomorphometry

### Is This Feasible? Yes, With Caveats

Comparative planetary geomorphometry is **well-established and actively practiced**. This is not speculative—it's happening now, particularly for specific landforms.

**Success stories you can learn from**:

**Barchan dunes** (Rubanenko et al. 2022): Used CNN to analyze >1 million barchan dunes on Mars (CTX imagery). Measured width, length, height, volume using dimensionless ratios. **Key finding**: Mars/Earth dunes follow similar scaling laws despite different absolute sizes. Mars dunes 2.4× wider, 3.4× longer on average. Size decreases with atmospheric density: L ∼ ρ_f^(-0.68), consistent with hydrodynamic theory. **Why it worked**: Fluid dynamics principles apply; dimensionless parameters capture key physics.

**Valley networks** (Seybold et al. 2018): Analyzed branching angles from digital valley networks. Mars valleys branch at ~40° (narrow angles), comparable to arid Earth regions like Upper Colorado basin (41°), narrower than humid regions. **Interpretation**: Mars valleys formed by surface runoff in arid climate, not groundwater. **Why it worked**: Geometric parameters (angles) are scale-independent.

**Crater morphometry** (Watters et al. 2015): Small craters (25m-5km) using HiRISE stereo DEMs. Found scaling laws from large craters overestimate depth/volume at small diameters. Gravity-driven collapse transition at D~1km where rim slopes exceed repose angles. **Challenge demonstrated**: Gravity effects (Mars 0.38g vs Earth 1g) significantly affect morphology—must account for this.

### Data Sources and Resolution Reality

**Mars topographic data**:
- **MOLA**: 463m gridded globally (±1m vertical accuracy)
- **HRSC**: 50-75m/pixel DEMs, 25m for select areas  
- **CTX**: 6-20m/pixel DEMs from stereo pairs
- **HiRISE**: 1-2m/pixel DEMs (tens of cm vertical precision), but only ~1% of Mars covered at this resolution

**Earth comparison data**:
- **SRTM**: 30m global
- **LiDAR**: Sub-meter to cm (limited areas)
- **Site-specific high-resolution**: Often better than Mars for analog sites

**Critical insight**: Mars often has BETTER resolution for selected sites than global Earth data. HiRISE at 1m beats SRTM at 30m. The challenge isn't resolution quality—it's coverage (HiRISE covers <1% of planet) and matching scales appropriately.

**Your approach**: Select comparable resolution datasets for specific comparisons. Don't compare HiRISE (1m) to SRTM (30m)—that's methodologically invalid. Either use MOLA (463m) vs coarsened Earth data, or HiRISE vs LiDAR for local studies.

### The Gravity-Atmosphere Problem

**Physical reality you must address**:
- Mars gravity: 3.71 m/s² (38% of Earth)
- Mars atmosphere: 0.6% of Earth's pressure

**Implications**:
- Different slope stability angles
- Different crater formation dynamics  
- Different volcanic edifice sizes possible
- Atmospheric effects on aeolian transport

**Your solution**: Use dimensionless morphometric parameters. Height/width ratios, aspect ratios, angles, branching angles, curvature measures—these are scale-invariant and gravity-adjusted naturally when normalized.

**For TDA specifically**: Persistence ratios (death-birth / maximum elevation) are dimensionless. Topological features (number of components, loops) are gravity-independent. **This is actually a TDA advantage**—topology is inherently invariant to these physical differences in ways that absolute measurements are not.

### Methodological Best Practices

**What works**:
✅ Dimensionless morphometric ratios
✅ Statistical distributions of geometric parameters
✅ Scaling law analysis (power-law relationships)
✅ Branching/orientation angle analysis  
✅ Automated feature detection with ML
✅ Multi-scale terrain analysis

**What doesn't work**:
❌ Direct pixel-by-pixel comparison
❌ Process attribution from morphometry alone
❌ Ignoring gravity/atmospheric differences
❌ Assuming morphological similarity = process similarity
❌ Comparing vegetated Earth terrain to Mars

**Your TDA implementation**: Focus on dimensionless topological features. Compare persistence diagram distributions between Mars and Earth analogs. Test hypothesis: "Do Earth and Mars regions formed by similar processes (e.g., aeolian) share topological signatures despite different scales and gravity?"

### Realistic Scope for Your Proposal

**Highly feasible**:
- Compare dune fields on both planets using TDA
- Analyze valley network topology Earth vs Mars
- Study crater-modified terrain topological signatures
- Test if TDA-based similarity metrics match geomorphologist assessments of Earth-Mars analogs

**Feasible with care**:
- Develop Mars landscape classification transferable from Earth training data
- Quantify morphometric similarity for specific landform types
- Multi-scale comparison accounting for resolution differences

**Not feasible** (avoid these):
- Global comprehensive meter-resolution comparison
- Process attribution from topology alone
- Direct comparison without gravity/atmosphere corrections
- Features with no Earth analogs (CO2 sublimation terrain)

**My recommendation**: Start with a focused landform type (dune fields or valleys) where Earth-Mars comparison is established, then show TDA provides additional discriminative power. This builds on proven methodology rather than attempting too much novelty at once.

## Section 4: Making Your Methods Paper Defensible

### Anatomy of Successful Methods Papers

Three exemplars analyzed—geomorphons, HAND index, and TWI—reveal a consistent pattern for defensibility:

**Step 1: Identify specific technical failures of existing methods**

Geomorphons did this brilliantly: "All auto-mapping techniques...achieved by means of differential geometry...is scale-dependent; changing pixel size produces different maps...differential geometry produces infinite number of possible values requiring additional heuristic rules."

Notice the specificity: not "terrain classification is hard" but "differential geometry has three specific problems: scale-dependence, infinite values, and heuristic rule requirements."

**Your TDA version might be**: "Current landscape classification relies on pixel-level features (slope, curvature) or learned patterns (CNN weights) that lack transferability across regions. Geomorphons achieve efficiency but cannot distinguish process (e.g., depositional vs erosional fans). Deep learning achieves accuracy but provides no interpretable features to understand why classifications succeed or fail. What's missing is a method that captures **structural relationships**—how landform elements connect topologically—that are invariant to scale, rotation, and transferable across geographic contexts."

**Step 2: Provide theoretical justification**

HAND index: Based on "topology of relative soil gravitational potentials, or local draining potentials"—clear physical principle.

Geomorphons: Borrowed from computer vision (Local Binary Patterns), established method adapted to new domain.

**Your TDA version**: "Persistent homology provides a theoretically rigorous multi-scale framework for quantifying topological features—peaks (0-dimensional homology), valleys (1-dimensional), and basins (2-dimensional)—with proven stability guarantees (Cohen-Steiner et al. 2007). Unlike pixel-based features, topological signatures are invariant to rotation, translation, and small deformations, with quantifiable robustness via bottleneck/Wasserstein distances."

**Step 3: Rigorous multi-site validation**

HAND: 18,000 km² validation + field transect data comparing to water table depths. Showed 55% more variance explained than horizontal distance. Tested transferability to "ungauged catchments with contrasting geologies."

Geomorphons: Statistical analysis showing 50% of terrain covered by 8 patterns, tested at multiple scales (L=100m, 300m, 1000m).

**Your TDA requirements**:
- **Minimum 3 study sites** with different landscape types (e.g., fluvial-dominated, aeolian, glacial)
- **Ground truth**: Use published geomorphic maps (e.g., Chinese 1:1,000,000 landform map, USGS geomorphic province maps)
- **Quantitative comparison**: Report accuracy, F1-scores, confusion matrices
- **Baseline comparison**: Test against geomorphons, TPI, and Random Forest with traditional features on SAME datasets
- **Statistical significance**: Not just mean accuracy—report confidence intervals, McNemar's test for paired classifier comparison
- **Transferability test**: Train on one region, test on another; report accuracy drop

### The "Necessity Not Novelty" Framing

**Weak framing** (what NOT to say): "TDA is a new mathematical tool that has not been applied to landscape classification, so we will apply it."

**Strong framing** (what to say): "Current methods face a fundamental dilemma: unsupervised methods (geomorphons, TPI) achieve computational efficiency but fail at X [cite failure mode]; supervised deep learning achieves accuracy but lacks interpretability and transferability. We need methods that bridge this gap—interpretable features that enable supervised learning with better generalization. Persistent homology provides this bridge by extracting theoretically-grounded, multi-scale topological features proven stable and invariant. We demonstrate this solves X by testing on Y and comparing rigorously to Z baselines."

### Validation Checklist for Defensibility

Your methods paper MUST include:

**Problem validation**:
- [ ] Specific technical limitation identified with citations
- [ ] Quantified failure mode with examples or data
- [ ] Established problem significance (affects real applications)

**Theory validation**:
- [ ] Mathematical formulation clearly stated
- [ ] Theoretical stability guarantees cited (Cohen-Steiner et al. for PH stability)
- [ ] Parameter choices justified with physical/mathematical reasoning

**Empirical validation**:
- [ ] ≥3 test sites with different characteristics
- [ ] Comparison to ≥2 baseline methods (recommend: geomorphons + Random Forest)
- [ ] Same data and protocols for fair comparison
- [ ] Multiple metrics (accuracy, F1, kappa, class-specific performance)
- [ ] Statistical significance tests (confidence intervals, McNemar's test)
- [ ] Transferability tested (train on region A, test on region B)

**Reproducibility**:
- [ ] Algorithm described in sufficient detail for reimplementation
- [ ] Code made publicly available (GitHub)
- [ ] Data sources specified with access information
- [ ] Parameters documented
- [ ] Computational requirements stated

**Intellectual honesty**:
- [ ] Limitations acknowledged explicitly
- [ ] Failure modes discussed
- [ ] Scope of applicability clearly bounded
- [ ] Future work needs identified

### What Makes Methods "Defensible" vs "Interesting"

**"Interesting" but not defensible**: "TDA finds topological features in DEMs that correlate with landscape types. Here are the results on our study area."

**Defensible**: "Existing methods achieve X% accuracy but fail at Y. We hypothesized TDA would address Y because [theory]. We tested on N sites, comparing to M baselines. TDA achieves Z% accuracy (95% CI: [a,b]), significantly better than baseline B (p<0.05, McNemar's test) and comparable to baseline C. TDA shows W% better transferability across regions. Limitations include [specific issues]. This demonstrates TDA is necessary for [specific application] where [specific advantages matter]."

The difference is: theoretical justification + rigorous empirical comparison + statistical significance + honest limitation acknowledgment.

## Section 5: TDA Methods Selection for Your Application

### What Filtration to Use: Clear Winner for DEMs

**Strongly recommended: Sublevel set filtration with cubical complexes**

**Why this is optimal**:
1. **Semantic correspondence**: Elevation values naturally define filtration parameter (water level rising/falling)
2. **Computational efficiency**: Cubical persistence much faster than simplicial for gridded data
3. **Interpretability**: Features directly map to terrain structures
   - H₀ (0-dimensional): Peaks/plateaus appearing as water recedes
   - H₁ (1-dimensional): Valley loops forming
   - H₂ (2-dimensional): Enclosed depressions/basins
4. **Native structure**: DEMs are already regular grids—cubical complexes preserve this

**Implementation**: Treat DEM as function f: Grid → ℝ where f(pixel) = elevation. Build sublevel filtration F_r = {pixels where elevation ≤ r}. Use GUDHI CubicalComplex or Ripser in cubical mode.

**Alternative to consider**: Superlevel filtration (water receding instead of rising) emphasizes peaks over valleys. Try both; they capture complementary information.

**Don't use**: Vietoris-Rips or Čech complexes on point clouds sampled from DEMs—these are computationally expensive and less natural for gridded elevation data.

### Persistence Vectorization: Two Strong Options

**Option 1: Persistence Landscapes** (recommended for beginners)

**Advantages**:
- Parameter-free (no tuning required)
- Stable (inherits theoretical stability guarantees)
- Invertible (no information loss)
- Performs well (85-95% accuracy in comparative studies)
- Fast computation
- Functional representation enables statistical analysis

**How it works**: Transforms (birth, death) points to (birth, persistence) coordinates, creates "tenting" functions, takes k-th maximum at each point. Result is sequence of piecewise-linear functions.

**Classification performance**: SHREC14: ~85%, Protein datasets: 80-90%, consistently high across domains.

**Best for**: Initial exploration, when you want robust results without parameter tuning.

**Option 2: Persistence Images** (recommended for interpretability)

**Advantages**:
- Fixed-dimensional vectors (direct ML compatibility)
- Excellent interpretability (can visualize as heatmaps)
- Feature selection possible with Sparse SVM
- Strong performance (90-96% on MNIST)
- Weighting function emphasizes important features

**Parameters needed**:
- Resolution (pixel grid size): 20×20 is standard, robust choice
- Gaussian variance σ: 0.01 works well, method is robust to this choice
- Weighting function: Use persistence (emphasizes long-lived features)

**Classification performance**: Often matches or exceeds landscapes, especially with SVM or Random Forest.

**Best for**: When interpretability matters—you can visualize which topological features (regions of persistence diagram) discriminate landscape classes.

**My recommendation**: Start with persistence landscapes for initial results (easiest, parameter-free). If reviewers ask "what topological features matter?"—switch to persistence images with Sparse SVM to identify discriminative regions of the diagram.

### What Homology Dimensions to Compute

**Compute H₀ and H₁ for DEMs**:

**H₀ (0-dimensional homology)**: Connected components
- Birth: New peak/plateau appears above water level  
- Death: Merges with another component
- Long bars: Prominent, isolated peaks
- Short bars: Small bumps/noise

**H₁ (1-dimensional homology)**: Loops/cycles
- Birth: Valley loop forms as water rises
- Death: Loop filled/eliminated
- Long bars: Significant basins, valleys with clear drainage loops
- Short bars: Small topographic depressions

**H₂ (2-dimensional homology)**: Voids (only for 3D data)
- Not typically useful for 2D DEM analysis
- Omit unless you have true 3D subsurface data

**Practical implementation**: Compute both H₀ and H₁, concatenate vectorized features: [H₀_features, H₁_features]. This captures both peak/basin structure (H₀) and valley/drainage topology (H₁).

### Machine Learning Pipeline

**Recommended workflow**:

```
1. Compute persistence diagrams (H₀, H₁) for each DEM sample
2. Vectorize using persistence landscapes OR images
3. Concatenate dimensions: features = [H₀_vector, H₁_vector]
4. Optional: Combine with traditional features [TDA_features, slope_mean, curvature_mean, ...]
5. Train classifier:
   - Start with Random Forest (robust, minimal tuning)
   - Try SVM with RBF kernel
   - If using persistence images: SSVM for feature selection
6. Validate:
   - 10-fold cross-validation
   - Independent test set (different geographic region)
   - Compute bottleneck distances between class diagrams
```

**Expected performance based on literature**:
- TDA alone: 75-85% (estimate based on similar applications)
- TDA + traditional features (hybrid): 80-90% (following Syzdykbayev 2024 lesson)
- Traditional features alone: 73-87% (from landscape classification literature)

**Your defensibility story**: If TDA alone matches traditional, you've shown equivalence with interpretability advantage. If hybrid exceeds either alone, you've demonstrated complementary information—topology + geometry > either alone.

### Known Failure Modes to Acknowledge

**Be upfront about these limitations**:

1. **False positive problem**: Syzdykbayev 2024 found "notable incidence of false positives" with pure topological approach. **Mitigation**: Hybrid approach combining TDA with geometric features.

2. **Noise sensitivity**: Small features near diagonal in persistence diagrams often noise. **Mitigation**: Use confidence thresholds (bootstrap), filter by persistence threshold, or use Distance-to-Measure (DTM) instead of raw elevations.

3. **Topological vs topographical**: TDA captures topology (connectivity, loops) but may miss geometric details. Two very different landscapes might have similar topology. **Mitigation**: Combine with geometric features or acknowledge this limitation explicitly.

4. **Computational cost**: Persistent homology has exponential worst-case complexity, though practical performance is usually manageable for DEMs. **Mitigation**: Use cubical complexes (efficient), subsample if needed, report computational requirements.

5. **Interpretability requires expertise**: While "more interpretable than CNNs," persistence diagrams require topological knowledge to interpret. **Mitigation**: Provide clear visual explanations, use persistence images to show discriminative features.

6. **Not guaranteed to outperform**: TDA provides different features, not necessarily better ones. Some landscapes may not have discriminative topological signatures. **Mitigation**: Position as complementary approach; test empirically; acknowledge when traditional methods suffice.

### Defensible Methodological Choices Summary

**For a novice wanting maximum defensibility**:

1. **Filtration**: Sublevel set on cubical complex (most natural, efficient, interpretable for DEMs)
2. **Vectorization**: Persistence landscapes first (parameter-free, stable, good performance)
3. **Homology**: H₀ and H₁ (capture peaks and valleys)
4. **ML model**: Random Forest (robust, standard)
5. **Validation**: 10-fold CV + independent test region + bottleneck bootstrap
6. **Comparison**: Against geomorphons (efficiency baseline) and Random Forest with traditional features (accuracy baseline)
7. **Reporting**: Diagrams with confidence bands, accuracy ± std dev, bottleneck distances between classes

**Cite these for theoretical justification**:
- Cohen-Steiner et al. (2007) for stability theorems
- Bubenik (2015) for persistence landscapes
- Adams et al. (2017) for persistence images
- Carlsson (2009) or Wasserman (2018) for TDA foundations

## Critical Synthesis: Your Path Forward

### What You Now Know

**TDA + terrain is genuinely novel**: With <5 directly relevant papers, you're pioneering, not following. This is exciting but raises the bar—you must prove necessity, not just demonstrate novelty.

**Baselines are strong**: Geomorphons (efficient), deep learning (accurate ~90%), traditional ML (solid ~80%). You need compelling advantages: interpretability + transferability + comparable accuracy, or hybrid approach showing TDA provides complementary information.

**Earth-Mars is feasible**: Well-established methodology, especially for specific landforms. Use dimensionless parameters, match resolutions carefully, and TDA's inherent invariances are actually an advantage here.

**Defensibility requires rigor**: Multi-site validation, fair baseline comparison, statistical significance, honest limitations. Follow the geomorphons/HAND paper template.

**Hybrid approaches work best**: The Syzdykbayev 2024 lesson is clear—TDA alone had false positives; TDA + traditional features performed best. Don't fight this; embrace it.

### Recommended Research Design

**Phase 1: Proof of Concept** (essential for proposal)
- Select 2-3 study sites with published geomorphic maps (ground truth)
- Choose one well-defined landscape classification task (e.g., 5-10 landform classes)
- Compute TDA features (sublevel set, cubical complex, persistence landscapes)
- Baseline comparison: geomorphons + Random Forest with traditional features
- Test: TDA alone, Traditional alone, Hybrid
- Expected outcome: Demonstrate feasibility and identify where TDA helps

**Phase 2: Earth-Mars Comparison** (if Phase 1 succeeds)
- Select specific landform type (dunes or valleys recommended)
- Compile matched-resolution datasets (HiRISE + LiDAR or MOLA + coarsened SRTM)
- Compute dimensionless topological features
- Test hypothesis: Do Earth-Mars analogs share topological signatures?
- Quantify similarity with bottleneck/Wasserstein distances
- Validate: Do TDA-identified "similar" regions match geomorphologist assessments?

**Phase 3: Method Refinement** (publishable methods paper)
- Expand to 5+ diverse study sites (fluvial, aeolian, glacial, volcanic, karst)
- Rigorous multi-site validation
- Transferability testing (train on site A, test on B, C, D)
- Computational efficiency analysis
- Software development (Python package or GRASS GIS integration)

### Your Proposal Narrative Structure

**Title**: "Topological Signatures of Landscapes: Using Persistent Homology for Transferable Geomorphic Classification"

**Problem Statement**: "Automated landscape classification faces a fundamental tradeoff: unsupervised methods achieve efficiency but cannot distinguish process; supervised deep learning achieves accuracy but lacks interpretability and transferability across regions. Geomorphometry needs methods that extract interpretable, theoretically-grounded features that generalize across geographic contexts. Persistent homology—which quantifies multi-scale topological features with proven stability—offers this, yet has never been rigorously tested for landscape classification."

**Research Questions**:
1. Do topological signatures (persistent homology features) discriminate landscape types as effectively as traditional geomorphometric parameters?
2. Does combining topological and geometric features improve classification beyond either alone?
3. Do topological signatures transfer better across geographic regions than pixel-level features?
4. [If including Mars] Do Earth-Mars regions formed by similar processes share topological signatures despite different scales and gravity?

**Approach**:
- Compute persistent homology (H₀, H₁) using sublevel set filtration on DEMs
- Vectorize with persistence landscapes (parameter-free) and images (interpretable)
- Test on N sites with published ground truth geomorphic maps
- Rigorous comparison: TDA vs geomorphons vs Random Forest vs hybrid
- Statistical validation: cross-validation + independent test regions
- [If Mars] Dimensionless topological comparison Earth-Mars analogs

**Expected Contributions**:
1. First rigorous assessment of TDA for landscape classification with quantitative baseline comparison
2. Demonstration of topological features' interpretability and transferability
3. Open-source implementation (GRASS GIS plugin or Python package)
4. [If Mars] Methodology for quantifying Earth-Mars topographic similarity using topology

**Defensibility**: "This is necessary because [specific failure mode of existing methods]. TDA addresses this by [specific mechanism]. We will prove this works by [rigorous multi-site validation with statistical comparison]."

### Honest Risk Assessment

**What could go wrong**:
1. **TDA doesn't outperform baselines**: Possible. Mitigation: Position as complementary (hybrid approach) or focus on interpretability advantage.
2. **Computational cost too high**: Unlikely for DEMs (cubical complexes efficient), but acknowledge and quantify.
3. **Topological signatures don't transfer**: Would contradict theory but possible. Mitigation: Multi-site design lets you quantify transferability drop; honesty about limitations strengthens rather than weakens paper.
4. **Reviewers ask "why not just use geomorphons?"**: This is THE question. Answer: "Geomorphons succeed at morphological classification but cannot distinguish process and provide limited transferability. TDA provides interpretable topological features that capture drainage connectivity, peak relationships, and basin structure that geomorphons miss. We demonstrate this empirically by [results showing where TDA helps]."

**What makes this defensible despite risks**:
- Rigorous comparative methodology
- Multiple baselines
- Honest about limitations
- Theoretical justification (stability theorems)
- Embracing hybrid approach (TDA + traditional features)

### Final Recommendation

**This is achievable and defensible if you**:
1. Design rigorous comparisons into your study from the start
2. Test on multiple sites with different landscape types
3. Embrace hybrid approaches (don't claim TDA alone is sufficient)
4. Focus on interpretability and transferability as key advantages
5. Acknowledge limitations honestly
6. Follow the geomorphons/HAND paper structure for methods paper

**This will fail if you**:
1. Just apply TDA without comparative validation
2. Test on single site or landscape type
3. Claim TDA superiority without statistical proof
4. Ignore the Syzdykbayev 2024 lesson about false positives
5. Overclaim generality from limited testing

**Bottom line**: You're genuinely pioneering. The field is wide open. Success requires proving necessity through rigorous empirical comparison, not just demonstrating novelty. Design your study to answer "why is this necessary?" from day one, and you'll produce defensible, publishable research that advances the field.

The opportunity is real. The path is challenging but clear. Execute with rigor and honesty, and you'll contribute genuinely valuable methodology to geomorphometry.