# AI BI Assistant — Sales Intelligence & Forecasting Platform

An AI-powered business intelligence platform that helps users **understand sales data, get business insights, and forecast future sales**.

## What It Does

The platform combines AI, analytics, and machine learning in one application.

* Ask questions about business data using natural language
* Query sales data using SQL
* Get answers from business documents using RAG
* Forecast future sales using XGBoost
* Track and manage ML models with MLflow
* Serve predictions through a FastAPI API
* Monitor the API with Prometheus
* Detect changes in data using drift monitoring
* Automatically decide when model retraining is needed
* Run testing and deployment through GitHub Actions
* Deploy the application using Docker and Render

## How It Works

```text
User
  ↓
AI BI Assistant
  ↓
  ├── SQL Analytics
  │      ↓
  │   Business Data
  │
  ├── RAG
  │      ↓
  │   Business Documents
  │
  └── Sales Forecasting
         ↓
      XGBoost
         ↓
       MLflow
         ↓
      FastAPI
         ↓
     Monitoring
         ↓
    Drift Detection
         ↓
  Retraining Decision
```

## Sales Forecasting

The forecasting model uses historical sales, promotions, store information, calendar features, and other business features.

### Model Performance

| Metric | Result |
| ------ | -----: |
| MAE    |  80.41 |
| RMSE   | 275.69 |
| R²     |  0.953 |

Dataset:

* 194,238 total rows
* 155,390 training rows
* 38,848 testing rows

## MLOps

The forecasting model is deployed using a production-style MLOps workflow:

```text
Train
 ↓
Evaluate
 ↓
MLflow
 ↓
FastAPI
 ↓
Docker
 ↓
Render
 ↓
Prometheus
 ↓
Drift Detection
 ↓
Retraining Decision
```

GitHub Actions automatically runs code checks, model evaluation, drift monitoring, retraining decisions, and Docker builds.

## API

### `/predict`

Returns a sales prediction.

### `/health`

Checks whether the API is running.

### `/metrics`

Provides monitoring metrics for Prometheus.

## Technologies

**Python · Pandas · NumPy · Scikit-learn · XGBoost · MLflow · RAG · LLMs · SQL · FastAPI · Prometheus · Docker · GitHub Actions · GitHub · Render**

## Project Highlights

* Built an AI-based business intelligence assistant
* Combined **SQL, RAG, LLMs, and machine learning**
* Built a sales forecasting model
* Deployed the model as an API
* Added monitoring and data drift detection
* Added automated retraining decisions
* Built a CI/CD pipeline for the ML system

## Live API

https://ai-business-intelligence-assistant-kx4k.onrender.com

## API Documentation

https://ai-business-intelligence-assistant-kx4k.onrender.com/docs
