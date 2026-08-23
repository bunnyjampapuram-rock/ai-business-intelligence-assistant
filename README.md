# 🤖 AI Business Intelligence Assistant

An AI-powered Business Intelligence Assistant that allows users to interact with business data and company documents using natural language.

The application combines **LLM-based question routing, sales analytics, sales forecasting, and Retrieval-Augmented Generation (RAG)** into a single Streamlit application.

## 🚀 Features

### 📊 Business Sales Analytics

Users can ask natural-language questions such as:

* What is the total sales?
* What is the average sales?
* Which store has the highest sales?
* Which product family has the highest sales?
* What are the sales for beverages?
* Show monthly sales.
* Show sales by store.
* Show sales by product family.

The application converts the user's question into a business intent and executes the corresponding data analysis.

### 📈 Sales Forecasting

The application provides sales predictions using an **XGBoost regression model**.

Users can ask questions such as:

* Predict beverages sales.
* Predict sales for store 44.
* Predict GROCERY I sales for a specific date.

The forecasting workflow extracts:

* Store number
* Product family
* Forecast date

Missing parameters are collected through conversational interaction.

### 📚 Retrieval-Augmented Generation (RAG)

The assistant can answer questions using company documents.

Example questions:

* How many paid leave days do employees get?
* How many days can employees work from home?
* What are the working hours?
* What employee benefits are provided?
* How far in advance should planned leave be requested?

The RAG pipeline includes:

1. Document loading
2. Text chunking
3. Embedding generation
4. Similarity search
5. Relevant context retrieval
6. LLM-generated answer

### 🧭 Intelligent Question Routing

The application routes user questions to the appropriate system:

```text
                    User Question
                          │
                          ▼
                    Question Router
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
         FORECAST        SQL          RAG
             │            │            │
             ▼            ▼            ▼
       XGBoost Model   Sales Data   Documents
             │            │            │
             └────────────┼────────────┘
                          ▼
                    Final Answer
```

The router uses fast keyword-based routing and an **Ollama Llama 3.2 fallback classifier** when a direct match is not found.

## 🧠 Technologies

* Python
* Streamlit
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* Ollama
* Llama 3.2
* RAG
* Embeddings
* Cosine Similarity
* Requests
* Git & GitHub

## 🏗️ Project Structure

```text
AI_BI_PLATFROM/
│
├── app.py
├── router.py
├── llm_tools.py
├── llm_sql_tools.py
│
├── rag_loader.py
├── rag_chunker.py
├── rag_embeddings.py
├── rag_search.py
├── rag_answer.py
│
├── requirements.txt
├── .gitignore
│
├── Tools/
│   ├── forecast_tool.py
│   └── sql_tools.py
│
├── llm/
│   └── ollama_client.py
│
├── utils/
│   └── text_normalizer.py
│
├── data/
│   └── train_cleaned.csv
│
├── models/
│
└── rag_documents/
```

## 🔄 Application Workflow

```text
User
 │
 ▼
Streamlit Chat Interface
 │
 ▼
Question Normalization
 │
 ▼
Question Router
 │
 ├───────────────┬────────────────┐
 ▼               ▼                ▼
SQL           FORECAST           RAG
 │               │                │
 ▼               ▼                ▼
Intent        Parameter         Document
Extraction    Extraction        Retrieval
 │               │                │
 ▼               ▼                ▼
Sales Data     XGBoost          Embeddings
 │               │                │
 ▼               ▼                ▼
Analytics     Prediction       LLM Answer
 │               │                │
 └───────────────┴────────────────┘
                 │
                 ▼
             User Answer
```

## 💬 Conversational Parameter Collection

For forecasting questions, the application maintains forecast parameters using Streamlit session state.

For example:

```text
User:
Predict beverages sales

Assistant:
I need the following information:
store number, forecast date.

User:
Store 44 and 2017-09-01

Assistant:
Runs the forecast using:

Store: 44
Product Family: BEVERAGES
Forecast Date: 2017-09-01
```

This allows the assistant to collect missing information across multiple messages.

## 📚 RAG Pipeline

The RAG system follows this workflow:

```text
Company Documents
       │
       ▼
Document Loader
       │
       ▼
Text Chunking
       │
       ▼
Embedding Model
       │
       ▼
Vector Representations
       │
       ▼
Cosine Similarity Search
       │
       ▼
Relevant Chunks
       │
       ▼
Llama 3.2
       │
       ▼
Final Answer
```

## 📈 Machine Learning Model

The sales forecasting component uses **XGBoost** to predict future sales.

The forecasting pipeline includes:

* Data preprocessing
* Feature engineering
* Time-based features
* Lag features
* Rolling features
* Promotion-related features
* Categorical feature processing
* Model training
* Model evaluation
* Prediction

The trained model is used by the application through the forecasting tool.

## 🛡️ Repository Security

Large raw datasets and sensitive environment files are excluded from the GitHub repository.

For example:

```text
.env
venv/
__pycache__/
data/train_original.csv
```

The original raw dataset is kept locally and is not required in the public repository.

## ▶️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/bunnyjampapuram-rock/ai-business-intelligence-assistant.git
cd ai-business-intelligence-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Install and run Ollama

The application uses Ollama with the Llama 3.2 model.

Make sure Ollama is running locally and the required model is available.

### 6. Start the Streamlit application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🎯 Project Objective

The goal of this project is to demonstrate how traditional Business Intelligence, Machine Learning, Large Language Models, and Retrieval-Augmented Generation can be combined into a single AI-powered analytics assistant.

The system allows users to interact with business information using natural language instead of manually writing SQL queries or searching through company documents.

## 👨‍💻 Author

**Bunny Jampapuram**

GitHub:
https://github.com/bunnyjampapuram-rock
