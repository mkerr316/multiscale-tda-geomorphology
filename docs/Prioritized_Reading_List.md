# Prioritized Reading List for Thesis Revision

**Purpose:** Essential papers to read BEFORE revising your proposal  
**Timeline:** 1-2 weeks of focused reading  
**Organized by:** Priority level and topic area

---

## TIER 1: MUST READ IMMEDIATELY (This Week)

### 1. The Bhuyan Paper (Your Key Comparison Point)

**Citation:** Bhuyan, K., Rana, K., Ferrer, J.V., Cotton, F., Ozturk, U., Catani, F., & Malik, N. (2024). Landslide topology uncovers failure movements. *Nature Communications*, 15, 2633. https://doi.org/10.1038/s41467-024-46741-7

**Why critical:** This is the 2024 Nature Communications paper your proposal keeps citing. You need to understand:
- What topological features they actually used (ALH, ALC, Betti curves - NOT full persistence diagrams)
- Their 80-94% cross-continental accuracy claims
- How they integrated topological with geometric features
- Their interpretation methods

**Key finding:** Topological features (94% accuracy) vastly outperformed geometric features alone (~65%), but the integration was essential. They found "notable false positives" with pure topological information.

**Action:** Read their Methods and Feature Extraction sections carefully. Note that they analyzed landslide polygon topology, not continuous DEM analysis like you're proposing.

**Open access:** Yes (Nature Communications open access)  
**Time to read:** 2-3 hours

---

### 2. The Spatial CV Debate (You MUST Understand This)

**PRO-Spatial CV Paper:**

**Citation:** Ploton, P., Mortier, F., Réjou-Méchain, M., et al. (2020). Spatial validation reveals poor predictive performance of large-scale ecological mapping models. *Nature Communications*, 11, 4540. https://doi.org/10.1038/s41467-020-18321-y

**Key finding:** Random CV yielded R²=0.53 (strong), but spatial CV revealed true R²=0.14 (near-null). Models predicted via spatial proximity, not environmental relationships. 28-50% performance inflation documented.

**ANTI-Spatial CV Paper:**

**Citation:** Wadoux, A.M.J.-C., Brus, D.J., & Heuvelink, G.B.M. (2021). Spatial cross-validation is not the right way to evaluate map accuracy. *Methods in Ecology and Evolution*, 12, 2138-2149. https://doi.org/10.1111/2041-210X.13650

**Key finding:** Spatial CV "has no theoretical underpinning" and severely overestimates errors (pessimistic bias). Standard CV with probability sampling is more appropriate for map accuracy assessment.

**BALANCED Review:**

**Citation:** Roberts, D.R., Bahn, V., Ciuti, S., et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography*, 40, 913-929. https://doi.org/10.1111/ecog.02881

**Key takeaway:** Different CV strategies test different questions. Spatial CV tests model transferability (extrapolation), not map accuracy. Choose method based on your actual research objective.

**Action:** Read all three papers. Understand the controversy. Your proposal currently takes Ploton's side uncritically; you need to present a more nuanced view.

**Time to read:** 4-5 hours total for all three

---

### 3. Euler Characteristic Foundations (Your Core Method)

**Citation:** Smith, A., & Zavala, V.M. (2021). The Euler characteristic: A general topological descriptor for complex data. *Computers & Chemical Engineering*, 154, 107463. https://doi.org/10.1016/j.compchemeng.2021.107463

**Why critical:** This is the most comprehensive recent review of EC as a topological descriptor. Covers:
- Mathematical foundations you need to fix your β₂≈0 claim
- Applications to 2D spatial fields (relevant for DEMs)
- Computational advantages over full persistent homology
- Interpretability and limitations

**Key sections:**
- Section 2: EC definition and properties (fix your math)
- Section 5: 2D spatial fields example (directly relevant)
- Section 6: Computational efficiency discussion

**Action:** Use this to rewrite your EC justification (Lines 156-159 in original proposal). Their explanation of why EC works for height fields is exactly what you need.

**Access:** Behind paywall, but available on ResearchGate  
**Time to read:** 3-4 hours

---

## TIER 2: READ BEFORE REVISING METHODS SECTION (Within 2 Weeks)

### 4. Persistence Landscapes (Your PH Vectorization Method)

**Citation:** Bubenik, P. (2015). Statistical topological data analysis using persistence landscapes. *Journal of Machine Learning Research*, 16, 77-102. http://jmlr.org/papers/v16/bubenik15a.html

**Why important:** You're using persistence landscapes as your primary PH vectorization. You should understand:
- Why they're theoretically stable (1-Wasserstein stability)
- How to choose number of landscapes (you say 5, but why?)
- Computational properties compared to images

**Key sections:**
- Section 3: Definition and properties
- Section 4: Statistical properties and stability
- Section 6: Applications examples

**Open access:** Yes (JMLR open access)  
**Time to read:** 2-3 hours (technical, slow reading)

---

### 5. Spatial CV Implementation (Practical Guide)

**Citation:** Valavi, R., Elith, J., Lahoz-Monfort, J.J., & Guillera-Arroita, G. (2019). blockCV: An r package for generating spatially or environmentally separated folds for k-fold cross-validation of species distribution models. *Methods in Ecology and Evolution*, 10, 225-232. https://doi.org/10.1111/2041-210X.13107

**Why important:** This is THE practical guide for implementing spatial block CV. Provides:
- How to determine block size (2× autocorrelation range)
- blockCV R package implementation
- Comparison to random CV on real data

**Action:** If you decide to use spatial block CV (not required for revised scope), this is your implementation guide.

**Time to read:** 1-2 hours + package vignettes

---

### 6. SHAP for Random Forests (Interpretability)

**Citation:** Lundberg, S.M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems*, 30. https://proceedings.neurips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html

**Original SHAP paper - the foundational work**

**Citation:** Hooker, G., Mentch, L., & Zhou, S. (2023). Debiasing SHAP scores in random forests. *AStA Advances in Statistical Analysis*, 107, 421-454. https://doi.org/10.1007/s10182-023-00479-7

**Recent critical work showing SHAP bias toward high-cardinality features**

**Why important:** Your proposal uses SHAP for interpretability (good choice), but you should know its limitations. Recent work shows SHAP inflates importance of continuous/high-cardinality features - relevant since EC features are continuous.

**Action:** Read both. Understand that SHAP is powerful but imperfect. Mention these limitations when discussing interpretability.

**Time to read:** 3 hours total

---

## TIER 3: READ IF TIME ALLOWS (Background Knowledge)

### 7. Geomorphometry Reviews (Understanding the Field)

**Citation:** Pike, R.J., Evans, I.S., & Hengl, T. (2009). Geomorphometry: A brief guide. In *Developments in Soil Science* (Vol. 33, pp. 3-30). Elsevier. https://doi.org/10.1016/S0166-2481(08)00001-9

**Why useful:** Classic review of geomorphometry as a field. Helps you understand traditional methods you're comparing against.

**Time to read:** 2 hours

---

**Citation:** Amatulli, G., McInerney, D., Sethi, T., et al. (2020). Geomorpho90m, empirical evaluation and accuracy assessment of global high-resolution geomorphometric layers. *Scientific Data*, 7, 162. https://doi.org/10.1038/s41597-020-0479-6

**Why useful:** Modern geomorphometry dataset and methods. Shows state-of-the-art for terrain classification. Includes geomorphons (your baseline).

**Time to read:** 1-2 hours

---

### 8. Other TDA-Terrain Papers (Know Your Competition)

**Citation:** Syzdykbayev, M., Karimi, B., & Karimi, H.A. (2020). Persistent homology on LiDAR data to detect landslides. *Remote Sensing of Environment*, 246, 111816. https://doi.org/10.1016/j.rse.2020.111816

**The 2020 paper showing 70-96% landslide detection accuracy**

**Follow-up (harder to find):** Syzdykbayev et al. (2024) found "notable false positives" with pure topological information. Need to track this down - likely a conference paper or preprint.

**Time to read:** 1-2 hours

---

**Citation:** Corcoran, P., & Jones, C.B. (2023). Topological data analysis for geographical information science using persistent homology. *International Journal of Geographical Information Science*, 37(4), 712-745. https://doi.org/10.1080/13658816.2022.2147530

**Why useful:** Recent review of TDA for GIS applications. Broader context for your work.

**Time to read:** 2-3 hours

---

## TIER 4: OPTIONAL DEEP DIVES

### Persistent Homology Foundations
- Edelsbrunner, H., & Harer, J. (2010). *Computational Topology: An Introduction*. AMS. (Textbook)
- Cohen-Steiner, D., Edelsbrunner, H., & Harer, J. (2007). Stability of persistence diagrams. *Discrete & Computational Geometry*, 37, 103-120.

### Geomorphons (Your Baseline Method)
- Jasiewicz, J., & Stepinski, T.F. (2013). Geomorphons—a pattern recognition approach to classification and mapping of landforms. *Geomorphology*, 182, 147-156.

### Spatial Autocorrelation Theory
- Cressie, N.A.C. (1993). *Statistics for Spatial Data* (Revised Edition). Wiley.
- Legendre, P. (1993). Spatial autocorrelation: Trouble or new paradigm? *Ecology*, 74, 1659-1673.

---

## READING STRATEGY (1-2 Week Plan)

### Week 1: Core Papers (Must Read)
- **Monday-Tuesday:** Bhuyan et al. 2024 (Nature Comm) - understand their methods and results
- **Wednesday:** Ploton et al. 2020 (pro spatial CV)
- **Thursday:** Wadoux et al. 2021 (anti spatial CV) + Roberts et al. 2017 (balanced view)
- **Friday:** Smith & Zavala 2021 (EC foundations)

**Weekend:** Start drafting revised EC justification (Lines 156-159) using Smith & Zavala

### Week 2: Methods Papers + Begin Revisions
- **Monday:** Bubenik 2015 (persistence landscapes)
- **Tuesday:** SHAP papers (Lundberg 2017 + Hooker 2023)
- **Wednesday:** Valavi 2019 (if using spatial CV)
- **Thursday-Friday:** Begin proposal revisions based on reading

**Weekend:** Complete first draft of revised proposal sections

---

## CITATION MANAGEMENT TIPS

**Essential citations to add to your proposal:**

**Intro/Literature Review:**
- Bhuyan et al. (2024) - landslide topology, Nature Comm ← YOUR KEY REFERENCE
- Wadoux et al. (2021) - spatial CV controversy ← BALANCE THE DEBATE
- Smith & Zavala (2021) - EC foundations ← JUSTIFY YOUR METHOD

**Methods:**
- Bubenik (2015) - persistence landscapes theory
- Valavi et al. (2019) - blockCV implementation (if using)
- Lundberg & Lee (2017) - SHAP foundations

**Revise/Remove:**
- Your claim of "<5 rigorous papers" needs updating - say "fewer than 15 applications, fewer than 5 with rigorous validation"
- Add Syzdykbayev 2024 finding on "false positives" to balance your TDA enthusiasm
- Cite Pike et al. 2009 and Amatulli et al. 2020 for geomorphometry baseline

---

## KEY TAKEAWAYS FROM READING

After completing Tier 1-2 reading, you should be able to:

1. **Explain EC properly:** Why β₂=0 for 2D height fields (sublevel filtration on 2D surface)
2. **Navigate spatial CV debate:** Understand both pro (Ploton) and anti (Wadoux) positions; choose pragmatic middle ground
3. **Cite Bhuyan correctly:** Know what they actually did (landslide polygon topology) vs. what you're doing (continuous DEM analysis)
4. **Justify persistence landscapes:** Explain why you chose landscapes over images (stability, theoretical guarantees)
5. **Use SHAP appropriately:** Understand limitations (bias toward continuous features) while leveraging interpretability

---

## QUESTIONS TO ANSWER AFTER READING

1. **For committee meeting:**
   - Why EC instead of full PH? (Answer: computational efficiency, parameter-free, theoretically sound)
   - Why not just use traditional geomorphometry? (Answer: test if topology adds information; EC is novel for terrain)
   - What if EC fails? (Answer: still publishable as negative result, documents failure modes)

2. **For proposal revision:**
   - Which spatial CV approach makes sense for my research question? (Answer: leave-one-province-out for transferability)
   - How do I frame EC mathematically? (Answer: use Smith & Zavala explanation)
   - What's my baseline comparison? (Answer: RF on geomorphometry + geomorphons)

3. **For yourself:**
   - Is this a 2.5-year thesis or a 4-year PhD? (Answer after revisions: 2.5-year Master's if you focus on EC vs. PH only)
   - What's my unique contribution? (Answer: first systematic EC application to terrain classification with computational benchmarking)
   - What happens if it doesn't work? (Answer: still graduate; publish "why EC failed"; save others from wasting time)

---

## WHERE TO FIND PAPERS

**Open Access:**
- Nature Communications papers (Bhuyan, Ploton): Direct from journal website
- JMLR papers (Bubenik): http://jmlr.org
- ArXiv preprints: https://arxiv.org

**Behind Paywalls (Access via University):**
- Smith & Zavala 2021: Try ResearchGate if no institutional access
- Methods in Ecology and Evolution (Wadoux, Valavi): Check university library
- Ecography (Roberts): Check university library

**If you can't access:**
- Email authors directly (most will send PDF)
- Check author personal websites (many post PDFs)
- ResearchGate often has author-uploaded versions
- Your university ILL (Interlibrary Loan) service

---

## FINAL READING RECOMMENDATION

**START HERE:** Bhuyan et al. 2024 + Smith & Zavala 2021 + Wadoux et al. 2021

These three papers address your committee's biggest concerns:
1. **Bhuyan:** What does TDA for terrain actually look like? (They're your comparison point)
2. **Smith & Zavala:** How do I explain EC mathematically? (Fix your β₂≈0 claim)
3. **Wadoux:** Am I using spatial CV appropriately? (Navigate the controversy)

**After these three, you'll be able to:**
- Defend your choice of EC as primary method
- Explain the math correctly
- Choose appropriate validation strategy
- Revise your proposal with confidence

**Reading these three papers = 8-10 hours of focused work = Your weekend plan**

---

**Good luck with the reading and revisions! This is doable.**

