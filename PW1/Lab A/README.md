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