# PROPOSAL COMPARISON: Original vs. Revised Scope

**Purpose:** Clear side-by-side comparison for committee review  
**Date:** October 30, 2025

---

## RESEARCH QUESTIONS

| **Original Proposal** | **Revised Proposal (Recommended)** |
|-----------------------|-------------------------------------|
| **RQ1:** Does Euler characteristic suffice or is full PH necessary? PLUS vectorization comparison (landscapes vs. images vs. scalars) | **Primary RQ:** Can EC provide computationally efficient classification with accuracy comparable to PH? |
| **RQ2:** Do hybrid models (TDA + traditional) outperform either alone? | **Sub-question (RQ1d):** Do EC+Traditional hybrids improve accuracy? |
| **RQ3:** Do topological features transfer better spatially than traditional features? | **Sub-question (RQ1c):** Do EC features transfer across provinces as well as PH? |
| **RQ4:** Can topological features map to geological processes more directly? | **Sub-question (RQ1d):** Which EC features discriminate provinces and why? |
| **TOTAL: 4 independent RQs** | **TOTAL: 1 primary RQ with 3 focused sub-questions** |

---

## METHODS AND MODELS

| **Aspect** | **Original** | **Revised** |
|------------|--------------|-------------|
| **Topological methods** | EC + 3 PH vectorizations (landscapes, images, scalar summaries) | EC + 1 PH vectorization (landscapes only) |
| **Traditional baseline** | Geomorphometry + Geomorphons + multiple ML models | Geomorphometry + Geomorphons (single RF baseline) |
| **Total models tested** | 10+ (Traditional, Geomorphons, EC, PH scalars, PH landscapes, PH images, Hybrid×3, Ensemble) | 4 (Traditional, EC-only, PH landscapes-only, EC+Traditional) |
| **Scales tested** | Multi-scale: 1 km, 5 km, 10 km windows | Single scale: 1 km windows only |
| **Advanced methods** | Mapper algorithm, TLSPs via sliding windows (if time) | None - focus on core comparison |
| **ML algorithms** | RF, XGBoost, Cubist, ensemble stacking | RF only (standard for terrain classification) |

---

## SAMPLE SIZE AND SCOPE

| **Aspect** | **Original** | **Revised** |
|------------|--------------|-------------|
| **Sites per province** | 20-30 sites | 20 sites |
| **Total provinces** | 4 (Blue Ridge, Coastal Plain, Valley & Ridge, Piedmont) | 3-4 (Piedmont optional based on testbed) |
| **Total sites** | 80-120 | 60-80 |
| **Windows per site** | 1-3 (multi-scale) | 1 (single scale) |
| **Total analysis units** | 240-360 | 60-80 |
| **Computational load** | 40-80 hours PH + multi-scale + vectorizations | 30 hours PH + EC (~5 hours) |

---

## VALIDATION STRATEGY

| **Aspect** | **Original** | **Revised** |
|------------|--------------|-------------|
| **Primary validation** | Spatial block CV (5-fold) with extensive exploration of block size | Standard 5-fold CV (primary results) |
| **Secondary validation** | Random CV for comparison (show inflation) | Leave-one-province-out (transferability test) |
| **Tertiary validation** | Leave-one-province-out AND distance-decay analysis | None (streamlined) |
| **Spatial CV exploration** | Test multiple block sizes, compare CV strategies | Single approach: leave-one-province-out only |
| **CV controversy** | Extensive discussion of Roberts vs. Ploton vs. Wadoux | Brief acknowledgment, choose pragmatic approach |

---

## STATISTICAL TESTING

| **Aspect** | **Original** | **Revised** |
|------------|--------------|-------------|
| **Primary test** | MANOVA on topological feature space | Confusion matrices (standard for classification) |
| **Model comparison** | McNemar's test for all pairwise (45+ tests for 10 models) | McNemar's test for 3 key comparisons (EC vs. Traditional, PH vs. Traditional, Hybrid vs. both) |
| **Multiple testing correction** | Debate Holm-Bonferroni vs. Benjamini-Hochberg | Use Benjamini-Hochberg (more powerful, standard choice) |
| **Effect sizes** | Cohen's d, ΔR², Matthews Correlation Coefficient | Cohen's d, bootstrap CI (simpler, sufficient) |
| **Power analysis** | Complex MANOVA power with spatial autocorrelation adjustment | Acknowledge limited power; prioritize effect sizes over p-values |
| **Pre-registration** | Discuss pre-registering hypotheses to avoid p-hacking | State expected results upfront but don't formally pre-register |

---

## TIMELINE

| **Phase** | **Original Duration** | **Revised Duration** | **Reduction** |
|-----------|-----------------------|----------------------|---------------|
| **Testbed** | 12 weeks (3 months) | 12 weeks (3 months) | No change ✓ |
| **Data acquisition** | 3 months | 2 months | -1 month |
| **Feature extraction** | 4 months (multi-scale, all vectorizations) | 3 months (single scale, EC + PL only) | -1 month |
| **Modeling** | 3 months (10+ models, extensive CV) | 2 months (4 models, streamlined) | -1 month |
| **Transferability** | 3 months (spatial CV + leave-one-out + distance decay) | 3 months (leave-one-province-out only) | No change |
| **Advanced methods** | 3 months (if time allows) | 0 months (cut entirely) | -3 months |
| **Interpretation** | 3 months | 3 months | No change |
| **Thesis writing** | 2 months (first draft) + 3 months (revisions) | 2 months (draft) + 6 months (revisions) | +1 month for writing |
| **TOTAL** | **27 months research + 5 months writing = 32 months** (realistically 36-42) | **16 months research + 8 months writing = 24 months** | **-8 to -18 months** |

---

## COMPUTATIONAL REQUIREMENTS

| **Resource** | **Original** | **Revised** | **Benefit** |
|--------------|--------------|-------------|-------------|
| **PH computation time** | 80-120 sites × 30-45 min = 40-90 hours | 60-80 sites × 30 min = 30-40 hours | -25% time |
| **EC computation time** | 80-120 sites × 5 min = 7-10 hours | 60-80 sites × 5 min = 5-7 hours | Already fast |
| **Multi-scale overhead** | 3× for each scale | 1× (no multi-scale) | -66% total compute |
| **Vectorization methods** | 3 methods × all sites | 1 method × all sites | -66% vectorization time |
| **Total computational load** | ~150-200 CPU-hours | ~40-50 CPU-hours | **-75% reduction** |
| **HPC requirement** | Strongly recommended | Helpful but not required | Can use laptop if needed |

---

## DELIVERABLES

| **Deliverable** | **Original** | **Revised** |
|-----------------|--------------|-------------|
| **Testbed report** | 15-20 pages | 15-20 pages ✓ |
| **Thesis length** | 150-200 pages (PhD-length) | 100-120 pages (Master's-standard) |
| **Thesis chapters** | 5 chapters + extensive appendices | 5 chapters + focused appendices |
| **Publications expected** | 2-3 papers (too optimistic for Master's) | 1 paper (realistic) |
| **Code repository** | GitHub + Zenodo DOI ✓ | GitHub + Zenodo DOI ✓ |
| **Docker/Conda** | Not mentioned | Required (committee asked for this) |

---

## SUCCESS CRITERIA COMPARISON

### Original Proposal (3 Tiers)

**Tier 1 (Minimum):** ≥70% accuracy, topological features contribute significantly  
**Tier 2 (Strong):** ≥80% accuracy, hybrid outperforms by ≥5%  
**Tier 3 (Exceptional):** ≥85% accuracy, ≥10% improvement, transferability demonstrated

### Revised Proposal (More Realistic)

**Tier 1 (Minimum):** ≥65% accuracy (better than random 33%), computational advantage documented  
**Tier 2 (Strong):** ≥75% accuracy, EC within 10% of PH but 5-10× faster  
**Tier 3 (Exceptional):** EC matches/exceeds PH accuracy with major computational advantage

**Key difference:** Original focused on absolute accuracy; revised focuses on **computational-accuracy tradeoff**

---

## GEOLOGICAL INTERPRETATION

| **Aspect** | **Original** | **Revised** |
|------------|--------------|-------------|
| **Spatial scale** | Assumes 1 km windows capture fold architecture | Acknowledges 1 km = local scale, NOT fold wavelength |
| **Valley & Ridge prediction** | "High H₁ from parallel ridges enclosing valleys" (fold scale) | "High H₁ from local valley sidewalls" (hillslope scale) |
| **Blue Ridge prediction** | "Isolated peaks from complex fold interference" | "High H₀ from local terrain ruggedness" |
| **Scale limitation** | Mentioned briefly | **Explicitly acknowledged:** "Future work needed for fold-scale analysis" |
| **Geological outcomes** | Ambitious claims about fold architecture | Modest claims about local-scale topological differences |

---

## WHAT STAYS THE SAME (Your Strengths)

✓ **Testbed-then-scale design** with objective decision gate  
✓ **Reproducibility plan** (code, data, documentation)  
✓ **Spatial awareness** (acknowledge autocorrelation, use appropriate validation)  
✓ **Multiple success pathways** (publishable even if TDA underperforms)  
✓ **SHAP interpretability** analysis  
✓ **Computational benchmarking** (runtime, memory, scalability)  
✓ **Honest uncertainty** (framed as methods comparison, not TDA advocacy)

---

## WHAT CHANGES (And Why)

### Major Changes:

1. **Research focus:** From "comprehensive TDA evaluation" → "EC vs. PH computational efficiency"
2. **Sample size:** From 80-120 sites × 3 scales = 240-360 units → 60-80 sites × 1 scale = 60-80 units
3. **Model count:** From 10+ models → 4 core models
4. **Timeline:** From 32-42 months realistic → 24 months achievable
5. **Scope:** From PhD dissertation → focused Master's thesis

### Why These Changes Matter:

**Feasibility:** 24 months is realistic for Master's; 32-42 months is not  
**Focus:** 1 clear question > 4 partial answers  
**Novelty:** EC for terrain is genuinely novel; vectorization comparison is incremental  
**Graduation:** Reduces risk of not finishing

---

## RISK ASSESSMENT

| **Risk** | **Original Proposal** | **Revised Proposal** |
|----------|----------------------|----------------------|
| **Doesn't finish in time** | HIGH (too much work) | LOW (realistic scope) |
| **Computational bottleneck** | MEDIUM (40-90 hrs PH, need HPC) | LOW (30-40 hrs, laptop feasible) |
| **Methods don't work** | MEDIUM (but still publishable) | LOW (EC speed advantage is contribution regardless) |
| **Weak geology connection** | MEDIUM (ambitious fold predictions) | LOW (modest local-scale claims) |
| **Committee rejection** | HIGH (currently PhD scope) | LOW (focused, realistic Master's) |

---

## RECOMMENDATIONS SUMMARY

### DO THIS:
1. ✅ Focus on EC vs. PH computational efficiency (Option A from main document)
2. ✅ Cut to 4 models, 60-80 sites, single scale
3. ✅ Keep testbed-then-scale design (it's excellent)
4. ✅ Fix β₂≈0 mathematical justification
5. ✅ Add scale limitation discussion (1 km = local topology, not fold architecture)
6. ✅ Update literature review with missing citations
7. ✅ Add Docker/Conda environment specification

### DON'T DO THIS:
1. ❌ Try to keep all 4 RQs by "streamlining" - you can't streamline 4 questions into 1 thesis
2. ❌ Argue with committee about scope - they're right, listen to them
3. ❌ Add more methods to "strengthen" - addition = subtraction from Master's feasibility
4. ❌ Defend multi-scale as "essential" - it's nice-to-have for PhD, not required for Master's
5. ❌ Push back on "new geological knowledge" critique - reframe contribution, don't defend

---

## THE BOTTOM LINE

**Original = PhD Dissertation**  
→ 4 research questions  
→ 10+ models, 3 scales  
→ 32-42 months realistic timeline  
→ 2-3 expected publications  
→ Risk: Don't finish

**Revised = Focused Master's Thesis**  
→ 1 clear research question  
→ 4 core models, 1 scale  
→ 24 months achievable timeline  
→ 1 strong publication  
→ Benefit: Graduate on time with solid contribution

**Committee will approve:** A focused, realistic proposal with clear contribution  
**Committee will NOT approve:** An overly ambitious proposal that student cannot complete

**Your choice is clear: Scope down, execute rigorously, graduate successfully.**

---

## NEXT STEPS (Action Items)

1. **Read:** Full literature review document (~50 pages)
2. **Decide:** Commit to Option A (EC Thesis) or alternative
3. **Schedule:** 1-hour committee meeting to discuss revised scope
4. **Revise:** Cut proposal to 30-40 pages, single RQ focus
5. **Add:** Missing sections (computational efficiency, scale limitations, revised geology)
6. **Fix:** Mathematical justifications, literature review gaps
7. **Resubmit:** Within 2-3 weeks for final approval

