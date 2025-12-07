# RetailPulse AI: B2B Churn Prediction Engine
A Compound AI System for predicting B2B Churn using AWS SageMaker Canvas.

### 🚀 Project Overview
RetailPulse is an autonomous retention architecture designed to detect "Silent Attrition" in offline B2B retail. By leveraging **AWS SageMaker Canvas**, this project operationalizes a predictive model to identify churn risk 60 days before revenue impact.

### 📂 Repository Contents
* **`RetailPulse_Research_Paper.pdf`**: Full architectural breakdown and methodology.
* **`AWS_Clean_Upload.csv`**: The synthesized training dataset (N=1,000 retailers).
* **`Screenshots/`**: Evidence of model accuracy and single-prediction simulations.

### 🛠️ Tech Stack
* **Platform:** AWS SageMaker Canvas (No-Code ML)
* **Model Type:** Binary Classification (XGBoost)
* **Target Variable:** `Churned_YesNo`
* **Performance:** 95%+ Predictive Accuracy

### ⚡ Key Findings
1. **Recency is Critical:** The `DaysSinceLastOrder` variable accounted for the majority of model impact.
2. **The 45-Day Threshold:** Retailers inactive for >45 days show a non-linear spike in churn probability.

---
*Created by Sumanta Pani - Product Manager Portfolio*
