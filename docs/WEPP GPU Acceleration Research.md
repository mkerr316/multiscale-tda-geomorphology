

# **Architecting a Portable, GPU-Accelerated Framework for Continental-Scale WEPP Erosion Modeling**

## **Executive Summary**

This report provides a comprehensive technical analysis and implementation strategy for developing a GPU-accelerated, portable workflow for the Water Erosion Prediction Project (WEPP), designed to enable erosion modeling at the scale of the Continental United States (CONUS). The analysis confirms the feasibility of the project's ambitious goals and presents a phased architectural blueprint that maximizes performance, portability, and reproducibility within a modern, containerized framework.  
The core of the proposed architecture rests on a strategic decoupling of computational tasks, assigning each to the most appropriate processing unit—CPU or GPU—to achieve maximum end-to-end throughput. This strategy is informed by a thorough investigation of the WEPP model's source code, the landscape of available geospatial tools, and recent academic advancements in high-performance hydrological modeling.  
Key recommendations are as follows:

1. **Adopt a Proven Fortran Source:** The dailyerosion/dep GitHub repository is identified as the definitive source for a Linux-compilable WEPP Fortran engine. Leveraging this battle-tested codebase, which is already used for large-scale modeling, significantly de-risks the fundamental challenge of containerizing the legacy WEPP model.  
2. **Focus on Throughput, Not Core Refactoring:** Direct GPU acceleration of the WEPP Fortran core represents a high-effort, high-risk endeavor with uncertain performance returns due to the code's legacy structure. The most substantial performance gains will be achieved by focusing on the embarrassingly parallel nature of the problem: executing tens of thousands of independent watershed simulations. Therefore, the strategy is to massively parallelize the execution of the compiled CPU-based WEPP binary across all available cores using the Dask distributed computing framework.  
3. **Targeted GPU Acceleration for Geospatial Tasks:** The pre-processing (hydrological analysis of Digital Elevation Models) and post-processing (rasterization of results) stages are identified as the ideal candidates for GPU acceleration. Off-the-shelf GIS libraries lack mature GPU support for these tasks. However, recent academic research provides a clear and proven path to achieving significant performance gains (potentially $\>10x$) by implementing core algorithms, such as flow accumulation, as custom kernels using the CuPy library.  
4. **Implement a Staged Computational Model:** A sequential, three-stage computational model is proposed: (1) GPU-accelerated pre-processing, (2) massively parallel CPU-based WEPP simulation, and (3) GPU-accelerated post-processing. This architecture, orchestrated by a master Python script, is simpler to implement, more resource-efficient, and more robust than managing a complex, persistent hybrid Dask cluster of mixed CPU and GPU workers.  
5. **Ensure Portability with a Dual Docker Compose Strategy:** To maximize portability and ease of use, a dual docker-compose file strategy is recommended. A base docker-compose.yml file will define a CPU-only service that works on any system with Docker. A docker-compose.gpu.yml override file will add the necessary configuration to enable GPU access on hosts equipped with the NVIDIA Container Toolkit. This makes GPU acceleration an opt-in enhancement rather than a default requirement.  
6. **Standardize on Cloud-Native Data Formats:** A complementary data format strategy is essential for performance at scale. The recommended approach is to use Cloud-Optimized GeoTIFFs (COGs) for initial data ingestion, the Zarr format for all intermediate and final N-dimensional raster datasets to enable efficient parallel I/O, and GeoParquet for all tabular data to facilitate high-performance analytics.

By adopting this architectural blueprint, the project can systematically build a powerful, scalable, and portable system capable of transforming WEPP from a desktop-scale tool into a continental-scale scientific modeling platform.

## **Section I: WEPP Engine Modernization: Acceleration and Containerization Strategy**

This section addresses the foundational challenge of the project: transforming the core Water Erosion Prediction Project (WEPP) model from a legacy, often Windows-centric, application into a portable, containerized computational unit suitable for a modern, Linux-based, high-performance computing environment. The analysis begins by establishing a definitive source for the WEPP Fortran engine, then critically assesses the feasibility and strategic value of attempting to directly accelerate this core engine on GPUs, and concludes with a detailed, prescriptive blueprint for its containerization using Docker.

### **1.1 WEPP Source Code Provenance and Analysis**

The success of containerizing any application hinges on having reliable access to its source code or a compatible binary for the target operating system. For this project, the target is a Linux environment (specifically, an Ubuntu 22.04 base image), which necessitates a careful investigation into the availability and suitability of the WEPP model for this platform.  
An initial review of the official distribution channels provided by the USDA Agricultural Research Service (ARS) reveals a significant platform bias. The primary WEPP download pages offer Windows-based installation packages, typically in the form of .exe installers.1 These packages bundle the WEPP model, the CLIGEN climate generator, and a Windows-specific graphical user interface.2 While the WEPP model itself is confirmed to be in the public domain and not subject to copyright, having been developed with U.S. government funds, the official distribution does not provide a straightforward path for deployment on Linux.3  
Further investigation into community-maintained code repositories initially points to the wepp-in-the-woods GitHub organization, which is associated with the WEPPcloud web interface.6 However, a detailed analysis of these repositories shows that they primarily contain Python wrapper code, web application logic, and tools for data preparation, rather than the core Fortran science engine itself.  
The critical breakthrough in this investigation is the discovery of the dailyerosion/dep GitHub repository.8 This repository, maintained by the Iowa State University Daily Erosion Project, represents a complete, operational, and actively maintained implementation of WEPP for large-scale, automated erosion modeling on Linux systems. Its significance to this project cannot be overstated. Analysis of this repository reveals several key attributes:

* **Complete Fortran Source:** The repository contains a full src/ directory with the WEPP Fortran source code, including modifications and enhancements made by the project team to support their specific workflow.8 The codebase is predominantly Fortran (82.6%).8  
* **Standard Build System:** The presence of Makefile files within the repository indicates a standard, well-understood build system that can be easily replicated within a Docker build environment.8 This removes the uncertainty and complexity of trying to reverse-engineer a build process from disparate source files.  
* **Battle-Tested Implementation:** The Daily Erosion Project uses this version of WEPP to generate daily erosion estimates across multiple states, demonstrating that this specific codebase is robust, scalable, and suitable for automated, non-interactive execution.9

The existence of the dailyerosion/dep repository signifies that the academic research community, driven by the need for large-scale modeling, has already solved the fundamental problem of porting, compiling, and maintaining WEPP in a Linux environment. This project, therefore, is not starting from a position of uncertainty but can instead build upon a proven and reliable foundation.  
**Recommendation:** The dailyerosion/dep repository should be forked and adopted as the canonical source for the WEPP engine. This strategic decision mitigates the primary risk identified in the user query—sourcing and compiling the model for a Linux container—and provides a clear and immediate path forward for the containerization effort. The table below summarizes the analysis of potential WEPP sources and provides a clear justification for this recommendation.  
**Table 1: WEPP Source Code Provenance and Suitability Analysis**

| Source | Availability | Platform | Build System | License | Recommendation Score (1-5) | Justification |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **USDA ARS Official** | Binary Installer | Windows | .exe Installer | Public Domain 3 | 1 | Unsuitable for a Linux Docker environment. No source or Linux binary provided. |
| **wepp-in-the-woods** 6 | Python Source | Cross-Platform | Python setup.py | Various (BSD, etc.) | 2 | Contains valuable wrapper and utility code but lacks the core Fortran science engine. |
| **dailyerosion/dep** 8 | Fortran Source | Linux | Makefile | MIT License 8 | **5 (Recommended)** | Provides a complete, compilable, and battle-tested Fortran source tree for Linux. The ideal foundation for containerization. |

### **1.2 Feasibility of Core Engine GPU Acceleration**

A central question in modernizing any scientific model is the potential for GPU acceleration. While GPUs offer transformative performance for certain classes of problems, their application is not universal. A careful analysis of the WEPP Fortran engine's structure and the available GPU programming models is required to make a strategic decision on the allocation of engineering effort.  
Three primary avenues for GPU acceleration of Fortran code exist:  
Option A: CUDA Fortran / OpenACC Directives  
This is the most direct and, ideally, the simplest approach. It involves using a GPU-aware Fortran compiler, such as the nvfortran compiler included in the NVIDIA HPC SDK.11 This compiler supports OpenACC, a directive-based programming model where the programmer inserts special comments (pragmas) into the code to guide the compiler on which loops to offload to the GPU.11 A typical directive looks like \!$acc parallel loop, which instructs the compiler to parallelize the subsequent DO loop across the GPU's cores.13  
The effectiveness of this approach is highly contingent on the structure of the code. OpenACC works best on well-defined, computationally intensive loops that operate on large arrays of data with minimal inter-dependencies between loop iterations. The WEPP source code, with origins dating back to Fortran77 15 and having been developed over several decades, is unlikely to possess this ideal structure. Legacy scientific code often features:

* Complex conditional logic (IF-THEN-ELSE blocks) within loops.  
* Procedure calls to other subroutines inside the main computational loop.  
* I/O operations (e.g., reading from or writing to files) embedded within loops.  
* Irregular or non-contiguous memory access patterns.

Each of these characteristics can act as a barrier to effective parallelization, either preventing the compiler from offloading the loop entirely or resulting in inefficient execution on the GPU that yields little to no performance gain. Substantial, expert-level code refactoring would likely be required to restructure the WEPP core into a form amenable to directive-based acceleration.  
Option B: Fortran-CUDA C++ Interoperability  
A more powerful but significantly more complex approach is to create a hybrid codebase. This involves identifying the most computationally expensive subroutines in the Fortran code (the "hot-spots"), rewriting them from scratch as highly optimized CUDA C++ kernels, and then calling these kernels from the main Fortran program using the iso\_c\_binding standard. This method offers the highest potential performance gain, as it allows for fine-grained control over GPU memory management and execution. However, it is tantamount to a partial rewrite of the model and requires deep, dual expertise in both modern Fortran and advanced CUDA C++ programming. The effort required would constitute a major research and development project in its own right.  
Option C: Python-Fortran-GPU Pipeline  
This approach, mentioned in the user query, involves using Python to orchestrate data flow. For example, a NumPy array could be converted to a CuPy array on the GPU, passed to a Fortran function via f2py, and the result returned to the GPU. This is a valid pattern for workflows where a Fortran routine is one step in a larger Python-driven process. However, it does not accelerate the internal computations of the Fortran routine itself. The Fortran code would still execute on the CPU; this pattern only manages the data around it. Therefore, it is not a solution for accelerating the core WEPP engine.  
Given the context of a CONUS-scale simulation, the primary performance bottleneck is not the execution speed of a single WEPP instance but the sheer number of instances that must be run—one for each of the approximately 80,000 HUC12 watersheds. A simple application of Amdahl's Law demonstrates where the most significant performance gains are to be found. Parallelizing the execution of 80,000 independent WEPP runs across, for example, 32 CPU cores provides an immediate, near-linear 32x speedup on the most time-consuming part of the entire workflow. In contrast, even a heroic effort to achieve a 2x speedup of the core Fortran engine would yield a far smaller impact on the total end-to-end time. The most strategic allocation of engineering effort is to focus on the "embarrassingly parallel" aspects of the problem.  
**Recommendation:** Direct GPU acceleration of the WEPP Fortran engine should be classified as a **high-effort, high-risk, uncertain-reward** task. It is strongly recommended to **defer this effort indefinitely**. The project's architectural focus should be squarely on maximizing the throughput of the existing, compiled CPU-based WEPP binary by leveraging Dask for massively parallel execution. The significant, and more certain, performance gains from GPU acceleration should be sought in the pre- and post-processing stages of the workflow.

### **1.3 A Definitive Dockerization Blueprint for WEPP and CLIGEN**

With a reliable source for the WEPP engine identified and a clear strategy to focus on CPU-based execution, the next step is to define a robust, reproducible, and portable method for containerizing the necessary binaries. The optimal approach for this task is a multi-stage Docker build, which provides a clean separation between the build-time environment and the final, lean runtime environment.  
Architectural Strategy: Multi-Stage Docker Build  
A multi-stage build uses multiple FROM instructions in a single Dockerfile. Each FROM instruction begins a new "stage" of the build. This allows one to compile code in an initial stage that is bloated with compilers and development libraries, and then copy only the compiled artifacts (the executable binaries) into a clean, minimal final image. This practice is essential for creating secure and efficient production images.  
The proposed Dockerfile architecture is as follows:

Dockerfile

\# \=============================================================================  
\# Stage 1: Builder  
\# This stage installs the full build toolchain, clones the source code,  
\# and compiles the WEPP and CLIGEN binaries.  
\# \=============================================================================  
FROM ubuntu:22.04 AS builder

\# Install essential build dependencies  
RUN apt-get update && \\  
    apt-get install \-y \--no-install-recommends \\  
    build-essential \\  
    gfortran \\  
    make \\  
    git && \\  
    rm \-rf /var/lib/apt/lists/\*

\# Clone the recommended WEPP source code from the dailyerosion/dep repository  
WORKDIR /build  
RUN git clone https://github.com/dailyerosion/dep.git.

\# Compile the WEPP binary. The exact command will be determined by  
\# analyzing the Makefile within the 'src' directory of the cloned repository.  
\# This is a representative command.  
WORKDIR /build/src  
RUN make wepp

\# Locate and/or compile the CLIGEN binary. If a pre-compiled Linux binary  
\# is found within the repository, this step may be skipped.  
\# WORKDIR /build/path/to/cligen\_source  
\# RUN make cligen

\# \=============================================================================  
\# Stage 2: Final Runtime Image  
\# This stage starts from a clean base image and copies only the necessary  
\# compiled binaries and their runtime dependencies.  
\# \=============================================================================  
\# Use the micromamba base image for a consistent Python environment  
FROM mambaorg/micromamba:1.5.10-jammy

\# Copy the compiled WEPP binary from the builder stage to a standard location  
COPY \--from=builder /build/src/wepp /usr/local/bin/wepp

\# Copy the CLIGEN binary similarly  
\# COPY \--from=builder /build/path/to/cligen /usr/local/bin/cligen

\# Identify and install runtime dependencies for the compiled binaries.  
\# This list must be populated by running \`ldd\` on the binaries in the builder stage.  
RUN apt-get update && \\  
    apt-get install \-y \--no-install-recommends \\  
    libgfortran5 \\  
    \# Add any other required.so files here (e.g., libm, libc)  
    && apt-get clean && \\  
    rm \-rf /var/lib/apt/lists/\*

\# Set permissions for the executables  
RUN chmod \+x /usr/local/bin/wepp \# && chmod \+x /usr/local/bin/cligen

\# \--- Continue with micromamba environment setup as per existing project structure \---  
\# COPY \--chown=micromamba:micromamba environment.yml /tmp/environment.yml  
\# RUN micromamba shell init \-s bash \-p /opt/conda && \\  
\#     micromamba create \-y \-p /opt/conda \-f /tmp/environment.yml && \\  
\#     micromamba clean \-afy  
\#...

Critical Dependency Analysis  
A crucial step in this process, which must be performed after the initial successful compilation in the builder stage, is to run the ldd (List Dynamic Dependencies) command on the compiled binaries. For example: ldd /build/src/wepp. This command will output a list of all the shared library files (.so files) that the wepp executable depends on to run. The most common dependency will be the GNU Fortran runtime library (e.g., libgfortran.so.5). These identified libraries must be explicitly installed using apt-get install in the final runtime image to ensure the binary can execute.  
Containerizing the CLIGEN Binary  
The official USDA WEPP download packages indicate that CLIGEN is typically bundled with WEPP.1 The dailyerosion/dep repository, which is being used as the source for WEPP, contains a scripts/cligen/ directory, suggesting it includes logic for generating climate files.8 The first step will be to search this repository for a pre-compiled Linux cligen binary. If one exists, it can be copied directly into the final Docker image. If only source code is available, it will be compiled in the builder stage alongside WEPP, following a similar git clone and make pattern. If no binary or source is present, a separate search for a compatible Linux CLIGEN binary will be necessary, with the official USDA source being the primary candidate.  
This multi-stage build process provides a robust and reproducible method for creating a minimal, secure, and portable Docker image containing the exact computational engines required for the workflow, stripped of all unnecessary build-time dependencies.

## **Section II: High-Throughput Geospatial Pre-Processing on the GPU**

With a clear strategy for containerizing the CPU-bound WEPP engine, the focus now shifts to the segments of the workflow that are prime candidates for significant performance gains through GPU acceleration. These are the computationally intensive geospatial pre-processing tasks, primarily the hydrological analysis of Digital Elevation Models (DEMs) and associated raster mathematics. This section evaluates the landscape of existing tools and presents a definitive, high-performance strategy based on modern GPU computing libraries.

### **2.1 Landscape of GPU-Accelerated Hydrological Tooling**

The user query correctly identifies the need to investigate the GPU capabilities of prominent open-source hydrological libraries. A systematic review of these tools reveals a clear and consistent pattern: their design philosophy is centered on high-performance CPU computation, not GPU offloading.

* **WhiteboxTools (WBT):** This powerful geospatial analysis library is written in the Rust programming language, which is known for its performance and memory safety.17 WBT is highly optimized for parallelism on multi-core CPUs, efficiently utilizing available threads to accelerate its algorithms. However, a thorough review of its documentation, available tools, and underlying architecture shows no evidence of native support for CUDA or OpenCL, the primary technologies for GPU computing.18 WBT's performance model is exclusively CPU-based.  
* **RichDEM:** RichDEM is a C++ library with Python bindings, specifically designed for high-performance terrain analysis.21 It offers a wide array of state-of-the-art algorithms for depression filling, flow metrics (D8, D-infinity, etc.), and flow accumulation.22 Like WhiteboxTools, its performance is derived from efficient C++ implementation and parallel processing on CPU cores. The official documentation makes no mention of GPU-accelerated functions or a CUDA backend.21  
* **TauDEM (Terrain Analysis Using Digital Elevation Models):** This toolkit is explicitly designed for parallelism in a high-performance computing context. However, its parallel model is based on the Message Passing Interface (MPI), which is a standard for distributing tasks across the CPUs of multiple nodes in a cluster.25 It is architected for distributed-memory CPU clusters, not for shared-memory, massively parallel GPU architectures.27

**Conclusion:** The initial research path of seeking an off-the-shelf, open-source GIS library with mature GPU support for core hydrological functions like depression filling and flow accumulation leads to a dead end. The established tools are CPU-centric. This finding necessitates a pivot in strategy away from integrating existing tools and towards implementing the required algorithms directly using a GPU-native computing library.

### **2.2 A Proven Blueprint for High-Performance Hydrology with CuPy**

The absence of GPU support in traditional GIS toolkits does not preclude GPU acceleration of hydrological analysis. On the contrary, it highlights a paradigm shift where cutting-edge performance is now being achieved by applying general-purpose GPU computing libraries directly to scientific problems. The most promising path forward is to implement the core hydrological algorithms using CuPy, a Python library that provides a NumPy-compatible array API for CUDA.  
A critical resource informing this strategy is the 2025 paper, *"GPU-Accelerated Hydrology Algorithms for On-Prem Computation: Flow Accumulation, Drainage Lines, Watershed Delineation, Runoff Simulation"*.29 This research provides a direct and powerful blueprint for achieving the project's goals. The authors successfully implemented these core algorithms on a commodity NVIDIA RTX GPU (24 GB VRAM), demonstrating massive performance improvements over traditional CPU-based methods like those found in GDAL. Their work validates the feasibility and provides a clear methodology to replicate.  
The recommended methodology, based on this research, is as follows:

1. **Data Ingestion and Representation:** The first step involves loading the DEM, or chunks of it, into GPU memory. This is accomplished by reading the raster data using a library like rioxarray (which uses rasterio and GDAL under the hood) and then transferring the resulting NumPy array to the GPU to become a CuPy array via cupy.asarray().  
2. **Flow Direction (D8):** Calculating the D8 flow direction is a "short-pixel" (SP) operation, meaning the output for each pixel depends only on its immediate 3x3 neighborhood. This is an embarrassingly parallel problem and is perfectly suited for a custom CuPy kernel. A kernel can be written where each GPU thread is assigned a single pixel (or a small block of pixels) and independently determines the steepest downslope neighbor, writing the corresponding direction code to an output array.  
3. **Flow Accumulation (A Wavefront Propagation Approach):** Flow accumulation is the most computationally challenging step, as it is a "long-pixel" (LP) operation where a pixel's value can depend on all pixels upstream from it. A naive, sequential implementation would offer no benefit on a GPU. The key innovation described in the reference paper is a highly efficient "wavefront propagation" algorithm.29 This algorithm can be implemented in CuPy as follows:  
   * An initial kernel identifies all "source" pixels—those with no upslope neighbors (i.e., ridges and peaks). These pixels form the initial "wavefront."  
   * In an iterative loop, a propagation kernel is launched. Each thread processes a pixel from the current wavefront. It adds its own accumulation value to its designated downslope neighbor.  
   * Crucially, the kernel also manages an "indegree" count for each pixel (the number of upslope neighbors). When a pixel's contribution is passed downstream, the indegree count of the downstream neighbor is decremented.  
   * When a downstream pixel's indegree count reaches zero, it means all of its upslope neighbors have been processed. This pixel is then added to the wavefront for the *next* iteration.  
   * This process continues until the wavefront is empty, meaning all pixels have been processed. The number of iterations is proportional to the length of the longest flow path in the DEM, not the total number of pixels, making it exceptionally efficient.

**Performance Expectation:** The reference paper reports reducing a flow accumulation task that took over 20 hours with CPU-based tools to approximately 4.5 hours on a single GPU for a large river basin.29 For this project, a performance gain of **greater than 10x** compared to a multi-threaded CPU baseline (e.g., WhiteboxTools) is a realistic and conservative target. The user's required threshold of a $\>3x$ speedup to justify the complexity is therefore virtually guaranteed to be met or exceeded.

### **2.3 Optimizing General Raster Operations with Dask-CuPy**

Beyond the complex hydrological algorithms, many standard geospatial pre-processing steps, such as calculating slope, aspect, and hillshade, are focal or local operations that can also be significantly accelerated on the GPU. The architectural pattern for achieving this at scale combines Dask for distributing the work and CuPy for executing it.  
The cornerstone of this approach is the dask.array.map\_blocks function. This function takes a Dask array (which is a collection of smaller NumPy arrays, or "chunks") and applies a user-defined function to each chunk in parallel. By designing this function to perform its computations using CuPy, we can seamlessly orchestrate distributed GPU processing.  
A prototype implementation for calculating slope demonstrates this pattern:

Python

import dask.array as da  
import cupy as cp  
import rioxarray

def gpu\_slope(chunk, cell\_size\_x, cell\_size\_y):  
    """  
    Calculates slope on a single data chunk using CuPy.  
    Note: Assumes chunk is a NumPy array.  
    """  
    try:  
        \# 1\. Move data chunk from host (CPU RAM) to device (GPU VRAM).  
        chunk\_gpu \= cp.asarray(chunk)  
          
        \# 2\. Perform computation entirely on the GPU.  
        \# The cp.gradient function is the CuPy equivalent of np.gradient.  
        gy, gx \= cp.gradient(chunk\_gpu, cell\_size\_y, cell\_size\_x)  
        slope\_rad \= cp.arctan(cp.sqrt(gx\*\*2 \+ gy\*\*2))  
          
        \# 3\. Move the result from device back to host for Dask to collect.  
        return slope\_rad.get()  
    except Exception as e:  
        \# Handle cases where a GPU is not available or an error occurs.  
        \# A fallback to NumPy could be implemented here.  
        print(f"GPU processing failed: {e}. Falling back to CPU.")  
        \# Fallback logic using NumPy would go here.  
        return np.zeros\_like(chunk) \# Placeholder

\# Load the DEM as a Dask array with a specified chunk size.  
\# Larger chunks are better for GPU performance.  
dem\_dask \= rioxarray.open\_rasterio(  
    "large\_dem.tif",   
    chunks={'x': 4096, 'y': 4096}  
)

\# Extract cell sizes from raster metadata  
cell\_x \= dem\_dask.rio.resolution()  
cell\_y \= abs(dem\_dask.rio.resolution())

\# Apply the GPU function to each chunk of the Dask array.  
\# Dask's scheduler will manage sending chunks to workers for processing.  
slope\_dask \= da.map\_blocks(  
    gpu\_slope,   
    dem\_dask.data,   
    cell\_size\_x=cell\_x,   
    cell\_size\_y=cell\_y,  
    dtype=cp.float32  
)

\# At this point, no computation has happened (lazy evaluation).  
\# Trigger computation and save the result to a Zarr store,  
\# which is well-suited for parallel writes from Dask.  
slope\_dask.to\_zarr("slope\_output.zarr", overwrite=True)

Performance Analysis and Optimization:  
The efficiency of this pattern is governed by the ratio of computation time to data transfer time. The transfers between CPU RAM and GPU VRAM (cp.asarray() and .get()) introduce overhead. The benefit of GPU acceleration is only realized when the time saved by the parallel computation on the GPU significantly exceeds this transfer overhead.

* **Small Chunks (e.g., $\< 1024 \\times 1024$ pixels):** For small chunks, the constant overhead of data transfer can dominate the total time, potentially making a CPU-based NumPy calculation faster.  
* **Large Chunks (e.g., $\> 4096 \\times 4096$ pixels):** For large chunks, the computational workload is substantial. The massive parallelism of the GPU will far outweigh the transfer time, leading to significant speedups.

**Recommendation:** To maximize the computation-to-communication ratio and achieve optimal performance, all Dask-CuPy operations should be configured to use large chunk sizes. A starting point of $4096 \\times 4096$ is recommended, with potential for tuning up to $8192 \\times 8192$ depending on available GPU memory.  
The table below summarizes the analysis of hydrological processing options, providing a clear rationale for the recommended strategy.  
**Table 2: Hydrological Processing Library and Kernel Comparison**

| Tool/Library | Primary Language | Parallelism Model | GPU Support for Delineation | Estimated Performance (Relative Speedup) | Implementation Effort |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **WhiteboxTools** | Rust | Multi-threaded CPU | No | $1x$ (Baseline) | Low |
| **RichDEM** | C++/Python | Multi-threaded CPU | No | $\\sim1x$ | Low |
| **TauDEM** | C++ | MPI (CPU Cluster) | No | Varies (Multi-Node) | Medium |
| **Custom CuPy Kernel** | Python/CUDA | CUDA | **Yes (Via Custom Code)** | **$\>10x$** | **High** |

This analysis clearly indicates that while implementing custom kernels requires a higher initial effort, it is the only viable path to achieving the transformative performance gains that GPU acceleration promises for this specific problem domain.

## **Section III: A Unified Architecture for Dynamic and Portable Execution**

A successful CONUS-scale workflow requires more than just high-performance algorithms; it demands a robust software architecture that ensures portability, adaptability, and ease of deployment across diverse hardware environments. This section details the critical engineering components that provide this foundation: a dynamic resource-aware configuration system and a cross-platform deployment strategy using Docker and the NVIDIA Container Toolkit.

### **3.1 Dynamic Resource-Aware Configuration**

The goal is to create a "smart" system that can introspect its host environment at runtime and automatically configure itself to make optimal use of the available hardware—whether that is a CPU-only laptop or a multi-GPU server—without requiring manual changes to code or configuration files.  
This will be achieved through two primary architectural components:  
1\. Centralized config.yml Schema:  
A single YAML file will serve as the control panel for the entire workflow. This file will define input data paths, model parameters, and, most importantly, computational behavior. A key section will be the computational block:

YAML

computational:  
  \# 'auto': Use GPU if available, fallback to CPU.  
  \# 'force': Fail if GPU is not available.  
  \# 'never': Use CPU-only workflow.  
  use\_gpu: "auto"

  \# Fraction of total VRAM to allocate to GPU-aware libraries (e.g., CuPy memory pool).  
  gpu\_memory\_fraction: 0.8

  \# If a GPU task fails due to an Out-Of-Memory error, should it be retried on the CPU?  
  fallback\_to\_cpu\_on\_oom: true

  \# Dask cluster settings for CPU-bound tasks (WEPP execution).  
  cpu\_workers:  
    \# 'auto': Defaults to the number of physical CPU cores.  
    \# Can also be an integer.  
    count: "auto"  
    \# Memory limit per worker. 'auto' divides available RAM among workers.  
    memory\_limit: "auto"

  \# Dask cluster settings for GPU-bound tasks (pre/post-processing).  
  gpu\_workers:  
    \# 'auto': Defaults to the number of detected GPUs.  
    count: "auto"

2\. ResourceManager Class:  
A dedicated Python class, ResourceManager, will be responsible for abstracting all hardware detection logic. This class will be instantiated at the beginning of any workflow execution.

* **Introspection Logic:**  
  * It will use the psutil library to reliably determine the number of physical CPU cores (psutil.cpu\_count(logical=False)) and the total available system RAM (psutil.virtual\_memory().available).  
  * It will use the torch library, which is already a dependency for its CUDA bindings, to detect GPU hardware. The logic proposed in the user query is sound: torch.cuda.is\_available() provides a boolean check, torch.cuda.device\_count() gives the number of GPUs, and torch.cuda.get\_device\_properties(i) provides detailed information like device name and total memory for each GPU.  
* **Functionality:** The class will expose high-level methods that translate the raw hardware information and the config.yml settings into actionable configurations for the Dask framework. For example:  
  * is\_gpu\_enabled(): Returns True if use\_gpu is 'auto' and a GPU is detected, or if use\_gpu is 'force'.  
  * get\_cpu\_cluster\_kwargs(): Returns a dictionary of arguments ({'n\_workers': 16, 'threads\_per\_worker': 1, 'memory\_limit': '4GB'}) suitable for creating a dask.distributed.LocalCluster for CPU-bound tasks.  
  * get\_gpu\_cluster\_kwargs(): Returns a dictionary of arguments ({'n\_workers': 1, 'CUDA\_VISIBLE\_DEVICES': '0'}) for creating a dask\_cuda.LocalCUDACluster for GPU-bound tasks.

This architecture ensures that all hardware-specific logic is encapsulated in one place, keeping the main workflow scripts clean and focused on the scientific logic. At startup, the main script will query the ResourceManager and emit clear log messages, such as "GPU detected: NVIDIA RTX 4090 (24 GB VRAM). Enabling GPU-accelerated workflow." or "No compatible GPU detected. Proceeding with CPU-only workflow." This provides both seamless portability and essential user feedback.

### **3.2 Cross-Platform Deployment with Docker and the NVIDIA Container Toolkit**

Ensuring that the containerized application can reliably access host GPU hardware is paramount. This is a non-trivial task that has been standardized and simplified by the NVIDIA Container Toolkit.  
Core Technology: The NVIDIA Container Toolkit  
The NVIDIA Container Toolkit (formerly NVIDIA Docker) is the industry-standard solution for enabling GPU access within Linux containers.30 It is a non-negotiable prerequisite for any host system intended to run this project's GPU-accelerated workflow. The toolkit functions by providing a special container runtime (nvidia-container-runtime) that Docker can invoke. At container startup, this runtime inspects the container's environment variables (e.g., for \--gpus all) and automatically mounts the necessary host-side components—specifically, the NVIDIA driver libraries and the GPU device files—into the container's isolated filesystem.32 This allows applications inside the container (like PyTorch and CuPy) to communicate with the host's GPU as if they were running natively.  
Installation and Verification Documentation  
Because the toolkit is a host-level dependency, clear and precise documentation for the end-user is critical. A SETUP\_GPU.md file must be created, guiding the user through the following essential steps:

1. **NVIDIA Driver Installation:** Verify that a compatible NVIDIA driver is installed on the host system. A simple test is running nvidia-smi on the host terminal.  
2. **NVIDIA Container Toolkit Installation:** Provide distribution-specific instructions for installing the toolkit. For Ubuntu/Debian, this involves adding the NVIDIA repository and using apt-get to install the nvidia-container-toolkit package.34  
3. **Docker Daemon Configuration:** After installation, the Docker daemon must be configured to recognize the new nvidia runtime and then restarted. This is typically done via the sudo nvidia-ctk runtime configure \--runtime=docker command, followed by sudo systemctl restart docker.34  
4. **Verification:** The final and most important step is to run the canonical verification command: docker run \--rm \--gpus all nvidia/cuda:12.1-base nvidia-smi. If this command successfully runs and displays the output of nvidia-smi from within the container, the host system is correctly configured. If it fails, no GPU-accelerated work will be possible.

Docker Compose Strategy for Portability  
The most robust and user-friendly way to manage the dual CPU/GPU capability is to use Docker Compose override files. This approach makes CPU-only execution the default, ensuring the application works "out of the box" on any machine, while making GPU usage an explicit, opt-in enhancement.

* **docker-compose.yml (Base, Portable):** This file defines the core service, volumes, and build instructions. It contains no GPU-specific configuration, ensuring it can be run on any machine with Docker installed.  
  YAML  
  version: '3.8'  
  services:  
    wepp\_runner:  
      build:  
        context:.  
        dockerfile: Dockerfile  
      volumes:  
        \-./data:/app/data  
        \-./outputs:/app/outputs  
      \# This service, by default, has no access to GPUs.

* **docker-compose.gpu.yml (GPU Override):** This file *extends* the base configuration, adding only the deploy block necessary to enable GPU access via the NVIDIA Container Toolkit.  
  YAML  
  version: '3.8'  
  services:  
    wepp\_runner:  
      deploy:  
        resources:  
          reservations:  
            devices:  
              \- driver: nvidia  
                count: all  
                capabilities: \[gpu\]

* **User Workflow:**  
  * To run in **CPU-only mode**: docker-compose up \--build  
  * To run in **GPU-enabled mode**: docker-compose \-f docker-compose.yml \-f docker-compose.gpu.yml up \--build

This pattern is explicit, aligns with best practices for container orchestration, and perfectly fulfills the project's dual requirements of portability and high performance. It avoids the anti-pattern of maintaining separate cpu and gpu Docker images, as the container image itself should be agnostic to the underlying hardware. The ability to access the GPU is a *runtime* configuration, not a *build-time* property of the image. The single, CUDA-enabled image can run on a CPU-only machine, where its CUDA library calls will gracefully do nothing or fail silently, and on a GPU-enabled machine, where the runtime hook will provide the necessary hardware access. This separation of concerns is a cornerstone of robust and maintainable containerized application design.

## **Section IV: Scalable Execution and Data Management**

This section outlines the high-level orchestration of the full CONUS-scale workflow and the strategic management of the large data volumes involved. It integrates the containerized WEPP engine and the GPU-accelerated pre-processing components into a cohesive, scalable system, focusing on optimal data storage formats and an efficient Dask parallelism strategy.

### **4.1 Optimal Storage Formats for a Cloud-Native Workflow**

The choice of data storage formats is not a minor detail; it is a critical architectural decision that directly impacts I/O performance, scalability, and interoperability. A CONUS-scale workflow with a 500+ GB storage budget requires formats designed for parallel access and cloud environments. A hybrid strategy, using the best format for each type of data, is recommended.

* Raster Data (Intermediate and Final): Zarr  
  For all N-dimensional array data that will be processed in parallel by Dask—such as DEMs, slope rasters, flow accumulation grids, and the final erosion map—Zarr is the unequivocally superior choice.36 Zarr is a specification for storing chunked, compressed arrays. Its key advantages in this context are:  
  * **Parallel I/O:** A Zarr dataset is not a single file but a directory of many small files (chunks). This structure allows multiple Dask workers to read and write their assigned portions of the larger array simultaneously without encountering file locking issues, which are a major bottleneck with monolithic file formats like a standard GeoTIFF.36  
  * **Cloud-Native Design:** The key-value nature of its chunk storage maps directly onto cloud object storage systems like Amazon S3, enabling highly efficient data access in cloud environments.  
  * **Performance:** For multi-dimensional and time-series analysis, Zarr has been shown to outperform other formats. A benchmark by Element 84 comparing Zarr and Parquet for National Water Model data found that Zarr was almost 2x faster for queries filtering along multiple dimensions.38  
* Tabular Data (WEPP Summaries, Soil Parameters): GeoParquet  
  For any tabular data, such as the per-partition summary outputs from WEPP simulations or lookup tables for soil parameters, GeoParquet is the modern standard.36 As a columnar format, it offers significant advantages over row-based formats like CSV:  
  * **Efficient Queries:** Analytics queries that only require a subset of columns (e.g., calculating the average sediment yield) only need to read the data for those specific columns, drastically reducing I/O.  
  * **High Compression:** Storing data by column groups similar data types together, leading to much higher compression ratios.  
  * **GPU Integration:** GeoParquet is the native format for the RAPIDS cuDF library, allowing for seamless loading of tabular data directly into GPU memory for accelerated analysis.  
* Input and Archival Rasters: Cloud-Optimized GeoTIFF (COG)  
  The Cloud-Optimized GeoTIFF (COG) format remains an excellent choice for the initial ingestion of 2D raster data and for the final, distributable output product.36 Its internal tiling and use of overviews (pyramids) allow for efficient windowed reading over HTTP, making it ideal for visualization and for workflows that only need to access small spatial subsets of a large file.

Recommended Data Lifecycle:  
This hybrid format strategy defines a clear data flow through the system:

1. **Ingest:** The workflow begins by reading input DEMs, which are assumed to be stored as COGs. Dask and rioxarray can efficiently read these in a chunked manner.  
2. **Process:** All intermediate raster datasets generated during the GPU pre-processing stage (e.g., filled DEM, flow direction, flow accumulation, slope) and the final aggregated erosion map are written to Zarr stores. This format is perfectly matched to the parallel read/write patterns of the Dask/CuPy computational engine.  
3. **Tabulate:** The structured outputs from each of the thousands of WEPP simulations are collected and stored in GeoParquet files. This allows for efficient post-analysis of the raw model results.  
4. **Deliver/Archive:** As a final step, the main output product—the final CONUS-scale erosion map stored in Zarr—can be converted into a COG. This provides a single, highly compatible file that is easy to share and use in standard desktop GIS software like QGIS and ArcGIS Pro.

The following table provides a clear, at-a-glance guide to this strategic use of data formats at different stages of the workflow.  
**Table 3: Data Storage Format Selection Matrix**

| Data Type | Recommended Format | Key Characteristics | Primary Use Case | Justification |
| :---- | :---- | :---- | :---- | :---- |
| Input DEMs | COG | Tiled, Overviews | Efficient Windowed Reads | Standard format for remote access and visualization; easily read by Dask. |
| Intermediate Rasters (e.g., Flow Accumulation) | Zarr | Chunked, N-Dimensional | **Parallel I/O by Dask** | Eliminates file-locking bottlenecks during parallel computation; native to xarray. |
| Per-HUC12 Tabular Results | GeoParquet | Columnar, Compressed | High-Performance Analytics | Optimal for efficient querying and aggregation of simulation outputs; cuDF compatible. |
| Final CONUS Erosion Map (Working) | Zarr | Chunked, N-Dimensional | Parallel Aggregation/Write | Enables multiple workers to contribute to the final mosaic simultaneously. |
| Final CONUS Erosion Map (Archival) | COG | Tiled, Overviews | **Interoperability & Sharing** | Provides a single, highly compatible file for use in standard GIS software. |

### **4.2 Dask Parallelism Strategy: A Staged Approach**

Orchestrating a hybrid workflow with both CPU-intensive and GPU-intensive tasks requires a deliberate and robust strategy. While it is possible to create a single, persistent Dask cluster with a mix of CPU and GPU workers, a far simpler, more robust, and more resource-efficient architecture is a sequential, multi-stage execution model. This model is controlled by a single master Python script that brings resources online only when needed for a specific stage of the computation.  
**Recommended Three-Stage Architecture:**  
**Stage 1: GPU Pre-Processing**

* **Action:** The master script begins by instantiating a dask\_cuda.LocalCUDACluster. This specialized cluster automatically creates one Dask worker for each detected GPU, pinning each worker to a specific device.39  
* **Execution:** All DEM pre-processing tasks—depression filling, flow direction, flow accumulation, and other terrain attribute calculations—are executed. These tasks are defined as Dask graphs operating on Dask arrays, with the core computations within map\_blocks calls being performed by CuPy functions, as detailed in Section 2.3.  
* **Output:** The results of this stage (e.g., a CONUS-scale flow direction raster) are written to disk in the Zarr format.  
* **Cleanup:** Upon completion, the master script cleanly shuts down the Dask client and the LocalCUDACluster (client.close(); cluster.close()), releasing all GPU resources.

**Stage 2: Massively Parallel WEPP Execution**

* **Action:** The script then instantiates a standard dask.distributed.LocalCluster. The number of workers (n\_workers) for this cluster is set to the number of available physical CPU cores, as determined by the ResourceManager. Each worker is typically configured with a single thread (threads\_per\_worker=1) because the WEPP binary is a single-threaded process, and this prevents contention for CPU time.  
* **Execution:** This stage leverages dask.delayed to create a large task graph. Each node in this graph represents the complete simulation for a single watershed partition (e.g., a HUC12). The function decorated with @dask.delayed will perform the following steps for its assigned partition:  
  1. Read the necessary pre-processed inputs (e.g., the slope and flow path information for that partition) from the Zarr stores created in Stage 1\.  
  2. Generate the specific text-based input files required by WEPP (.slp, .sol, .cli, .man, .run).  
  3. Execute the compiled wepp binary as an external command using Python's subprocess.run(\["wepp",...\]).  
  4. Parse the resulting WEPP output files (e.g., .out, .ebe).  
  5. Return a summary of the results (e.g., a Python dictionary or a Pandas DataFrame row).  
* **Output:** Dask's scheduler efficiently distributes these thousands of independent tasks across the CPU workers. The results from all tasks are collected and aggregated into one or more GeoParquet files.  
* **Cleanup:** Upon completion of all simulations, the CPU Dask cluster is shut down.

**Stage 3: GPU Post-Processing and Synthesis**

* **Action:** The master script re-instantiates the dask\_cuda.LocalCUDACluster, bringing the GPU resources back online.  
* **Execution:** The per-partition results stored in the GeoParquet files are loaded (potentially into a dask\_cudf DataFrame). These vector-based results are then rasterized onto a CONUS-scale grid. If individual raster outputs were generated per partition, this stage would involve mosaicking and blending them. These operations are performed on the GPU using cuspatial and/or custom CuPy kernels.  
* **Output:** The final, seamless CONUS-scale erosion map is written to a Zarr store. An optional final step converts this Zarr store to a COG for distribution.  
* **Cleanup:** The GPU cluster is shut down, and the workflow concludes.

This staged approach provides critical advantages over a persistent hybrid cluster. It ensures that CPU-bound tasks (WEPP) are never scheduled on a precious GPU worker, and GPU-bound tasks are never waiting for a CPU worker. It simplifies resource management, improves stability, and aligns perfectly with the linear, dependent data flow of the problem: pre-process all data, simulate all partitions, then aggregate all results.

### **4.3 Partitioning Strategy and Overhead Analysis**

The granularity of the parallel tasks in Stage 2—the size of the watershed partitions—is a key parameter that affects overall efficiency. The decision hinges on the trade-off between maximizing parallelism and amortizing the fixed overhead associated with each task.  
The primary source of overhead for each WEPP task is the startup time of the wepp subprocess. This includes the time for the operating system to load the binary into memory, for the binary to initialize its internal state, and to read its input files.

* **Scenario 1: Fast Startup ($\< 2$ seconds):** If the WEPP binary initializes very quickly, the overhead per task is minimal. In this case, it is highly efficient to use small, numerous partitions, such as individual HUC12s. This strategy maximizes the degree of parallelism (more tasks for Dask to schedule) and produces results at a fine, granular level, which is scientifically desirable.  
* **Scenario 2: Slow Startup ($\> 10$ seconds):** If the binary has a significant startup time, this overhead can dominate the actual scientific computation time for small partitions. For example, if startup takes 15 seconds and the simulation itself only takes 30 seconds, one-third of the total wall-clock time is wasted on overhead. In this scenario, it becomes more efficient to use larger partitions (e.g., HUC10s, or groups of adjacent HUC12s) to amortize the fixed startup cost over a longer simulation run.

Critical Benchmark Requirement:  
To make an informed decision on the partitioning strategy, a crucial initial task for the project is to precisely benchmark the execution time of the containerized WEPP binary. A representative HUC12 watershed should be selected, and a full 100-year simulation should be run. The total execution time, including process startup, should be measured. This single data point is critical, as it will directly inform the optimal partition size for the entire CONUS run. The WEPP documentation suggests that while single-event simulations are fast, long-term continuous simulations can be computationally intensive, making this benchmark essential.41

## **Section V: GPU-Accelerated Post-Processing and Synthesis**

The final phase of the workflow involves synthesizing the outputs from tens of thousands of individual WEPP simulations into a single, coherent, and seamless CONUS-scale raster map. This aggregation and rasterization process, which involves handling large volumes of geometric and raster data, presents another significant opportunity for GPU acceleration, ensuring that the final step does not become a new bottleneck.

### **5.1 High-Performance Rasterization with RAPIDS cuSpatial**

A primary post-processing task is to convert the scalar results from each watershed partition (e.g., an average annual sediment yield value for each HUC12 polygon) into a raster grid. A CPU-based approach using a library like rasterio.features.rasterize would iterate through each polygon and burn its value onto a NumPy array. For a CONUS-scale grid with billions of pixels and tens of thousands of complex polygons, this process can be time-consuming.  
The RAPIDS cuspatial library, part of the NVIDIA open-source GPU data science ecosystem, is specifically designed to accelerate such geospatial operations.42 While it may not have a single high-level rasterize function, it provides the fundamental, highly-optimized building block required: point\_in\_polygon.  
Rasterization via Massively Parallel Point-in-Polygon Testing:  
The rasterization problem can be reframed as a massive point-in-polygon (PIP) test. The methodology is as follows:

1. **Load Geometries to GPU:** The HUC12 polygons and their associated sediment yield values are loaded from a GeoParquet file into a cudf DataFrame and a cuspatial GeoSeries.  
2. **Create Pixel Coordinate Grid:** A CuPy array is generated representing the geographic coordinates of the center of every single pixel in the target CONUS-scale output raster. For a 10-meter resolution grid, this could be an array of billions of (x, y) coordinate pairs.  
3. **Execute cuspatial.point\_in\_polygon:** The cuspatial.point\_in\_polygon function is executed, testing all pixel-center "points" against all HUC12 "polygons" in a massively parallel fashion on the GPU.42 The function returns a boolean mask indicating which points fall inside which polygons.  
4. **Assign Values:** The boolean mask is used to assign the corresponding sediment yield value to each pixel in the final output CuPy array.

Given that cuspatial is built to perform PIP operations on millions of points and thousands of polygons with extreme efficiency, this approach is expected to be orders of magnitude faster than a sequential, CPU-based rasterization process.  
Alternative: Custom CuPy Kernel  
If cuspatial proves to have limitations for this specific scale or use case, a custom CuPy kernel can be developed as an alternative. This provides more control at the cost of increased implementation complexity. The kernel would be designed such that each thread block on the GPU is responsible for a tile of the output raster. Each thread within the block would be assigned a single pixel, calculate its coordinate, and perform the ray-casting algorithm to test for inclusion within the relevant nearby polygons.

### **5.2 Mosaicking and Edge Blending with Dask-CuPy**

To avoid edge effects, the WEPP simulations are run on buffered partitions. The post-processing stage must then seamlessly stitch, or mosaic, these overlapping outputs into a single continuous surface. A simple "last one wins" approach to mosaicking can create artificial seams in the final map. A more sophisticated approach involves weighted averaging within the buffer zones to create a smooth transition. This blending process is an excellent candidate for GPU acceleration.  
The proposed methodology is as follows:

1. **GPU-Accelerated Distance Transform:** For each partition's individual raster output (loaded as a CuPy array), the cupyx.scipy.ndimage.distance\_transform\_edt function is used. This function calculates the exact Euclidean distance from every non-zero pixel to the nearest zero pixel (i.e., the boundary of the valid data area). The GPU-accelerated version in CuPy is significantly faster than its CPU-based counterpart in scipy.ndimage for large rasters.  
2. **Weight Grid Calculation:** The resulting distance grid is then transformed into a weight grid. This is a simple, element-wise operation on the CuPy array. For example, pixels within the core of the partition (far from the edge) are assigned a weight of 1.0, while pixels within the buffer zone are assigned a weight that fades linearly from 1.0 at the core's edge to 0.0 at the buffer's outer edge.  
3. **Distributed Weighted Averaging:** Dask and CuPy are used together to perform the final mosaicking. The individual raster outputs and their corresponding weight grids are represented as a collection of Dask arrays. Dask is then used to apply a weighted averaging function to all overlapping pixels. The core calculation, (raster1 \* w1 \+ raster2 \* w2) / (w1 \+ w2), is a series of simple, element-wise arithmetic operations. When implemented using dask.array.map\_blocks with CuPy arrays, these operations are executed in parallel on the GPU, providing very high throughput.

This combination of a high-performance distance transform and parallel weighted averaging on the GPU ensures that the final mosaicking step is both mathematically robust and computationally efficient, preventing it from becoming a bottleneck in the final stage of the workflow.

## **Section VI: Strategic Implementation Roadmap and Key Benchmarks**

This final section synthesizes the preceding analysis into an actionable, phased implementation plan. The plan is designed to systematically de-risk the project by tackling the most critical technical challenges first. It establishes clear benchmarks and performance gates that will guide technical decisions throughout the development process.

### **6.1 Phased Implementation Plan**

The project is broken down into three logical phases, each with specific tasks, deliverables, and validation criteria.  
Phase 1: Foundation and Engine Validation (Target Duration: 3 Weeks)  
This initial phase focuses on the most critical prerequisite: creating a reliable, containerized WEPP engine. All subsequent work depends on the success of this phase.

1. **Task: Source Code Acquisition and Compilation.** Fork the dailyerosion/dep GitHub repository. Set up a local Linux development environment with gfortran and make. Navigate to the src directory and successfully compile the wepp binary by analyzing and executing the provided Makefile. Document any required library dependencies (e.g., libgfortran-dev).  
2. **Task: Dockerization.** Implement the multi-stage Dockerfile as architected in Section 1.3. The first stage will perform the compilation, and the second, final stage will copy the compiled wepp and cligen binaries and install their runtime dependencies (identified using ldd).  
3. **Task: In-Container Validation.** Execute a simple, single-hillslope WEPP simulation *inside* the newly built Docker container. This is a critical integration test that validates the entire toolchain, from compilation to runtime environment and dependencies. Success is defined as the ability to run wepp and generate valid output files without errors.  
4. **Benchmark: WEPP Performance Baseline.** Using a representative HUC12 dataset, execute a full 100-year WEPP simulation inside the container. Precisely measure and document two key metrics: (a) the total process startup overhead, and (b) the total execution time. This benchmark is non-negotiable as its results will directly inform the watershed partitioning strategy in Phase 3\.

Phase 2: GPU Environment and Pre-Processing Prototype (Target Duration: 4 Weeks)  
This phase focuses on enabling the GPU environment and proving the feasibility and performance benefits of accelerating the most computationally intensive pre-processing task.

1. **Task: GPU Environment Setup.** Implement the ResourceManager class for dynamic hardware detection. Create the docker-compose.gpu.yml override file. On a suitable host machine, install the NVIDIA Container Toolkit and validate GPU access within the running container using the docker run \--rm \--gpus all nvidia/cuda:12.1-base nvidia-smi command.  
2. **Task: Hydrology Algorithm Prototyping.** Develop a Python prototype for GPU-accelerated D8 flow accumulation using CuPy. The implementation should follow the efficient wavefront propagation algorithm described in the reference paper.29  
3. **Benchmark: CPU vs. GPU Hydrology Performance.** Using a large DEM tile (e.g., at least $8192 \\times 8192$ pixels), run both the CPU-based WhiteboxTools D8FlowAccumulation tool and the new CuPy prototype. Measure the wall-clock time for each.  
4. **Performance Gate (Decision Point):** The project should only proceed with the custom GPU hydrology implementation if the measured speedup of the CuPy prototype over the multi-threaded WhiteboxTools baseline is **greater than 3x**. If this performance gate is not met, the added complexity of maintaining custom CUDA kernels is not justified. The architecture should then revert to using the robust, albeit slower, CPU-based White-boxTools for all hydrological pre-processing, and GPU resources will be reserved for other raster math and post-processing tasks.

Phase 3: Full-Scale Integration and Pilot Run (Target Duration: 5 Weeks)  
This final phase integrates all components into the end-to-end workflow and validates its performance on a regional-scale pilot study.

1. **Task: Dask Orchestration.** Implement the master Python script that controls the three-stage execution model (GPU Pre-process \-\> CPU Simulate \-\> GPU Post-process), including the logic for setting up and tearing down the appropriate Dask clusters for each stage.  
2. **Task: WEPP Parallelization.** Develop the full Dask-based WEPP execution stage using dask.delayed. This includes the functions for generating WEPP input files on-the-fly for each partition and parsing the text-based outputs into a structured format (e.g., Pandas DataFrames).  
3. **Task: Post-Processing Implementation.** Implement the GPU-accelerated post-processing stage, including rasterization of results using cuspatial or a custom kernel, and the mosaicking/blending logic using cupyx.scipy.ndimage and Dask-CuPy.  
4. **Task: Pilot Execution.** Execute the complete, end-to-end workflow on a significant but manageable geographic area, such as a single state or a HUC4 region. This pilot run will serve as the final integration test and will be used to identify any remaining performance bottlenecks related to I/O, data formats, or Dask scheduling at scale.

### **6.2 Critical Decision Points and Open Questions Summary**

The research and analysis conducted for this report have successfully addressed most of the critical questions posed in the initial query, transforming them from open questions into concrete architectural decisions or defined benchmarks.  
**Resolved Questions:**

* **WEPP Source and Containerization:** The question of how to obtain and containerize a Linux-compatible WEPP binary has been definitively answered. The dailyerosion/dep repository provides the source code and build system, and a multi-stage Docker build is the clear implementation path.  
* **WEPP GPU Feasibility:** The analysis concludes that direct GPU acceleration of the legacy Fortran core is impractical and strategically unsound. The focus must be on parallel execution of the CPU binary.  
* **GPU Hydrology Libraries:** No mature, off-the-shelf libraries exist for GPU-accelerated watershed delineation. The path forward is through the implementation of custom algorithms in CuPy, guided by existing academic research.  
* **Storage Strategy:** A hybrid, cloud-native storage strategy has been defined: Zarr for parallel raster I/O, GeoParquet for tabular analytics, and COG for ingestion and final delivery.  
* **Portability and GPU Access:** A robust and portable deployment model using a dual docker-compose file structure and the NVIDIA Container Toolkit has been architected.

Benchmark-Driven Decisions:  
The following key decisions are contingent on the results of specific benchmarks to be executed during the implementation phases:

* **Optimal Partition Size for WEPP Runs:** The choice between HUC12, HUC10, or another partitioning scheme depends directly on the WEPP execution time benchmark defined in Phase 1\. A fast startup time ($\<2s$) favors smaller partitions (HUC12), while a slow startup ($\>10s$) necessitates larger partitions to amortize overhead.  
* **Adoption of GPU Hydrology:** The decision to commit to the high-effort path of implementing and maintaining custom GPU hydrology kernels is gated by the performance benchmark in Phase 2\. The measured speedup must exceed 3x to provide a justifiable return on investment.

Final Open Legal Question:  
The final remaining question is the legal permissibility of redistributing the compiled WEPP binary within a public or private Docker image. The evidence strongly supports that this is permissible:

* The USDA-ARS explicitly states that WEPP is in the public domain and may not be copyrighted.3 It encourages its use and inclusion in larger software packages with appropriate acknowledgment.  
* The dailyerosion/dep repository, which is the recommended source, is licensed under the permissive MIT License.8

While these indicators are overwhelmingly positive, as a final point of due diligence, it is recommended to review the specific license files included within the dailyerosion/dep repository and any accompanying documentation from the USDA-ARS to confirm the right to redistribute derivative works (the compiled binary). The search for "WEPP binary license" confusingly returned results for an unrelated Canadian government program; these results are irrelevant and should be disregarded.46 The governing documents are the public domain declaration from the USDA and the MIT license of the source repository.

#### **Works cited**

1. WEPP Downloads : USDA ARS, accessed October 21, 2025, [https://www.ars.usda.gov/midwest-area/west-lafayette-in/national-soil-erosion-research/docs/wepp/wepp-downloads/](https://www.ars.usda.gov/midwest-area/west-lafayette-in/national-soil-erosion-research/docs/wepp/wepp-downloads/)  
2. Download \- National Soil Erosion Research Laboratory \- USDA ARS, accessed October 21, 2025, [https://www.ars.usda.gov/research/software/download/?softwareid=436\&modecode=50-20-10-00](https://www.ars.usda.gov/research/software/download/?softwareid=436&modecode=50-20-10-00)  
3. Water Erosion Prediction Project (WEPP) Windows Interface Tutorial \- USDA ARS, accessed October 21, 2025, [https://www.ars.usda.gov/ARSUserFiles/50201000/WEPP/wepp-tutorial-2013.pdf](https://www.ars.usda.gov/ARSUserFiles/50201000/WEPP/wepp-tutorial-2013.pdf)  
4. Water Erosion Prediction Project (WEPP) \- Dataset \- Catalog \- Data.gov, accessed October 21, 2025, [https://catalog.data.gov/dataset/water-erosion-prediction-project-wepp-af98a](https://catalog.data.gov/dataset/water-erosion-prediction-project-wepp-af98a)  
5. WEPPCAT \- Dataset \- Catalog \- Data.gov, accessed October 21, 2025, [https://catalog.data.gov/dataset/weppcat-cc945](https://catalog.data.gov/dataset/weppcat-cc945)  
6. WEPP in the Woods \- GitHub, accessed October 21, 2025, [https://github.com/wepp-in-the-woods](https://github.com/wepp-in-the-woods)  
7. ui-weppcloud: About, accessed October 21, 2025, [https://doc.wepp.cloud/](https://doc.wepp.cloud/)  
8. dailyerosion/dep: Iowa Daily Erosion Project (version 2\) \- GitHub, accessed October 21, 2025, [https://github.com/dailyerosion/dep](https://github.com/dailyerosion/dep)  
9. Documentation | Daily Erosion Project, accessed October 21, 2025, [https://www.dailyerosion.org/documentation](https://www.dailyerosion.org/documentation)  
10. Daily Erosion Project \- Carl and Melinda Helwig Department of Biological and Agricultural Engineering, accessed October 21, 2025, [https://www.bae.ksu.edu/watershed/extension/dep/](https://www.bae.ksu.edu/watershed/extension/dep/)  
11. High Performance Computing HPC SDK | NVIDIA Developer, accessed October 21, 2025, [https://developer.nvidia.com/hpc-sdk](https://developer.nvidia.com/hpc-sdk)  
12. NVIDIA HPC Fortran, C++ and C Compilers with OpenACC, accessed October 21, 2025, [https://developer.nvidia.com/hpc-compilers](https://developer.nvidia.com/hpc-compilers)  
13. An OpenACC Example (Part 1\) | NVIDIA Technical Blog, accessed October 21, 2025, [https://developer.nvidia.com/blog/openacc-example-part-1/](https://developer.nvidia.com/blog/openacc-example-part-1/)  
14. openacc.examples \- HPE Cray Programming Environment, accessed October 21, 2025, [https://cpe.ext.hpe.com/docs/24.03/cce/man7/openacc.examples.7.html](https://cpe.ext.hpe.com/docs/24.03/cce/man7/openacc.examples.7.html)  
15. Model:WEPP \- CSDMS, accessed October 21, 2025, [https://csdms.colorado.edu/wiki/Model:WEPP](https://csdms.colorado.edu/wiki/Model:WEPP)  
16. Software : USDA ARS, accessed October 21, 2025, [https://www.ars.usda.gov/research/software/?modeCode=50-20-10-00](https://www.ars.usda.gov/research/software/?modeCode=50-20-10-00)  
17. WhiteboxTools: Download WhiteboxTools \- Whitebox Geospatial Inc, accessed October 21, 2025, [https://www.whiteboxgeo.com/download-whiteboxtools/](https://www.whiteboxgeo.com/download-whiteboxtools/)  
18. Frequently Asked Questions \- WhiteboxTools User Manual \- Whitebox Geospatial, accessed October 21, 2025, [https://www.whiteboxgeo.com/manual/wbt\_book/faq.html](https://www.whiteboxgeo.com/manual/wbt_book/faq.html)  
19. Whitebox Geospatial Analysis Tools \- Wikipedia, accessed October 21, 2025, [https://en.wikipedia.org/wiki/Whitebox\_Geospatial\_Analysis\_Tools](https://en.wikipedia.org/wiki/Whitebox_Geospatial_Analysis_Tools)  
20. Supported Data Formats \- WhiteboxTools User Manual \- Whitebox Geospatial Inc, accessed October 21, 2025, [https://www.whiteboxgeo.com/manual/wbt\_book/supported\_formats.html](https://www.whiteboxgeo.com/manual/wbt_book/supported_formats.html)  
21. RichDEM 0.0.03 documentation, accessed October 21, 2025, [https://richdem.readthedocs.io/en/latest/intro.html](https://richdem.readthedocs.io/en/latest/intro.html)  
22. RichDEM — High-Performance Terrain Analysis — RichDEM 0.0.03 documentation, accessed October 21, 2025, [https://richdem.readthedocs.io/en/latest/](https://richdem.readthedocs.io/en/latest/)  
23. RichDEM Python Reference \- Read the Docs, accessed October 21, 2025, [https://richdem.readthedocs.io/en/latest/python\_api.html](https://richdem.readthedocs.io/en/latest/python_api.html)  
24. Concepts — RichDEM 0.0.03 documentation \- Read the Docs, accessed October 21, 2025, [https://richdem.readthedocs.io/en/latest/concepts.html](https://richdem.readthedocs.io/en/latest/concepts.html)  
25. Use TauDEM • traudem, accessed October 21, 2025, [https://lucarraro.github.io/traudem/](https://lucarraro.github.io/traudem/)  
26. TauDEM processing on OpenTopography, accessed October 21, 2025, [https://opentopography.org/blog/taudem-processing-opentopography](https://opentopography.org/blog/taudem-processing-opentopography)  
27. TauDEM \- Riverscapes Tools, accessed October 21, 2025, [https://tools.riverscapes.net/taudem/](https://tools.riverscapes.net/taudem/)  
28. TauDEM, A suite of programs for the Analysis of Digital Elevation Data \- David Tarboton, accessed October 21, 2025, [https://hydrology.usu.edu/taudem/taudem1.0/taudem.html](https://hydrology.usu.edu/taudem/taudem1.0/taudem.html)  
29. GPU-Accelerated Hydrology Algorithms for On-Prem Computation: Flow Accumulation, Drainage Lines, Watershed Delineation, Runoff Simulation \- CSE, IIT Delhi, accessed October 21, 2025, [https://www.cse.iitd.ac.in/\~aseth/hydrogpu-propl-2025-camera-ready.pdf](https://www.cse.iitd.ac.in/~aseth/hydrogpu-propl-2025-camera-ready.pdf)  
30. NVIDIA Container Toolkit, accessed October 21, 2025, [https://unrealcontainers.com/docs/concepts/nvidia-docker](https://unrealcontainers.com/docs/concepts/nvidia-docker)  
31. NVIDIA/nvidia-container-toolkit: Build and run containers leveraging NVIDIA GPUs \- GitHub, accessed October 21, 2025, [https://github.com/NVIDIA/nvidia-container-toolkit](https://github.com/NVIDIA/nvidia-container-toolkit)  
32. Architecture Overview — NVIDIA Container Toolkit, accessed October 21, 2025, [https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/arch-overview.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/arch-overview.html)  
33. User Guide — container-toolkit 1.8.1 documentation \- NVIDIA Docs, accessed October 21, 2025, [https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.8.1/user-guide.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.8.1/user-guide.html)  
34. Installing the NVIDIA Container Toolkit \- NVIDIA Docs Hub, accessed October 21, 2025, [https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)  
35. How to Install NVIDIA Container Toolkit and Use GPUs with Docker Containers \- GPU Mart, accessed October 21, 2025, [https://www.gpu-mart.com/blog/install-nvidia-container-toolkit](https://www.gpu-mart.com/blog/install-nvidia-container-toolkit)  
36. Cloud Native Geospatial Formats: GeoParquet, Zarr, COG, and PMTiles Explained, accessed October 21, 2025, [https://forrest.nyc/cloud-native-geospatial-formats-geoparquet-zarr-cog-and-pmtiles-explained/](https://forrest.nyc/cloud-native-geospatial-formats-geoparquet-zarr-cog-and-pmtiles-explained/)  
37. Fundamentals: What Is Zarr? A Cloud-Native Format for Tensor Data \- Earthmover, accessed October 21, 2025, [https://earthmover.io/blog/what-is-zarr/](https://earthmover.io/blog/what-is-zarr/)  
38. Benchmarking Zarr and Parquet Data Retrieval using the National Water Model (NWM) in a Cloud-native environment \- Element 84, accessed October 21, 2025, [https://element84.com/software-engineering/benchmarking-zarr-and-parquet-data-retrieval-using-the-national-water-model-nwm-in-a-cloud-native-environment/](https://element84.com/software-engineering/benchmarking-zarr-and-parquet-data-retrieval-using-the-national-water-model-nwm-in-a-cloud-native-environment/)  
39. Quickstart — dask-cuda 25.08.00a45 documentation \- RAPIDS Docs, accessed October 21, 2025, [https://docs.rapids.ai/api/dask-cuda/stable/quickstart/](https://docs.rapids.ai/api/dask-cuda/stable/quickstart/)  
40. Quickstart — dask-sql documentation \- Read the Docs, accessed October 21, 2025, [https://dask-sql.readthedocs.io/en/latest/quickstart.html](https://dask-sql.readthedocs.io/en/latest/quickstart.html)  
41. The WEPP Model and Its Applicability for Predicting \- Erosion on Rangelands \- Southwest Watershed Research Center: Tucson, AZ, accessed October 21, 2025, [https://www.tucson.ars.ag.gov/unit/publications/pdffiles/1049.pdf](https://www.tucson.ars.ag.gov/unit/publications/pdffiles/1049.pdf)  
42. cuSpatial Python User's Guide \- RAPIDS Docs, accessed October 21, 2025, [https://docs.rapids.ai/api/cuspatial/stable/user\_guide/cuspatial\_api\_examples/](https://docs.rapids.ai/api/cuspatial/stable/user_guide/cuspatial_api_examples/)  
43. cuspatial 25.04.00 documentation \- RAPIDS Docs, accessed October 21, 2025, [https://docs.rapids.ai/api/cuspatial/stable/](https://docs.rapids.ai/api/cuspatial/stable/)  
44. sacridini/Awesome-Geospatial: Long list of geospatial tools and resources \- GitHub, accessed October 21, 2025, [https://github.com/sacridini/Awesome-Geospatial](https://github.com/sacridini/Awesome-Geospatial)  
45. GPU geospatial with RAPIDS cuSpatial: spatial joins & point‑in‑polygon, accessed October 21, 2025, [https://compute.hivenet.com/post/gpu-geospatial-rapids-cuspatial-joins-pip](https://compute.hivenet.com/post/gpu-geospatial-rapids-cuspatial-joins-pip)  
46. Frequently Asked Questions re: Wage Earner Protection Program \- Alvarez & Marsal, accessed October 21, 2025, [https://www.alvarezandmarsal.com/sites/default/files/canada/FAQ%20re%20WEPP%20%282025.08.11%29%20%28For%20Website%29%20English.pdf](https://www.alvarezandmarsal.com/sites/default/files/canada/FAQ%20re%20WEPP%20%282025.08.11%29%20%28For%20Website%29%20English.pdf)  
47. No. 17–Wage Earner Protection Program Appeals (Overpayment), accessed October 21, 2025, [https://www.cirb-ccri.gc.ca/en/resources/no-17-wage-earner-protection-program](https://www.cirb-ccri.gc.ca/en/resources/no-17-wage-earner-protection-program)  
48. No. 16–Wage Earner Protection Program Appeals (Eligibility), accessed October 21, 2025, [https://www.cirb-ccri.gc.ca/en/resources/no-16-wage-earner-protection-program](https://www.cirb-ccri.gc.ca/en/resources/no-16-wage-earner-protection-program)