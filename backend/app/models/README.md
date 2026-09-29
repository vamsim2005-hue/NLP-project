# Model Artifacts Directory

This directory stores trained scikit-learn models, vectorizers, and evaluation metrics:

- `sentiment_model.pkl`: Serialized Logistic Regression model trained for binary sentiment classification.
- `sentiment_vectorizer.pkl`: Fitted `TfidfVectorizer` mapping text n-grams into feature vectors.
- `sentiment_metrics.json`: Evaluated test metrics (accuracy, precision, recall, f1, confusion matrix) saved directly from model evaluation for the Performance Dashboard.
- Future artifacts (Spam, Fake News, Toxicity) will be placed here during subsequent phases.
