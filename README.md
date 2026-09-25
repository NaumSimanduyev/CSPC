# CSPC - Computer Science for Physics and Chemistry
My coursework repository. Each practical is under PW<n>/Lab <X>/.

## Setup
Create the environment for a given lab:
conda env create -f PW<n>/Lab\ <X>/environment.yml
conda activate cspc

---

## PW1 - Lab A: Reproducible Foundations
**What I built:**
- I determined the difference in speed between the NumPy implementation and plain Python.
- I checked the precision of the program's calculations, comparing them with the formula N_0 * exp(-lambda * time).

**Speed comparison (loop vs NumPy):**
- loop: 3.429 s
- numpy: 0.0126 s
- speed-up: 271.8x faster

**Tests:** All passed except one with a negative lambda (ValueError).

**Conclusion:**
- For huge loops and scientific calculations, it is preferable to use NumPy rather than common Python tools. The bigger your data gets, the more NumPy is preferred (in my test, it was 272 times faster).

## PW1 - Lab B: Data, Plotting, and Automation
**What the data showed:**
- The observed counts (`decay_observed.csv`) drop from 5000 atoms at t=0 to under 20 by t≈19.5s, following a clearly decreasing curve that is steep at first and flattens out at later times.

**Did it match the analytical law?**
- Yes. Plotted side-by-side with the analytical curve N0*exp(-λt) (λ=0.3), the observed data traces the same exponential decay shape and overall scale. The small point-to-point noise (visible mainly at large t, where counts are low) is expected statistical scatter, not a mismatch with the law.

**Snakemake pipeline:**
- The `Snakefile` defines a single rule that takes `decay_observed.csv` as input and runs `plot_STUDENT.py` to produce `figure.png`, the observed-vs-analytical comparison figure.

## PW2 - Lab A: Motion from Tracking Data
**Why the acceleration was noisy:**
- This happens because as the step of the independent variable decreases (h → h²; by the definition of the derivative), the small difference between two values gets rounded off by the program, which plays a large role in the final result.

**The mean acceleration I measured:**
- -8.579687500 m/s²

**What did integrating back show?**
- Integrating back reduced errors, up to a maximum error of 0.78456 m (since integration is just a sum).