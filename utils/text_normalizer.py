import re
from difflib import get_close_matches


# ============================================================
# COMMON BUSINESS WORDS
# ============================================================

BUSINESS_VOCABULARY = [

    # --------------------------------------------------------
    # Sales
    # --------------------------------------------------------

    "sales",
    "sale",
    "monthly",
    "month",
    "monthly sales",
    "sales by month",
    "month wise sales",
    "sales month wise",

    # --------------------------------------------------------
    # Store
    # --------------------------------------------------------

    "store",
    "stores",
    "store sales",
    "top store",
    "best store",

    # --------------------------------------------------------
    # Product
    # --------------------------------------------------------

    "product",
    "products",
    "family",
    "families",
    "product family",
    "product families",

    # --------------------------------------------------------
    # Business operations
    # --------------------------------------------------------

    "total",
    "average",
    "maximum",
    "minimum",
    "highest",
    "lowest",
    "top",
    "best",
    "compare",
    "comparison",

    # --------------------------------------------------------
    # Common words
    # --------------------------------------------------------

    "show",
    "give",
    "get",
    "find",
    "what",
    "which",
    "how",
    "much",
    "did",
    "me",
    "for",
    "the",
    "in",
    "by",
    "all"
]


# ============================================================
# COMMON TYPO MAP
# ============================================================

COMMON_TYPOS = {

    # Monthly
    "mothly": "monthly",
    "montly": "monthly",
    "monthy": "monthly",
    "monhtly": "monthly",
    "monthl": "monthly",

    # Sales
    "salse": "sales",
    "saels": "sales",
    "salees": "sales",
    "saless": "sales",

    # Grocery
    "grocry": "grocery",
    "grocerry": "grocery",
    "groceryy": "grocery",
    "grocrey": "grocery",

    # Beverage
    "beverges": "beverages",
    "bevrages": "beverages",
    "bevarages": "beverages",
    "beverageses": "beverages",
    "baverages": "beverages",

    # Store
    "stroe": "store",
    "stoer": "store",
    "storr": "store",

    # Family
    "famly": "family",
    "familly": "family",
    "familiy": "family",

    # Average
    "avrage": "average",
    "averge": "average",
    "avragee": "average",

    # Maximum
    "maxmimum": "maximum",
    "maximun": "maximum",
    "maxium": "maximum",

    # Minimum
    "minumum": "minimum",
    "minimun": "minimum",
    "minmum": "minimum",

    # Highest
    "higest": "highest",
    "heighest": "highest",
    "highst": "highest",
    "high": "highest",

    # Lowest
    "lowst": "lowest",
    "loest": "lowest",
    "low": "lowest",

    # Product
    "prodcut": "product",
    "prodcuct": "product",
    "prodict": "product",

    # Compare
    "comapre": "compare",
    "compar": "compare",
    "compair": "compare",
}


# ============================================================
# CORRECT ONE WORD
# ============================================================

def correct_word(word):

    clean_word = word.lower().strip()

    if not clean_word:
        return word



    # --------------------------------------------------------
    # Do not fuzzy-match numbers or date-like values
    # --------------------------------------------------------

    if re.search(r"\d", clean_word):
        return word


    # --------------------------------------------------------
    # Direct typo dictionary
    # --------------------------------------------------------

    if clean_word in COMMON_TYPOS:

        return COMMON_TYPOS[
            clean_word
        ]


    # --------------------------------------------------------
    # Already valid word
    # --------------------------------------------------------

    if clean_word in BUSINESS_VOCABULARY:

        return clean_word


    # --------------------------------------------------------
    # Fuzzy matching
    # --------------------------------------------------------

    matches = get_close_matches(
        clean_word,
        BUSINESS_VOCABULARY,
        n=1,
        cutoff=0.80
    )


    if matches:

        return matches[0]


    return word


# ============================================================
# NORMALIZE QUESTION
# ============================================================

def normalize_question(question):

    if not question:

        return question


    # --------------------------------------------------------
    # Preserve original question
    # --------------------------------------------------------

    original_question = question


    # --------------------------------------------------------
    # Convert to lowercase
    # --------------------------------------------------------

    question = question.lower().strip()


    # --------------------------------------------------------
    # Correct individual words
    # --------------------------------------------------------

    words = question.split()

    corrected_words = []


    for word in words:



        if re.search(r"\d", word):

            corrected_words.append(word)

            continue

        # Keep punctuation separate
        clean_word = re.sub(
            r"[^\w]",
            "",
            word
        )

        punctuation = re.sub(
            r"[\w]",
            "",
            word
        )


        corrected_word = correct_word(
            clean_word
        )


        corrected_words.append(
            corrected_word + punctuation
        )


    normalized_question = " ".join(
        corrected_words
    )


    
    # Special Grocery number handling

    normalized_question = re.sub(
        r"\bgrocery\s*1\b",
        "GROCERY I",
        normalized_question,
        flags=re.IGNORECASE
    )


    normalized_question = re.sub(
        r"\bgroceries\s*1\b",
        "GROCERY I",
        normalized_question,
        flags=re.IGNORECASE
    )


    # --------------------------------------------------------
    # Return normalized question
    # --------------------------------------------------------

    return normalized_question