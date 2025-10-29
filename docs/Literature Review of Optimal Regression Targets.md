# Optimal Regression Targets for TDA-Based Terrain Analysis in Georgia

Topological Data Analysis (TDA) applied to 10m DEMs offers powerful alternatives to erosion prediction for classifying geological provinces in Georgia. This research identifies **seven viable regression targets** that combine scientific rigor, computational tractability, and available validation data—all while leveraging the unique capabilities of persistent homology to extract terrain features that traditional methods miss.

## Top-ranked regression target candidates

### 1. Landslide susceptibility mapping (Highest recommendation)

**Scientific value**: Landslide susceptibility represents the **premier application** for TDA-based terrain analysis. Recent breakthrough research (Bhuyan et al., 2024, *Nature Communications*) achieved 80-94% accuracy classifying landslide movement types using topological features—dramatically outperforming traditional geometric methods (94% vs 65%). The USGS recently completed continental-scale susceptibility mapping using 613,724 landslide locations, establishing this as a national priority for natural hazard mitigation.

**Topological feature relationships**: The connection between persistent homology and landslide physics is exceptionally strong. Six key topological properties capture critical failure characteristics: **Average Lifetime of Holes (ALH)** measures material compactness (slides maintain cohesive structure with longer ALH; flows fragment with shorter ALH); **Bottleneck Amplitude of Holes (BAH)** combined with ALH quantifies sinuosity (flows follow channelized topography creating multiple small voids; slides move straight with fewer large holes); **Average Lifetime of Connected Components (ALC)** captures slope variation (sharp transitions in falls/slides yield longer lifetimes; constant slopes in flows yield shorter lifetimes). These topological features encode the three-dimensional geometry, depth, and kinematic progression that 2D geometric properties cannot capture.

**Computational tractability**: Proven tractable at CONUS scale. Machine learning models (CNN-DNN, Random Forest, XGBoost) process 30m DEMs efficiently, with 90m resolution acceptable for continental analysis. GPU resources enable 10m DEM processing for regional studies. The USGS implementation demonstrates operational feasibility. Computational complexity is manageable using cubical complexes for gridded elevation data, with 0- and 1-dimensional persistent homology computed in near-linear time.

**Data availability on Microsoft Planetary Computer**: While landslide inventories aren't directly available on Planetary Computer, the **USGS National Landslide Inventory** (600,000+ events) provides comprehensive ground truth accessible through separate channels. Supporting datasets on Planetary Computer include: **Copernicus DEM** (30m) for validation, **Sentinel-2** imagery (10m) for change detection, **USGS LCMAP** land cover (30m) as predictor variables, and **gridMET** climate data (4km daily) for precipitation triggering analysis.

**Geographic variation across Georgia provinces**: Landslide susceptibility varies dramatically across Georgia's physiographic regions. The **Blue Ridge** province (elevations 1,600-4,784 ft, slopes >30°) has highest susceptibility with steep crystalline bedrock, deep saprolite, and extreme relief. The **Valley and Ridge** (folded sedimentary rocks, 700-1,600 ft elevation) shows moderate susceptibility controlled by structure and differential weathering. The **Piedmont** (500-1,700 ft, moderate slopes 5-15°) experiences sheet failures in thick saprolite when vegetation removed. The flat **Coastal Plain** (<2° slopes, unconsolidated sediments) has minimal landslide risk. This province-scale variation makes landslide susceptibility ideal for demonstrating topological classification capabilities.

**Pros**: Exceptional societal impact (saves lives and infrastructure); breakthrough TDA research demonstrates method viability; aligns with NSF natural hazards priorities; excellent publication potential in *Landslides*, *Engineering Geology*, *Natural Hazards*, *Nature Scientific Reports*; validation data comprehensive; strong mechanistic physics basis connecting topology to failure mechanics; proven at continental scale.

**Cons**: Requires accessing USGS landslide inventory (not on Planetary Computer); may need regional inventories for Georgia-specific validation; temporally discrete events rather than continuous predictions; requires careful attention to landslide detection completeness and bias.

**Publishability**: Exceptional. Novel application of persistent homology to Georgian provinces, comparison of topological versus geometric features, testing scale dependencies from 10m to 90m DEMs, and validation against independent inventories all offer strong publication pathways for undergraduate research.

---

### 2. Soil moisture distribution patterns (Excellent alternative)

**Scientific value**: Soil moisture is critical for drought forecasting, agricultural planning, ecosystem function, carbon cycling, and water resource management. Topographic controls on moisture distribution are well-established, making this an ideal target for demonstrating how terrain topology governs hydrological processes. Recent implementations achieved R² values of 0.69-0.78 using machine learning with terrain indices, with Swedish national forest mapping reaching 2m resolution across entire landscapes.

**Topological feature relationships**: Persistent homology captures moisture-relevant terrain features through convergence analysis. **0-dimensional homology** (connected components) identifies discrete accumulation basins where water collects. **1-dimensional homology** (loops/holes) reveals enclosed depressions that retain moisture and influence local water tables. Persistence values encode the depth and prominence of these features—longer persistence indicates significant, stable moisture accumulation zones; shorter persistence reflects transient, minor features. **Betti curves** track how moisture-relevant features appear and disappear across elevation thresholds, directly relating to saturation dynamics. Traditional metrics like Topographic Wetness Index (TWI) and Depth-to-Water (DTW) can be enriched with topological features capturing multi-scale convergence patterns.

**Computational tractability**: Highly tractable at CONUS scale. Well-established algorithms and indices (TWI, DTW) provide baseline methods, while TDA adds novel persistent convergence features. The Depth-to-Water model shows superior performance with Kmatch90 values of 7.8% for LiDAR DEMs. Machine learning frameworks (Random Forest, XGBoost) integrate topological features efficiently. Processing 10m DEMs across Georgia's ~60,000 square miles is feasible with available GPU resources.

**Data availability on Microsoft Planetary Computer**: **Excellent**. Direct validation possible using **SMAP satellite** soil moisture products (though 9-10km resolution). Supporting datasets include: **gNATSGO** soil properties (30m) providing soil texture, available water capacity, drainage class, and hydrologic group; **TerraClimate** (4km monthly) with soil moisture and actual evapotranspiration from 1958-2021; **gridMET** (4km daily) with precipitation, evapotranspiration, and vapor pressure deficit; **io-lulc** land cover (10m annual 2017-2022) affecting infiltration; **Sentinel-2** (10m) for deriving vegetation indices (NDVI, NDWI) related to moisture.

**Geographic variation across Georgia provinces**: Soil moisture patterns vary distinctly across provinces. The **Blue Ridge** has rapid drainage on steep slopes but persistent moisture in coves and convergent areas. The **Piedmont** shows moderate retention controlled by topographic position, with clay-rich soils (6-15 cm/h infiltration) creating perched water tables in convergent areas. The **Coastal Plain** exhibits high infiltration (13-28 cm/h) in sandy soils with moisture controlled by water table depth rather than surface topography. The **Valley and Ridge** has complex patterns with limestone valleys retaining moisture through karst systems while sandstone ridges drain rapidly. This variation enables testing topological moisture prediction across dramatically different hydrogeologic settings.

**Pros**: Satellite validation eliminates field campaign requirements; critical for multiple applications; clear mechanistic connection between topology and moisture; strong seasonal dynamics add temporal dimension; aligns with NSF water sustainability priorities; proven at national scales; excellent for demonstrating topological reasoning about flow accumulation and convergence; can show results visually through moisture maps.

**Cons**: SMAP satellite data coarser (9-10km) than 10m DEM requires careful upscaling/downscaling strategy; temporal validation needed across seasons; may require some ground truth sensors for fine-scale validation; integration with precipitation data essential for full model.

**Publishability**: High. Papers in *Water Resources Research*, *Hydrological Processes*, *Journal of Hydrology* frequently publish terrain-moisture studies. Novel angle: applying persistent homology to capture multi-scale convergence patterns that traditional TWI misses, demonstrating superior performance for predicting fine-scale moisture variation.

---

### 3. Above-ground biomass estimation (Strong carbon focus)

**Scientific value**: Above-ground biomass (AGB) estimation is fundamental for carbon accounting, climate change mitigation commitments (Paris Agreement), forest management, and ecosystem services valuation. National and continental-scale implementations using machine learning achieve R² = 0.77-0.81 (RMSE = 14-23%), establishing feasibility and scientific importance. Carbon stored in living vegetation represents a major climate feedback, making accurate spatial prediction essential.

**Topological feature relationships**: Terrain topology influences biomass through multiple pathways that persistent homology can capture. **Elevation** controls temperature and growing season length, with topological features identifying distinct elevation zones and ecotones. **Aspect** (captured through directional persistence) affects solar radiation and moisture availability—north-facing slopes in Georgia mountains support richer mesophytic forests while south-facing slopes have xeric communities. **Topographic position** (positive persistence = ridges, negative = valleys) correlates with site productivity, with convergent areas accumulating nutrients and water supporting higher biomass. **Terrain roughness** from persistence measures relates to disturbance history and forest age structure. The multi-scale nature of persistent homology matches the hierarchical organization of forests, from individual tree gaps to landscape-scale elevation gradients.

**Computational tractability**: Successfully implemented at national/continental scales using 30m resolution (aligned with Landsat). Machine learning (Random Forest, XGBoost) integrates terrain features with multispectral indices efficiently. GPU resources enable processing 10m Sentinel-2 data for finer-scale analysis. Combining TDA features from DEMs with vegetation indices from imagery creates powerful predictor sets.

**Data availability on Microsoft Planetary Computer**: **Good to Excellent**. **Sentinel-2 Level-2A** (10m resolution, 2015-present) provides multispectral bands for calculating NDVI, EVI, and other vegetation indices that correlate with biomass. **Landsat Collection 2 Level-2** (30m, 1972-present) offers historical context. **HLS** (Harmonized Landsat Sentinel-2, 30m) increases temporal frequency. **io-lulc** (10m annual) provides forest classification. Validation requires National Forest Inventory data and GEDI LiDAR data (not on Planetary Computer but freely available). Field plots from University of Georgia research forests could provide additional ground truth.

**Geographic variation across Georgia provinces**: Biomass varies dramatically across provinces. **Blue Ridge** supports highest biomass (~200-400 Mg/ha) in mesophytic cove forests on north-facing slopes at mid-elevations, with lower biomass on exposed ridges and south-facing xeric slopes. **Piedmont** has moderate biomass (100-250 Mg/ha) with pine-hardwood mixtures, influenced by land use history and topographic moisture gradients. **Coastal Plain** shows lower biomass (50-150 Mg/ha) in pine flatwoods and sand hills, with higher biomass (150-300 Mg/ha) in bottomland hardwood swamps controlled by water table position. **Valley and Ridge** has intermediate biomass with oak-hickory forests on ridges and richer forests in limestone valleys. This creates distinct biomass-topological feature relationships across provinces.

**Pros**: Aligns strongly with climate mitigation priorities; multiple data sources available; proven ML performance; strong publication venues (*Remote Sensing*, *Forest Ecology and Management*, *Carbon Balance*); clear practical applications (carbon markets, forest management); combines remote sensing and terrain analysis demonstrating technical breadth; NSF carbon cycle priority area.

**Cons**: Best performance requires combining DEM features with multispectral imagery (not just terrain); validation requires accessing National Forest Inventory or field data; forest structure complexity may require lidar validation; temporal snapshots rather than dynamic predictions.

**Publishability**: High. Novel contributions: applying persistent homology to capture terrain features controlling forest productivity; comparing performance across geological provinces with different substrate; testing whether topological features improve upon traditional terrain metrics; demonstrating scale-dependent relationships between terrain and biomass.

---

### 4. Soil organic carbon (SOC) storage prediction (Climate-critical)

**Scientific value**: Soil organic carbon constitutes a massive component of the global carbon cycle (approximately 2,500 gigatons—more than atmospheric and vegetation carbon combined), making accurate spatial prediction essential for climate modeling, agricultural productivity assessment, and carbon sequestration potential evaluation. Topographic controls on SOC storage are pronounced in complex terrain, with documented aspect-driven temperature differences of 5°C creating 2x differences in SOC stocks—north-facing slopes containing 50% of catchment SOC in just 38% of area in some studies.

**Topological feature relationships**: Persistent homology captures SOC-relevant terrain processes through multiple mechanisms. **Curvature** (from persistent component analysis) identifies erosion (convex) versus deposition (concave) zones—eroded SOC from upslope accumulates in convergent areas detected by 1-dimensional homology. **Aspect persistence** encodes solar radiation and temperature differences controlling decomposition rates (5°C temperature differences documented between north/south slopes). **Elevation features** relate to temperature and decomposition kinetics. **Topographic position** (from 0-dimensional persistence) identifies whether locations are sources (ridges, high persistence) or sinks (valleys, enclosed basins) for organic matter. **Slope length and steepness** encoded in persistence diagrams relate to residence time and transport distance. The multi-scale nature of TDA captures both fine-scale microtopography creating "microrefugia" with enhanced SOC storage and landscape-scale patterns.

**Computational tractability**: Achievable at regional to national scales. Machine learning (Random Forest, SVM, Neural Networks) achieves R² = 0.58-0.81, with complex terrain actually increasing both prediction challenge and scientific interest. 30-100m resolution typical, making 10m DEM analysis computationally feasible with GPU resources. Some computational expense in soil sampling and laboratory analysis for validation, but prediction mapping is efficient.

**Data availability on Microsoft Planetary Computer**: **Moderate**. **gNATSGO** (gridded National Soil Survey Geographic Database, 30m) provides soil organic matter content, which correlates with SOC. However, detailed SOC measurements require accessing USDA soil survey databases and research soil samples. Supporting predictors available: **Copernicus DEM** (30m), **Sentinel-2/Landsat** for vegetation indices correlating with productivity and SOC inputs, **TerraClimate/gridMET** for temperature and moisture controlling decomposition, **io-lulc** land cover affecting SOC management, **USGS LCMAP** for land use change history (agriculture to forest transitions).

**Geographic variation across Georgia provinces**: SOC storage patterns vary strongly across provinces. **Blue Ridge** has moderate SOC (2-6% in forest soils) with strong aspect control—north-facing slopes accumulate more due to cooler, moister conditions and slower decomposition. **Piedmont** shows variable SOC (1-4%) with historical agriculture depleting stocks; convergent landscape positions show enhanced accumulation from erosion upslope. The thick saprolite layer (10-30 feet) may store significant subsurface carbon. **Coastal Plain** has highly variable SOC: low in upland sandy soils (0.5-2%) but extremely high in organic swamp soils (10-30%) in Okefenokee Basin and river bottomlands where saturated conditions preserve organic matter. **Valley and Ridge** shows structural control with limestone soils having different SOC dynamics than sandstone-derived soils. This dramatic variation across provinces enables testing topological SOC prediction in contrasting settings.

**Pros**: Critical for climate modeling and carbon cycle science; strong topographic controls documented with clear mechanisms; NSF carbon priorities; good publication potential (*Geoderma*, *Soil Science*, *Biogeosciences*); aspect effects well-established providing mechanistic validation; demonstrates terrain-process relationships; combines with land use history for enhanced understanding.

**Cons**: Requires soil sampling for ground truth validation (lab analysis expensive and time-consuming); spatial sampling density limited by field access and cost; temporal dynamics slower than other targets (decades to centuries); gNATSGO provides organic matter but detailed SOC requires additional data; subsurface storage in saprolite difficult to measure.

**Publishability**: High. Novel angles: applying TDA to capture erosion-deposition patterns controlling SOC redistribution; testing aspect-controlled temperature effects on SOC in Appalachian terrain; comparing saprolite carbon in Piedmont versus surface SOC in Coastal Plain; demonstrating topological features outperform simple slope/aspect for SOC prediction.

---

### 5. Wetland classification and hydrological features (Excellent TDA match)

**Scientific value**: Wetlands provide critical ecosystem services including flood mitigation, water quality improvement, carbon storage, and biodiversity habitat. Wetland location and type are strongly controlled by topographic position, making this an ideal application for demonstrating how persistent homology identifies hydrologically-relevant landscape features. With 35+ million mapped wetland features nationally, this represents a massive dataset for training and validation.

**Topological feature relationships**: This target offers the **most intuitive connection** between persistent homology and landscape function. **1-dimensional homology** (loops/holes) literally identifies enclosed depressions where wetlands form—persistence values encode depression depth and water storage capacity. **0-dimensional homology** tracks connectivity of wetland complexes. Wetlands occur in **"persistent" topographic lows** that retain water—the longer a depression persists in the filtration (larger birth-death difference), the more significant the wetland-forming potential. **Betti curves** showing when depressions appear and merge directly relate to filling and spilling dynamics in wetland hydrology. This creates an almost perfect match between TDA mathematics and wetland geomorphology.

**Computational tractability**: Highly tractable. Wetland prediction from DEMs is well-established using depression analysis, TWI, and terrain convergence. TDA adds rigorous mathematical framework for depression detection through persistent homology of sublevel sets. Vector wetland data can be converted to raster for comparison. Machine learning classification of wetland presence/type is computationally efficient.

**Data availability on Microsoft Planetary Computer**: **Excellent**. **FWS National Wetlands Inventory (NWI)** is directly available as GeoParquet vector data with 35+ million features covering Georgia completely. This provides comprehensive ground truth for wetland location and Cowardin classification types. Supporting data: **gNATSGO** hydrologic soil group and drainage class (30m), **TerraClimate** soil moisture and water balance (4km monthly), **Sentinel-2** for NDWI and wetland vegetation indices (10m), **io-lulc** includes flooded vegetation and water classes (10m), **Landsat/USGS LCMAP** for temporal wetland dynamics.

**Geographic variation across Georgia provinces**: Wetland types vary dramatically by province. **Coastal Plain** dominates wetland area with extensive cypress-tupelo swamps, bottomland hardwoods along rivers, Carolina bays (elliptical depressions), and the massive Okefenokee Swamp (persistent topographic low of enormous extent). **Piedmont** has fewer wetlands—mainly riparian zones along streams and occasional headwater seeps in convergent areas. **Blue Ridge** supports montane wetlands in coves and valley bottoms, often spring-fed. **Valley and Ridge** has karst-influenced wetlands in limestone areas where groundwater emerges. **Appalachian Plateau** has limited area but plateau-top wetlands in flat areas. This province-specific variation enables testing topological wetland prediction across dramatically different hydrogeomorphic settings.

**Pros**: Nearly perfect match between TDA mathematics and target phenomenon (depressions = 1D homology); comprehensive validation data directly available on Planetary Computer; intuitive for explaining TDA to broader audiences; excellent visualization opportunities; multiple wetland types for classification; aligns with water resources and ecosystem priorities; computationally straightforward; demonstrates practical conservation applications.

**Cons**: Relatively "solved" problem using traditional depression analysis (less novel scientifically); wetland dynamics include vegetation and hydrology beyond just topography; NWI mapping quality varies by region and date; may be too straightforward for demonstrating full TDA capabilities; publication in wetland-specific journals rather than top-tier methodological venues.

**Publishability**: Moderate to high. Best framed as methodological contribution showing persistent homology provides superior depression characterization versus traditional methods. Potential venues: *Wetlands*, *Hydrological Processes*, *Remote Sensing*. Novel angle: multi-scale persistence analysis capturing nested wetland complexes; comparing performance across provinces; predicting wetland type (not just presence) from topological signatures.

---

### 6. Near-surface microclimate (temperature) patterns (High science interest)

**Scientific value**: Fine-scale temperature variation in complex terrain creates climate refugia critical for species persistence under climate change. Recent research documents 2-4°C temperature differences over <1000m distances in mountainous areas—often exceeding projected broad-scale climate warming. These "microclimatic buffering" zones may enable species survival. This represents cutting-edge research in conservation biogeography and climate adaptation science, with recent papers in *Science Advances* and *Global Change Biology* demonstrating high scientific interest.

**Topological feature relationships**: Persistent homology captures microclimate-controlling terrain features through several pathways. **Depression detection** (1D homology) identifies cold air pooling zones where dense cold air drains and accumulates at night, creating temperature inversions with valley bottoms 2-5°C cooler than slopes. **Topographic position** (0D homology persistence) distinguishes valley bottoms (cold, stable air masses), mid-slopes (transitional), and ridgetops (exposed to free atmosphere). **Aspect persistence** encodes solar radiation differences creating steep north-south temperature gradients. **Topographic convergence** identified by persistent features relates to air drainage patterns and frost pocket formation. **Sky view factor** (calculable from DEM) relates to radiative cooling rates. Multi-scale persistence analysis captures both fine-scale microtopography (<100m) creating local cold pockets and landscape-scale elevation gradients.

**Computational tractability**: Achievable at fine scales (1-30m) where microclimate variations are strongest. Computational tools available (NicheMapR, microclima R packages) provide frameworks. Can downscale coarse climate data (gridMET 4km) to terrain-corrected predictions. Machine learning regression using terrain features achieves good performance where sensor networks exist. Processing 10m DEMs across study areas is feasible.

**Data availability on Microsoft Planetary Computer**: **Moderate**. Coarse climate data available: **gridMET** (4km daily temperature, 1979-present), **TerraClimate** (4km monthly temperature, 1958-2021), **NOAA NClimGrid** (5km monthly). However, fine-scale validation requires dense temperature sensor networks not available on Planetary Computer. Some temperature sensors in research networks (AmeriFlux, NEON sites) could provide validation. Supporting data: **Copernicus DEM** (30m), **Sentinel-2** for land surface temperature and NDVI affecting energy balance, **io-lulc** land cover affecting surface temperatures.

**Geographic variation across Georgia provinces**: Microclimate buffering varies strongly by terrain complexity. **Blue Ridge** exhibits strongest effects with deep coves maintaining cool, moist conditions 2-4°C cooler than exposed ridges—creating climate refugia for cold-adapted species. Valley bottoms show strong nighttime inversions. **Piedmont** has moderate microclimate variation in dissected terrain with north-facing slopes cooler and moister. **Coastal Plain** has minimal topographic relief so microclimate effects weak, dominated by land cover rather than terrain. **Valley and Ridge** shows complex patterns with valleys experiencing cold air drainage and ridges more exposed. This variation enables testing whether topological complexity metrics predict microclimate buffering strength.

**Pros**: Cutting-edge research area with recent high-impact publications; strong climate adaptation relevance; clear mechanistic connections between topology and temperature; NSF climate priorities; excellent visualization of persistent cold air pools; demonstrates practical conservation applications (climate refugia mapping); relatively novel application of TDA; strong graduate school signal showing interdisciplinary thinking.

**Cons**: Requires deploying temperature sensor networks for validation (expensive, time-intensive); coarse-resolution climate data on Planetary Computer requires downscaling; temporal dynamics complex with daily and seasonal cycles; may require field campaign for undergraduate project; less established literature base than other targets; prediction accuracy depends on local weather station density.

**Publishability**: High for methodologically strong work. Target venues: *Global Change Biology*, *Ecological Applications*, *Methods in Ecology and Evolution*, *Journal of Applied Ecology*. Novel contribution: demonstrating persistent homology captures cold air pooling better than traditional indices; quantifying topological complexity as predictor of microclimate buffering; mapping climate refugia across Georgia provinces.

---

### 7. Stream network extraction and watershed characteristics (Solid baseline)

**Scientific value**: Accurate stream network delineation from DEMs is fundamental for hydrological modeling, water resource management, and flood forecasting. Watershed characteristics derived from terrain (area, slope, shape, relief) are primary predictors in numerous environmental models. While well-established scientifically, this represents a proven application where TDA could provide methodological improvements.

**Topological feature relationships**: Stream networks are fundamentally topological structures that persistent homology can characterize rigorously. **0-dimensional homology** tracks connected components (individual watershed basins), while **1-dimensional homology** can identify enclosed basins and internal drainage. **Drainage density** relates to the number and persistence of channels in the landscape. **Stream ordering** (Strahler, Shreve) is essentially a topological property encoding network hierarchy. **Pfafstetter numbering** is a topological coding scheme. **Persistence landscapes** could capture multi-scale drainage organization from small tributaries to major rivers. TDA could formalize watershed similarity measures for prediction in ungauged basins (major hydrological challenge).

**Computational tractability**: Highly tractable—stream extraction from DEMs is computationally efficient using flow direction and accumulation algorithms. TDA analysis of extracted networks adds minimal computational overhead. CONUS-scale implementations exist (National Hydrography Dataset). Comparing TDA-derived characteristics with traditional metrics is straightforward.

**Data availability on Microsoft Planetary Computer**: **Good indirectly**. Stream networks themselves not directly available, but can be derived from DEMs. **USGS stream gauge** locations and discharge data available through separate USGS APIs (10,000+ gauges nationally). Supporting data on Planetary Computer: **Copernicus DEM** (30m), **gridMET/TerraClimate** precipitation for rainfall-runoff modeling, **gNATSGO** soil infiltration and hydrologic group affecting runoff, **io-lulc** land cover affecting runoff coefficients.

**Geographic variation across Georgia provinces**: Stream characteristics vary across provinces. **Blue Ridge** has high drainage density, steep gradients, V-shaped valleys, and flashy hydrographs. **Piedmont** shows moderate drainage density with shallow rocky channels and rapids. **Coastal Plain** has low gradients, meandering channels, wide floodplains, and slow response times. **Valley and Ridge** shows structural control with rectangular drainage patterns. Stream networks thus reflect underlying geology and topography distinctly across provinces.

**Pros**: Well-established scientific basis; operational models exist (TOPMODEL, National Water Model); excellent validation data from stream gauges; clear practical applications; computationally straightforward; watershed similarity analysis could be novel TDA contribution; demonstrates hydrological understanding; aligns with NSF water priorities.

**Cons**: Somewhat incremental advance over established methods (less novel); stream extraction already very effective with traditional algorithms; TDA contribution may be seen as marginal improvement; publication venues may view as methodological refinement rather than breakthrough; may be perceived as less ambitious for undergraduate research; extensive existing literature makes novelty challenging.

**Publishability**: Moderate. Best positioned as methodological comparison showing TDA provides improved watershed similarity measures or enhanced network characterization. Potential venues: *Water Resources Research*, *Journal of Hydrology*, *Hydrological Processes*. Most impact if demonstrating TDA enables better prediction in ungauged basins or captures watershed functional similarity missed by traditional metrics.

---

## Summary comparison table

| Target | Scientific Impact | Computational Feasibility | Data Availability (MPC) | Publishability | Province Variation | TDA Feature Match | Overall Rank |
|--------|------------------|---------------------------|------------------------|---------------|-------------------|------------------|--------------|
| **Landslide Susceptibility** | ⭐⭐⭐⭐⭐ Exceptional | ⭐⭐⭐⭐⭐ Proven CONUS-scale | ⭐⭐⭐⭐ Good (USGS inventory separate) | ⭐⭐⭐⭐⭐ Nature, top journals | ⭐⭐⭐⭐⭐ Dramatic | ⭐⭐⭐⭐⭐ Breakthrough demos | **#1** |
| **Soil Moisture** | ⭐⭐⭐⭐⭐ Critical applications | ⭐⭐⭐⭐⭐ Well-established | ⭐⭐⭐⭐⭐ Excellent (SMAP, gNATSGO) | ⭐⭐⭐⭐ Strong venues | ⭐⭐⭐⭐⭐ Strong variation | ⭐⭐⭐⭐⭐ Intuitive convergence | **#2** |
| **Above-Ground Biomass** | ⭐⭐⭐⭐⭐ Carbon/climate | ⭐⭐⭐⭐ Proven national scale | ⭐⭐⭐⭐ Good (needs GEDI too) | ⭐⭐⭐⭐ Strong venues | ⭐⭐⭐⭐⭐ Strong variation | ⭐⭐⭐⭐ Multi-pathway | **#3** |
| **Soil Organic Carbon** | ⭐⭐⭐⭐⭐ Carbon/climate | ⭐⭐⭐⭐ Regional scale proven | ⭐⭐⭐ Moderate (needs soil samples) | ⭐⭐⭐⭐ Good venues | ⭐⭐⭐⭐⭐ Dramatic (aspect) | ⭐⭐⭐⭐ Erosion/deposition | **#4** |
| **Wetland Features** | ⭐⭐⭐⭐ Ecosystem services | ⭐⭐⭐⭐⭐ Highly tractable | ⭐⭐⭐⭐⭐ Excellent (NWI direct) | ⭐⭐⭐ Moderate venues | ⭐⭐⭐⭐⭐ Type variation | ⭐⭐⭐⭐⭐ Perfect (depressions) | **#5** |
| **Microclimate Temperature** | ⭐⭐⭐⭐⭐ Climate refugia | ⭐⭐⭐ Sensor networks needed | ⭐⭐⭐ Moderate (coarse climate) | ⭐⭐⭐⭐⭐ Top ecology journals | ⭐⭐⭐⭐⭐ Strong (Blue Ridge) | ⭐⭐⭐⭐ Cold air pools | **#6** |
| **Stream Networks** | ⭐⭐⭐⭐ Water resources | ⭐⭐⭐⭐⭐ Highly tractable | ⭐⭐⭐⭐ Good (derived + gauges) | ⭐⭐⭐ Incremental advance | ⭐⭐⭐⭐ Drainage patterns | ⭐⭐⭐ Topological structure | **#7** |

**Rating scale**: ⭐⭐⭐⭐⭐ Exceptional, ⭐⭐⭐⭐ Strong, ⭐⭐⭐ Moderate, ⭐⭐ Limited, ⭐ Weak

## Recommended project approach

**Primary recommendation**: Start with **landslide susceptibility** as the main regression target, with **soil moisture** as a strong secondary option if field validation proves challenging.

**Project workflow**:

1. **Acquire 10m DEMs** from USGS 3DEP for Georgia's physiographic provinces (focus on Blue Ridge, Valley & Ridge, Piedmont, Coastal Plain boundaries)

2. **Compute persistent homology** using:
   - GUDHI or Giotto-TDA (Python) for accessibility and ML integration
   - Cubical complexes (most efficient for gridded DEMs)
   - 0- and 1-dimensional homology (computationally feasible, physically interpretable)
   - Extract 6 key features: ALH, ALC, BCC, BCH, WAH, BAH (from Bhuyan et al., 2024)

3. **Extract traditional terrain features** for comparison:
   - Slope, aspect, curvature, elevation
   - TWI, TPI, TRI, roughness
   - Flow accumulation, drainage density
   - Multi-scale analysis (30m, 100m, 500m windows)

4. **Access validation data**:
   - **Primary**: USGS National Landslide Inventory for locations in Georgia
   - **Secondary**: Microsoft Planetary Computer for soil properties (gNATSGO), wetlands (NWI), land cover (io-lulc)
   - **Supporting**: Climate data (gridMET) for precipitation triggers

5. **Train ML models**:
   - Random Forest (most robust, interpretable)
   - XGBoost (often highest performance)
   - Compare: TDA features only, traditional features only, combined
   - Use SHAP values to interpret feature importance
   - Implement spatial cross-validation (avoid spatial autocorrelation bias)

6. **Test across provinces**:
   - Train on Blue Ridge, test on Piedmont (transfer learning)
   - Analyze which topological features most distinguish provinces
   - Quantify how prediction accuracy varies by geological setting

7. **Scale analysis**:
   - Compare 10m, 30m, 90m DEMs
   - Test multi-resolution persistent homology
   - Determine optimal scale for each province type

**Expected contributions**: Novel application of persistent homology to Appalachian physiographic provinces; demonstration that topological features outperform traditional geometric metrics for landslide classification; quantification of scale-dependent relationships; and transferability analysis across geological settings—all publishable as undergraduate research in *Natural Hazards*, *Landslides*, or *Earth Surface Processes and Landforms*.

**Timeline feasibility**: A focused one-year undergraduate project could reasonably complete: DEM acquisition and preprocessing (1 month), persistent homology computation (1-2 months learning + computation), landslide inventory compilation (1 month), ML model training and validation (2 months), cross-province analysis (1 month), manuscript preparation (2-3 months)—leaving buffer for challenges and revisions.

This approach combines cutting-edge methodology (TDA), critical societal application (landslide hazards), excellent data availability, proven computational tractability, and strong alignment with current NSF priorities for natural hazards and climate resilience—positioning the student exceptionally well for geography PhD applications focused on climate, geomorphology, or computational geography.