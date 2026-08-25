from llm.ollama_client import ask_llm


# ============================================================
# FAST ROUTER
# ============================================================

def route_question(question):

    # --------------------------------------------------------
    # Safety
    # --------------------------------------------------------

    if question is None:
        return "UNKNOWN"

    question = str(question).strip()

    if not question:
        return "UNKNOWN"

    q = question.lower()


    # ========================================================
    # 1. FORECAST
    # ========================================================

    forecast_keywords = [
        "forecast",
        "predict",
        "prediction",
        "predict sales",
        "forecast sales",
        "future sales",
        "future demand",
        "tomorrow sales",
        "next day sales",
        "next week sales",
        "next month sales",
    ]

    if any(
        keyword in q
        for keyword in forecast_keywords
    ):

        print("FAST ROUTER: FORECAST")

        return "FORECAST"


    # ========================================================
    # 2. RAG / DOCUMENT QUESTIONS
    # ========================================================

    # Company documents / policies / employee questions
    # must go to RAG.

    rag_keywords = [

        # Company policy
        "company policy",
        "company policies",
        "company rule",
        "company rules",
        "company",
        "companies",

        # Employees
        "employee",
        "employees",

        # Policies
        "policy",
        "policies",

        # Documents
        "procedure",
        "procedures",
        "manual",
        "documentation",
        "document",
        "documents",
        "employee handbook",
        "handbook",

        # Leave
        "leave policy",
        "leave policies",
        "paid leave",
        "leave days",
        "paid days",

        # Work from home
        "work from home",
        "work-from-home",
        "wfh",
        "remote work",
        "remote working",

        # Working hours
        "working hours",
        "work hours",
        "office hours",

        # Benefits
        "employee benefits",
        "benefits",
        "health insurance",
        "professional training",
        "training programs",

        # Approval
        "manager approval",
        "approval",

        # HR
        "hr policy",
        "hr policies",
        "hr procedure",
        "hr procedures",

        # Guidelines
        "guideline",
        "guidelines",
    ]


    if any(
        keyword in q
        for keyword in rag_keywords
    ):

        print("FAST ROUTER: RAG")

        return "RAG"


    # ========================================================
    # 3. SQL / SALES QUESTIONS
    # ========================================================

    sql_keywords = [

        # Sales
        "sales",
        "sale",
        "sold",
        "selling",
        "revenue",

        # Stores
        "store",
        "stores",

        # Product families
        "family",
        "families",
        "beverages",
        "grocery",
        "groceries",
        "automotive",
        "baby care",
        "beauty",
        "books",
        "bread",
        "dairy",
        "delicatessen",
        "eggs",
        "frozen foods",
        "hardware",
        "home",
        "ladieswear",
        "liquor",
        "meats",
        "personal care",
        "pet supplies",
        "play",
        "poultry",
        "prepared foods",
        "produce",
        "school",
        "seafood",
        "toys",

        # Analysis
        "total",
        "average",
        "avg",
        "maximum",
        "minimum",
        "highest",
        "lowest",
        "top",
        "monthly",
        "month",
        "performance",
        "compare",
    ]


    if any(
        keyword in q
        for keyword in sql_keywords
    ):

        print("FAST ROUTER: SQL")

        return "SQL"


    # ========================================================
    # 4. OLLAMA FALLBACK
    # ========================================================

    print("FAST ROUTER: No direct match")

    print("Calling Ollama...")


    prompt = f"""
You are an AI Business Intelligence router.

Classify the user's question into exactly ONE category.

Allowed categories:

FORECAST
SQL
RAG
UNKNOWN


============================================================
UNKNOWN
============================================================

Use UNKNOWN for questions unrelated to:

- sales
- forecasting
- stores
- product families
- company documents
- company policies
- company procedures
- employee handbook


============================================================
FORECAST
============================================================

Use FORECAST for questions about predicting future sales.

Examples:

"predict sales for store 44"

"forecast beverages sales"

"what will grocery sales be tomorrow?"

"predict next month's sales"


============================================================
SQL
============================================================

Use SQL for questions about existing business sales data.

Examples:

"what are total sales?"

"what is the average sales?"

"which store sold the most?"

"what about beverages?"

"how about beverages?"

"beverages"

"what about grocery?"

"how much did beverages sell?"

"show beverages sales"

"sales by product family"

"monthly sales"


IMPORTANT:

A product family question is a SQL question.

For example:

"what about beverages"

MUST be SQL.

"how about grocery"

MUST be SQL.


============================================================
RAG
============================================================

Use RAG for questions about company documents,
company policies, employee information,
procedures, manuals, handbooks, benefits,
working hours, leave, or work-from-home rules.

Examples:

"what is the company leave policy?"

"show me the employee handbook"

"what is the HR procedure?"

"what is the company policy?"

"how many paid leave days do employees get?"

"how many days can employees work from home?"

"what are the working hours?"

"do employees get health insurance?"

"do employees receive professional training?"


IMPORTANT:

Questions about employee/company policies MUST be RAG.

Questions about sales/product families/stores MUST be SQL.


============================================================
USER QUESTION
============================================================

{question}


Return ONLY ONE WORD:

FORECAST
SQL
RAG
UNKNOWN
"""


    # ========================================================
    # ASK OLLAMA
    # ========================================================

    result = ask_llm([
        {
            "role": "user",
            "content": prompt
        }
    ])


    # ========================================================
    # CLEAN RESPONSE
    # ========================================================

    result = str(
        result
    ).strip().upper()


    # ========================================================
    # VALIDATE RESPONSE
    # ========================================================

    if result == "FORECAST":
        return "FORECAST"

    if result == "SQL":
        return "SQL"

    if result == "RAG":
        return "RAG"

    if result == "UNKNOWN":
        return "UNKNOWN"

    # ========================================================
    # SAFE DEFAULT
    # ========================================================

    return "UNKNOWN"