# REVISED THESIS PROPOSAL: ONE-PAGE EXECUTIVE SUMMARY

**Student:** Michael Kerr  
**Date:** October 30, 2025  
**Degree:** Master of Science (2.5 years)

---

## PROPOSED REVISION: From PhD Scope to Focused Master's Thesis

### ORIGINAL PROPOSAL (Current)
- **4 Research Questions** spanning methods comparison, hybrid integration, spatial transferability, and interpretability
- **10+ models** to compare (EC, 3 PH vectorizations, traditional, hybrids, ensembles)
- **Multi-scale analysis** (1 km, 5 km, 10 km windows)
- **80-120 sites** across 4 provinces with extensive spatial CV exploration
- **Advanced methods** (Mapper, TLSPs if time allows)
- **Estimated timeline:** 27-30 months of research + writing (actually 36-42 months realistic)
- **Verdict:** PhD dissertation scope, not Master's thesis

### REVISED PROPOSAL (Recommended)
- **1 Primary Research Question:** Can Euler characteristic analysis provide computationally efficient landscape classification with accuracy comparable to full persistent homology?
- **4 models** to compare (Traditional, EC-only, PH landscapes-only, EC+Traditional hybrid)
- **Single scale** (1 km windows), multi-scale deferred to future work
- **60-80 sites** across 3-4 provinces with standard CV + leave-one-province-out
- **No advanced methods** - focus on core EC vs. PH comparison
- **Estimated timeline:** 16 months research + 8 months writing = 24 months total
- **Verdict:** Rigorous, focused Master's thesis with clear contribution

---

## WHY EULER CHARACTERISTIC? (Your Novel Contribution)

**The Gap:** Euler characteristic has **never been systematically applied to terrain classification** despite being:
- Computationally efficient (5-10 min/site vs. 30-45 min for full PH)
- Theoretically well-understood (parameter-free)
- Widely used in other domains (cosmology, material science, chemical engineering)

**The Question:** Is the 5-10× computational speedup worth the potential accuracy loss? Or does EC capture sufficient topological information for landscape classification?

**The Contribution:** Establishing whether expensive PH computation is necessary, or whether simple EC suffices—a practical question with immediate value for continent-scale geomorphometric applications.

---

## WHAT YOU SACRIFICE (And Why It's OK)

| **Removed** | **Rationale** |
|------------|---------------|
| Persistence images comparison | PH landscapes sufficient; images more for visualization |
| Multi-scale analysis (3 scales) | Single scale establishes feasibility; multi-scale for PhD |
| Advanced methods (Mapper, TLSPs) | Too ambitious; focus on core comparison |
| Extensive spatial CV comparison | Pick one approach (leave-one-province-out); don't wade into CV controversy |
| 6 extra models | 4 models sufficient for key comparisons |

**Key principle:** Answer ONE question excellently, not FOUR questions adequately.

---

## WHAT YOU KEEP (Your Strengths)

✓ **Testbed-then-scale design** - 3-month proof-of-concept with objective decision gate  
✓ **Rigorous validation** - Standard CV + leave-one-province-out transferability test  
✓ **Computational benchmarking** - Runtime, memory, scalability analysis (your key contribution)  
✓ **Reproducibility** - GitHub + Zenodo DOI, Docker container, complete pipeline  
✓ **SHAP interpretability** - Which EC features discriminate provinces?  
✓ **Multiple success pathways** - Publishable regardless of whether EC "wins"

---

## REVISED TIMELINE (24 Months)

| **Phase** | **Duration** | **Deliverables** |
|-----------|-------------|------------------|
| **Testbed** | Months 1-3 | 60 sites, 4 models, decision gate report |
| **Main Study** | Months 4-16 | Scale to 80 sites, all analyses, computational benchmarks |
| **Writing** | Months 17-24 | Complete thesis, defense, revisions |
| **Buffer** | Built-in | 2 weeks per phase for delays |

---

## SUCCESS CRITERIA (Realistic for Master's)

**Tier 1 (Minimum Success):** EC achieves ≥65% accuracy; computational advantage documented → **You graduate**

**Tier 2 (Strong Success):** EC within 10% of PH accuracy but 5-10× faster → **Strong thesis, good job prospects**

**Tier 3 (Exceptional):** EC matches/exceeds PH accuracy with major speed advantage → **Top-tier thesis, PhD fellowship quality**

**Critical insight:** Success ≠ "EC beats PH." Success = understanding the computational-accuracy tradeoff.

---

## ADDRESSING COMMITTEE CONCERNS

| **Concern** | **Response** |
|-------------|--------------|
| **Scope creep** | Cut from 4 RQs to 1; from 10 models to 4; from 27 months to 16 months research |
| **Novelty vs. validation** | Frame as "computational geomorphometry" not pure methods; EC for terrain is novel |
| **Geological knowledge** | Revise predictions for local-scale (1 km) topology, not fold architecture; acknowledge scale limitation |
| **Scale mismatch** | Accept 1 km = local scale; explicitly state we're NOT capturing fold wavelength (for PhD) |
| **Math claims** | Fix β₂≈0 justification; add proper theoretical explanation |

---

## THE BOTTOM LINE

**Current proposal verdict:** PhD scope - you cannot finish this in 2.5 years

**Revised proposal verdict:** Focused Master's thesis answering a clear, valuable question

**Your choice:** 
- Option A: Accept scope reduction → Graduate in 2.5 years with strong thesis
- Option B: Try to do everything → Burn out, extend timeline, possibly don't finish

**Committee recommendation:** Revise and resubmit with Option A focus.

---

## NEXT STEPS

1. **Schedule committee meeting** (1 hour) to discuss revised scope
2. **Revise proposal** cutting to 30-40 pages with single RQ focus
3. **Add missing sections:** computational efficiency rationale, scale limitations, revised geological outcomes
4. **Fix mathematical claims:** β₂≈0 justification, EC theoretical background
5. **Update literature review:** add Bhuyan 2024, Wadoux 2021, Smith & Zavala 2021
6. **Resubmit for approval** within 2-3 weeks

---

**Contact for questions:**  
Michael Kerr, Graduate Student  
Department of Geography  
University of Georgia

