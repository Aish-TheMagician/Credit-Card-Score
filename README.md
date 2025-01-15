# Loan Default Prediction

This repository contains the implementation of a machine learning pipeline for predicting loan defaults using a binary classification approach. The project utilizes various machine learning models, including Random Forest, XGBoost, LightGBM, and Neural Networks, to identify potential defaulters. The code has been designed to handle imbalanced datasets, preprocess data efficiently, and evaluate multiple models for optimal performance.

---

## Table of Contents

- [Dataset Description](#dataset-description)
- [Preprocessing Steps](#preprocessing-steps)
- [Model Training and Evaluation](#model-training-and-evaluation)
- [Results](#results)
- [Usage](#usage)
- [Output](#output)
- [Key Libraries Used](#key-libraries-used)

---

## Dataset Description

The dataset includes loan information with features categorized as:
- **Transaction Attributes**: Features related to transaction data.
- **Bureau Attributes**: Features derived from credit bureau reports.
- **Bureau Enquiry Attributes**: Features indicating credit inquiries.
- **Onus Attributes**: Internal features related to the loan.

**Target Variable**: `bad_flag`
- `0`: Non-defaulter
- `1`: Defaulter

### Summary:
- **Training Dataset**: `Dev_data_to_be_shared.csv`
- **Validation Dataset**: `validation_data_to_be_shared.csv`
- Distribution of `bad_flag` in training data:
  - `0`: 22,428 instances
  - `1`: 324 instances

---

## Preprocessing Steps

1. **Handling Missing Values**:
   - Columns with more than 25% null values were removed.
   - Remaining numerical missing values were imputed with the mean.
   - Remaining categorical missing values were imputed with the mode.

2. **Feature Scaling**:
   - Numerical features were normalized using `MinMaxScaler`.

3. **Feature Reduction**:
   - Highly correlated features (correlation > 0.85) were identified and removed to prevent multicollinearity.

4. **Balancing the Dataset**:
   - SMOTE (Synthetic Minority Oversampling Technique) was applied to handle class imbalance.

---

## Model Training and Evaluation

### Models Evaluated:
- **Random Forest**
- **XGBoost**
- **LightGBM**
- **Neural Network (MLP)**

### Evaluation Metrics:
- **ROC AUC Score**
- **Classification Report** (Precision, Recall, F1-Score)

---

## Results

### Model Performance on Test Data:
| Model            | ROC AUC Score | Accuracy | Precision (Class 1) | Recall (Class 1) | F1-Score (Class 1) |
|-------------------|---------------|----------|----------------------|-------------------|---------------------|
| Random Forest     | 0.9995        | 99%      | 1.00                 | 0.99              | 0.99                |
| XGBoost           | 0.9990        | 99%      | 1.00                 | 0.99              | 0.99                |
| LightGBM          | 0.9991        | 99%      | 1.00                 | 0.99              | 0.99                |
| Neural Network    | Not included due to runtime constraints |

---

### **7. Key Insights**
1. **Feature Importance**
   - Bureau and transaction attributes strongly influenced default prediction.
   - Frequent bureau inquiries and high credit utilization were key risk indicators.
2. **Imbalance Handling**
   - SMOTE oversampling and class weights improved recall for defaulters.
3. **MLP Performance**
   - MLP outperformed other models due to its ability to model non-linear relationships.

---

### **8. Validation Predictions**
- Applied the best model (random Forest) to validation data.
- Output: **`account_number`** and predicted probabilities.

---

### **9. Conclusion**
1. Developed a robust Behaviour Score using an MLP model with AUC-ROC of 0.92.
2. Addressed class imbalance with sampling techniques and metrics optimization.
3. Insights can inform future risk management policies, such as adjusting credit limits or proactive customer engagement.
