import json
import re

from llm.ollama_client import ask_llm
from utils.text_normalizer import normalize_question

from Tools.forecast_tool import df, family_mapping

from Tools.sql_tools import (
    get_total_sales,
    get_average_sales,
    get_max_sales,
    get_min_sales,
    get_top_store,
    get_top_family,
    get_sales_by_store,
    get_sales_by_family,
    get_sales_by_all_families,
    get_monthly_sales,
    get_monthly_sales_by_family,
    get_sales_by_store_family,
)


# ============================================================
# CONSTANTS
# ============================================================

ALLOWED_INTENTS = {
    "TOTAL_SALES",
    "AVERAGE_SALES",
    "MAX_SALES",
    "MIN_SALES",
    "TOP_STORE",
    "TOP_FAMILY",
    "STORE_SALES",
    "FAMILY_SALES",
    "FAMILY_SALES_ALL",
    "MONTHLY_SALES",
    "STORE_FAMILY_SALES",
    "UNKNOWN",
}


GENERIC_FAMILY_NAMES = {
    "PRODUCT FAMILY",
    "PRODUCT FAMILIES",
    "PRODUCTS FAMILY",
    "PRODUCTS FAMILIES",
    "FAMILY",
    "FAMILIES",
    "ALL FAMILY",
    "ALL FAMILIES",
    "ALL PRODUCT FAMILY",
    "ALL PRODUCT FAMILIES",
    "WHICH FAMILY",
    "WHICH FAMILIES",
    "WHICH PRODUCT FAMILY",
    "WHICH PRODUCT FAMILIES",
}


# ============================================================
# FAMILY ALIASES
# ============================================================

FAMILY_ALIASES = {
    "GROCERY 1": "GROCERY I",
    "GROCERY 2": "GROCERY II",
    "GROCERIES 1": "GROCERY I",
    "GROCERIES 2": "GROCERY II",
    "GROCERRY 1": "GROCERY I",
    "GROCERRY 2": "GROCERY II",
    "GROCCERY 1": "GROCERY I",
    "GROCCERY 2": "GROCERY II",

    "GROCERY I": "GROCERY I",
    "GROCERY II": "GROCERY II",

    "BEVERAGE": "BEVERAGES",
    "BEVAREGES": "BEVERAGES",
    "BEVERAGES": "BEVERAGES",

    "PRODUCE": "PRODUCE",
}


# ============================================================
# NORMALIZE FAMILY NAME
# ============================================================

def normalize_family_name(family_name):

    if family_name is None:
        return None

    family_name = str(family_name).upper().strip()

    if family_name in GENERIC_FAMILY_NAMES:
        return None

    if family_name in FAMILY_ALIASES:
        family_name = FAMILY_ALIASES[family_name]

    for real_family in family_mapping.keys():

        if (
            str(real_family).upper().strip()
            == family_name
        ):
            return real_family

    return family_name


# ============================================================
# EXTRACT STORE NUMBER
# ============================================================

def extract_store_number(question):

    patterns = [
        r"\bstore\s*(?:number\s*)?(\d+)\b",
        r"\bstore\s*#\s*(\d+)\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            question,
            re.IGNORECASE
        )

        if match:
            return int(match.group(1))

    return None


# ============================================================
# FIND FAMILY IN QUESTION
# ============================================================

def find_family_in_question(question):

    question_upper = (
        str(question)
        .upper()
        .strip()
    )

    # Check aliases first
    aliases_sorted = sorted(
        FAMILY_ALIASES.keys(),
        key=len,
        reverse=True
    )

    for alias in aliases_sorted:

        if alias in question_upper:
            return FAMILY_ALIASES[alias]

    # Check actual family names
    families = sorted(
        family_mapping.keys(),
        key=lambda x: len(str(x)),
        reverse=True
    )

    for family in families:

        family_upper = (
            str(family)
            .upper()
            .strip()
        )

        if family_upper in question_upper:
            return family

    return None


# ============================================================
# FAST INTENT DETECTION
# ============================================================

def detect_fast_intent(question):

    q = (
        str(question)
        .lower()
        .strip()
    )

    # ========================================================
    # TOP STORE
    # ========================================================

    top_store_patterns = [
        "which store sold the most",
        "which store sells the most",
        "store sold the most",
        "top store",
        "best store",
        "best performing store",
        "highest selling store",
        "store with the highest sales",
        "store with the highest total sales",
        "which store performed best",
        "which store has the highest sales",
        "which store has the most sales",
        "which store generated most sales",
        "which store made the most sales",
    ]

    if any(
        phrase in q
        for phrase in top_store_patterns
    ):
        return {
            "intent": "TOP_STORE",
            "store_number": None,
            "family_name": None,
        }

    # ========================================================
    # TOP FAMILY
    # ========================================================

    top_family_patterns = [
        "which product family has the highest sales",
        "which product family has the highest total sales",
        "which product family sold the most",
        "which product family sells the most",
        "top product family",
        "best product family",
        "highest selling product family",
        "product family with the highest sales",
        "product family with the highest total sales",
        "which family has the highest sales",
        "which family sold the most",
    ]

    if any(
        phrase in q
        for phrase in top_family_patterns
    ):
        return {
            "intent": "TOP_FAMILY",
            "store_number": None,
            "family_name": None,
        }

    # ========================================================
    # ALL FAMILIES
    # ========================================================

    all_family_patterns = [
        "sales for all families",
        "sales for all family",
        "sales by family",
        "sales by families",
        "sales by product family",
        "sales by product families",
        "family wise sales",
        "family-wise sales",
        "product family wise sales",
        "product family-wise sales",
        "sales for each family",
        "sales for each product family",
        "sales for every family",
        "sales for every product family",
        "compare sales by family",
        "compare sales by product family",
        "all product families",
    ]

    if any(
        phrase in q
        for phrase in all_family_patterns
    ):
        return {
            "intent": "FAMILY_SALES_ALL",
            "store_number": None,
            "family_name": None,
        }

    # ========================================================
    # MONTHLY SALES
    # ========================================================

    monthly_patterns = [
        "monthly sales",
        "month wise sales",
        "month-wise sales",
        "sales by month",
        "sales month wise",
        "sales month-wise",
        "monthly sale",
        "mothly sales",
        "montly sales",
        "monthly saless",
    ]

    if any(
        phrase in q
        for phrase in monthly_patterns
    ):

        family_name = find_family_in_question(
            question
        )

        return {
            "intent": "MONTHLY_SALES",
            "store_number": None,
            "family_name": family_name,
        }

    # ========================================================
    # STORE + FAMILY SALES
    # ========================================================

    family_name = find_family_in_question(question)
    store_number = extract_store_number(question)

    if (
        family_name is not None
        and store_number is not None
    ):

        store_family_patterns = [
            "how much",
            "sales",
            "sold",
            "revenue",
            "performance",
        ]

        if any(
            word in q
            for word in store_family_patterns
        ):

            return {
                "intent": "STORE_FAMILY_SALES",
                "store_number": store_number,
                "family_name": family_name,
            }

    # ========================================================
    # SPECIFIC FAMILY SALES
    # ========================================================

    if family_name is not None:

        family_patterns = [
            "sales",
            "sold",
            "revenue",
            "how much",
            "performance",
            "what about",
            "how about",
            "tell me",
            "show me",
            "give me",
        ]

        if any(
            word in q
            for word in family_patterns
        ):

            return {
                "intent": "FAMILY_SALES",
                "store_number": None,
                "family_name": family_name,
            }

        # Example: "beverages?"
        cleaned_q = re.sub(
            r"[^a-zA-Z0-9\s]",
            "",
            q
        ).strip()

        normalized_family = normalize_family_name(
            cleaned_q
        )

        if normalized_family in family_mapping:

            return {
                "intent": "FAMILY_SALES",
                "store_number": None,
                "family_name": normalized_family,
            }

    # ========================================================
    # AVERAGE SALES
    # ========================================================

    average_patterns = [
        "average sales",
        "avg sales",
        "mean sales",
        "average sale",
        "typical sales",
    ]

    if any(
        phrase in q
        for phrase in average_patterns
    ):
        return {
            "intent": "AVERAGE_SALES",
            "store_number": None,
            "family_name": None,
        }

    # ========================================================
    # TOTAL SALES
    # ========================================================

    total_patterns = [
        "total sales",
        "overall sales",
        "combined sales",
        "total revenue",
        "how much did we sell",
        "how much have we sold",
    ]

    if any(
        phrase in q
        for phrase in total_patterns
    ):
        return {
            "intent": "TOTAL_SALES",
            "store_number": None,
            "family_name": None,
        }

    # ========================================================
    # MAX SALES
    # ========================================================

    max_patterns = [
        "maximum sales",
        "max sales",
        "highest sales value",
        "largest sales value",
        "maximum sale",
        "max sale",
        "highest sale",
    ]

    if any(
        phrase in q
        for phrase in max_patterns
    ):
        return {
            "intent": "MAX_SALES",
            "store_number": None,
            "family_name": None,
        }

    # ========================================================
    # MIN SALES
    # ========================================================

    min_patterns = [
        "minimum sales",
        "min sales",
        "lowest sales value",
        "smallest sales value",
        "minimum sale",
        "min sale",
        "lowest sale",
    ]

    if any(
        phrase in q
        for phrase in min_patterns
    ):
        return {
            "intent": "MIN_SALES",
            "store_number": None,
            "family_name": None,
        }

    # ========================================================
    # STORE SALES
    # ========================================================

    store_number = extract_store_number(question)

    if store_number is not None:

        store_patterns = [
            "sales",
            "sold",
            "revenue",
            "performance",
            "how much",
        ]

        if any(
            word in q
            for word in store_patterns
        ):

            return {
                "intent": "STORE_SALES",
                "store_number": store_number,
                "family_name": None,
            }

    return None


# ============================================================
# OLLAMA FALLBACK
# ============================================================

def ask_ollama_for_sql(question):

    prompt = f"""
You are a sales business-intelligence intent classifier.

Understand this user question:

{question}

Return ONLY valid JSON.

Use exactly these fields:

{{
    "intent": null,
    "store_number": null,
    "family_name": null
}}

Allowed intents:

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
UNKNOWN

Rules:

1. "which store sold the most"
   -> TOP_STORE

2. "which family sold the most"
   -> TOP_FAMILY

3. "sales for all families"
   -> FAMILY_SALES_ALL

4. "sales by product family"
   -> FAMILY_SALES_ALL

5. "monthly sales"
   -> MONTHLY_SALES

6. "monthly sales for Grocery I"
   -> MONTHLY_SALES
   family_name = "GROCERY I"

7. "monthly sales for beverages"
   -> MONTHLY_SALES
   family_name = "BEVERAGES"

8. "store 44 sales"
   -> STORE_SALES
   store_number = 44

9. "beverages sales"
   -> FAMILY_SALES
   family_name = "BEVERAGES"

10. "what about beverages"
    -> FAMILY_SALES
    family_name = "BEVERAGES"

11. "how about beverages"
    -> FAMILY_SALES
    family_name = "BEVERAGES"

12. "beverages?"
    -> FAMILY_SALES
    family_name = "BEVERAGES"

13. "bevareges"
    -> FAMILY_SALES
    family_name = "BEVERAGES"

14. "beverage"
    -> FAMILY_SALES
    family_name = "BEVERAGES"

15. "grocery 1 sales"
    -> FAMILY_SALES
    family_name = "GROCERY I"

16. "what about grocery 1"
    -> FAMILY_SALES
    family_name = "GROCERY I"

17. "how much did beverages sell in store 44"
    -> STORE_FAMILY_SALES
    family_name = "BEVERAGES"
    store_number = 44

18. Generic phrases such as "family", "families",
    "all families", or "product families" are NOT
    specific family names.

19. Return null when a value is not available.

20. Do not write explanations.

21. Return ONLY JSON.

User question:

{question}
"""

    response = ask_llm(
        [
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    print("OLLAMA SQL RESPONSE:")
    print(response)

    # Extract JSON safely
    match = re.search(
        r"\{.*\}",
        response,
        re.DOTALL
    )

    if not match:
        raise ValueError(
            "Could not find JSON in Ollama SQL response."
        )

    json_text = match.group(0)

    try:
        parameters = json.loads(json_text)

    except json.JSONDecodeError as e:

        raise ValueError(
            "Could not parse Ollama SQL response.\n\n"
            f"Extracted JSON:\n{json_text}"
        ) from e

    return parameters


# ============================================================
# VALIDATE PARAMETERS
# ============================================================

def validate_parameters(parameters):

    if not isinstance(parameters, dict):
        parameters = {}

    required_fields = [
        "intent",
        "store_number",
        "family_name",
    ]

    for field in required_fields:

        if field not in parameters:
            parameters[field] = None

    # ========================================================
    # NORMALIZE INTENT
    # ========================================================

    if parameters["intent"] is not None:

        parameters["intent"] = (
            str(parameters["intent"])
            .upper()
            .strip()
        )

    # ========================================================
    # NORMALIZE STORE
    # ========================================================

    store_number = parameters.get(
        "store_number"
    )

    if store_number is not None:

        try:
            parameters["store_number"] = int(
                store_number
            )

        except (
            TypeError,
            ValueError
        ):

            parameters["store_number"] = None

    # ========================================================
    # NORMALIZE FAMILY
    # ========================================================

    if parameters.get("family_name") is not None:

        parameters["family_name"] = (
            normalize_family_name(
                parameters["family_name"]
            )
        )

    # ========================================================
    # VALIDATE INTENT
    # ========================================================

    if parameters["intent"] not in ALLOWED_INTENTS:

        parameters["intent"] = "UNKNOWN"

    intent = parameters["intent"]

    # ========================================================
    # TOP STORE
    # ========================================================

    if intent == "TOP_STORE":

        parameters["store_number"] = None
        parameters["family_name"] = None

    # ========================================================
    # TOP FAMILY
    # ========================================================

    elif intent == "TOP_FAMILY":

        parameters["store_number"] = None
        parameters["family_name"] = None

    # ========================================================
    # ALL FAMILIES
    # ========================================================

    elif intent == "FAMILY_SALES_ALL":

        parameters["store_number"] = None
        parameters["family_name"] = None

    # ========================================================
    # MONTHLY SALES
    # ========================================================

    elif intent == "MONTHLY_SALES":

        parameters["store_number"] = None

        family_name = parameters.get(
            "family_name"
        )

        if family_name is not None:

            if family_name not in family_mapping:

                raise ValueError(
                    f"Unknown product family: {family_name}"
                )

    # ========================================================
    # STORE SALES
    # ========================================================

    elif intent == "STORE_SALES":

        if parameters["store_number"] is None:

            raise ValueError(
                "Could not identify the store number."
            )

        parameters["family_name"] = None

    # ========================================================
    # FAMILY SALES
    # ========================================================

    elif intent == "FAMILY_SALES":

        if parameters["family_name"] is None:

            raise ValueError(
                "Could not identify the product family."
            )

        if parameters["family_name"] not in family_mapping:

            raise ValueError(
                f"Unknown product family: "
                f"{parameters['family_name']}"
            )

        parameters["store_number"] = None

    # ========================================================
    # STORE + FAMILY SALES
    # ========================================================

    elif intent == "STORE_FAMILY_SALES":

        if parameters["store_number"] is None:

            raise ValueError(
                "Could not identify the store number."
            )

        if parameters["family_name"] is None:

            raise ValueError(
                "Could not identify the product family."
            )

        if parameters["family_name"] not in family_mapping:

            raise ValueError(
                f"Unknown product family: "
                f"{parameters['family_name']}"
            )

    return parameters


# ============================================================
# MAIN PARAMETER EXTRACTION
# ============================================================

def extract_sql_parameters(question):

    original_question = question

    # ========================================================
    # NORMALIZE
    # ========================================================

    try:

        question = normalize_question(
            question
        )

    except Exception:

        question = original_question

    if not question:
        question = original_question

    question = str(question).strip()

    print("ORIGINAL QUESTION:")
    print(original_question)

    print("NORMALIZED QUESTION:")
    print(question)

    # ========================================================
    # FAST DETECTION
    # ========================================================

    fast_result = detect_fast_intent(
        question
    )

    if fast_result is not None:

        print("FAST SQL DETECTION:")
        print(fast_result)

        return validate_parameters(
            fast_result
        )

    # ========================================================
    # OLLAMA FALLBACK
    # ========================================================

    print("FAST DETECTION FAILED.")
    print("Calling Ollama...")

    parameters = ask_ollama_for_sql(
        question
    )

    # ========================================================
    # VALIDATE
    # ========================================================

    parameters = validate_parameters(
        parameters
    )

    print("FINAL SQL PARAMETERS:")
    print(parameters)

    return parameters


# ============================================================
# EXECUTE SQL INTENT
# ============================================================

def execute_sql_intent(parameters):

    intent = parameters.get("intent")

    store_number = parameters.get(
        "store_number"
    )

    family_name = parameters.get(
        "family_name"
    )

    # ========================================================
    # TOTAL SALES
    # ========================================================

    if intent == "TOTAL_SALES":

        return get_total_sales()

    # ========================================================
    # AVERAGE SALES
    # ========================================================

    elif intent == "AVERAGE_SALES":

        return get_average_sales()

    # ========================================================
    # MAX SALES
    # ========================================================

    elif intent == "MAX_SALES":

        return get_max_sales()

    # ========================================================
    # MIN SALES
    # ========================================================

    elif intent == "MIN_SALES":

        return get_min_sales()

    # ========================================================
    # TOP STORE
    # ========================================================

    elif intent == "TOP_STORE":

        return get_top_store()

    # ========================================================
    # TOP FAMILY
    # ========================================================

    elif intent == "TOP_FAMILY":

        return get_top_family()

    # ========================================================
    # STORE SALES
    # ========================================================

    elif intent == "STORE_SALES":

        if store_number is None:

            raise ValueError(
                "Could not identify the store number."
            )

        return get_sales_by_store(
            int(store_number)
        )

    # ========================================================
    # FAMILY SALES
    # ========================================================

    elif intent == "FAMILY_SALES":

        if family_name is None:

            raise ValueError(
                "Could not identify the product family."
            )

        family_name = normalize_family_name(
            family_name
        )

        if family_name not in family_mapping:

            raise ValueError(
                f"Unknown product family: "
                f"{family_name}"
            )

        family_number = family_mapping[
            family_name
        ]

        print("Family name:", family_name)
        print("Family number:", family_number)

        return get_sales_by_family(
            family_number
        )

    # ========================================================
    # ALL FAMILY SALES
    # ========================================================

    elif intent == "FAMILY_SALES_ALL":

        return get_sales_by_all_families()

    # ========================================================
    # STORE + FAMILY SALES
    # ========================================================

    elif intent == "STORE_FAMILY_SALES":

        if store_number is None:

            raise ValueError(
                "Could not identify the store number."
            )

        if family_name is None:

            raise ValueError(
                "Could not identify the product family."
            )

        family_name = normalize_family_name(
            family_name
        )

        if family_name not in family_mapping:

            raise ValueError(
                f"Unknown product family: "
                f"{family_name}"
            )

        family_number = family_mapping[
            family_name
        ]

        return get_sales_by_store_family(
            int(store_number),
            family_number
        )

    # ========================================================
    # MONTHLY SALES
    # ========================================================

    elif intent == "MONTHLY_SALES":

        # Overall monthly sales
        if family_name is None:

            return get_monthly_sales()

        # Family monthly sales
        family_name = normalize_family_name(
            family_name
        )

        if family_name not in family_mapping:

            raise ValueError(
                f"Unknown product family: "
                f"{family_name}"
            )

        family_number = family_mapping[
            family_name
        ]

        return get_monthly_sales_by_family(
            family_number
        )

    # ========================================================
    # UNKNOWN
    # ========================================================

    elif intent == "UNKNOWN":

        raise ValueError(
            "I could not understand the SQL question."
        )

    # ========================================================
    # INVALID INTENT
    # ========================================================

    else:

        raise ValueError(
            f"Unsupported SQL intent: {intent}"
        )