# Material Fingerprinting
We propose [Material Fingerprinting](https://doi.org/10.48550/arXiv.2508.07831), see [GitHub](https://github.com/Material-Fingerprinting/), a new method for the rapid discovery of mechanical material models from direct or indirect data that avoids solving potentially non-convex optimization problems. The core assumption of Material Fingerprinting is that each material exhibits a unique response when subjected to a standardized experimental setup. This response can be interpreted as the material's fingerprint, essentially a unique identifier that encodes all pertinent information about the material's mechanical characteristics. Consequently, if a database containing fingerprints and their corresponding mechanical models is established during an offline phase, an unseen material can be characterized rapidly in an online phase. This is accomplished by measuring its fingerprints and employing a pattern recognition algorithm to identify the best matching fingerprint in the database.


## Reference

```
Moritz Flaschel, Denisa Martonová, Carina Veil, and Ellen Kuhl  
Material Fingerprinting: A shortcut to material model discovery without solving optimization problems  
2025  
DOI: https://doi.org/10.48550/arXiv.2508.07831
```

## How to cite the code

```
Moritz Flaschel, Denisa Martonová, Carina Veil, and Ellen Kuhl  
Supplementary software for "Material Fingerprinting: A shortcut to material model discovery without solving optimization problems"  
2025  
DOI: http://doi.org/10.5281/zenodo.16778796
```