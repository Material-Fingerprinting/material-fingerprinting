![Material Fingerprinting Logo](https://raw.githubusercontent.com/Material-Fingerprinting/material-fingerprinting-hyperelasticity/main/plots/logo.png)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17098250.svg)](https://doi.org/10.5281/zenodo.17098250)

We propose [Material Fingerprinting](https://doi.org/10.48550/arXiv.2508.07831), a new method for the rapid discovery of mechanical material models from direct or indirect data that avoids solving potentially non-convex optimization problems. The core assumption of Material Fingerprinting is that each material exhibits a unique response when subjected to a standardized experimental setup. This response can be interpreted as the material's fingerprint, essentially a unique identifier that encodes all pertinent information about the material's mechanical characteristics. Consequently, if a database containing fingerprints and their corresponding mechanical models is established during an offline phase, an unseen material can be characterized rapidly in an online phase. This is accomplished by measuring its fingerprints and employing a pattern recognition algorithm to discover the best matching fingerprint in the database.

![Material Fingerprinting](https://raw.githubusercontent.com/Material-Fingerprinting/material-fingerprinting-hyperelasticity/main/plots/abstract.png)

The figure above illustrates the concept of Material Fingerprinting in both direct and indirect experimental setups. The supervised case involves homogeneous deformation fields, yielding direct strain-stress data pairs. The unsupervised case, in contrast, uses complex specimen geometries that produce heterogeneous deformation fields and only provide indirect displacement and force measurements.

![Material Fingerprinting](https://raw.githubusercontent.com/Material-Fingerprinting/material-fingerprinting-hyperelasticity/main/plots/pattern_recognition_matrices.png)

At the core of Material Fingerprinting is a straightforward pattern recognition algorithm. The figure above demonstrates how a new measurement is compared against all fingerprints in the database, correctly discovering the underlying material model — in this case, the Ogden model.

## Installation

This repository provides the actively maintained, [pip-installable package](https://pypi.org/project/material-fingerprinting/) for Material Fingerprinting. The package requires Python version 3.10 or greater. To install the latest version, run the following in your Python environment:

```
pip install material-fingerprinting
```

If you have already installed Material Fingerprinting and want to upgrade to the latest version, run the following:

```
pip install --upgrade --force-reinstall material-fingerprinting
```

## Example

After installing Material Fingerprinting, run the following [Python script](https://github.com/Material-Fingerprinting/material-fingerprinting/blob/main/example_UTCSS.py) to test the installation:

```python
import numpy as np
import material_fingerprinting as mf
# experimental data - this can be replaced by the user
F11 = np.array([0.7, 0.731578947368421, 0.763157894736842, 0.7947368421052632, 0.8263157894736842, 0.8578947368421053, 0.8894736842105263, 0.9210526315789473, 0.9526315789473685, 0.9842105263157894, 1.0157894736842106, 1.0473684210526315, 1.0789473684210527, 1.1105263157894738, 1.1421052631578947, 1.1736842105263159, 1.2052631578947368, 1.236842105263158, 1.2684210526315791, 1.3])
P11 = np.array([-514.4903790087465, -432.4853727035757, -361.07919497406556, -298.0450562094262, -241.6387671319149, -190.47903319886626, -143.46051524390043, -99.68990192707167, -58.43836225134238, -19.105803736164418, 18.806261662160683, 55.715507549699275, 91.97486010059563, 127.88501566129888, 163.7042672666993, 199.65627382279067, 235.93624412319468, 272.71589046790206, 310.1474205804502, 348.36677287209835])
F12 = np.array([0.0001, 0.026410526315789475, 0.05272105263157895, 0.07903157894736842, 0.1053421052631579, 0.13165263157894735, 0.15796315789473683, 0.1842736842105263, 0.2105842105263158, 0.23689473684210527, 0.2632052631578947, 0.2895157894736842, 0.3158263157894737, 0.3421368421052632, 0.36844736842105263, 0.39475789473684214, 0.4210684210526316, 0.44737894736842104, 0.47368947368421055, 0.5])
P12 = np.array([0.04000000020003427, 10.567894878723784, 21.117728784805728, 31.711357676748666, 42.37063751285542, 53.11742425142862, 63.97357385077116, 74.96094226918581, 86.10138546497544, 97.4167593964426, 108.9289200218903, 120.65972329962132, 132.6310251879383, 144.86468164514412, 157.3825486295415, 170.2064820994333, 183.35833801312225, 196.85997232891114, 210.7332410051028, 225.00000000000006])
# let's make some noise
P11 += 20 * np.random.randn(*P11.shape)
P12 += 10 * np.random.randn(*P12.shape)
# prepare data for discovery
measurement1 = mf.Measurement("uniaxial tension/compression", F11, P11)
measurement2 = mf.Measurement("simple shear", F12, P12)
# discover model with Material Fingerprinting
mf.discover([measurement1, measurement2])  
```

In less than a second, Material Fingerprinting discovers the material model and plots its response alongside the provided data.

## References

1. Flaschel, Moritz; Martonová, Denisa; Veil, Carina; Kuhl, Ellen. *Material Fingerprinting: A shortcut to material model discovery without solving optimization problems*. Computer Methods in Applied Mechanics and Engineering, 2026. DOI: [10.1016/j.cma.2025.118573](http://doi.org/10.1016/j.cma.2025.118573)

2. Martonová, Denisa; Kuhl, Ellen; Flaschel, Moritz. *Material Fingerprinting for rapid discovery of hyperelastic models: First experimental validation*. Journal of the Mechanics and Physics of Solids, 2026. DOI: [10.1016/j.jmps.2025.106463](http://doi.org/10.1016/j.jmps.2025.106463)

## How to cite the code

```bibtex
@software{flaschel2025python,
  author       = {Flaschel, Moritz and Martonová, Denisa and Veil, Carina and Kuhl, Ellen},
  title        = {Python package for Material Fingerprinting},
  year         = {2025},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.17098250},
  url          = {https://github.com/Material-Fingerprinting/material-fingerprinting}
}
```

## Release Notes

| Version | Changes |
|---------|---------|
| 0.1.4   | print cosine similarity |
| 0.1.3   | save data as pickle; added pure shear and equibiaxial tension/compression |
| 0.0.3   | added pure uniaxial tension, compression and pure simple shear |
| 0.0.2   | initial release for supervised Material Fingerprinting for uniaxial tension, compression and simple shear data |
