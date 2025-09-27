# 🫀 Cardiac Shape Modeling:  Sex Differences in Healthy Heart Anatomy

This repository accompanies the paper:

> **"Unveiling sex dimorphism in the healthy cardiac anatomy: fundamental differences between male and female heart shapes"**  
> **Beatrice Moscoloni, Cameron Beeche, Julio A. Chirinos, Patrick Segers, Mathias Peirlinck**

We present a **statistical shape modeling pipeline** to quantify sex-based anatomical differences in the biventricular heart structure, using cardiac magnetic resonance (CMR) data from the UK Biobank. The analysis isolates intrinsic shape differences between male and female hearts, accounting for confounding factors like age, blood pressure, and body size.

When using, please cite:

~~~bibtex
@article{Moscoloni2025,
  title = {Unveiling sex dimorphism in the healthy cardiac anatomy: Fundamental differences between male and female heart shapes},
  ISSN = {1469-7793},
  url = {http://dx.doi.org/10.1113/JP288667},
  DOI = {10.1113/jp288667},
  journal = {The Journal of Physiology},
  publisher = {Wiley},
  author = {Moscoloni, Beatrice and Beeche, Cameron and Chirinos, Julio A. and Segers, Patrick and Peirlinck, Mathias},
  year = {2025},
  month = sep
}
~~~

This repository contains:
- Scripts for mesh processing, shape modeling, and statistical analysis
- Configuration files for anatomical mapping
- Example visualizations and mode reconstructions

📝 For details, see the [paper](https://physoc.onlinelibrary.wiley.com/doi/10.1113/JP288667).

This repository does not include the raw image processing and segmentation code. Instead, we build upon established, openly available tools for preprocessing cardiac MRI data. As such we refer the user to these pre-existing repositories for setup and usage instructions:

- **Segmentation Model**: [https://github.com/baiwenjia/ukbb_cardiac](https://github.com/baiwenjia/ukbb_cardiac). Bai et al., 2018.
- **Motion Correct and Resolution Enhancement Model**: [https://github.com/shuowang26/SRHeart](https://github.com/shuowang26/SRHeart). Wang et al., 2021.

While our statistical shape modeling pipeline has been applied to cardiac geometries in the context of this work, it can be adapted to any manually or automatically segmented anatomical structure. 

Additionally, the supplementary material folder contains the animations of the first 8 modes of variation from our study. 

## 📬 Contact

For questions, suggestions, or collaborations, please contact:

Beatrice Moscoloni  
Department of BioMechanical Engineering, Delft University of Technology, Delft, The Netherlands  
📧 [B.Moscoloni@tudelft.nl](mailto:B.Moscoloni@tudelft.nl)

Mathias Peirlinck  
Department of BioMechanical Engineering, Delft University of Technology, Delft, The Netherlands  
mplab-me at tudelft nl



