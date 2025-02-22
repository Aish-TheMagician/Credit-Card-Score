# Importing Libraries and Data

!pip uninstall -y scikit-learn
!pip install scikit-learn==1.3.1

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.max_columns', 2000)
from sklearn.decomposition import PCA
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, roc_curve, f1_score
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
sns.set_palette("crest")

train_data = pd.read_csv('/content/drive/MyDrive/convolve 25/train.csv')
test_data = pd.read_csv('/content/drive/MyDrive/convolve 25/test.csv')

"""# Functions

"""

def print_shape():
  print("Train Data Shape:", train_data.shape)
  print("Validation Data Shape:", test_data.shape)

def print_class(data):
  data = pd.DataFrame(data)
  bad_flag_counts = data['bad_flag'].value_counts(normalize=True)
  sns.barplot(x=bad_flag_counts.index, y=bad_flag_counts.values)
  plt.title("Distribution of bad_flag (Target Variable)")
  plt.xlabel("Bad Flag")
  plt.ylabel("Proportion")
  plt.show()

def apply_pca(dataset, columns, n_comp):

  scaler = StandardScaler()
  scaled_data = scaler.fit_transform(dataset[columns])

  pca = PCA(n_components = n_comp)
  data_pca = pd.DataFrame(pca.fit_transform(scaled_data))
  return data_pca

def print_result(model, X_validation, y_validation):
  y_pred = model.predict(X_validation)
  print("Classification Report:")
  print(classification_report(y_validation, y_pred))

  print(f"Accuracy : {accuracy_score(y_validation, y_pred):.4f}")
  print(f"F1 score : {f1_score(y_validation, y_pred):.4f}")
  y_pred_prob = model.predict_proba(X_validation)[:, 1]
  roc_auc = roc_auc_score(y_validation, y_pred_prob)
  print(f"The ROC AUC Score is : {roc_auc:.4f}")

def plot_roc(model, X_validation, y_validation):
  y_pred_prob = model.predict_proba(X_validation)[:, 1]
  roc_auc = roc_auc_score(y_validation, y_pred_prob)
  fpr, tpr, thresholds = roc_curve(y_validation, y_pred_prob)
  plt.figure(figsize=(8, 6))
  plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve (AUC = {roc_auc:.4f})')
  plt.plot([0, 1], [0, 1], color='gray', linestyle='--')  # Diagonal line (random classifier)
  plt.xlabel('False Positive Rate')
  plt.ylabel('True Positive Rate')
  plt.title('Receiver Operating Characteristic (ROC) Curve')
  plt.legend(loc='lower right')
  plt.grid(True)
  plt.show()

"""# EDA and Preprocessing

"""

train_data.head()

train_data.describe()

print_shape()

transaction_cols = [col for col in train_data.columns if col.startswith('transaction_attribute')]
bureau_cols = [col for col in train_data.columns if col.startswith('bureau')]
bureau_enquiry_cols = [col for col in train_data.columns if col.startswith('bureau_enquiry')]
onus_cols = [col for col in train_data.columns if col.startswith('onus_attribute')]

print(f"Transaction Attributes: {len(transaction_cols)}")
print(f"Bureau Attributes: {len(bureau_cols)}")
print(f"Bureau Enquiry Attributes: {len(bureau_enquiry_cols)}")
print(f"Onus Attributes: {len(onus_cols)}")

print_class(train_data)

"""**This graph illustrates the class imblance in the data which should be handled**

**Dropping columns with more than 10% nan values**
"""

null_percentages = train_data.isnull().sum() * 100 / len(train_data)
print("Percentage of null values in each column:")
null_percentages

train_data = train_data.loc[:, train_data.isna().sum() <= train_data.shape[0]/10]
test_data = test_data.loc[:, test_data.isna().sum() <= test_data.shape[0]/10]
print_shape()

"""Imputing the numerical columns with the mean value"""

numerical_cols = train_data.select_dtypes(include=['number']).columns
for col in numerical_cols:
    if train_data[col].isnull().any():
        train_data[col] = train_data[col].fillna(train_data[col].mean())
        test_data[col] = test_data[col].fillna(test_data[col].mean())

columns = train_data.columns.tolist()[2:]

train_pca = apply_pca(train_data, columns, 160)
test_pca = apply_pca(test_data, columns, 160)

"""**Applying SMOTE to counter the class imblance present in the dataset**"""

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(train_pca, train_data['bad_flag'])

print_class(y_resampled)

X_train, X_validation, y_train, y_validation = train_test_split(X_resampled, y_resampled, test_size = 0.25, random_state = 69)

"""# Random Forest Classifier"""

rf_classifier = RandomForestClassifier()
rf_classifier.fit(X_train, y_train)
rf_pred = rf_classifier.predict(X_validation)

print_result(rf_classifier, X_validation, y_validation)

plot_roc(rf_classifier, X_validation, y_validation)

"""# XGBoost Classifier"""

xgb_classifier = XGBClassifier(n_estimators = 150, eval_metric='logloss')
xgb_classifier.fit(X_train, y_train)
xgb_pred = xgb_classifier.predict(X_validation)

print_result(xgb_classifier, X_validation, y_validation)

plot_roc(xgb_classifier, X_validation, y_validation)

"""# MLP Classifier"""

mlp_classifier = MLPClassifier(max_iter=1000)
mlp_classifier.fit(X_train, y_train)
mlp_pred = mlp_classifier.predict(X_validation)

print_result(mlp_classifier, X_validation, y_validation)

plot_roc(mlp_classifier, X_validation, y_validation)

"""# Ensemble"""

base_models = [
    ('randomforest', rf_classifier),
    ('xgboost', xgb_classifier),
    ('mlp', mlp_classifier)
]

voting_clf = VotingClassifier(
    estimators=base_models,
    voting='soft'
)
voting_clf.fit(X_train, y_train)
y_pred = voting_clf.predict(X_validation)

print_result(voting_clf, X_validation, y_validation)

plot_roc(voting_clf, X_validation, y_validation)

test_preds = voting_clf.predict_proba(test_pca)[:, 1]
results = pd.DataFrame({
    'account_number': test_data['account_number'],
    'predicted_probability': test_preds
})
results.to_csv("Team_ARS_prediction.csv", index=False)

results
