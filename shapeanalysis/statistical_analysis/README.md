# 📊 Sex-Specific Statistical Shape Analysis

This notebook contains the analysis accompanying the study of sex-based anatomical variation in cardiac shape using statistical shape modeling.

---

## 🧠 Analysis Overview

The notebook performs:

1. **Data integration** of shape coefficients with demographic and physiological metadata
2. **Group comparisons** (male vs female) using:
   - Hotelling’s T² test
   - Levene’s test for variance homogeneity
3. **Shape coefficient correction** via linear regression against:
   - Age
   - Blood pressure
   - Body size metrics (BMI, BSA, Height, Weight)
4. **Multivariate testing** on corrected scores
5. **Logistic Regression Analysis** on correct and uncorrected scores.

---

## 📦 Output

- Updated DataFrame with corrected shape scores
- T² test statistics and p-values for each correction strategy
- ROC curves for each correction strategy.
- Optional export: `corrected_shape_scores.xlsx`

---

## 🛠 Requirements

- `pandas`, `numpy`, `scipy`, `statsmodels`
- `hotelling` (for multivariate testing)

---

## ▶️ Usage

Run the notebook step by step. No additional inputs required beyond the shape coefficients and demographics, with subjectID-based correspondence between the two.

