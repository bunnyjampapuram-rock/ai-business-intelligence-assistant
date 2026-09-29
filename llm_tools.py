import re
from datetime import datetime, timedelta


# ============================================================
# BUSINESS FAMILIES
# ============================================================

BUSINESS_FAMILIES = [
    "AUTOMOTIVE",
    "BABY CARE",
    "BEAUTY",
    "BEVERAGES",
    "BOOKS",
    "BREAD/BAKERY",
    "CELEBRATION",
    "CLEANING",
    "DAIRY",
    "DELI",
    "EGGS",
    "FROZEN FOODS",
    "GROCERY I",
    "GROCERY II",
    "HARDWARE",
    "HOME AND KITCHEN I",
    "HOME AND KITCHEN II",
    "HOME APPLIANCES",
    "HOME CARE",
    "LADIESWEAR",
    "LAWN AND GARDEN",
    "LINGERIE",
    "LIQUOR,WINE,BEER",
    "MAGAZINES",
    "MEATS",
    "PERSONAL CARE",
    "PET SUPPLIES",
    "PLAYERS AND ELECTRONICS",
    "POULTRY",
    "PREPARED FOODS",
    "PRODUCE",
    "SCHOOL AND OFFICE SUPPLIES",
    "SEAFOOD",
]


# ============================================================
# DATASET DATE CONFIGURATION
# ============================================================

LATEST_DATA_DATE = datetime(
    2017,
    8,
    15
)


# ============================================================
# FAMILY NORMALIZATION
# ============================================================

def detect_family(question):

    question_upper = str(question).upper().strip()

    # --------------------------------------------------------
    # GROCERY I
    # --------------------------------------------------------

    if re.search(
        r"\bgrocery\s*(?:1|one|i)\b",
        question_upper
    ):
        return "GROCERY I"

    # --------------------------------------------------------
    # GROCERY II
    # --------------------------------------------------------

    if re.search(
        r"\bgrocery\s*(?:2|two|ii)\b",
        question_upper
    ):
        return "GROCERY II"

    # --------------------------------------------------------
    # DIRECT FAMILY MATCH
    # --------------------------------------------------------

    # Longest names first so that more specific names
    # are checked before shorter names.

    for family in sorted(
        BUSINESS_FAMILIES,
        key=len,
        reverse=True
    ):

        if family in question_upper:

            return family

    # --------------------------------------------------------
    # COMMON USER VARIATIONS
    # --------------------------------------------------------

    family_variations = {

        "BREAD": "BREAD/BAKERY",

        "BAKERY": "BREAD/BAKERY",

        "DELICATESSEN": "DELI",

        "LIQUOR": "LIQUOR,WINE,BEER",

        "WINE": "LIQUOR,WINE,BEER",

        "BEER": "LIQUOR,WINE,BEER",

        "PLAY": "PLAYERS AND ELECTRONICS",

        "ELECTRONICS": "PLAYERS AND ELECTRONICS",

        "SCHOOL": "SCHOOL AND OFFICE SUPPLIES",

        "OFFICE": "SCHOOL AND OFFICE SUPPLIES",
    }

    for keyword, family in family_variations.items():

        if re.search(
            rf"\b{re.escape(keyword)}\b",
            question_upper
        ):

            return family

    return None


# ============================================================
# STORE NUMBER EXTRACTION
# ============================================================

def detect_store_number(question):

    question = str(question)

    # --------------------------------------------------------
    # Examples:
    #
    # store 44
    # store number 44
    # store no 44
    # store #44
    # --------------------------------------------------------

    patterns = [

        r"\bstore\s*(?:number|no\.?|#)?\s*(\d+)\b",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            question,
            re.IGNORECASE
        )

        if match:

            return int(
                match.group(1)
            )

    return None


# ============================================================
# DATE EXTRACTION
# ============================================================

def detect_forecast_date(question):

    question = str(question).strip()

    question_lower = question.lower()


    # ========================================================
    # 1. YYYY-MM-DD
    # ========================================================

    match = re.search(
        r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b",
        question
    )

    if match:

        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))

        try:

            date_value = datetime(
                year,
                month,
                day
            )

            return date_value.strftime(
                "%Y-%m-%d"
            )

        except ValueError:

            return None


    # ========================================================
    # 2. September 1 2017
    # 3. September 1, 2017
    # ========================================================

    month_pattern = (
        r"\b("
        r"january|february|march|april|may|june|"
        r"july|august|september|october|november|december"
        r")"
        r"\s+"
        r"(\d{1,2})"
        r"(?:st|nd|rd|th)?"
        r"(?:,\s*|\s+)"
        r"(\d{4})"
        r"\b"
    )

    match = re.search(
        month_pattern,
        question_lower,
        re.IGNORECASE
    )

    if match:

        month_name = match.group(1)
        day = int(match.group(2))
        year = int(match.group(3))

        try:

            date_value = datetime.strptime(
                f"{month_name} {day} {year}",
                "%B %d %Y"
            )

            return date_value.strftime(
                "%Y-%m-%d"
            )

        except ValueError:

            return None


    # ========================================================
    # 3. DD/MM/YYYY
    # ========================================================

    match = re.search(
        r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b",
        question
    )

    if match:

        day = int(match.group(1))
        month = int(match.group(2))
        year = int(match.group(3))

        try:

            date_value = datetime(
                year,
                month,
                day
            )

            return date_value.strftime(
                "%Y-%m-%d"
            )

        except ValueError:

            return None


    # ========================================================
    # 4. TODAY
    # ========================================================

    if re.search(
        r"\btoday\b",
        question_lower
    ):

        return LATEST_DATA_DATE.strftime(
            "%Y-%m-%d"
        )


    # ========================================================
    # 5. TOMORROW
    # ========================================================

    if re.search(
        r"\btomorrow\b",
        question_lower
    ):

        tomorrow = (
            LATEST_DATA_DATE
            + timedelta(days=1)
        )

        return tomorrow.strftime(
            "%Y-%m-%d"
        )


    # ========================================================
    # 6. NEXT DAY
    # ========================================================

    if re.search(
        r"\bnext\s+day\b",
        question_lower
    ):

        next_day = (
            LATEST_DATA_DATE
            + timedelta(days=1)
        )

        return next_day.strftime(
            "%Y-%m-%d"
        )


    # ========================================================
    # 7. NO DATE FOUND
    # ========================================================

    return None


# ============================================================
# EXTRACT FORECAST PARAMETERS
# ============================================================

def extract_forecast_parameters(question):

    # --------------------------------------------------------
    # Safety
    # --------------------------------------------------------

    if question is None:

        return {
            "store_number": None,
            "family_name": None,
            "forecast_date": None
        }


    question = str(
        question
    ).strip()


    # ========================================================
    # DETECT STORE
    # ========================================================

    store_number = detect_store_number(
        question
    )


    # ========================================================
    # DETECT FAMILY
    # ========================================================

    family_name = detect_family(
        question
    )


    # ========================================================
    # DETECT DATE
    # ========================================================

    forecast_date = detect_forecast_date(
        question
    )


    # ========================================================
    # CREATE RESULT
    # ========================================================

    parameters = {

        "store_number": store_number,

        "family_name": family_name,

        "forecast_date": forecast_date

    }


    # ========================================================
    # DEBUG INFORMATION
    # ========================================================

    print(
        "\n=============================="
    )

    print(
        "FORECAST PARAMETER EXTRACTION"
    )

    print(
        "=============================="
    )

    print(
        "Question:",
        question
    )

    print(
        "Store:",
        store_number
    )

    print(
        "Family:",
        family_name
    )

    print(
        "Date:",
        forecast_date
    )

    print(
        "==============================\n"
    )


    # ========================================================
    # RETURN
    # ========================================================

    return parameters