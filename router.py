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
        "forecast sales",
        "predict sales",
        "future sales",
        "future demand",
        "tomorrow sales",
        "next day sales",
        "next week sales",
        "next month sales",
        "future sales",
        "expected sales",
        "estimate sales",
    ]

    if any(keyword in q for keyword in forecast_keywords):

        print("FAST ROUTER: FORECAST")

        return "FORECAST"


    # ========================================================
    # 2. RAG / COMPANY DOCUMENT QUESTIONS
    # ========================================================

    rag_keywords = [

        "company policy",
        "company policies",
        "company rule",
        "company rules",

        "employee",
        "employees",

        "policy",
        "policies",

        "procedure",
        "procedures",

        "manual",
        "documentation",
        "document",
        "documents",

        "employee handbook",
        "handbook",

        "leave policy",
        "leave policies",
        "paid leave",
        "leave days",

        "work from home",
        "work-from-home",
        "wfh",
        "remote work",
        "remote working",

        "working hours",
        "work hours",
        "office hours",

        "employee benefits",
        "benefits",
        "health insurance",

        "professional training",
        "training programs",

        "manager approval",
        "approval",

        "hr policy",
        "hr policies",
        "hr procedure",
        "hr procedures",

        "guideline",
        "guidelines",
    ]

    if any(keyword in q for keyword in rag_keywords):

        print("FAST ROUTER: RAG")

        return "RAG"


    # ========================================================
    # 3. SQL / EXISTING SALES DATA
    # ========================================================

    sql_keywords = [

        # Sales
        "sales",
        "sale",
        "sell",
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

    if any(keyword in q for keyword in sql_keywords):

        print("FAST ROUTER: SQL")

        return "SQL"


    # ========================================================
    # 4. UNKNOWN
    # ========================================================

    print("FAST ROUTER: UNKNOWN")

    return "UNKNOWN"