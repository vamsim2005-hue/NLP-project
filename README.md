# NLP Classification Dashboard

A production-grade, portfolio-quality full-stack Natural Language Processing (NLP) web application uniting classical machine learning classifiers into a unified, responsive analytics dashboard.

Built with **FastAPI** (Python) for inference microservices and **React + Vite + Tailwind CSS** for modern user experience.

---

## 📌 Architecture Overview

The system decouples machine learning inference and model serialization from user presentation:

```text
+-------------------------------------------------------------------------+
|                              React Frontend                             |
|       (Vite + React Router + Tailwind CSS + Recharts + Lucide Icons)     |
|                                                                         |
|    [ Dashboard ]      [ Sentiment ]      [ Performance ]     [ Spam/News]
+------------------------------------+------------------------------------+
                                     |
                          REST API Requests (JSON)
                                     |
+------------------------------------v------------------------------------+
|                             FastAPI Backend                             |
|                        (Uvicorn + Pydantic v2)                          |
|                                                                         |
|    GET /health           POST /api/sentiment/predict   GET /api/metrics |
+------------------------------------+------------------------------------+
                                     |
                              Model Ingestion
                                     |
+------------------------------------v------------------------------------+
|                         Machine Learning Pipeline                       |
|         (Preprocessing + TF-IDF Vectorizer + Scikit-Learn Models)       |
|                                                                         |
|  Raw Text -> Regex/Stopwords -> Sublinear TF-IDF -> Logistic Regression |
|  Artifacts: sentiment_model.pkl, sentiment_vectorizer.pkl               |
+-------------------------------------------------------------------------+
```

---

## 🧠 NLP Models & Pipelines

### 1. Sentiment Analysis (Active - Phase 1)
- **Algorithm**: Logistic Regression ($C = 1.5$)
- **Feature Extraction**: Sublinear TF-IDF ($n$-gram range `(1, 2)`, 10,000 max features)
- **Dataset**: Stanford Sentiment Treebank (SST-2) (6,920 sentences, stratified 80/20 train/test split)
- **Classes**: `negative` (0), `positive` (1)
- **Output**: Predicted class, confidence score, and full class probability distribution.

### 2. Spam Detection (Phase 2 - Upcoming)
- **Algorithm**: Multinomial Naive Bayes + TF-IDF
- **Target**: `ham` (legitimate message) vs. `spam` (unsolicited promotion/phishing)

### 3. Fake News Detection (Phase 3 - Upcoming)
- **Algorithm**: Logistic Regression + TF-IDF
- **Target**: `real` vs. `fake` news articles based on lexical framing and headline-body dynamics.

### 4. Toxic Comment Detection (Phase 4 - Upcoming)
- **Algorithm**: One-vs-Rest Logistic Regression + TF-IDF
- **Target**: Multi-label detection across `toxic`, `severe_toxic`, `obscene`, `threat`, `insult`, `identity_hate`.

---

## 📊 Real Model Performance (Phase 1 & 2 Baselines)

Evaluated on held-out unseen test samples:

| Model | Algorithm | Accuracy | Precision | Recall | F1 Score | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Sentiment Analysis** | TF-IDF + Logistic Regression | **77.10%** | **77.16%** | **77.10%** | **77.03%** | **Deployed (Phase 1)** |
| **Spam Detection** | TF-IDF + Multinomial NB | **98.38%** | **98.41%** | **98.38%** | **98.34%** | **Deployed (Phase 2)** |
| **Fake News** | TF-IDF + Logistic Regression | — | — | — | — | Scheduled (Phase 3) |
| **Toxicity** | Multi-label One-vs-Rest LR | — | — | — | — | Scheduled (Phase 4) |

### Test Confusion Matrices

#### 1. Sentiment Analysis ($N = 1,384$)
```text
                 Predicted Negative   Predicted Positive
Actual Negative:        479                  183
Actual Positive:        134                  588
```

#### 2. Spam Detection ($N = 1,114$)
```text
                 Predicted Ham (Clean)   Predicted Spam
Actual Ham:              965                   0
Actual Spam:              18                  131
```

---

## 📂 Project Structure

```text
nlp-classification-dashboard/
├── README.md                  # Comprehensive documentation
├── .gitignore                 # Secrets, cache, and artifact exclusions
├── LICENSE                    # MIT Open Source License
├── docker-compose.yml         # Container orchestration
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI entrypoint, CORS, routers, error handling
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── sentiment.py   # /api/sentiment/predict & /metrics endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── sentiment_service.py # Preprocessing & inference caching
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── prediction.py  # Pydantic request/response validation
│   │   └── models/
│   │       ├── README.md
│   │       ├── sentiment_model.pkl
│   │       ├── sentiment_vectorizer.pkl
│   │       └── sentiment_metrics.json
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── ModelCard.jsx
│   │   │   ├── TextInput.jsx
│   │   │   ├── PredictionCard.jsx
│   │   │   ├── ConfidenceBar.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   └── ErrorMessage.jsx
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Sentiment.jsx
│   │   │   ├── Spam.jsx
│   │   │   ├── FakeNews.jsx
│   │   │   ├── Toxicity.jsx
│   │   │   └── ModelPerformance.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
│
├── ml/
│   ├── datasets/              # Dataset documentation & cached TSV/CSV
│   │   ├── sentiment/
│   │   ├── spam/
│   │   ├── fake_news/
│   │   └── toxicity/
│   ├── scripts/
│   │   └── train_sentiment.py # Sentiment model training & serialization
│   └── utils/
│       ├── preprocessing.py   # Regex, HTML unescape, lowercasing, stopwords
│       └── evaluation.py      # Accuracy, Precision, Recall, F1, Confusion Matrix
│
└── tests/
    └── test_sentiment.py      # Automated API & model validation tests
```

---

## 🚀 Quickstart & Installation

### Prerequisites
- Python 3.10+ (Python 3.11 recommended)
- Node.js 18+ and npm (optional for React frontend)

### ⚡ Option A: Interactive All-in-One App (`app.py`)
Run the unified Streamlit web application with real-time Sentiment Analysis, Spam Detection, Batch Inference, and Interactive Metrics:
```bash
# Install dependencies
pip install -r requirements.txt

# Launch interactive web app
streamlit run app.py
# Or directly:
python app.py
```
Open `http://localhost:8501` to use the interactive dashboard.

---

### 🌐 Option B: Full-Stack (FastAPI + React)

#### 1. Train the ML Models (Optional - pre-trained models already included)
```bash
python ml/scripts/train_sentiment.py
python ml/scripts/train_spam.py
```

#### 2. Run Backend Tests
```bash
python tests/test_sentiment.py
python tests/test_spam.py
```

#### 3. Start the FastAPI Backend
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
- Interactive Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

#### 4. Start the React Frontend
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 🐳 Docker Deployment

Start the entire application (Backend + Frontend) with Docker Compose:

```bash
docker compose up --build
```
- React Application: `http://localhost:3000`
- FastAPI Backend: `http://localhost:8000`
- API Health Check: `http://localhost:8000/health`

---

## 🔌 API Reference

### Health Check
- **`GET /health`**
  ```json
  { "status": "ok" }
  ```

### Sentiment Prediction
- **`POST /api/sentiment/predict`**
  - **Body**:
    ```json
    { "text": "This movie was absolutely wonderful and brilliant!" }
    ```
  - **Response**:
    ```json
    {
      "prediction": "positive",
      "confidence": 0.9412,
      "probabilities": {
        "negative": 0.0588,
        "positive": 0.9412
      }
    }
    ```

### Model Performance Metrics
- **`GET /api/metrics`**
  - Returns serialized evaluation results for all active models.

---

## 🔮 Roadmap & Future Improvements
- **Phase 2**: Spam Detection with Multinomial Naive Bayes
- **Phase 3**: Fake News Detection with Logistic Regression & lexical features
- **Phase 4**: Multi-label Toxic Comment Detection
- **Phase 5**: Model monitoring, prediction latency telemetry, and database history
- **Deep Learning Upgrade**: DistilBERT / RoBERTa fine-tuned transformer checkpoints for comparison against classical baselines.
