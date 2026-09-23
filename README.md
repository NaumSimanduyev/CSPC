# CSPC - Computer Science for Physics and Chemistry
My coursework repository. Each practical is under PW<n>/Lab <X>/.
## Setup
Create the environment for a given lab:
conda env create -f PW<n>/Lab\ <X>/environment.yml
conda activate cspc
---
## PW1 - Lab A: Reproducible Foundations
**What I built:**
- I have determined the difference in speed between implementation via numpy library and common python 
- I have checked the precision of the program's calculations , comparing them with the formula(N_0 * exp^(-lambda * time))
**Speed comparison (loop vs NumPy):**
- loop : 3.429 s
- numpy : 0.0126s
- speed-up: 271.8x faster
**Tests:** all except one with negative lambda(ValueError)
**Conclusion:**
- For huge loops and scientific calculations it is more preferred to use NumPy rather than common python tools. The bigger your data gets, the more NumPy is preferred ( in my test, it is 272 times faster).
## PW1 - Lab B: Data, Plotting, and Automation
**What the data showed:**
- The observed counts (`decay_observed.csv`) drop from 5000 atoms at t=0 down to under 20 by t≈19.5s, following a clear decreasing curve that is steep at first and flattens out at later times.
**Did it match the analytical law?**
- Yes. Plotted side-by-side with the analytical curve N0\*exp(-λt) (λ=0.3), the observed data traces the same exponential decay shape and the same overall scale. The small point-to-point noise (visible mainly at large t, where counts are low) is expected statistical scatter, not a mismatch with the law.
**Snakemake pipeline:**
- The `Snakefile` defines a single rule that takes `decay_observed.csv` as input and runs `plot_STUDENT.py` to produce `figure.png`, the observed-vs-analytical comparison figure.