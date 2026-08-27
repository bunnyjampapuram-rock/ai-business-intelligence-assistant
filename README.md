# 🤖 AI Business Intelligence Assistant

An AI-powered Business Intelligence and **Sales Forecasting platform** that enables users to interact with historical sales data, machine-learning forecasts, business analytics, and company documents using natural language.

The project combines:

* 📈 **XGBoost Sales Forecasting**
* 🧠 LLM-powered question understanding
* 🧭 Intelligent intent routing
* 📊 Business sales analytics
* 📚 Retrieval-Augmented Generation (RAG)
* 🔎 Embedding-based semantic search
* 💬 Conversational parameter collection
* 🌐 Streamlit deployment

The **core machine-learning component is the sales forecasting system**, which uses historical grocery sales data, time-series feature engineering, lag features, rolling features, promotion information, oil-price features, and an XGBoost regression model to forecast future sales.

The forecasting and analytics capabilities are then integrated into a conversational AI interface.

---

# 🌐 Live Demo

🚀 **Streamlit App:**

https://ai-business-intelligence-assistant-7lynbi3ekeo2heyczsdxir.streamlit.app/

🔗 **GitHub Repository:**

https://github.com/bunnyjampapuram-rock/ai-business-intelligence-assistant


---
## Predicting sales 
![sales forecast](sreenshots/Screenshot(1).png)








# 📈 1. AI Sales Forecasting — Core Machine Learning Component

The primary machine-learning component of this project is an **XGBoost-based sales forecasting system** trained on historical grocery sales data.

The system allows users to forecast sales for a specific:

* Store
* Product family
* Forecast date

### Example

```text
User:

Predict beverages sales for store 44 on 2017-09-01.

        ↓

Question Understanding

        ↓

Store = 44
Family = BEVERAGES
Date = 2017-09-01

        ↓

Forecast Feature Generation

        ↓

XGBoost Model

        ↓

Sales Prediction

        ↓

Predicted Sales
```

The forecasting system was designed to generate future predictions using historical sales patterns and engineered temporal, promotional, and external features.

---

# 🧠 2. XGBoost Forecasting Pipeline

The forecasting model was developed using historical grocery sales data.

The complete pipeline is:

```text
Historical Sales Data
        ↓
Data Cleaning
        ↓
Feature Engineering
        ↓
Time-Based Features
        ↓
Lag Features
        ↓
Rolling Features
        ↓
Promotion Features
        ↓
Oil-Price Features
        ↓
Categorical Features
        ↓
Log-Transformed Target
        ↓
XGBoost Regression
        ↓
Prediction
        ↓
Inverse Transformation
        ↓
Final Sales Forecast
```

### Important Features

```text
year
month
day
day_of_week
week
quarter
day_of_year

sale_lag_14
sale_lag_21
sale_lag_28

sale_roll_7_21
promo_roll_3

onpromotion
is_weekend

oil_roll_7
oil_fwd_1
oil_fwd_3
oil_fwd_7
```

The model uses a **log-transformed sales target** during training and converts predictions back to the original sales scale during inference.

---

# 📊 3. Forecast Feature Engineering

The forecasting system uses multiple categories of engineered features.

### Time-Based Features

```text
year
month
day
day_of_week
week
quarter
day_of_year
```

These features allow the model to learn seasonal and calendar-based sales patterns.

### Lag Features

```text
sale_lag_14
sale_lag_21
sale_lag_28
```

Lag features provide historical sales information from previous time periods.

### Rolling Features

```text
sale_roll_7_21
promo_roll_3
```

Rolling features help capture recent sales and promotion trends.

### Promotion Features

```text
onpromotion
promo_roll_3
```

These features capture the effect of promotions on sales.

### Oil-Price Features

```text
oil_roll_7
oil_fwd_1
oil_fwd_3
oil_fwd_7
```

Oil-price information is incorporated as an external feature because changes in oil prices can correlate with economic and transportation conditions.

---

# 🔮 4. Conversational Sales Forecasting

Users can request predictions using natural language.

Examples:

```text
Predict beverages sales for store 44.

Predict Grocery I sales for store 44.

Predict Grocery I sales for store 44 on 2017-09-01.
```

The forecasting system extracts:

```text
Store Number
Product Family
Forecast Date
```

If required information is missing, the assistant collects it conversationally.

### Example

```text
User:

Predict beverages sales.

Assistant:

I need the store number and forecast date.

User:

Store 44 and 2017-09-01.

        ↓

Store = 44
Family = BEVERAGES
Date = 2017-09-01

        ↓

XGBoost Forecast

        ↓

Predicted Sales
```

The application maintains forecasting parameters using **Streamlit session state**, allowing information to be collected across multiple messages.

---

# 🏪 5. Business Sales Analytics

In addition to forecasting, the application provides natural-language business analytics over historical sales data.

Users can ask questions without manually writing SQL queries.

Examples:

```text
What is the total sales?

What is the average sales?

What is the maximum sales?

What is the minimum sales?

Which store has the highest sales?

Which product family has the highest sales?

What are the sales for beverages?

Show sales by store.

Show sales by product family.

Show monthly sales.
```

The application converts the question into a structured business intent and executes the corresponding deterministic business function.

---

# 🏪 6. Store-Level Analytics

The system supports both individual-store analysis and analysis across all stores.

Examples:

```text
Store 44 sales

How much did store 44 sell?

Show sales for store 44

Show sales by store

Show store-wise sales

Show sales for all stores

Which store has the highest sales?
```

The application extracts the store number when required and routes the request to the appropriate sales-analysis tool.

Example:

```text
User:

How much did store 44 sell?

↓

Intent:

STORE_SALES

↓

Store Number:

44

↓

Sales Tool:

get_sales_by_store(44)
```

---

# 🛒 7. Product-Family Analytics

The assistant supports individual product-family analysis and comparison across product families.

Examples:

```text
What are the sales for beverages?

How much did beverages sell?

What about Grocery 1?

Show sales by product family.

Show family-wise sales.

Which product family has the highest sales?
```

The system also handles common variations and spelling mistakes.

Examples:

```text
beverage
beverages
bevareges

grocery 1
grocery 2
groceries 1
groceries 2
```

These are normalized to the product-family names used by the dataset.

For example:

```text
grocery 1
    ↓
GROCERY I
```

and:

```text
bevareges
    ↓
BEVERAGES
```

---

# 🏪 + 🛒 8. Store + Product-Family Analytics

The application can combine store and product-family parameters in a single natural-language question.

### Example

```text
How much did beverages sell in store 44?
```

The system extracts:

```text
Intent:

STORE_FAMILY_SALES

Store:

44

Product Family:

BEVERAGES
```

It then executes:

```text
get_sales_by_store_family(44, "BEVERAGES")
```

Example result:

```text
Store: 44
Product Family: BEVERAGES
Total Sales: 1,170,688.00
```

This allows users to perform detailed business analysis without manually constructing SQL queries.

---

# 📅 9. Monthly Sales Analytics

The application supports overall monthly analysis as well as product-family-specific monthly analysis.

Examples:

```text
Show monthly sales.

Show monthly sales for beverages.

Show monthly sales for Grocery I.

Show monthly sales for Grocery II.
```

The system detects the monthly-sales intent and optionally extracts the requested product family.

```text
Monthly Sales

      │
      ├── Overall Monthly Sales
      │
      └── Family Monthly Sales
```

---

# 🧭 10. Intelligent Question Routing

The application uses a multi-stage routing architecture.

```text
                         User Question
                              │
                              ▼
                    Question Normalization
                              │
                              ▼
                       Intelligent Router
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
           SQL Route     Forecast Route    RAG Route
              │               │               │
              ▼               ▼               ▼
       Intent Detection   Parameter       Document
       + Parameters       Extraction      Retrieval
              │               │               │
              ▼               ▼               ▼
       Sales Analytics      XGBoost       Embeddings
              │               │               │
              ▼               ▼               ▼
       Business Result    Prediction     Relevant Context
                                              │
                                              ▼
                                         LLM Answer
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                       Final Response
```

The router uses:

1. Question normalization
2. Fast rule-based intent detection
3. Parameter extraction
4. Deterministic business tools
5. LLM fallback classification when required

This architecture allows common business questions to be handled quickly while supporting more flexible natural-language queries.

---

# 🧩 11. Structured Business Intents

The business analytics layer converts natural-language questions into structured intents.

Supported intents include:

```text
TOTAL_SALES

AVERAGE_SALES

MAX_SALES

MIN_SALES

TOP_STORE

TOP_FAMILY

STORE_SALES

FAMILY_SALES

FAMILY_SALES_ALL

MONTHLY_SALES

STORE_FAMILY_SALES

STORE_SALES_ALL

UNKNOWN
```

### Example

User:

```text
How much did beverages sell in store 44?
```

Structured representation:

```json
{
  "intent": "STORE_FAMILY_SALES",
  "store_number": 44,
  "family_name": "BEVERAGES"
}
```

The structured parameters are then passed to the appropriate deterministic business tool.

This separation between **language understanding** and **business execution** makes the system easier to validate and maintain.

---

# 🤖 12. LLM Integration

The application uses **`gpt-oss:120b` served through the Ollama API**.

Current configuration:

```text
OLLAMA_URL=https://ollama.com/api/chat
MODEL_NAME=gpt-oss:120b
```

The LLM is primarily used for:

* Intent classification fallback
* Natural-language understanding
* RAG answer generation

The application does **not** use Llama 3.2 in its current configuration.

The architecture intentionally does not rely on the LLM to calculate business numbers.

Instead:

```text
Natural Language
       ↓
LLM / Rule-Based Router
       ↓
Structured Parameters
       ↓
Deterministic Business Tool
       ↓
Actual Business Data
       ↓
Final Answer
```

This reduces the risk of the model inventing sales values.

---

# 📚 13. Retrieval-Augmented Generation (RAG)

The assistant can answer questions using company documents.

Examples:

```text
How many paid leave days do employees get?

How many days can employees work from home?

What are the working hours?

What employee benefits are provided?

How far in advance should planned leave be requested?
```

The RAG pipeline follows:

```text
Company Documents
        ↓
Document Loader
        ↓
Text Chunking
        ↓
Embedding Generation
        ↓
Vector Representations
        ↓
Cosine Similarity Search
        ↓
Relevant Document Chunks
        ↓
gpt-oss:120b
        ↓
Final Answer
```

The assistant therefore grounds document-related answers in retrieved company information rather than relying only on general model knowledge.

---

# 🔎 14. Embedding-Based Semantic Search

The RAG system represents document chunks as numerical vectors.

When the user asks a question:

```text
User Question
      ↓
Question Embedding
      ↓
Similarity Comparison
      ↓
Relevant Document Chunks
      ↓
LLM
      ↓
Answer
```

The application uses **cosine similarity** to identify document chunks that are most relevant to the user's question.

This enables semantic retrieval even when the user's wording does not exactly match the wording in the source document.

---

# 🔤 15. Question Normalization

A normalization layer improves robustness against common variations in user input.

For example:

```text
grocery 1
Grocery 1
groceries 1
GROCERY I
```

can be mapped to:

```text
GROCERY I
```

Similarly:

```text
beverage
beverages
bevareges
```

can be normalized to:

```text
BEVERAGES
```

This normalization happens before intent detection and parameter extraction.

---

# 💬 16. Conversational Parameter Collection

Forecasting requests may not contain all required parameters in a single message.

For example:

```text
User:

Predict beverages sales.
```

The application identifies:

```text
Family:

BEVERAGES

Missing:

Store Number
Forecast Date
```

The assistant asks for the missing information.

The user can then provide:

```text
Store 44 and 2017-09-01
```

The application combines the information and executes the forecast.

This conversational workflow is implemented using **Streamlit session state**.

---

# 📊 Supported Business Questions

### Overall Sales

```text
What is the total sales?

What is the average sales?

What is the maximum sales?

What is the minimum sales?
```

### Store Analytics

```text
Store 44 sales

How much did store 44 sell?

Show sales by store.

Show store-wise sales.

Show sales for all stores.

Which store has the highest sales?
```

### Product-Family Analytics

```text
What are the sales for beverages?

How much did beverages sell?

What about Grocery 1?

Show sales by product family.

Show family-wise sales.

Which product family has the highest sales?
```

### Store + Family Analytics

```text
How much did beverages sell in store 44?

How much did Grocery I sell in store 44?

Show Grocery II sales for store 20.
```

### Monthly Analytics

```text
Show monthly sales.

Show monthly sales for beverages.

Show monthly sales for Grocery I.
```

### Forecasting

```text
Predict beverages sales for store 44 on 2017-09-01.

Forecast Grocery I sales for store 44.

Predict sales for store 44.
```

### Company Documents

```text
How many paid leave days do employees get?

What are the work-from-home policies?

What are the working hours?

What employee benefits are provided?
```

---

# 🏗️ Project Structure

```text
ai-business-intelligence-assistant/

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
├── README.md
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
│   └── xgb_model.pkl
│
└── rag_documents/
    └── company documents
```

---

# 🔄 End-to-End Application Workflow

```text
                              USER
                                │
                                ▼
                        Streamlit Chat UI
                                │
                                ▼
                     Question Normalization
                                │
                                ▼
                       Intelligent Router
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
          SQL Route        Forecast Route       RAG Route
              │                 │                 │
              ▼                 ▼                 ▼
       Intent Detection   Parameter Extraction  Document Search
              │                 │                 │
              ▼                 ▼                 ▼
       Store / Family      Store + Family +    Embeddings
          Parameters       Forecast Date           │
              │                 │                 ▼
              ▼                 ▼              Similarity
       Sales Analytics       XGBoost              Search
              │                 │                 │
              ▼                 ▼                 ▼
        Business Result      Prediction      Relevant Chunks
              │                 │                 │
              │                 │                 ▼
              │                 │             gpt-oss:120b
              │                 │                 │
              └─────────────────┼─────────────────┘
                                ▼
                         Final Response
```

---

# 🛠️ Technologies Used

| Technology        | Purpose                                 |
| ----------------- | --------------------------------------- |
| Python            | Application development                 |
| Pandas            | Data processing and analytics           |
| NumPy             | Numerical computation                   |
| Scikit-learn      | Machine-learning utilities              |
| XGBoost           | Sales forecasting                       |
| Streamlit         | Web application and chat interface      |
| Ollama            | LLM API integration                     |
| gpt-oss:120b      | LLM reasoning/classification/generation |
| RAG               | Document question answering             |
| Embeddings        | Semantic document retrieval             |
| Cosine Similarity | Vector similarity search                |
| Requests          | API communication                       |
| Git               | Version control                         |
| GitHub            | Source-code hosting and deployment      |

---

# 🛡️ Repository Security

Sensitive information and unnecessary large files should not be committed to GitHub.

The repository excludes files such as:

```text
.env
venv/
__pycache__/
data/train_original.csv
```

API keys and other secrets should be provided through environment variables or the deployment platform's secret-management system.

> ⚠️ Never commit real API keys, passwords, tokens, or credentials to GitHub.

---

# ⚙️ Environment Variables

The application uses environment variables for LLM configuration.

Example:

```text
OLLAMA_URL=https://ollama.com/api/chat

MODEL_NAME=gpt-oss:120b

OLLAMA_API_KEY=your_api_key
```

The actual API key should never be committed to GitHub.

For deployment, configure these values using the hosting platform's **Secrets / Environment Variables** section.

---

# ▶️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/bunnyjampapuram-rock/ai-business-intelligence-assistant.git

cd ai-business-intelligence-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Configure:

```text
OLLAMA_URL
MODEL_NAME
OLLAMA_API_KEY
```

Do not commit the real API key to GitHub.

### 6. Run the application

```bash
streamlit run app.py
```

---

# 🌐 Deployment

The application is deployed through a Streamlit-compatible hosting platform.

Deployment requires:

1. GitHub repository
2. `app.py`
3. `requirements.txt`
4. Required model files
5. Required application data
6. RAG documents
7. LLM environment variables / secrets

The LLM API key should be configured through the deployment platform's secret-management system.

After deployment, users can access the application through the public Streamlit URL.

---

# 🧪 Example End-to-End Interaction

## 📈 Sales Forecasting

```text
User:

Predict beverages sales.

Assistant:

I need the store number and forecast date.

User:

Store 44 and 2017-09-01.

System:

Store → 44

Family → BEVERAGES

Date → 2017-09-01

System:

XGBoost Forecast

Assistant:

Predicted Sales: ...
```

## 📊 Business Analytics

```text
User:

How much did beverages sell in store 44?

System:

Intent → STORE_FAMILY_SALES

Store → 44

Family → BEVERAGES

Business Tool:

get_sales_by_store_family(44, "BEVERAGES")

Assistant:

Store: 44

Product Family: BEVERAGES

Total Sales: 1,170,688.00
```

## 📚 RAG

```text
User:

How many paid leave days do employees get?

System:

RAG Route

    ↓

Document Retrieval

    ↓

Relevant Context

    ↓

gpt-oss:120b

    ↓

Grounded Answer
```

---

# 🎯 Project Objective

The objective of this project is to demonstrate how **Machine Learning, Business Intelligence, Large Language Models, and Retrieval-Augmented Generation** can be integrated into a single AI-powered application.

The project demonstrates:

* XGBoost sales forecasting
* Time-series feature engineering
* Lag and rolling features
* Promotion and oil-price features
* Log-transformed target modeling
* Natural-language business analytics
* Intelligent question routing
* Structured intent detection
* Parameter extraction
* Store-level sales analysis
* Product-family analysis
* Store + product-family analysis
* Monthly sales analysis
* Conversational forecasting parameter collection
* LLM-based fallback classification
* RAG-based document question answering
* Embedding-based semantic search
* Streamlit application development
* API-based LLM integration
* Git/GitHub version control
* Environment-variable-based secret management

---

# 🧠 Architecture Principle

A key design principle of this project is to use the LLM as a **language-understanding and reasoning layer**, while deterministic application tools perform the actual business operations.

```text
Natural Language
       │
       ▼
Question Router
       │
       ▼
Structured Intent + Parameters
       │
       ▼
Deterministic Business Tools
       │
       ├── Sales Analytics
       │
       ├── XGBoost Forecasting
       │
       └── RAG Retrieval
       │
       ▼
Actual Data / Retrieved Context
       │
       ▼
Final Answer
```

This architecture provides a clear separation between **AI-based language understanding** and **deterministic business execution**.

For forecasting, the LLM does not generate the numerical prediction. Instead, it extracts the required parameters and the **XGBoost model performs the actual prediction**.

---

# 🔮 Future Improvements

Potential future improvements include:

* Advanced agentic workflows
* Multi-step business reasoning
* Interactive analytics dashboards
* Automated report generation
* More forecasting models
* Model monitoring
* Advanced vector databases
* Role-based access control
* Production-grade observability
* Automated evaluation of LLM responses

---

# 👨‍💻 Author

## Bunny Jampapuram

GitHub:

https://github.com/bunnyjampapuram-rock

---

# ⭐ Project Highlights

**AI Business Intelligence Assistant**

**XGBoost Sales Forecasting + LLM + RAG + Business Analytics + Streamlit**

A production-style natural-language business intelligence application centered around **machine-learning sales forecasting**, while integrating **business analytics, document retrieval, semantic search, and LLM-powered question understanding** into a single conversational interface.
