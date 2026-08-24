import requests
import json
import re
import os

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "https://ollama.com/api/chat"
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "llama3.2"
)

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

BUSINESS_FAMILIES = [
    "BEVERAGES",
    "GROCERY I",
    "GROCERY II",
    "DAIRY",
    "MEATS",
    "PRODUCE",
    "SEAFOOD",
    "POULTRY",
    "PERSONAL CARE",
    "PET SUPPLIES",
    "TOYS",
    "BOOKS",
    "BEAUTY",
    "AUTOMOTIVE",
    "BABY CARE",
    "BREAD/BAKERY",
    "DELI",
    "EGGS",
    "FROZEN FOODS",
    "HARDWARE",
    "LADIESWEAR",
    "LIQUOR,WINE,BEER",
    "PLAY",
    "PREPARED FOODS",
]


def extract_forecast_parameters(question):

    detected_family = None

    question_upper = str(question).upper()

    for family in BUSINESS_FAMILIES:

        if family in question_upper:

            detected_family = family
            break

        if re.search(
            r"\bgrocery\s*(1|one|i)\b",
            question_upper
        ):

            detected_family = "GROCERY I"

        elif re.search(
            r"\bgrocery\s*(2|two|ii)\b",
            question_upper
        ):

            detected_family = "GROCERY II"

    prompt = f"""
You are a sales forecasting parameter extraction system.

Extract ONLY information that the user explicitly provides.

We need exactly these three fields:

1. store_number
2. family_name
3. forecast_date

IMPORTANT RULES:

- NEVER guess a store number.
- NEVER use today's date.
DATE RULES:

- If the user provides an exact date, convert it to YYYY-MM-DD.
- If the user says "tomorrow", "today", "next day", etc., do NOT return those words.
- For this sales forecasting dataset, the latest available historical date is 2017-08-15.
- Therefore:
  "tomorrow" = "2017-08-16"
  "next day" = "2017-08-16"
- If the user does not provide any date or relative date, return null.
- NEVER invent an unrelated date.
- If the user does not provide a store number, return null.
- If the user does not provide a product family, return null.
- "grocery 1", "grocery one", and "grocery i" mean "GROCERY I".
- Return ONLY ONE JSON object.
- Do NOT explain anything.
- Do NOT return markdown.

Example 1:

User:
Predict sales for store 44 GROCERY I on September 1 2017

Output:
{{"store_number":44,"family_name":"GROCERY I","forecast_date":"2017-09-01"}}

Example 2:

User:
Predict sales for GROCERY I

Output:
{{"store_number":null,"family_name":"GROCERY I","forecast_date":null}}

Example 3:

User:
Predict sales for store 44

Output:
{{"store_number":44,"family_name":null,"forecast_date":null}}

Example 4:

User:
Predict sales for grocery 1 on September 1 2017

Output:
{{"store_number":null,"family_name":"GROCERY I","forecast_date":"2017-09-01"}}

USER QUESTION:
{question}
"""


    payload = {
        "model": MODEL_NAME,

        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],

        "stream": False,
        'format':'json'
    }


    # ========================================================
    # SEND REQUEST
    # ========================================================

    response = requests.post(
    OLLAMA_URL,
    json=payload,
    headers={
        "Authorization": f"Bearer {OLLAMA_API_KEY}"
    }
)
    response.raise_for_status()


    # ========================================================
    # GET RESPONSE
    # ========================================================

    result = response.json()

    answer = result["message"]["content"]
    question_lower = question.lower()

    family_keywords = [
        "beverages",
        "grocery",
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
        "school and office supplies",
        "seafood",
        "toys"
    ]

    family_mentioned = any(
         family in question_lower
        for family in family_keywords
    )

    print("\n==============================")
    print("OLLAMA RESPONSE")
    print("==============================")
    print(answer)


    # ========================================================
    # EXTRACT JSON
    # ========================================================

    match = re.search(
        r'\{.*?\}',
        answer,
        re.DOTALL
    )
    

    if not match:

        raise ValueError(
            "Ollama did not return a valid JSON object.\n\n"
            f"Ollama response:\n{answer}"
        )


    json_text = match.group(0)


    # ========================================================
    # PARSE JSON
    # ========================================================

    try:

        parameters = json.loads(json_text)

    except json.JSONDecodeError as e:

        raise ValueError(
            "Could not parse Ollama response as JSON.\n\n"
            f"Extracted JSON:\n{json_text}"
        ) from e


    if not family_mentioned:
        parameters["family_name"] = None


    # ========================================================
    # NORMALIZE FAMILY NAME
    # ========================================================

    family_name = parameters.get("family_name")


    if family_name:

        family_name = family_name.upper().strip()


        if family_name in [
            "GROCERY 1",
            "GROCERY ONE"
        ]:

            family_name = "GROCERY I"


        parameters["family_name"] = family_name




    # ========================================================
    # DIRECT FAMILY DETECTION OVERRIDE
    # ========================================================

    if detected_family is not None:

        parameters["family_name"] = detected_family



    # ========================================================
    # RETURN
    # ========================================================

    print("\nEXTRACTED PARAMETERS:")
    print(parameters)

    return parameters