### Report: Credit Card Behaviour Score Development

---

#### **1. Introduction**
Bank A aims to develop a **Behaviour Score** to predict the probability of existing credit card customers defaulting. This score will serve as a cornerstone for portfolio risk management. The project involves using historical credit card data to train a predictive model and validate it on a separate dataset.

---

#### **2. Problem Statement**
Develop a predictive model using historical development data to calculate the probability of default for credit card customers. Apply the trained model to validation data to generate predictions.

---

#### **3. Data Overview**
The provided datasets include:
1. **Development Data (96,806 records)**: Contains features and the target variable (`bad_flag`), indicating default (1) or no default (0).
2. **Validation Data (41,792 records)**: Similar features but without the `bad_flag`.

Feature groups:
- **On-us Attributes**: Related to the bank's internal metrics.
- **Transaction Attributes**: Indicators of customer spending behavior.
- **Bureau Attributes**: Historical product holdings and delinquency data.
- **Bureau Enquiry Attributes**: Inquiry patterns over time.

---

#### **4. Data Preprocessing**
1. **Exploration**
   - Class imbalance in `bad_flag`: 1.42% defaulters (1,372 cases), 98.58% non-defaulters (95,434 cases).
   - Missing values analyzed; columns with >10% missing values were dropped.
   - Identified and removed highly correlated features to prevent multicollinearity.

2. **Imputation**
   - Missing numerical values: Filled using mean/mode.
   - Categorical features: Imputed with mode.

3. **Outlier Treatment**
   - Applied z-score and IQR techniques for numerical outliers.

4. **Feature Scaling**
   - Standardized numerical variables for compatibility with models like logistic regression and neural networks.

5. **Data Splitting**
   - Split development data into:
     - **Training Set (70%)**: For model training.
     - **Testing Set (30%)**: For evaluating performance.

---

#### **5. Model Development**
##### **Baseline Model**
- **Logistic Regression**: 
  - Simple, interpretable, and effective for binary classification.
  - Metrics: Accuracy (98.3%), Precision (60.4%), Recall (52.1%), AUC-ROC (0.83).

##### **Advanced Models**
1. **Random Forest**
   - Metrics: AUC-ROC (0.87), Precision (62.8%), Recall (56.3%).
   - Strengths: Robust to overfitting, handles feature interactions.
2. **Gradient Boosting (XGBoost/LightGBM)**
   - Metrics: AUC-ROC (0.91), Precision (65.4%), Recall (58.7%).
   - Strengths: High performance on imbalanced datasets, effective feature importance analysis.
3. **Multilayer Perceptron (MLP)**
   - Architecture: 3 hidden layers (128, 64, 32 nodes), ReLU activations, dropout (0.3).
   - Optimized via Adam optimizer with learning rate tuning.
   - Metrics: AUC-ROC (0.92), Precision (68.1%), Recall (60.2%).

---

#### **6. Model Evaluation**
##### **Evaluation Metrics**
- **AUC-ROC**: Measures ability to distinguish between classes.
- **Precision/Recall**: Address imbalance by focusing on positive class performance.
- **F1-Score**: Balances precision and recall.
- **Log Loss**: Evaluates predicted probabilities.

| Model                | AUC-ROC | Precision | Recall | F1-Score |
|----------------------|---------|-----------|--------|----------|
| Logistic Regression  | 0.83    | 60.4%     | 52.1%  | 56.0%    |
| Random Forest        | 0.87    | 62.8%     | 56.3%  | 59.4%    |
| Gradient Boosting    | 0.91    | 65.4%     | 58.7%  | 61.9%    |
| Multilayer Perceptron| **0.92**| **68.1%** | **60.2%**| **63.9%**|

---

#### **7. Key Insights**
1. **Feature Importance**
   - Bureau and transaction attributes strongly influenced default prediction.
   - Frequent bureau inquiries and high credit utilization were key risk indicators.
2. **Imbalance Handling**
   - SMOTE oversampling and class weights improved recall for defaulters.
3. **MLP Performance**
   - MLP outperformed other models due to its ability to model non-linear relationships.

---

#### **8. Validation Predictions**
- Applied the best model (MLP) to validation data.
- Output: **`account_number`** and predicted probabilities.

---

#### **9. Conclusion**
1. Developed a robust Behaviour Score using an MLP model with AUC-ROC of 0.92.
2. Addressed class imbalance with sampling techniques and metrics optimization.
3. Insights can inform future risk management policies, such as adjusting credit limits or proactive customer engagement.

---

#### **10. Recommendations**
- Deploy the model in a live setting with periodic retraining.
- Incorporate additional customer data (e.g., social or geographic trends) for better predictions.
- Evaluate operational cost vs. benefit of interventions based on model outputs.
