# SMS Spam Collection Dataset

## Dataset Information
- **Name**: SMS Spam Collection Dataset
- **Task**: Binary Spam Classification (`ham` = legitimate, `spam` = unsolicited)
- **Original Source**: Tiago A. Almeida and José María Gómez Hidalgo / UCI Machine Learning Repository
- **Mirror**: `https://raw.githubusercontent.com/justmarkham/DAT8/master/data/sms.tsv`
- **Total Records**: 5,572 messages
- **Class Distribution**: ~4,825 ham, ~747 spam
- **License**: Public Domain / Research Citation (Almeida, Hidalgo, Silva, 2011)

## Data Structure
TSV format with two columns:
- Column 0: `label` (`ham` or `spam`)
- Column 1: `message` (the SMS / text content)

## Automation
The dataset is downloaded automatically if not present locally by `ml/scripts/train_spam.py` into:
`ml/datasets/spam/sms_spam.tsv`.
