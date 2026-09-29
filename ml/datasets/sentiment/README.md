# Sentiment Analysis Dataset

## Dataset Information
- **Name**: Stanford Sentiment Treebank (SST-2) / Movie Review Dataset
- **Task**: Binary Sentiment Classification (Negative = 0, Positive = 1)
- **Source**: Stanford NLP Group & ClaireTT Sentiment Classification Benchmark
- **Original Source URL**: [Stanford CoreNLP SST](https://nlp.stanford.edu/sentiment/)
- **Mirror**: `https://raw.githubusercontent.com/clairett/pytorch-sentiment-classification/master/data/SST2/train.tsv`
- **Format**: Tab-Separated Values (TSV) with columns: `text\tlabel`
- **License**: Research & Educational Open Access

## Data Structure
The dataset consists of single sentences extracted from movie reviews, labeled as either:
- `0`: Negative sentiment
- `1`: Positive sentiment

## Automation
The dataset is downloaded automatically if not present by `ml/scripts/train_sentiment.py` and stored as:
`ml/datasets/sentiment/sentiment_train.tsv`.
