

# **A Methodological Framework for Predicting Soil Organic Carbon Using Topological Data Analysis of High-Resolution Topography**

## **Part I: Statistical and Spatial Experimental Design**

This part establishes the statistical foundation of the study, ensuring that the experimental design is robust, adequately powered, and accounts for the complex spatial and multivariate nature of the data. A rigorous design is paramount to ensuring that any detected differences are statistically meaningful and not artifacts of insufficient sampling or unmitigated spatial dependencies.

### **Section 1.1: Power, Sampling, and Provincial Analysis**

This section addresses the core statistical design questions related to hypothesis testing across the five provinces of interest.

#### **1.1.1 Sample Size and Statistical Power for Provincial Comparison (MANOVA)**

The primary hypothesis posits that the suites of topological features, represented by Topological Landscape Summary Profiles (TLSPs), differ significantly across the five provinces. A Multivariate Analysis of Variance (MANOVA) is the appropriate statistical test for this hypothesis, as it simultaneously evaluates group mean differences across several dependent variables while accounting for their intercorrelations.1 To avoid the common pitfall of underpowered studies, which are prone to Type II errors (false negatives), a prospective power analysis is an essential and non-negotiable step in the research design.2 The goal of this analysis is to determine the minimum sample size required per province to detect a scientifically meaningful effect with a specified level of confidence.  
**Effect Size Estimation**  
The cornerstone of any power analysis is the specification of a target effect size. This value quantifies the magnitude of the difference the study aims to detect and should be grounded in existing evidence rather than arbitrary convention.

* **Literature-Based Estimation:** A review of recent (2020-2025) literature on soil organic carbon (SOC) prediction provides a strong basis for estimating a realistic effect size. Studies using various environmental and spectral covariates with machine learning models have reported coefficients of determination ($R^2$) in the range of 0.62 to 0.75.4 These values indicate that a substantial portion of SOC variance is explainable by environmental factors. For the purpose of this study, which seeks to evaluate the *additional* contribution of novel topological features, targeting a small to medium effect size is a conservative and scientifically defensible strategy. An effect size $f^2$ (the standard metric for F-tests) in the range of 0.15 to 0.25, corresponding to approximately 13% to 20% of the variance explained by the provincial differences, represents a reasonable target.  
* **Pilot Data Analysis:** If preliminary data are available from one or two provinces, a direct calculation of the multivariate effect size (e.g., Pillai's Trace or Wilks' Lambda) can be performed. This empirical estimate, derived directly from the study's context, would provide the most robust basis for the power calculation.

**Formal Power Calculation for MANOVA**  
The G\*Power software package is a standard and flexible tool for conducting prospective power analyses for a wide range of statistical tests, including MANOVA.6 The analysis would be configured as follows within the F tests family, selecting MANOVA: Global effects.

* **Type of power analysis:** *A priori* (to compute the required sample size).  
* **Input Parameters:**  
  * *Effect size $f^2(V)$:* This will be derived from the literature review or pilot data, as described above. G\*Power includes a utility to convert from other effect size metrics, such as partial eta-squared ($\\eta\_p^2$).  
  * *α err prob (Type I error rate):* Set to the conventional level of 0.05.9  
  * *Power (1 \- β err prob) (Type II error rate):* Set to the conventional level of 0.80, providing an 80% chance of detecting a true effect.3  
  * *Number of groups:* 5 (for the five provinces).  
  * *Number of response variables:* This corresponds to the number of TLSP summary statistics that will be used as dependent variables. Based on standard practice, extracting metrics such as the mean, max, integral, and $L^2$ norm for both H₀ and H₁ persistence landscapes would result in approximately 8 to 10 response variables.10

It is important to note that specific, step-by-step guides for this exact MANOVA configuration in GPower can be difficult to locate, which introduces a risk of misconfiguration.8 Given this potential for error, a more transparent and rigorous approach is to supplement the GPower calculation with a **simulation-based power analysis**. This method, often employed for complex designs like mixed-effects models 3, involves a computational script (e.g., in R) that performs the following steps:

1. Define the parameters of the multivariate distribution for the five groups, including the mean vectors, covariance matrix, and the target effect size.  
2. Generate a large number (e.g., 5,000) of simulated datasets of a given sample size based on these parameters.  
3. For each simulated dataset, perform a MANOVA and record whether the null hypothesis is rejected at the specified α-level.  
4. The statistical power for that sample size is the proportion of simulations in which the null hypothesis was correctly rejected.  
5. Repeat this process for a range of sample sizes to generate a power curve and identify the sample size that achieves the desired 80% power.

This simulation approach provides a more robust, transparent, and defensible sample size estimate that is tailored precisely to the study's design.  
**Power for Nested Model Comparison ($\\Delta R^2$, Likelihood Ratio Test)**  
A key secondary hypothesis is whether the topological features provide significant explanatory power *above and beyond* a baseline model of traditional covariates. This is formally tested by comparing nested regression models and assessing the significance of the change in R-squared ($\\Delta R^2$) using a likelihood ratio test (LRT).12 Power calculations for LRTs are not straightforward, as their statistical properties can be sensitive to sample size and model specification.12  
Therefore, a simulation-based approach is again recommended. Frameworks available in R packages such as powerlmm and simR can be adapted for this purpose.13 The procedure involves:

1. Defining a "full" data-generating process where the TLSP features are known to contribute a specific, modest amount to the total variance (e.g., an additional 5-10%).  
2. Simulating numerous datasets from this process.  
3. Fitting both the reduced model (baseline covariates only) and the full model (baseline \+ TLSPs) to each simulated dataset and performing an LRT.  
4. Power is calculated as the proportion of simulations where the LRT correctly identifies the contribution of the TLSPs as statistically significant.

**Local Cube Sampling and Within-Province Sample Sizes**  
Local Cube sampling is a sophisticated, spatially balanced sampling method that ensures samples are well-spread across the landscape and can be balanced on auxiliary variables.14 A primary concern is ensuring this method provides sufficient sample density within each province to meet the MANOVA power requirements.  
The correct implementation is a stratified approach:

1. The total required sample size, $N$, is determined from the power analysis.  
2. This total is allocated among the provinces, typically equally ($N/5$ per province).  
3. Within each province, Local Cube sampling is then applied to select the specific sample locations.  
   This hierarchical design guarantees that both the overall spatial balance and the per-province sample size requirements are met. It is important to distinguish this sampling design methodology from the "space-time cube" tools available in GIS software, which are used for data aggregation and visualization rather than for survey design.16

#### **1.1.2 Province-Level Analysis Design**

**Minimum Sample Size per Province for Robust MANOVA**  
While the formal power analysis will ultimately dictate the sample size, several rules of thumb provide a lower bound for MANOVA robustness.

* A common guideline is that the sample size in each group must exceed the number of dependent variables.18 With 8-10 TLSP features, this implies a bare minimum of \>10 samples per province.  
* For robustness against moderate violations of normality, a sample size that yields at least 20 degrees of freedom for the error term is often recommended.20  
  However, these minimums are almost certain to be far below the sample size required to achieve 80% power for detecting a small-to-medium effect size. The result from the formal power analysis should be considered the definitive minimum sample size.

**Provinces as Fixed vs. Random Effects**  
The decision of whether to treat provinces as fixed or random effects fundamentally alters the scope of the research question and the generalizability of the results.

* **Fixed Effects:** This approach treats the five specific provinces as the only entities of interest. The analysis will test for differences *among these five provinces*. The conclusions drawn cannot be statistically generalized to any other provinces.21 This is appropriate if these provinces were selected for their unique and specific characteristics that are the focus of the study.  
* **Random Effects:** This approach treats the five provinces as a random sample from a larger population of all possible provinces in the region. The analysis aims to make an inference about the overall variability *among provinces in general*.21 This is the scientifically stronger and more desirable approach if the goal is to develop a general, widely applicable model of the relationship between topography and SOC.

**Recommendation:** The primary goal of developing a generalizable predictive model strongly favors treating **provinces as a random effect**. However, a known statistical issue is that estimating the variance component for a random effect with only five levels can be unstable.23  
A pragmatic, multi-stage approach is therefore recommended.

1. For the initial provincial comparison, model provinces as a **fixed effect** within the MANOVA framework. This directly and cleanly answers the specific question: "Do the topological signatures of these five specific provinces differ?"  
2. For the main SOC predictive modeling stage, incorporate province as a **random intercept** in a hierarchical linear model. This properly accounts for the non-independence of samples within the same province, adjusts standard errors accordingly, and allows for the partitioning of variance between the within-province and between-province levels.

**Handling Hierarchical Nesting (Subregions within Provinces)**  
Geographic data often possess a natural hierarchical structure (e.g., sample sites nested within watersheds, which are nested within provinces).24 Ignoring this nested structure violates the core statistical assumption of observation independence, leading to pseudo-replication, underestimated standard errors, and an inflated risk of Type I errors.25  
This structure must be explicitly accounted for using a multilevel (or hierarchical) model. In the context of the main SOC prediction task, this would be formulated as a linear mixed-effects model. For a two-level nesting structure (e.g., subregion within province), the model would take the form:  
$SOC\_{ij} \= \\beta\_0 \+ \\beta\_1 \\cdot TLSP1\_{ij} \+... \+ (u\_{0j} \+ v\_{0ij})$  
where $u\_{0j}$ is the random intercept for province $j$, and $v\_{0ij}$ is the random intercept for subregion $i$ within province $j$. This model correctly partitions the variance at each level of the hierarchy and provides valid statistical inference.

### **Section 1.2: Mitigating Spurious Discoveries and Model Overfitting**

This section details the necessary procedures to ensure the final predictive model is robust, generalizable, and not simply an artifact of overfitting to spatial dependencies or a high-dimensional feature space.

#### **1.2.1 Multiple Testing Correction**

When a large number of hypotheses are tested simultaneously, the probability of obtaining a false positive (a Type I error) increases substantially.26 Procedures to correct for multiple testing are therefore essential for maintaining statistical rigor.

* **Number of Features and Hypotheses:** The TDA pipeline is expected to generate a suite of features from each DEM window. For example, extracting eight summary statistics from H₀ and H₁ persistence landscapes would yield eight features.10 If the statistical significance of each of these features is assessed individually (e.g., to determine which specific features differ between provinces or which are significant predictors of SOC), a multiple testing correction is mandatory.  
* **Level of Correction:** Correction should be applied at the level of the hypotheses being tested. The primary MANOVA test ("Do the provinces differ across the full suite of TLSPs?") is a single hypothesis and does not require correction. Correction becomes necessary for secondary, exploratory analyses, such as post-hoc tests to identify which specific TLSP features drive the overall multivariate difference.  
* **False Discovery Rate (FDR) Control:** For exploratory analyses involving many features, controlling the False Discovery Rate (FDR) is generally preferred over controlling the Family-Wise Error Rate (FWER). FDR-controlling procedures, such as the Benjamini-Hochberg method, are less conservative than FWER methods like the Bonferroni correction, providing greater statistical power to identify true effects while accepting a small proportion of false discoveries.26

**Benjamini-Hochberg (BH) vs. Benjamini-Yekutieli (BY)**  
The choice between the two main FDR procedures depends on the correlation structure of the test statistics.

* **Benjamini-Hochberg (BH):** The original BH procedure controls the FDR under the assumption that the tests are independent or exhibit a specific type of positive correlation.28 It is the more powerful of the two methods.  
* **Benjamini-Yekutieli (BY):** The BY procedure is a more conservative modification that is proven to control the FDR under *any* arbitrary dependence structure.28

Given that the TLSP features are all derived from the same underlying DEM data within a window, they are almost certain to be correlated. This correlation among predictors will translate to correlation among their associated test statistics (e.g., p-values from a regression model), violating the assumptions of the standard BH procedure. Therefore, the **Benjamini-Yekutieli procedure is the theoretically correct and safer choice**, as it guarantees FDR control regardless of the correlation structure. A practical strategy is to apply both procedures. If the results are largely concordant, the more powerful BH results may be reported. If they differ substantially, the more conservative BY results should be presented as the robust finding.

* **Table 2: Guide to Multiple Testing Correction Procedures for Correlated Spatial Features**  
  * **Justification:** The high dimensionality of the feature set necessitates a clear strategy for multiple testing. This table provides a concise decision-making guide for selecting the appropriate correction method based on the known properties of the data and the trade-off between statistical power and error control.  
  * **Columns:** Procedure, Assumed Data Structure, Power, When to Use.  
  * **Rows:**  
    * **No Correction:** (Independent tests, few hypotheses; High power; Not recommended here).  
    * **Bonferroni (FWER):** (Any structure; Very low power; When even one false positive is unacceptable).  
    * **Benjamini-Hochberg (FDR):** (Independent or positive dependence; High power; As a baseline, or if feature correlation is weak).  
    * **Benjamini-Yekutieli (FDR):** (Arbitrary dependence; Moderate power; **Recommended approach** for correlated geospatial features).

#### **1.2.2 Spatial Cross-Validation (CV) Implementation**

Standard k-fold cross-validation is statistically invalid for spatial data. Due to spatial autocorrelation (SAC), nearby data points are not independent. Randomly assigning them to training and testing folds allows the model to "peek" at the test data, leading to inflated and overly optimistic performance metrics.31 Spatial cross-validation (SCV) is a required methodology to obtain a realistic estimate of how the model will perform when predicting to new, un-sampled geographic locations.32

* **Optimal Spatial Block Size:** The size of the spatial blocks used to separate folds is the single most important parameter in SCV.33 The objective is to ensure that the minimum distance between any training point and any testing point is greater than the range of spatial autocorrelation in the model residuals.  
  * **Estimating the Autocorrelation Range:** This range must be estimated empirically from the data. The standard procedure is to first fit a non-spatial model (e.g., OLS regression) and then compute a **variogram or correlogram** on the model's residuals. The distance at which the semivariance plateaus (the "sill" in a variogram) or the Moran's I statistic drops to a non-significant level (in a correlogram) is the estimated range of spatial autocorrelation.33 This distance defines the minimum block size for the SCV. Correlograms of the predictors themselves can also provide a useful proxy.33  
* **Buffer Distance:** A simple blocking scheme can still leave training and testing points adjacent at block boundaries. To enforce true spatial separation, an **exclusion buffer** should be applied. This involves removing all training data points that fall within a specified distance of any testing fold point.36 The buffer distance should be set to the empirically determined autocorrelation range.36 The spatialsample package in R provides a straightforward implementation of this via a buffer argument in its CV functions.36  
* **Comparison of SCV Methods:**  
  * **Spatial Blocking (e.g., Roberts et al., 2017):** This method partitions the study area into a grid of contiguous blocks (squares or hexagons) and assigns entire blocks to different folds.31 It is computationally efficient and widely recognized as a robust approach.  
  * **Spatial Leave-One-Out (Buffered LOO):** In this approach, for each data point, a model is trained using all other data points that lie *outside* a buffer zone around the target point.34 While statistically robust, this method is computationally prohibitive for all but the smallest datasets.  
  * **Recommendation:** For a study of this scale, **spatial block cross-validation is the most practical and scientifically sound approach**.  
* **k-Value Selection:** The number of folds (the *k* in k-fold CV) is of secondary importance compared to the block size.33 A value of $k=5$ or $k=10$ is standard practice and provides a reasonable balance between bias and variance in the performance estimate.

#### **1.2.3 Spatial Autocorrelation (SAC) Model Selection**

If the residuals of a standard OLS regression model exhibit significant spatial autocorrelation (diagnosed using a test like Moran's I on the residuals 38), it indicates a violation of the independence assumption. This must be addressed by employing a spatial regression model that explicitly accounts for the spatial structure.

* **Decision Criteria for Model Selection:** The choice among common spatial autoregressive models depends on the assumed source of the spatial dependency.  
  * **Spatial Lag Model (SLM or SAR):** This model assumes a substantive spatial process where the value of the dependent variable (SOC) at one location is directly influenced by the values at neighboring locations. It is specified as $y \= \\rho W y \+ X\\beta \+ \\epsilon$, where $W$ is the spatial weights matrix and $\\rho$ is the spatial lag coefficient. This model is appropriate when a direct spatial process, such as lateral transport of organic matter, is hypothesized.39  
  * **Spatial Error Model (SEM):** This model assumes the spatial dependency resides in the error term, specified as $y \= X\\beta \+ u$, where $u \= \\lambda W u \+ \\epsilon$. This implies that the model's errors are correlated in space, typically due to the influence of unmeasured, spatially structured covariates. This is a very common scenario in environmental modeling.39  
  * **Eigenvector Spatial Filtering (ESF):** This is a flexible, non-parametric approach. It involves performing an eigendecomposition of the spatial weights matrix and using a subset of the eigenvectors as additional predictors in a standard regression model. These eigenvectors capture spatial patterns at various scales, effectively "filtering out" the spatial autocorrelation from the residuals.  
  * **Spatial Durbin Model (SDM):** This is a more general model that includes both a spatially lagged dependent variable and spatially lagged independent variables ($y \= \\rho W y \+ X\\beta \+ WX\\theta \+ \\epsilon$). It can account for both endogenous and exogenous spatial interactions.40  
* **Systematic Decision Process:**  
  1. Fit a standard OLS model.  
  2. Test the OLS residuals for SAC using Moran's I.  
  3. If SAC is significant, compute Lagrange Multiplier (LM) tests for both a missing spatial lag (LM-lag) and for spatial error (LM-error).  
  4. If only LM-lag is significant, the SLM is preferred. If only LM-error is significant, the SEM is preferred.  
  5. If both are significant, robust versions of the LM tests can help differentiate. If ambiguity remains, the SDM is often a robust choice.  
  6. A highly effective and pragmatic approach is to fit several candidate models (e.g., OLS, SLM, SEM, SDM, ESF) and select the model that minimizes an information criterion, such as the **Akaike Information Criterion (AIC)**.40  
* **Table 3: Decision Framework for Spatial Autoregressive Model Selection**  
  * **Justification:** Selecting the correct spatial model is critical for valid inference. This table provides a structured workflow, combining diagnostic tests and information criteria, to guide this complex decision.  
  * **Columns:** Step, Action, Diagnostic Tool, Decision Rule.  
  * **Rows:**  
    * **1\. Baseline Model:** (Fit OLS; Test residuals for SAC; Moran's I).  
    * **2\. Identify SAC Source:** (Run LM tests on OLS residuals; LM-lag, LM-error).  
    * **3\. Candidate Model Fitting:** (Fit SLM, SEM, SDM based on LM test results).  
    * **4\. Final Model Selection:** (Compare candidate models; AIC).  
    * **5\. Post-Fit Verification:** (Test spatial model residuals for remaining SAC; Moran's I).  
* **Spatial Weights Matrix (W) Specification:** For a regular 30m grid, a **Queen contiguity matrix** is a standard and appropriate choice. In this matrix, two grid cells are considered neighbors if they share either an edge or a corner. The matrix must be row-standardized so that the weights for each location's neighbors sum to one.  
* **Testing for Remaining SAC:** After fitting a spatial regression model, it is imperative to test its residuals for any remaining spatial autocorrelation using Moran's I.38 Significant residual SAC indicates that the chosen spatial model has not fully captured the spatial structure of the data, and further model refinement is necessary.  
* **Geographically Weighted Regression (GWR):** GWR is a distinct local modeling technique that addresses spatial *non-stationarity* (i.e., relationships that vary across space) rather than spatial autocorrelation.41 It fits a unique regression equation for every point in the dataset. While powerful for exploring spatially varying relationships, GWR is highly susceptible to multicollinearity and overfitting. A more advanced version, the Geographically Weighted Elastic Net (GWEN), has been developed to address these limitations.41 For this project, GWR should be considered an exploratory tool for post-hoc analysis rather than the primary predictive model.

#### **1.2.4 Variable Selection Strategy**

With covariates from multiple tiers (traditional geomorphometrics, environmental variables, and TDA features), the total number of predictors could easily exceed 50, creating a high-dimensional modeling problem. This introduces significant risks of model overfitting and multicollinearity.

* **Elastic Net Regularization:** A disciplined variable selection strategy is essential. **Elastic Net regression is the recommended approach**.42  
  * **Superiority over Stepwise Methods:** Traditional stepwise regression procedures are known to be unstable, are prone to finding local optima rather than the best overall model, and produce unreliable p-values and confidence intervals.38 Regularization methods like Elastic Net provide a more robust and statistically sound solution.  
  * **Advantages over LASSO:** The LASSO (L1 regularization) performs variable selection by shrinking some coefficients to exactly zero. However, when faced with a group of highly correlated predictors, it tends to arbitrarily select only one from the group. The Elastic Net penalty is a convex combination of the LASSO (L1) and Ridge (L2) penalties.42 The Ridge component encourages the model to shrink the coefficients of correlated predictors toward each other, effectively selecting or deselecting them as a group. This "grouped selection" property is highly advantageous for geospatial data, where many predictors (e.g., different measures of curvature) are inherently correlated.43  
  * **Implementation within Spatial CV:** To ensure robust selection of the regularization hyperparameters (the mixing parameter α and the penalty strength λ) and to prevent data leakage, the entire Elastic Net procedure must be nested *within* the spatial cross-validation loop.45  
* **VIF Thresholds for Multicollinearity Diagnosis:** The Variance Inflation Factor (VIF) is a crucial diagnostic for assessing multicollinearity among predictors.  
  * **Interpretation:** A VIF quantifies how much the variance of an estimated regression coefficient is inflated due to its correlation with other predictors. A VIF of 1 indicates no inflation. While there is no universal threshold, a common rule of thumb is that a **VIF exceeding 5 warrants investigation, and a VIF exceeding 10 is a sign of potentially problematic multicollinearity**.46  
  * **Application:** VIFs should be calculated on the full set of potential predictors prior to modeling. While Elastic Net is designed to handle multicollinearity, examining variables with very high VIFs can reveal redundancies. This can inform decisions to remove a variable based on domain knowledge or to proceed with the knowledge that the model will handle the group via regularization.  
* **Strategy for Tiered Variables:** Performing selection within each tier of variables before combining them is **not recommended**. This piecemeal approach is suboptimal because it can prematurely discard variables that may only become important in the presence of variables from other tiers (due to interaction effects). The most robust strategy is to present the full suite of theoretically justified variables from all tiers to the Elastic Net algorithm simultaneously and allow it to perform a holistic and data-driven selection.

---

## **Part II: Topological Feature Engineering from Digital Elevation Models**

This part details the core novelty of the project: the extraction of landscape features using TDA. The methodological choices made here directly impact the quality, interpretability, and predictive power of the inputs to the machine learning models.

### **Section 2.1: From Persistence Diagrams to Machine Learning Features**

This section focuses on the critical step of converting the abstract output of persistent homology—persistence diagrams—into a fixed-length vector representation (a process known as featurization or vectorization) that is suitable for use in standard machine learning algorithms.

#### **2.1.1 Persistence Diagram Vectorization Comparison**

Persistence diagrams are multisets of points in the plane, a format that is not directly compatible with most machine learning classifiers and regressors.49 Vectorization methods are therefore required to transform these diagrams into a stable, fixed-dimensional vector space representation.49 The two most prominent methods are Persistence Landscapes (PL) and Persistence Images (PI).  
**Theoretical Differences in Information Preservation**

* **Persistence Landscapes (PL):** A persistence diagram is transformed into a sequence of piecewise-linear functions $\\{\\lambda\_k(t)\\}\_{k=1}^\\infty$ in a Banach space. The mapping from a persistence diagram to its corresponding landscape is mathematically proven to be **invertible**.52 This is a powerful property, as it means that, in theory, **no information from the original diagram is lost** during the transformation. The representation is stable, parameter-free, and inherently non-linear.51  
* **Persistence Images (PI):** A persistence image is created by first transforming the (birth, death) coordinates of the diagram to (birth, persistence) coordinates. Then, a kernel function (typically a Gaussian) is centered on each point. The resulting surface is then integrated over a grid of pixels to create a raster image, which is flattened into a vector.49 This process involves user-defined parameters—the kernel bandwidth and the pixel resolution—and the discretization and integration steps mean that this transformation is **not invertible** and involves some degree of information loss compared to the PL method.

**Computational Cost Comparison**  
Multiple comparative studies have found that **Persistence Landscapes are computationally faster to generate than Persistence Images**, particularly as dataset size increases.54 The computational cost of generating a PI is directly tied to its resolution; a higher number of pixels increases the computation time.54 While newer methods are emerging that promise even greater speed 55, the comparison between PL and PI remains a key practical consideration.  
**Specific Recommendations and Formal Test of Performance**

* **Summary Statistics from Persistence Landscapes:** To convert the functional representation of a PL into a feature vector, summary statistics are extracted from the first few landscape functions (e.g., $\\lambda\_1, \\dots, \\lambda\_5$). A robust and standard set of features to extract for each landscape function includes:  
  * $L^p$ norms (for $p=1$ and $p=2$)  
  * Integral of the function  
  * Mean value  
  * Maximum value  
  * Variance of the function values  
* **Resolution for Persistence Images:** The pixel size or resolution of a PI is a critical hyperparameter that directly controls the trade-off between feature detail and vector dimensionality. There is no single optimal resolution; it is data-dependent and must be determined empirically.56 A coarse resolution (e.g., $10 \\times 10$ pixels) risks blurring important topological information, while a very fine resolution (e.g., $100 \\times 100$) can create an unwieldy, high-dimensional feature vector that is computationally expensive and increases the risk of overfitting. The most rigorous approach is to treat the PI resolution as a **hyperparameter to be tuned within the machine learning pipeline's cross-validation procedure**.57 By testing a range of resolutions (e.g., $10 \\times 10$, $20 \\times 20$, $30 \\times 30$) and selecting the one that yields the best cross-validated predictive performance, an optimal, data-driven choice can be made. The PersistenceImager class in the scikit-tda library facilitates this by allowing easy modification of the pixel\_size parameter.58  
* **Formal Performance Comparison:** The most effective way to determine which vectorization method is superior for this specific application is through empirical testing. The recommended strategy is to generate two distinct sets of topological features: one derived from Persistence Landscapes and one from Persistence Images. These can be treated as alternative "Tier 3" feature sets. The full modeling pipeline, including variable selection with Elastic Net and spatial cross-validation, should then be run twice: once with the PL features and once with the PI features. The vectorization method that results in the model with the best cross-validated performance (e.g., lowest RMSE) should be selected for the final analysis.

**Table 1: Comparative Analysis of TDA Vectorization Methods**

| Feature | Persistence Landscapes (PL) | Persistence Images (PI) |
| :---- | :---- | :---- |
| **Core Concept** | A sequence of functions in a Banach space, representing the "skyline" of the persistence diagram. | A kernel density estimate of the persistence diagram, discretized onto a pixel grid. |
| **Information Preservation** | Invertible; theoretically lossless. All information from the diagram is preserved.52 | Not invertible; discretization and kernel smoothing lead to some information loss. |
| **Stability** | Stable with respect to the bottleneck distance between diagrams.51 | Stable with respect to the bottleneck distance between diagrams.50 |
| **Computational Cost** | Generally faster to compute, especially for large datasets.54 | Slower, with computation time increasing with pixel resolution.54 |
| **Key Parameters** | Number of landscape functions to compute and summarize. | Pixel resolution (grid size) and kernel bandwidth (sigma). |
| **Parameter Sensitivity** | Relatively low sensitivity to the number of landscapes used. | Highly sensitive to the choice of pixel resolution and kernel bandwidth, requiring careful tuning. |
| **Typical Feature Vector** | (Number of landscapes) × (Number of summary statistics per landscape). | (Number of pixels in x-dimension) × (Number of pixels in y-dimension). |

### **Section 2.2: Foundational TDA Parameters and Geohydrological Preprocessing**

This section provides guidance on the initial, critical steps of the TDA workflow, from DEM preprocessing to defining the filtration itself. These choices are highly sensitive and can dramatically alter the resulting topological signatures.

#### **2.2.1 Filtration Parameter Selection**

Persistent homology operates on a filtration—a nested sequence of topological spaces. For a DEM, this is generated by analyzing the sublevel sets of the elevation function, which is analogous to flooding the landscape from its lowest point upwards.60 As the "water level" (the filtration value) rises, topological features—connected components (H₀) and loops (H₁)—are born and die at specific elevation values corresponding to critical points (minima, maxima, and saddles) of the function.63

* **Defining Meaningful Features via Persistence:** A core principle of TDA is that it captures features across *all* scales simultaneously. The significance of a feature is not determined by its absolute birth or death elevation but by its **persistence** (the difference between its death and birth values). Features that persist over a long range of filtration values are considered robust signals, while those with short persistence are often treated as noise.64 Therefore, it is not necessary to pre-select specific elevation quantiles to define features; the filtration should span the full dynamic range of elevation values within each analysis window.  
* **Normalization of Elevation:** It is **strongly recommended to normalize the elevation values within each analysis window** (e.g., scaling them to the range ) before computing the filtration. This step is crucial for comparability. Without normalization, a feature with a 10-meter persistence in a high-relief mountainous region would be treated identically to a 10-meter persistence feature in a low-relief coastal plain, despite their vastly different geomorphic significance. Normalization ensures that the persistence diagrams from different landscape settings are on a common scale, making persistence a measure of a feature's *relative* importance within its local topographic context.  
* **Handling Flat Areas:** Topographically flat areas in a DEM present a challenge for persistent homology because all cells within the flat have the same elevation value. This creates a large number of simplices that enter the filtration at the exact same time, leading to ambiguity in the filtration ordering and potentially creating computational artifacts.66  
  * **Pragmatic Solution:** The most straightforward approach is to apply a standard hydrological conditioning algorithm designed to resolve flat areas by imposing a slight, artificial gradient *before* the TDA analysis.66  
  * **Advanced Solution:** A more topologically principled, though complex, method is to use a multifiltration. This involves using a secondary function (e.g., distance from the nearest stream channel) as a tie-breaker for all points with the same primary filtration value (elevation). For the scope of this project, applying a standard flat-area correction algorithm is a sufficient and defensible preprocessing step.

#### **2.2.2 Edge Effects and Boundary Handling**

When conducting analysis using a moving window, features that are truncated by the window's edge are not represented accurately. This is a classic boundary problem in spatial analysis that must be addressed to ensure the integrity of the computed features.

* **Halo/Padding Implementation:** The standard solution is to use a **halo**, also known as padding.67 For each analysis window (e.g., a 500m x 500m area of interest), the TDA computation should be performed on a larger, temporary window that includes a surrounding buffer or halo (e.g., a 750m x 750m computational window). The persistence diagram is calculated for this larger area, but the resulting features are only assigned to the central 500m x 500m window. This ensures that the features calculated for the area of interest are not distorted by artificial edge effects.  
* **Halo Width Specification:** The width of the halo should be determined based on the scale of the geomorphic features of interest. A practical and robust rule of thumb is to set the halo width to be **half the size of the analysis window**. For a 500m window, this would mean a 250m halo on all sides, for a total computational window of 1000m x 1000m. This ensures that the center of the analysis window is maximally distant from any computational boundary.  
* **Handling Study Area Boundaries:** A similar issue arises for analysis windows located at the edge of the overall study area.  
  * **Recommendation:** The most robust and statistically clean approach is to **discard any analysis window whose halo would extend beyond the boundary of the available DEM data**. While this results in a slight reduction of the analyzable area (an inward buffer of the study area by the halo width), it is the only way to guarantee that all computed features are free from boundary-induced artifacts. Alternative methods, such as padding with NaN values or using irregular windows, are computationally complex and risk introducing their own artifacts.

#### **2.2.3 Hydrological and Preprocessing Considerations**

**Hydrological Conditioning: Pit-filling vs. Breaching**  
Raw DEMs contain spurious depressions or "pits" that must be removed to ensure continuous flow paths for hydrological modeling. The two primary methods for this are filling and breaching.

* **Pit-filling:** This method raises the elevation of all cells in a depression to the level of its lowest outlet or "pour point." A major side effect is the creation of perfectly flat areas, which are problematic for TDA.66  
* **Breaching:** This method carves a channel from the lowest point of a depression to the nearest lower cell outside of it. This method generally preserves more of the original topographic variation and avoids the creation of large artificial flats.69  
* **Recommendation for TDA:** Because TDA is focused on analyzing the shape of the terrain, **breaching is generally the more appropriate conditioning method**. It better preserves the underlying topographic structure that TDA aims to quantify. The choice can also be landscape-dependent; very deep, artificial depressions like quarries are better filled, while linear artifacts like road embankments are better breached.69 A crucial validation step is to compare the persistence diagrams generated from unconditioned, filled, and breached versions of a few sample DEM windows to visually assess the impact of each method on the topological signatures.

**Targeted Smoothing Justification**  
High-resolution LiDAR DEMs often exhibit a "rough" texture due to sensor noise or the detailed capture of micro-topography like vegetation hummocks.70 While smoothing filters (e.g., Gaussian blur) are often applied to reduce this roughness, this practice poses a significant risk to a TDA-based analysis.

* **The Risk of Oversmoothing:** The primary danger is that smoothing will remove or blur the very geomorphically meaningful micro-topographic features that TDA is designed to detect and quantify.70 What appears as "noise" at one scale of analysis is often a meaningful "signal" at a finer scale.  
* **TDA as an Inherent Filter:** Persistent homology is, by its nature, a multi-scale filtering technique. The persistence value (death \- birth) of a topological feature provides a natural and mathematically rigorous way to distinguish between low-persistence features (likely noise or minor texture) and high-persistence features (robust, significant landforms). Aggressively smoothing the DEM *before* applying TDA is therefore counter-productive, as it preemptively removes information that the TDA algorithm is designed to analyze.  
* **Recommendation:** **Aggressive *a priori* smoothing of the DEM should be avoided.** If necessary, a very light smoothing with a small kernel (e.g., a 3x3 Gaussian filter) may be applied to remove high-frequency sensor noise, but its effect must be carefully evaluated by comparing the persistence diagrams of smoothed and unsmoothed DEMs.71 The primary mechanism for separating signal from noise should be the persistence thresholding itself, not a preprocessing filter.

---

## **Part III: Data Integration, Validation, and Scientific Interpretation**

This part focuses on the practical aspects of using external datasets, validating the model, and, most importantly, translating the abstract mathematical outputs into meaningful scientific insights.

### **Section 3.1: Data Provenance and Integration Strategy**

#### **3.1.1 POLARIS Dataset Investigation**

A thorough understanding of the SOC target variable dataset, POLARIS, is critical to designing a valid study and avoiding analytical pitfalls.

* **POLARIS Methodology:** POLARIS is a 30m probabilistic soil properties database for the contiguous United States. It was created using a machine learning algorithm (DSMART-HPC) to spatially disaggregate the coarser polygon-based Soil Survey Geographic (SSURGO) database. This disaggregation was guided by a suite of high-resolution geospatial environmental covariates.72  
* **Use of Topographic Predictors in POLARIS:** Multiple sources confirm that **fine-scale (30m) elevation data were among the most important covariates used in the creation of POLARIS**.73 This fact is of paramount importance to the proposed research.  
* **Circularity Risk and Mitigation:** The use of topographic data in the creation of the target variable (POLARIS SOC) introduces a significant risk of **analytical circularity**. A model trained to predict POLARIS SOC using new topographic features (TLSPs) will likely show a strong relationship, but this relationship may be an artifact of both the predictors and the target variable being derived from the same underlying topographic information. This would not represent a novel scientific discovery.  
  To mitigate this critical issue, the research hypothesis and modeling strategy must be carefully reframed. The primary objective should not be simply to predict POLARIS SOC, but to test the hypothesis: **"Do advanced topological features (TLSPs) provide significant explanatory power for SOC distribution *above and beyond* the standard topographic derivatives that were likely used to create the POLARIS dataset?"**  
  This reframing necessitates a nested model comparison approach:  
  1. **Model 1 (Baseline):** Predict SOC using only standard topographic derivatives (e.g., slope, aspect, curvature, TWI) that serve as a proxy for the inputs to the POLARIS model.  
  2. **Model 2 (Full Model):** Predict SOC using the baseline derivatives *plus* the novel TLSP features.  
  3. **Evaluation:** The added value of the TDA approach is then quantified by the statistically significant improvement in model performance (e.g., the change in $R^2$) from Model 1 to Model 2, assessed via a likelihood ratio test.  
* **POLARIS Prediction Uncertainty:** A key feature of the POLARIS dataset is its probabilistic nature. For each 30m grid cell, it provides not just a single mean SOC value, but a full predictive distribution, often stored as a 100-bin histogram.75 This spatially explicit uncertainty information should be leveraged. Instead of predicting only the mean SOC, a more sophisticated approach would be to use a distributional regression model to predict the parameters of the SOC distribution (e.g., mean and variance). Alternatively, during model training, observations could be weighted by the inverse of the POLARIS prediction variance, thereby giving more influence to training points where the SOC estimate is more certain.  
* **Need for Independent Validation Data:** The ultimate test of the model's validity and its ability to overcome the circularity issue is to evaluate its performance against an **independent set of field-measured SOC samples**. These validation points must not have been used in the creation of either SSURGO or POLARIS. Procuring such a dataset (e.g., from sources like the National Soil Information System (NASIS), regional soil sampling campaigns, or Long-Term Ecological Research (LTER) network sites) is a critical task. Without this external validation, it is impossible to definitively claim that the model has learned a true soil-landscape relationship rather than simply re-learning the patterns inherent in the POLARIS model itself.

#### **3.1.2 DEM-to-SOC Scale Mismatch**

The project involves using a 10m resolution DEM to generate predictors for a 30m resolution SOC target variable. Handling this scale mismatch correctly is crucial for preserving the high-resolution information.

* **Incorrect Approach:** Aggregating the 10m DEM to 30m *before* analysis. This would discard the fine-scale topographic detail that is the central premise of the study.  
* **Correct Workflow:**  
  1. **Calculate Features at Native Resolution:** The TDA pipeline, including the moving window analysis, should be run on the **native 10m DEM**. This will produce a set of TLSP feature rasters at 10m resolution.  
  2. **Aggregate Predictors to Target Resolution:** The resulting 10m TLSP feature rasters should then be **aggregated to the 30m grid** of the POLARIS SOC data. This ensures that for each 30m target pixel, the corresponding predictor value is a summary of the nine underlying 10m feature pixels.  
* **Optimal Aggregation Method:** For continuous features like the summary statistics derived from persistence landscapes, **mean or median aggregation** is appropriate. The mean is a common choice, while the median offers greater robustness to potential outlier values within the 3x3 block of 10m pixels. While advanced interpolation methods like Kriging can be superior for downscaling 77, for simple aggregation (upscaling), mean or median is computationally efficient and statistically sound. The choice between them can be evaluated as part of a sensitivity analysis.

### **Section 3.2: Model Benchmarking and Geomorphic Interpretation**

#### **3.2.1 Baseline Model Literature Support**

To demonstrate the novel contribution of the TDA-based approach, its performance must be rigorously compared against a strong baseline model constructed from state-of-the-art, non-TDA covariates.

* **SCORPAN Framework:** The SCORPAN model, which posits that soil properties are a function of Soil, Climate, Organisms, Relief, Parent material, Age, and spatial position, provides the theoretical foundation for digital soil mapping.78 Recent SOC prediction studies (2020-2025) consistently leverage this framework, using machine learning models to link soil observations to a wide array of environmental covariates.79  
* **Baseline Model Specification:** Based on current literature, a robust baseline model should include covariates representing the key SCORPAN factors:  
  * **Relief (Tier 1):** A comprehensive set of standard topographic derivatives calculated from the 10m DEM and aggregated to 30m. This must include, at a minimum: slope, aspect, planform curvature, profile curvature, and the Topographic Wetness Index (TWI).  
  * **Other SCORPAN Factors (Tier 2):**  
    * *Climate:* Gridded climate data (e.g., PRISM) for variables like mean annual precipitation and temperature.  
    * *Organisms:* Land cover data (e.g., National Land Cover Database \- NLCD) and satellite-derived vegetation indices (e.g., time-series metrics of NDVI from Landsat/Sentinel).  
    * *Parent Material:* Data from digital geologic maps.  
    * *Space:* Latitude and longitude coordinates to capture broad spatial trends.  
* **Climate-Topography Interactions:** Interactions between covariates are often critical drivers of soil properties. For instance, the effect of solar radiation on soil temperature and moisture is strongly mediated by slope aspect. Such interactions should be explicitly included in the model, for example, as product terms (e.g., aspect \* solar\_radiation). The Elastic Net variable selection process can then determine which of these interaction terms are most important.

#### **3.2.2 Topological-to-Geomorphic Translation**

A key challenge and opportunity in this research is to translate the abstract mathematical features derived from TDA into physically meaningful geomorphic interpretations. A model that predicts well but remains a "black box" offers limited scientific insight.

* **Interpreting H₀ and H₁ Persistence:** When using a sublevel set filtration (which simulates flooding the landscape), the birth and death of topological features have direct physical analogues.  
  * **H₀ (Connected Components):** A 0-dimensional homology class represents a connected component. A new component is "born" at a local minimum. This component "dies" when it merges with an older, larger component as the flood level rises to a saddle point (its pour point). Therefore, a persistent H₀ feature corresponds to a **topographic basin or depression**.  
    * *Birth Elevation:* The elevation of the local minimum.  
    * *Death Elevation:* The elevation of the spillover saddle.  
    * *Persistence (Death \- Birth):* The **depth of the basin** relative to its outlet. Highly persistent H₀ features are deep, well-defined basins.  
  * **H₁ (Loops/Holes):** A 1-dimensional homology class represents a loop or hole. In the context of a 2D elevation surface, a loop is created when two separate hills become connected by a rising water level at a saddle point, encircling a relative depression. This interpretation is less direct for sublevel sets. A more intuitive interpretation comes from the dual perspective of a **superlevel set filtration** (draining the landscape from the top). In this case, an H₁ feature is born when a saddle is exposed, creating a "hole" in the landmass that separates two peaks. This hole dies when the basin between them is fully drained. A persistent H₁ feature from a sublevel set filtration corresponds to a **peak or ridge that is encircled by a saddle**.  
    * *Birth Elevation:* The elevation of the saddle that creates the encirclement.  
    * *Death Elevation:* The elevation of the peak within the encirclement.  
    * *Persistence (Death \- Birth):* A measure of the **prominence of the peak** relative to its surrounding saddle.60 Highly persistent H₁ features are prominent, isolated peaks or ridges.  
* **Quantitative Validation of Interpretations:** These qualitative interpretations can be quantitatively validated.  
  * **Method:** Use established geomorphometric software (e.g., Whitebox GAT, SAGA GIS) to automatically delineate discrete landform objects, such as basins or peaks, using methods like watershed segmentation or geomorphon analysis.  
  * **Analysis:** For each delineated object, calculate its physical properties (e.g., the measured depth of a basin). Concurrently, compute the persistence of the corresponding topological feature (e.g., H₀ persistence) for the same area. By correlating these two sets of measurements across hundreds of landforms, a strong statistical relationship would provide robust, quantitative evidence for the proposed geomorphic interpretation.

### **Section 3.3: Advanced Model Interrogation and Exploratory Analysis**

#### **3.3.1 SHAP for Spatial Models**

SHAP (SHapley Additive exPlanations) is a game theory-based, model-agnostic method for explaining individual predictions by fairly attributing the prediction's deviation from the baseline to each input feature.82 Its application to spatial models is a promising frontier for enhancing interpretability.

* **Applicability to Spatially-Structured Models:** SHAP can be applied to any predictive model, including the spatial regression models (ESF, SEM, etc.) proposed in this study. Recent research has successfully demonstrated the utility of analyzing the **spatial patterns of SHAP values** to interpret complex machine learning models in a geospatial context.84 However, there are important caveats. Standard SHAP implementations may ignore feature dependence (like spatial autocorrelation), which can lead to unreliable results.82 The recently proposed GeoShapley framework is designed to address this by explicitly treating location as a player in the model, but applying off-the-shelf SHAP and mapping the results is a valid and insightful first step.85  
* **Interpretation Strategy:** The most powerful way to use SHAP in this context is to apply it to the final, fully specified spatial model and then to **map the resulting SHAP values geographically**. For each sample location, SHAP calculates a contribution value for each predictor. This yields a new map for each predictor, showing where and by how much that predictor is pushing the SOC prediction up or down. Visualizing these maps can reveal spatially non-stationary feature importance—for example, it might show that slope is a strong positive driver of SOC in one province but a weak or negative driver in another. This provides a level of local, spatially explicit interpretability that is difficult to achieve with other methods.84  
* **Alternative and Complementary Methods:** Spatial Partial Dependence Plots (PDPs) can complement SHAP. A PDP shows the average marginal effect of a feature on the prediction. By generating separate PDPs for different geographic regions (e.g., each province), one can visualize how the average relationship between a predictor and SOC changes across the study area. This provides a regional view, while SHAP provides a local, per-prediction view.

#### **3.3.2 Mapper Algorithm Application**

The Mapper algorithm is another powerful tool from TDA that provides a simplified, graph-based representation of the high-dimensional structure of a dataset. It is exceptionally well-suited for exploratory data analysis, visualization, and clustering.87

* **Parameter Selection:** The application of Mapper requires several key parameter choices:  
  * **Filter Function:** This is a function that projects the high-dimensional data onto a lower-dimensional space (typically 1D or 2D). The choice of filter function determines the "lens" through which the data's structure is viewed. Excellent candidates for this project include:  
    * *Geographic coordinates (X, Y):* To explore purely spatial patterns and clustering.  
    * *Predicted SOC values:* To understand how data points cluster in terms of their model predictions, potentially revealing distinct SOC regimes.  
    * *Principal Components:* The first two principal components (PC1, PC2) of the full covariate matrix, to summarize the data's structure in predictor space.  
  * **Cover (Intervals and Overlap):** The range of the filter function's output is covered by a set of overlapping intervals. The **number of intervals** and the **percentage of overlap** are crucial tuning parameters that control the resolution of the resulting Mapper graph.88 These parameters typically require interactive exploration; common starting values are 30-50 intervals with 50-70% overlap.  
  * **Clustering Algorithm:** Within the data points that fall into each interval (the "pullback cover"), a standard clustering algorithm (e.g., DBSCAN, agglomerative clustering) is applied to identify clusters.  
* **Extracting Interpretable Insights:** The output of Mapper is a graph where nodes represent clusters of data points, and an edge connects two nodes if their corresponding clusters share members. The scientific insight comes from coloring the nodes of this graph by the average value of different variables. For example, coloring the nodes by the average measured SOC might reveal a "branch" or "flare" in the graph that corresponds to high-SOC samples. One can then interrogate the data points within the nodes of that branch to identify the common topographic and environmental characteristics that define this high-SOC regime, thus generating new, data-driven hypotheses about soil-landscape relationships.90

---

## **Part IV: Computational Strategy and Project Feasibility**

This part outlines the technical blueprint for implementing the research, focusing on performance, scalability, and ensuring long-term reproducibility of the complex computational workflow.

### **Section 4.1: Uncertainty Quantification and Sensitivity Analysis**

#### **4.1.1 DEM Error Propagation**

The source 10m DEM is an imperfect representation of the true land surface and contains vertical errors. These errors will propagate through the complex TDA pipeline, introducing uncertainty into the final TLSP features.91 A robust analysis requires quantifying this uncertainty.

* **Characterizing DEM Error:** The first step is to obtain the vertical accuracy specifications for the DEM from its metadata, typically reported as a Root Mean Square Error (RMSE). This provides the magnitude of the expected error.  
* **Monte Carlo Simulation for Error Propagation:** The standard and most robust method for modeling error propagation is Monte Carlo simulation.91 The workflow is as follows:  
  1. Model the DEM error not as simple random noise, but as a spatially correlated Gaussian random field. The parameters of this field (variance and autocorrelation length) can be derived from the DEM's RMSE and an empirical variogram calculated on flat areas of the DEM.  
  2. Generate a large ensemble (e.g., 100-1000) of these spatially correlated error fields.  
  3. Add each simulated error field to the original DEM, creating an ensemble of equally plausible DEMs.  
  4. Run the entire TDA feature extraction pipeline on each of these plausible DEMs.  
  5. This process results in a probability distribution of values for each TLSP feature at every location in the study area.  
* **Assessing TLSP Sensitivity and Confidence Intervals:** The output of the Monte Carlo simulation provides a direct way to assess the robustness of the topological features. By examining the variance of the output distributions, one can identify which TLSPs are most sensitive to small perturbations in the input elevation. This process also yields the necessary data to construct pointwise confidence intervals for the persistence landscape functions, providing a rigorous quantification of feature uncertainty.94

#### **4.1.2 Sensitivity Analysis Design**

The entire analysis pipeline, from TDA parameters to the machine learning model, involves numerous user-defined parameters. A sensitivity analysis is required to understand which of these parameters have the most significant influence on the final SOC prediction, thereby identifying the most critical methodological choices.95

* **Key Parameters to Test:** A comprehensive sensitivity analysis should investigate the impact of:  
  * TDA window size  
  * TDA vectorization method (PL vs. PI) and its parameters (e.g., PI resolution)  
  * DEM preprocessing choices (e.g., smoothing kernel width)  
  * Elastic Net hyperparameters (α and λ)  
* **Global Sensitivity Analysis (GSA) using Sobol Indices:** A simple one-at-a-time (OAT) sensitivity analysis is inadequate as it fails to capture interactions between parameters. A **Global Sensitivity Analysis (GSA)** is the state-of-the-art. The Sobol method is a variance-based GSA that decomposes the variance of the model output into contributions attributable to each input parameter individually (first-order Sobol index) and their interactions with other parameters (higher-order indices).96 The **total Sobol index** for a parameter quantifies its total contribution to the output variance, including all main effects and interaction effects.  
* **Implementation and Reporting:** While computationally intensive, GSA provides unparalleled insight into the model's behavior. The analysis involves running the model across a carefully designed set of parameter combinations. The results can be reported compactly and effectively with a bar chart showing the total Sobol index for each parameter, clearly ranking them by their overall influence on the model's predictions.96

### **Section 4.2: High-Performance Computing and Reproducibility Framework**

#### **4.2.1 Runtime and Feasibility Assessment**

The proposed analysis is computationally intensive. A feasibility assessment is a crucial first step.

* **Benchmarking:** The TDA computation should be benchmarked on a representative subset of the data, such as a single 10km x 10km DEM tile.97 The wall-clock time and peak memory usage for processing all windows within this tile should be recorded on the target hardware.  
* **Extrapolation and Fallback Strategies:** These benchmark results can be extrapolated to the full study area to estimate the total computational cost. If the estimated serial runtime is prohibitive (e.g., weeks or months), several strategies can be employed:  
  1. **Parallelization:** The moving window analysis is an "embarrassingly parallel" problem and is an ideal candidate for parallel processing using a framework like Dask. This is the preferred solution.  
  2. **Reduced Window Density:** Instead of a continuously sliding window, the analysis could be performed on a sparser grid of windows.  
  3. **Coarsening Resolution:** As a last resort, the input DEM could be resampled to a coarser resolution (e.g., 20m or 30m). This is highly undesirable as it undermines the core premise of using high-resolution data.

#### **4.2.2 Reproducibility Infrastructure**

For a computationally complex study, ensuring full reproducibility is a scientific imperative. This requires a multi-layered approach to versioning and environment control.99

* **Software Environment Encapsulation (Docker):** The entire computational environment—including the operating system, specific versions of Python/R, and all required libraries (e.g., GDAL, GUDHI, scikit-tda, Dask)—must be codified in a **Dockerfile**. This file serves as an executable blueprint for building a Docker container that can perfectly replicate the software environment on any machine, eliminating "works on my machine" problems and ensuring long-term computational reproducibility.101  
* **Data and Pipeline Versioning (Git \+ DVC):** A combination of Git and DVC (Data Version Control) will be used to manage the project assets.  
  * **Git:** All source code (scripts, notebooks) will be version-controlled with Git.  
  * **DVC:** Large data files (raw DEMs, intermediate raster products, final models) cannot be efficiently stored in Git. DVC is used to track these large files. It stores small "metafiles" in Git that point to the full data files stored in remote storage (e.g., an S3 bucket or institutional server). DVC also manages the computational pipeline, defining the stages of analysis and their dependencies in a dvc.yaml file. This creates an unbroken, version-controlled chain of provenance from raw data and code to final results.103  
* **Stochasticity Control:** All scripts involving random processes (e.g., cross-validation fold creation, machine learning model initialization) must be controlled by setting a single, global random seed at the beginning of execution to ensure that results are perfectly repeatable.

#### **4.2.3 Parallel Processing Verification**

**Dask** is the recommended framework for parallelizing the raster processing workflow in Python. It can intelligently break large rasters (Dask arrays) into smaller chunks and distribute the computation across multiple CPU cores or even a cluster of machines.105

* **Verification Plan:** It is critical to verify that the parallel implementation produces identical results to a serial implementation.  
  1. Run the full pipeline on a small test area in both serial mode and in parallel using Dask.  
  2. Compare the numerical outputs (the final TLSP feature rasters) to ensure they are identical within machine precision. Any discrepancies point to a bug in the parallelization logic.  
  3. The halo/padding implementation requires special attention in a parallel context. The dask.array.map\_overlap function is specifically designed for stencil or moving window operations and must be used to correctly handle the data exchange between chunks at their boundaries.  
* **Dask Dashboard Monitoring:** The Dask dashboard provides a real-time view of the computation and is essential for debugging and performance tuning. Key indicators of problems include excessive red coloring in the task stream (indicating high communication overhead), worker memory approaching its limit (risking crashes), or tasks remaining in a "waiting" state for extended periods (indicating a scheduling or dependency issue).105

---

## **Part V: Strategic Positioning and Broader Impact**

This part frames the research within the broader scientific and societal context, articulating its unique contributions and potential benefits, which is critical for a funding proposal such as one for the NSF.

### **Section 5.1: Contribution to the State-of-the-Art in Geomorphometry**

This research is positioned at the intersection of geomorphometry, data science, and soil science. To articulate its novelty, it is essential to compare the proposed TDA-based approach with both traditional and other emerging methods for landscape analysis.

* **Current State-of-the-Art:** Geomorphometry is evolving from a descriptive science focused on morphological metrics towards a more process-oriented discipline that aims to understand the mechanisms of landscape evolution.107 Key trends include the use of machine learning for landform classification, an emphasis on multi-scale analysis, and the exploitation of high-fidelity elevation data from sources like LiDAR.107  
* **Alternative Approaches:**  
  * **Traditional Geomorphometrics:** Relies on a set of well-established, locally computed derivatives of the DEM, such as slope, aspect, curvature, and TWI. These metrics are interpretable but often scale-dependent and may not capture complex, non-local spatial relationships.  
  * **Deep Learning:** The application of deep learning models, particularly Convolutional Neural Networks (CNNs), directly to DEM rasters is a powerful and emerging alternative. CNNs can learn complex spatial feature hierarchies automatically but often function as "black boxes," making the direct geomorphic interpretation of their learned features challenging.  
* **Unique Advantages of TDA:** The proposed TDA methodology offers a unique combination of strengths that positions it as a significant advancement over existing methods.  
  * **Mathematical Rigor and Enhanced Interpretability:** Unlike the often opaque features learned by deep learning models, TDA features are topological invariants with precise mathematical definitions. As detailed in Section 3.2.2, these abstract features (e.g., persistence of H₀ and H₁) can be directly translated into intuitive and physically meaningful geomorphic concepts like basin depth and peak prominence.  
  * **Inherent Multi-Scale Analysis:** Traditional methods often require the user to specify a scale of analysis (e.g., the window size for calculating curvature). TDA, through the mechanism of filtration, inherently captures features across all possible scales simultaneously. The persistence of a feature provides a natural, data-driven measure of its significance across these scales.  
  * **Robustness and Invariance:** TDA is, by design, robust to noise (short-persistence features can be filtered out) and is invariant to transformations like rotation and translation, focusing on the intrinsic shape of the data.

**Table 4: Strategic Comparison of Landscape Analysis Methodologies**

| Aspect | Traditional Geomorphometrics | Topological Data Analysis (TDA) | Deep Learning (e.g., CNNs) |
| :---- | :---- | :---- | :---- |
| **Key Principle** | Local derivatives and neighborhood analysis of the elevation surface. | Quantifying the multi-scale shape and connectivity of the landscape via algebraic topology. | Learning hierarchical spatial feature representations directly from raster data. |
| **Example Metrics** | Slope, Aspect, Curvature, Topographic Wetness Index (TWI). | Persistence of H₀ (basins), H₁ (peaks/ridges); Persistence Landscapes/Images. | Learned convolutional filters and feature maps at multiple network layers. |
| **Strengths** | Highly interpretable, computationally efficient, well-established. | Mathematically rigorous, inherently multi-scale, robust to noise, interpretable features. | High predictive power, learns complex/non-linear patterns automatically, no manual feature engineering. |
| **Weaknesses** | Scale-dependent, may miss non-local or complex shape features. | Computationally intensive, conceptually novel, requires vectorization for ML integration. | "Black box" nature, requires very large datasets, prone to overfitting, features lack direct physical meaning. |
| **Interpretability** | **High:** Each metric has a direct physical meaning (e.g., steepness). | **High (with translation):** Abstract features (H₀, H₁) can be rigorously translated to geomorphic concepts (basin depth, peak prominence). | **Low:** Learned filters are difficult to interpret geomorphically, requiring post-hoc methods like SHAP. |

### **Section 5.2: Broader Impacts and Dissemination Plan**

The societal and scientific relevance of this research extends beyond its core technical contributions. A strong plan for disseminating results and engaging with stakeholders is essential.

* **Educational Component:** The project will generate educational materials to promote the use of TDA in the geosciences. This will include the development of online tutorials (e.g., as Jupyter Notebooks) and teaching modules suitable for graduate-level courses in geoinformatics or computational geography. Findings and methods will also be presented in workshops at major scientific conferences (e.g., AGU, AAG).  
* **Stakeholder Engagement and Societal Benefit:** The primary output—improved, high-resolution SOC maps—has direct applications for several key stakeholders.  
  * **USDA and Land Trusts:** More accurate SOC maps can enhance decision-making in precision agriculture, help identify lands for conservation based on soil health, and inform sustainable land management practices.112  
  * **Carbon Markets:** The growth of voluntary carbon markets for agriculture is critically dependent on accurate, transparent, and scalable methods for Measurement, Reporting, and Verification (MRV) of soil carbon sequestration. This research can contribute directly to the "M" and "R" of MRV, providing a novel, data-driven approach to quantifying field-scale SOC stocks that could support the integrity and growth of these markets.79  
* **Open Science Plan:** The project will adhere to the principles of open and reproducible science.  
  * **Code:** All analysis code will be developed in a public GitHub repository under a permissive open-source license (e.g., MIT or BSD). The computational environment will be archived as a Docker image and made available on a public registry like Docker Hub. A software paper may be submitted to the Journal of Open Source Software (JOSS) to ensure the code is citable and peer-reviewed.  
  * **Data:** All final data products, including the generated TLSP feature rasters and the final SOC prediction maps and their uncertainty estimates, will be archived in a permanent public repository such as Zenodo or Figshare. The data will be assigned a Digital Object Identifier (DOI) to ensure long-term accessibility and citability.

---

## **Part VI: Project Management and Contingency Planning**

This final part addresses the practical realities of executing the research project, identifying potential roadblocks and developing contingency plans to ensure its successful completion.

### **Section 6.1: Risk Assessment and Data Management**

A proactive risk management plan is essential for a project of this complexity.115

* **Timeline Risk Assessment:**  
  * **High-Risk Tasks:**  
    1. **TDA Pipeline Development:** The development and optimization of the parallelized, moving-window TDA pipeline is a significant technical challenge and may encounter unforeseen computational bottlenecks.  
    2. **Model Tuning and Validation:** The nested spatial cross-validation loop for hyperparameter tuning of the Elastic Net model will be extremely computationally intensive and may overrun time estimates.  
    3. **Independent Validation Data Acquisition:** The entire project's claim to overcoming circularity rests on validation against independent field data. Delays in identifying, acquiring, or processing this data represent a major project dependency and risk.  
  * **Dependencies:** The entire modeling workflow is dependent on the successful and timely completion of the TDA feature generation pipeline. The scientific interpretation is dependent on the successful training of a predictive model.  
  * **Minimum Viable Product (MVP) and Contingencies:** If significant delays occur, the project scope can be reduced to a minimum viable product. This could involve:  
    * Focusing on only one TDA vectorization method (Persistence Landscapes, which are computationally faster).  
    * Reducing the scope of the sensitivity and uncertainty analyses.  
    * Restricting the geographic focus to a smaller subset of the provinces.  
  * **Contingency for H₂ Homology:** The query notes the potential exploration of H₂ (2-dimensional voids). Computing and interpreting H₂ is significantly more complex than H₀ and H₁. This should be explicitly designated as a "stretch goal" or "future work" and should not be part of the core project plan, to avoid jeopardizing the primary objectives.  
* **Data Availability and Management:**  
  * **Confirmation:** An immediate priority is to verify the accessibility of all required input datasets (10m DEM, POLARIS SOC and uncertainty layers, gridMET, etc.). This includes checking for broken download links, institutional access requirements, or data use agreements.  
  * **Storage and Backup:** The total data volume for this project will be substantial. A data management plan must be established, calculating the storage requirements for raw, intermediate, and final data products and ensuring that sufficient and secure storage (local or cloud-based) is available. A regular backup schedule must be implemented.  
  * **Contingency Plan:** A backup plan for key datasets should be considered. If access to the POLARIS dataset becomes an issue, an alternative national or global SOC product (e.g., SoilGrids) could be used as a substitute, though this would require acknowledging a significant change in the project's scope and resolution.

#### **Works cited**

1. MANOVA (Multivariate Analysis of Variance) \- GeeksforGeeks, accessed October 22, 2025, [https://www.geeksforgeeks.org/python/manova-multivariate-analysis-of-variance/](https://www.geeksforgeeks.org/python/manova-multivariate-analysis-of-variance/)  
2. Statistical Power, Sample Sizes, and the Software to Calculate Them Easily | BioScience, accessed October 22, 2025, [https://academic.oup.com/bioscience/article/56/7/607/234386](https://academic.oup.com/bioscience/article/56/7/607/234386)  
3. Power Analyses \- :: Environmental Computing, accessed October 22, 2025, [https://environmentalcomputing.net/statistics/power-analysis/](https://environmentalcomputing.net/statistics/power-analysis/)  
4. Prediction of the soil organic carbon in the LUCAS soil database based on spectral clustering \- Soil and Water Research, accessed October 22, 2025, [https://swr.agriculturejournals.cz/artkey/swr-202301-0006\_prediction-of-the-soil-organic-carbon-in-the-lucas-soil-database-based-on-spectral-clustering.php](https://swr.agriculturejournals.cz/artkey/swr-202301-0006_prediction-of-the-soil-organic-carbon-in-the-lucas-soil-database-based-on-spectral-clustering.php)  
5. Large-Scale Soil Organic Carbon Estimation via a Multisource Data Fusion Approach, accessed October 22, 2025, [https://www.mdpi.com/2072-4292/17/5/771](https://www.mdpi.com/2072-4292/17/5/771)  
6. G\*Power \- Psychologie \- HHU, accessed October 22, 2025, [https://www.psychologie.hhu.de/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower](https://www.psychologie.hhu.de/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower)  
7. G\*Power 3: a flexible statistical power analysis program for the social, behavioral, and biomedical sciences \- PubMed, accessed October 22, 2025, [https://pubmed.ncbi.nlm.nih.gov/17695343/](https://pubmed.ncbi.nlm.nih.gov/17695343/)  
8. A flexible statistical power analysis program for the social, behavioral, and biomedical sciences, accessed October 22, 2025, [https://www.uvm.edu/\~statdhtx/methods8/Supplements/GPower3-BRM-Paper.pdf](https://www.uvm.edu/~statdhtx/methods8/Supplements/GPower3-BRM-Paper.pdf)  
9. Sample Size Calculation with GPower \- UND School of Medicine & Health Sciences, accessed October 22, 2025, [https://med.und.edu/research/transcend/\_files/pdfs/berdc\_resource\_pdfs/sample\_size\_gpower\_module.pdf](https://med.und.edu/research/transcend/_files/pdfs/berdc_resource_pdfs/sample_size_gpower_module.pdf)  
10. pmc.ncbi.nlm.nih.gov, accessed October 22, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC8355525/\#:\~:text=For%20the%20Persistent%20Images%2C%20Persistence,computed%20from%20these%20persistence%20diagrams.](https://pmc.ncbi.nlm.nih.gov/articles/PMC8355525/#:~:text=For%20the%20Persistent%20Images%2C%20Persistence,computed%20from%20these%20persistence%20diagrams.)  
11. a flexible statistical power analysis program for the social ..., accessed October 22, 2025, [https://annescollege.fsu.edu/sites/g/files/upcbnu4516/files/flexible-statistical-power-analysis.pdf](https://annescollege.fsu.edu/sites/g/files/upcbnu4516/files/flexible-statistical-power-analysis.pdf)  
12. A Note on Likelihood Ratio Tests for Models with Latent Variables \- PMC, accessed October 22, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC7826319/](https://pmc.ncbi.nlm.nih.gov/articles/PMC7826319/)  
13. Power for Multilevel Analysis \- OSF, accessed October 22, 2025, [https://osf.io/qge2c/wiki/Power%20for%20Multilevel%20Analysis/](https://osf.io/qge2c/wiki/Power%20for%20Multilevel%20Analysis/)  
14. Doubly Balanced Spatial Sampling with Spreading and Restitution of Auxiliary Totals | Request PDF \- ResearchGate, accessed October 22, 2025, [https://www.researchgate.net/publication/235972605\_Doubly\_Balanced\_Spatial\_Sampling\_with\_Spreading\_and\_Restitution\_of\_Auxiliary\_Totals](https://www.researchgate.net/publication/235972605_Doubly_Balanced_Spatial_Sampling_with_Spreading_and_Restitution_of_Auxiliary_Totals)  
15. Doubly balanced spatial sampling with spreading and restitution of auxiliary totals, accessed October 22, 2025, [https://libra.unine.ch/bitstreams/80a277a3-d97f-4a40-aea8-badbf0c27795/download](https://libra.unine.ch/bitstreams/80a277a3-d97f-4a40-aea8-badbf0c27795/download)  
16. Explore a space-time cube | Documentation \- Learn ArcGIS, accessed October 22, 2025, [https://learn.arcgis.com/en/projects/explore-a-space-time-cube/](https://learn.arcgis.com/en/projects/explore-a-space-time-cube/)  
17. How Create Space Time Cube works—ArcGIS Pro | Documentation, accessed October 22, 2025, [https://pro.arcgis.com/en/pro-app/latest/tool-reference/space-time-pattern-mining/learnmorecreatecube.htm](https://pro.arcgis.com/en/pro-app/latest/tool-reference/space-time-pattern-mining/learnmorecreatecube.htm)  
18. What is Multivariate Analysis of Variance (MANOVA)? \- SixSigma.us, accessed October 22, 2025, [https://www.6sigma.us/six-sigma-in-focus/multivariate-analysis-of-variance-manova/](https://www.6sigma.us/six-sigma-in-focus/multivariate-analysis-of-variance-manova/)  
19. MANOVA Assumptions | Real Statistics Using Excel, accessed October 22, 2025, [https://real-statistics.com/multivariate-statistics/multivariate-analysis-of-variance-manova/manova-assumptions/](https://real-statistics.com/multivariate-statistics/multivariate-analysis-of-variance-manova/manova-assumptions/)  
20. Multivariate Analysis of Variance (MANOVA) \- NCSS, accessed October 22, 2025, [https://www.ncss.com/wp-content/themes/ncss/pdf/Procedures/NCSS/Multivariate\_Analysis\_of\_Variance-MANOVA.pdf](https://www.ncss.com/wp-content/themes/ncss/pdf/Procedures/NCSS/Multivariate_Analysis_of_Variance-MANOVA.pdf)  
21. Fixed-Effect vs Random-Effects Models for Meta-Analysis: 3 Points to Consider \- PMC \- NIH, accessed October 22, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC9393987/](https://pmc.ncbi.nlm.nih.gov/articles/PMC9393987/)  
22. Layman explanation of fixed, random, and mixed effects? : r/statistics \- Reddit, accessed October 22, 2025, [https://www.reddit.com/r/statistics/comments/4qzcgx/layman\_explanation\_of\_fixed\_random\_and\_mixed/](https://www.reddit.com/r/statistics/comments/4qzcgx/layman_explanation_of_fixed_random_and_mixed/)  
23. Random vs. fixed effects meta-analysis \- Datamethods Discussion Forum, accessed October 22, 2025, [https://discourse.datamethods.org/t/random-vs-fixed-effects-meta-analysis/7361](https://discourse.datamethods.org/t/random-vs-fixed-effects-meta-analysis/7361)  
24. The three nested levels of regions and sub-regions that maximise the... | Download Scientific Diagram \- ResearchGate, accessed October 22, 2025, [https://www.researchgate.net/figure/The-three-nested-levels-of-regions-and-sub-regions-that-maximise-the-capture-of-areas\_fig8\_222420778](https://www.researchgate.net/figure/The-three-nested-levels-of-regions-and-sub-regions-that-maximise-the-capture-of-areas_fig8_222420778)  
25. Nested ANOVA \- :: Environmental Computing, accessed October 22, 2025, [https://environmentalcomputing.net/statistics/linear-models/anova/anova-nested/](https://environmentalcomputing.net/statistics/linear-models/anova/anova-nested/)  
26. False Discovery Rate | Columbia University Mailman School of Public Health, accessed October 22, 2025, [https://www.publichealth.columbia.edu/research/population-health-methods/false-discovery-rate](https://www.publichealth.columbia.edu/research/population-health-methods/false-discovery-rate)  
27. The Effect of Correlation and Error Rate Specification on Thresholding Methods in fMRI Analysis \- Medical College of Wisconsin, accessed October 22, 2025, [https://www.mcw.edu/-/media/MCW/Departments/Biostatistics/tr042.pdf](https://www.mcw.edu/-/media/MCW/Departments/Biostatistics/tr042.pdf)  
28. 4.3 \-1995 \- Two Huge Steps for Biological Inference | STAT 555, accessed October 22, 2025, [https://online.stat.psu.edu/stat555/node/59/](https://online.stat.psu.edu/stat555/node/59/)  
29. The effect of correlation in false discovery rate estimation \- PMC \- PubMed Central, accessed October 22, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC3412603/](https://pmc.ncbi.nlm.nih.gov/articles/PMC3412603/)  
30. False discovery rate \- Wikipedia, accessed October 22, 2025, [https://en.wikipedia.org/wiki/False\_discovery\_rate](https://en.wikipedia.org/wiki/False_discovery_rate)  
31. Spatial cross-validation for GeoAI 1, accessed October 22, 2025, [https://www.acsu.buffalo.edu/\~yhu42/papers/2023\_GeoAIHandbook\_SpatialCV.pdf](https://www.acsu.buffalo.edu/~yhu42/papers/2023_GeoAIHandbook_SpatialCV.pdf)  
32. Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure, accessed October 22, 2025, [https://www.wsl.ch/lud/biodiversity\_events/papers/Roberts\_et\_al-2017-Ecography.pdf](https://www.wsl.ch/lud/biodiversity_events/papers/Roberts_et_al-2017-Ecography.pdf)  
33. Choosing blocks for spatial cross-validation: lessons from ... \- Frontiers, accessed October 22, 2025, [https://www.frontiersin.org/journals/remote-sensing/articles/10.3389/frsen.2025.1531097/full](https://www.frontiersin.org/journals/remote-sensing/articles/10.3389/frsen.2025.1531097/full)  
34. Choosing blocks for spatial cross-validation: lessons from a marine remote sensing case study \- Frontiers, accessed October 22, 2025, [https://www.frontiersin.org/journals/remote-sensing/articles/10.3389/frsen.2025.1531097/epub](https://www.frontiersin.org/journals/remote-sensing/articles/10.3389/frsen.2025.1531097/epub)  
35. Spatial Autocorrelation, accessed October 22, 2025, [https://kevintshoemaker.github.io/NRES-746/spatial\_autocorrelation.html](https://kevintshoemaker.github.io/NRES-746/spatial_autocorrelation.html)  
36. Buffering \- spatialsample, accessed October 22, 2025, [https://spatialsample.tidymodels.org/articles/buffering.html](https://spatialsample.tidymodels.org/articles/buffering.html)  
37. cv\_buffer: Use buffer around records to separate train and test folds... in blockCV: Spatial and Environmental Blocking for K-Fold and LOO Cross-Validation \- rdrr.io, accessed October 22, 2025, [https://rdrr.io/cran/blockCV/man/cv\_buffer.html](https://rdrr.io/cran/blockCV/man/cv_buffer.html)  
38. Spatial Autocorrelation Approaches to Testing Residuals from Least Squares Regression | PLOS One \- Research journals, accessed October 22, 2025, [https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0146865](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0146865)  
39. (PDF) The Application of Spatial Autoregressive Models for Analyzing the Influence of Spatial Factors on Real Estate Prices and Values \- ResearchGate, accessed October 22, 2025, [https://www.researchgate.net/publication/357207018\_The\_Application\_of\_Spatial\_Autoregressive\_Models\_for\_Analyzing\_the\_Influence\_of\_Spatial\_Factors\_on\_Real\_Estate\_Prices\_and\_Values](https://www.researchgate.net/publication/357207018_The_Application_of_Spatial_Autoregressive_Models_for_Analyzing_the_Influence_of_Spatial_Factors_on_Real_Estate_Prices_and_Values)  
40. Model selection for spatial econometrics using PROC SPATIALREG ..., accessed October 22, 2025, [https://blogs.sas.com/content/subconsciousmusings/2017/03/15/spatial-econometric-model-selection-using-proc-spatialreg/](https://blogs.sas.com/content/subconsciousmusings/2017/03/15/spatial-econometric-model-selection-using-proc-spatialreg/)  
41. Geographically Weighted Elastic Net: A Variable ... \- Kenan Li, accessed October 22, 2025, [https://kenan-li.github.io/assets/pdf/Li-AAG-18.pdf](https://kenan-li.github.io/assets/pdf/Li-AAG-18.pdf)  
42. Regularization and variable selection via the elastic net \- Purdue Department of Statistics, accessed October 22, 2025, [https://www.stat.purdue.edu/\~tlzhang/mathstat/ElasticNet.pdf](https://www.stat.purdue.edu/~tlzhang/mathstat/ElasticNet.pdf)  
43. Using elastic net regression to perform spectrally relevant variable selection \- ResearchGate, accessed October 22, 2025, [https://www.researchgate.net/publication/324751089\_Using\_elastic\_net\_regression\_to\_perform\_spectrally\_relevant\_variable\_selection](https://www.researchgate.net/publication/324751089_Using_elastic_net_regression_to_perform_spectrally_relevant_variable_selection)  
44. Stepwise regression \- Wikipedia, accessed October 22, 2025, [https://en.wikipedia.org/wiki/Stepwise\_regression](https://en.wikipedia.org/wiki/Stepwise_regression)  
45. Variable Selection with Elastic Net | R-bloggers, accessed October 22, 2025, [https://www.r-bloggers.com/2017/09/variable-selection-with-elastic-net/](https://www.r-bloggers.com/2017/09/variable-selection-with-elastic-net/)  
46. Multicollinearity and misleading statistical results \- PMC \- NIH, accessed October 22, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC6900425/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6900425/)  
47. 10.7 \- Detecting Multicollinearity Using Variance Inflation Factors | STAT 462, accessed October 22, 2025, [https://online.stat.psu.edu/stat462/node/180/](https://online.stat.psu.edu/stat462/node/180/)  
48. Variance Inflation Factor: How to Detect Multicollinearity \- DataCamp, accessed October 22, 2025, [https://www.datacamp.com/tutorial/variance-inflation-factor](https://www.datacamp.com/tutorial/variance-inflation-factor)  
49. which captures the multi-scale topological features of a dataset. A summary of persistent homology is provided by the \- arXiv, accessed October 22, 2025, [https://arxiv.org/html/2410.14193v2](https://arxiv.org/html/2410.14193v2)  
50. Topology Applied to Machine Learning: From Global to Local \- Frontiers, accessed October 22, 2025, [https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2021.668302/full](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2021.668302/full)  
51. Statistical Topological Data Analysis using Persistence Landscapes \- Journal of Machine Learning Research, accessed October 22, 2025, [https://www.jmlr.org/papers/volume16/bubenik15a/bubenik15a.pdf](https://www.jmlr.org/papers/volume16/bubenik15a/bubenik15a.pdf)  
52. The persistence landscape and some of its properties, accessed October 22, 2025, [https://arxiv.org/pdf/1810.04963](https://arxiv.org/pdf/1810.04963)  
53. The Persistence Landscape and Some of Its Properties \- ResearchGate, accessed October 22, 2025, [https://www.researchgate.net/publication/342459664\_The\_Persistence\_Landscape\_and\_Some\_of\_Its\_Properties](https://www.researchgate.net/publication/342459664_The_Persistence_Landscape_and_Some_of_Its_Properties)  
54. A Comparative Study of Machine Learning Methods for Persistence Diagrams \- Frontiers, accessed October 22, 2025, [https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2021.681174/full](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2021.681174/full)  
55. arXiv:2312.17093v3 \[math.AT\] 21 Oct 2024, accessed October 22, 2025, [https://arxiv.org/pdf/2312.17093](https://arxiv.org/pdf/2312.17093)  
56. Noise robustness of persistent homology on greyscale images ..., accessed October 22, 2025, [https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0257215](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0257215)  
57. Cross-Validation in Machine Learning: How to Do It Right \- Neptune.ai, accessed October 22, 2025, [https://neptune.ai/blog/cross-validation-in-machine-learning-how-to-do-it-right](https://neptune.ai/blog/cross-validation-in-machine-learning-how-to-do-it-right)  
58. Persistence Images — Persim 0.3.8 documentation, accessed October 22, 2025, [https://persim.scikit-tda.org/en/latest/notebooks/Persistence%20images.html](https://persim.scikit-tda.org/en/latest/notebooks/Persistence%20images.html)  
59. Persistence Images in Classification — Persim 0.3.8 documentation \- Scikit-TDA, accessed October 22, 2025, [https://persim.scikit-tda.org/en/latest/notebooks/Classification%20with%20persistence%20images.html](https://persim.scikit-tda.org/en/latest/notebooks/Classification%20with%20persistence%20images.html)  
60. 26 PERSISTENT HOMOLOGY, accessed October 22, 2025, [https://pub.ista.ac.at/\~edels/Papers/2017-05-PersDM.pdf](https://pub.ista.ac.at/~edels/Papers/2017-05-PersDM.pdf)  
61. 24 PERSISTENT HOMOLOGY \- CSUN, accessed October 22, 2025, [https://www.csun.edu/\~ctoth/Handbook/chap24.pdf](https://www.csun.edu/~ctoth/Handbook/chap24.pdf)  
62. Persistent homology \- Wikipedia, accessed October 22, 2025, [https://en.wikipedia.org/wiki/Persistent\_homology](https://en.wikipedia.org/wiki/Persistent_homology)  
63. Comparison of Persistence Diagrams \- arXiv, accessed October 22, 2025, [https://arxiv.org/pdf/2003.01352](https://arxiv.org/pdf/2003.01352)  
64. Topological data analysis \- Wikipedia, accessed October 22, 2025, [https://en.wikipedia.org/wiki/Topological\_data\_analysis](https://en.wikipedia.org/wiki/Topological_data_analysis)  
65. Computational Topology for Data Analysis: Notes from Book by \- CS@Purdue, accessed October 22, 2025, [https://www.cs.purdue.edu/homes/tamaldey/course/CTDA/topic4.pdf](https://www.cs.purdue.edu/homes/tamaldey/course/CTDA/topic4.pdf)  
66. An Automated Processing Algorithm for Flat Areas Resulting from DEM Filling and Interpolation \- ResearchGate, accessed October 22, 2025, [https://www.researchgate.net/publication/321202403\_An\_Automated\_Processing\_Algorithm\_for\_Flat\_Areas\_Resulting\_from\_DEM\_Filling\_and\_Interpolation](https://www.researchgate.net/publication/321202403_An_Automated_Processing_Algorithm_for_Flat_Areas_Resulting_from_DEM_Filling_and_Interpolation)  
67. How do I get rid of edge effects while using focal in R to smooth a raster?, accessed October 22, 2025, [https://gis.stackexchange.com/questions/187410/how-do-i-get-rid-of-edge-effects-while-using-focal-in-r-to-smooth-a-raster](https://gis.stackexchange.com/questions/187410/how-do-i-get-rid-of-edge-effects-while-using-focal-in-r-to-smooth-a-raster)  
68. THE HALOED LINE EFFECT FOR HIDDEN LINE ELIMINATION. Arthur Appel Computing Systems Department IBM Thomas J. Watson Research Cent, accessed October 22, 2025, [https://ohiostate.pressbooks.pub/app/uploads/sites/45/2017/09/halo-appel.pdf](https://ohiostate.pressbooks.pub/app/uploads/sites/45/2017/09/halo-appel.pdf)  
69. One of the most important differences between filling and breaching is... \- ResearchGate, accessed October 22, 2025, [https://www.researchgate.net/figure/One-of-the-most-important-differences-between-filling-and-breaching-is-not-where-they\_fig4\_320552504](https://www.researchgate.net/figure/One-of-the-most-important-differences-between-filling-and-breaching-is-not-where-they_fig4_320552504)  
70. LiDAR DEM Smoothing and the Preservation of Drainage Features \- ResearchGate, accessed October 22, 2025, [https://www.researchgate.net/publication/335220178\_LiDAR\_DEM\_Smoothing\_and\_the\_Preservation\_of\_Drainage\_Features](https://www.researchgate.net/publication/335220178_LiDAR_DEM_Smoothing_and_the_Preservation_of_Drainage_Features)  
71. Effects of LiDAR DEM Smoothing and Conditioning Techniques on a Topography‐Based Wetland Identification Model \- ResearchGate, accessed October 22, 2025, [https://www.researchgate.net/publication/332821978\_Effects\_of\_LiDAR\_DEM\_Smoothing\_and\_Conditioning\_Techniques\_on\_a\_Topography-Based\_Wetland\_Identification\_Model](https://www.researchgate.net/publication/332821978_Effects_of_LiDAR_DEM_Smoothing_and_Conditioning_Techniques_on_a_Topography-Based_Wetland_Identification_Model)  
72. POLARIS: A 30-meter probabilistic soil series map of the contiguous United States | Request PDF \- ResearchGate, accessed October 22, 2025, [https://www.researchgate.net/publication/301309046\_POLARIS\_A\_30-meter\_probabilistic\_soil\_series\_map\_of\_the\_contiguous\_United\_States](https://www.researchgate.net/publication/301309046_POLARIS_A_30-meter_probabilistic_soil_series_map_of_the_contiguous_United_States)  
73. POLARIS: A 30-meter probabilistic soil series map of the contiguous United States, accessed October 22, 2025, [https://pubs.usgs.gov/publication/70170912](https://pubs.usgs.gov/publication/70170912)  
74. POLARIS: A 30-meter probabilistic soil series map of the contiguous United States, accessed October 22, 2025, [https://collaborate.princeton.edu/en/publications/polaris-a-30-meter-probabilistic-soil-series-map-of-the-contiguou](https://collaborate.princeton.edu/en/publications/polaris-a-30-meter-probabilistic-soil-series-map-of-the-contiguou)  
75. POLARIS properties: 30-meter probabilistic maps of soil properties over the contiguous United States \- USGS, accessed October 22, 2025, [https://www.usgs.gov/publications/polaris-properties-30-meter-probabilistic-maps-soil-properties-over-contiguous-united](https://www.usgs.gov/publications/polaris-properties-30-meter-probabilistic-maps-soil-properties-over-contiguous-united)  
76. POLARIS Soil Properties: 30-m Probabilistic Maps of Soil Properties Over the Contiguous United States \- Scholars@Duke, accessed October 22, 2025, [https://scholars.duke.edu/individual/pub1381493](https://scholars.duke.edu/individual/pub1381493)  
77. (PDF) Comparison of the Resampling Methods for Gridded DEM ..., accessed October 22, 2025, [https://www.researchgate.net/publication/358134527\_Comparison\_of\_the\_Resampling\_Methods\_for\_Gridded\_DEM\_Downscaling](https://www.researchgate.net/publication/358134527_Comparison_of_the_Resampling_Methods_for_Gridded_DEM_Downscaling)  
78. Digital Soil Mapping \- Natural Resources Conservation Service, accessed October 22, 2025, [https://www.nrcs.usda.gov/sites/default/files/2022-09/SSM-ch5.pdf](https://www.nrcs.usda.gov/sites/default/files/2022-09/SSM-ch5.pdf)  
79. Digital soil mapping in support of voluntary carbon market programs ..., accessed October 22, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12404560/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12404560/)  
80. Sustainable soil organic carbon prediction using machine learning and the ninja optimization algorithm \- ResearchGate, accessed October 22, 2025, [https://www.researchgate.net/publication/394882604\_Sustainable\_soil\_organic\_carbon\_prediction\_using\_machine\_learning\_and\_the\_ninja\_optimization\_algorithm](https://www.researchgate.net/publication/394882604_Sustainable_soil_organic_carbon_prediction_using_machine_learning_and_the_ninja_optimization_algorithm)  
81. Sustainable soil organic carbon prediction using machine learning and the ninja optimization algorithm \- Frontiers, accessed October 22, 2025, [https://www.frontiersin.org/journals/environmental-science/articles/10.3389/fenvs.2025.1630762/full](https://www.frontiersin.org/journals/environmental-science/articles/10.3389/fenvs.2025.1630762/full)  
82. 18 SHAP – Interpretable Machine Learning, accessed October 22, 2025, [https://christophm.github.io/interpretable-ml-book/shap.html](https://christophm.github.io/interpretable-ml-book/shap.html)  
83. Practical guide to SHAP analysis: Explaining supervised machine learning model predictions in drug development \- NIH, accessed October 22, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11513550/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11513550/)  
84. Examining the spatial pattern of SHAP values \- University of Twente Research Information, accessed October 22, 2025, [https://research.utwente.nl/files/353759709/1-s2.0-S1674987124000240-main.pdf](https://research.utwente.nl/files/353759709/1-s2.0-S1674987124000240-main.pdf)  
85. GeoShapley: A Game Theory Approach to Measuring Spatial Effects ..., accessed October 22, 2025, [https://www.tandfonline.com/doi/full/10.1080/24694452.2024.2350982](https://www.tandfonline.com/doi/full/10.1080/24694452.2024.2350982)  
86. SHAP Value Analysis of a Random Forest Atmospheric Neutral Density Model \- arXiv, accessed October 22, 2025, [https://arxiv.org/html/2509.26299v1](https://arxiv.org/html/2509.26299v1)  
87. A distribution-guided Mapper algorithm \- arXiv, accessed October 22, 2025, [https://arxiv.org/html/2401.12237v1](https://arxiv.org/html/2401.12237v1)  
88. A distribution-guided Mapper algorithm \- PMC, accessed October 22, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11881416/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11881416/)  
89. tda-mapper — tda-mapper documentation, accessed October 22, 2025, [https://tda-mapper.readthedocs.io/](https://tda-mapper.readthedocs.io/)  
90. Topological Data Analysis Using the Mapper Algorithm \- University of Central Florida, accessed October 22, 2025, [https://purls.library.ucf.edu/go/DP0027840](https://purls.library.ucf.edu/go/DP0027840)  
91. Error propagation of DEM-based surface derivatives | Request PDF \- ResearchGate, accessed October 22, 2025, [https://www.researchgate.net/publication/246089014\_Error\_propagation\_of\_DEM-based\_surface\_derivatives](https://www.researchgate.net/publication/246089014_Error_propagation_of_DEM-based_surface_derivatives)  
92. Error propagation analysis in slope estimation by means of Digital Elevation Models, accessed October 22, 2025, [https://www6.uniovi.es/\~feli/SIG/ICA95.html](https://www6.uniovi.es/~feli/SIG/ICA95.html)  
93. (PDF) PROPAGATION OF DEM UNCERTAINTY: AN INTERVAL ..., accessed October 22, 2025, [https://www.researchgate.net/publication/251809223\_PROPAGATION\_OF\_DEM\_UNCERTAINTY\_AN\_INTERVAL\_ARITHMETIC\_APPROACH](https://www.researchgate.net/publication/251809223_PROPAGATION_OF_DEM_UNCERTAINTY_AN_INTERVAL_ARITHMETIC_APPROACH)  
94. Accuracy assessment and error propagation analysis of digital elevation model, accessed October 22, 2025, [https://www.researchgate.net/publication/255665763\_Accuracy\_assessment\_and\_error\_propagation\_analysis\_of\_digital\_elevation\_model](https://www.researchgate.net/publication/255665763_Accuracy_assessment_and_error_propagation_analysis_of_digital_elevation_model)  
95. Parameter Sensitivity Analysis of Stochastic Models Provides Insights into Cardiac Calcium Sparks \- PMC, accessed October 22, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC3870797/](https://pmc.ncbi.nlm.nih.gov/articles/PMC3870797/)  
96. Performing a Sensitivity Analysis UQ Study \- COMSOL, accessed October 22, 2025, [https://www.comsol.com/support/learning-center/article/performing-a-sensitivity-analysis-uq-study-93841/251](https://www.comsol.com/support/learning-center/article/performing-a-sensitivity-analysis-uq-study-93841/251)  
97. Raster processing benchmarks for Python and R packages \- GitHub, accessed October 22, 2025, [https://github.com/kadyb/raster-benchmark](https://github.com/kadyb/raster-benchmark)  
98. Developing the Raster Big Data Benchmark: A Comparison of Raster Analysis on Big Data Platforms \- MDPI, accessed October 22, 2025, [https://www.mdpi.com/2220-9964/9/11/690](https://www.mdpi.com/2220-9964/9/11/690)  
99. The five pillars of computational reproducibility: bioinformatics and beyond \- PMC, accessed October 22, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10591307/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10591307/)  
100. Reproducibility of computational workflows is automated using continuous analysis \- PMC, accessed October 22, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC6103790/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6103790/)  
101. Building a Reproducible ML Pipeline with Docker \+ DVC \+ UV \+ CUDA \- Medium, accessed October 22, 2025, [https://medium.com/@arnaldog12/building-a-reproducible-ml-pipeline-with-docker-dvc-uv-cuda-ac91ec232218](https://medium.com/@arnaldog12/building-a-reproducible-ml-pipeline-with-docker-dvc-uv-cuda-ac91ec232218)  
102. Reproducible Scientific Computing with Docker: A Game-Changer for Research and Data-Driven Products | by Lohitaksh Yogi | Medium, accessed October 22, 2025, [https://medium.com/@lohitakshyogi/reproducible-scientific-computing-with-docker-a-game-changer-for-research-and-data-driven-products-a80c3d8f555e](https://medium.com/@lohitakshyogi/reproducible-scientific-computing-with-docker-a-game-changer-for-research-and-data-driven-products-a80c3d8f555e)  
103. Docker \- Data Version Control · DVC, accessed October 22, 2025, [https://dvc.org/blog/tags/docker](https://dvc.org/blog/tags/docker)  
104. Tutorial: Scalable and Distributed ML Workflows with DVC and Ray ..., accessed October 22, 2025, [https://dvc.org/blog/dvc-ray](https://dvc.org/blog/dvc-ray)  
105. 10\. Introduction to Dask — Advanced Geospatial Analytics with Python, accessed October 22, 2025, [https://hamedalemo.github.io/advanced-geo-python/lectures/dask\_intro.html](https://hamedalemo.github.io/advanced-geo-python/lectures/dask_intro.html)  
106. Dask | Scale the Python tools you love, accessed October 22, 2025, [https://www.dask.org/](https://www.dask.org/)  
107. IJGI | Special Issue : Geomorphometry and Terrain Analysis \- MDPI, accessed October 22, 2025, [https://www.mdpi.com/journal/ijgi/special\_issues/geomorphometry\_terrain\_analysis](https://www.mdpi.com/journal/ijgi/special_issues/geomorphometry_terrain_analysis)  
108. Geomorphology-oriented digital terrain analysis: Progress and perspectives \- ResearchGate, accessed October 22, 2025, [https://www.researchgate.net/publication/349864072\_Geomorphology-oriented\_digital\_terrain\_analysis\_Progress\_and\_perspectives](https://www.researchgate.net/publication/349864072_Geomorphology-oriented_digital_terrain_analysis_Progress_and_perspectives)  
109. Geomorphometry: Today and Tomorrow \- PeerJ, accessed October 22, 2025, [https://peerj.com/preprints/27197.pdf](https://peerj.com/preprints/27197.pdf)  
110. Recent Advances and Challenges in Geomorphometry | Request PDF \- ResearchGate, accessed October 22, 2025, [https://www.researchgate.net/publication/353476111\_Recent\_Advances\_and\_Challenges\_in\_Geomorphometry](https://www.researchgate.net/publication/353476111_Recent_Advances_and_Challenges_in_Geomorphometry)  
111. Geomorphometry and terrain analysis: data, methods, platforms and applications, accessed October 22, 2025, [https://uni-salzburg.elsevierpure.com/en/publications/geomorphometry-and-terrain-analysis-data-methods-platforms-and-ap](https://uni-salzburg.elsevierpure.com/en/publications/geomorphometry-and-terrain-analysis-data-methods-platforms-and-ap)  
112. Digital Soil Mapping: Challenges and Opportunities, accessed October 22, 2025, [https://www.techsciresearch.com/blog/challenges-and-opportunities-in-digital-soil-mapping-an-overview/4558.html](https://www.techsciresearch.com/blog/challenges-and-opportunities-in-digital-soil-mapping-an-overview/4558.html)  
113. Full article: Digital soil mapping based on the similarity of geographic environment over spatial neighborhoods \- Taylor & Francis Online, accessed October 22, 2025, [https://www.tandfonline.com/doi/full/10.1080/17538947.2025.2471507?af=R](https://www.tandfonline.com/doi/full/10.1080/17538947.2025.2471507?af=R)  
114. Proximal and remote sensing – what makes the best farm digital soil maps?, accessed October 22, 2025, [https://www.publish.csiro.au/SR/SR23112](https://www.publish.csiro.au/SR/SR23112)  
115. Step 5: Risk management in projects \- Karlstads universitet, accessed October 22, 2025, [https://www.kau.se/en/research-support-handbook/step-5-manage-your-award/upon-approval-research-project/step-5-risk](https://www.kau.se/en/research-support-handbook/step-5-manage-your-award/upon-approval-research-project/step-5-risk)