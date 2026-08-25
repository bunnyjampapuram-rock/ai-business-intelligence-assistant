import pandas as pd

from Tools.forecast_tool import family_mapping


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(
    "data/train_cleaned.csv"
)


# ============================================================
# TOTAL SALES
# ============================================================

def get_total_sales():

    total_sales = df["sales"].sum()

    return total_sales


# ============================================================
# AVERAGE SALES
# ============================================================

def get_average_sales():

    average_sales = df["sales"].mean()

    return average_sales


# ============================================================
# MAXIMUM SALES
# ============================================================

def get_max_sales():

    max_sales = df["sales"].max()

    return max_sales


# ============================================================
# MINIMUM SALES
# ============================================================

def get_min_sales():

    min_sales = df["sales"].min()

    return min_sales


# ============================================================
# SALES BY STORE
# ============================================================

def get_sales_by_store(store_number):

    history = df[
        df["store_nbr"] == store_number
    ]

    if history.empty:
        return 0

    total_sales = history["sales"].sum()

    return total_sales


# ============================================================
# SALES BY PRODUCT FAMILY
# ============================================================

def get_sales_by_family(family_number):

    history = df[
        df["family"] == family_number
    ]

    if history.empty:
        return 0

    total_sales = history["sales"].sum()

    return total_sales


# ============================================================
# HIGHEST SALES STORE
# ============================================================

def get_top_store():

    store_sales = (
        df.groupby("store_nbr")["sales"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    top_store = store_sales.index[0]

    top_sales = store_sales.iloc[0]

    return top_store, top_sales


# ============================================================
# HIGHEST SALES PRODUCT FAMILY
# ============================================================

def get_top_family():

    family_sales = (
        df.groupby("family")["sales"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    top_family_number = family_sales.index[0]

    top_sales = family_sales.iloc[0]

    # --------------------------------------------------------
    # REVERSE FAMILY MAPPING
    # --------------------------------------------------------

    reverse_family_mapping = {

        int(number): name

        for name, number
        in family_mapping.items()

    }

    top_family_name = (
        reverse_family_mapping.get(
            int(top_family_number),
            f"Family {top_family_number}"
        )
    )

    return top_family_name, top_sales


# ============================================================
# MONTHLY SALES
# ============================================================

def get_monthly_sales(
    family_number=None
):

    temp_df = df.copy()

    # --------------------------------------------------------
    # CONVERT DATE
    # --------------------------------------------------------

    temp_df["date"] = pd.to_datetime(
        temp_df["date"]
    )

    # --------------------------------------------------------
    # FILTER FAMILY IF PROVIDED
    # --------------------------------------------------------

    if family_number is not None:

        temp_df = temp_df[
            temp_df["family"] == family_number
        ]

    # --------------------------------------------------------
    # GROUP BY MONTH
    # --------------------------------------------------------

    monthly_sales = (
        temp_df
        .groupby(
            temp_df["date"].dt.to_period("M")
        )["sales"]
        .sum()
    )

    # --------------------------------------------------------
    # PERIOD -> STRING
    # --------------------------------------------------------

    monthly_sales.index = (
        monthly_sales.index
        .astype(str)
    )

    return monthly_sales


# ============================================================
# MONTHLY SALES BY STORE
# ============================================================

def get_monthly_sales_by_store(
    store_number
):

    temp_df = df.copy()

    temp_df["date"] = pd.to_datetime(
        temp_df["date"]
    )

    history = temp_df[
        temp_df["store_nbr"] == store_number
    ]

    monthly_sales = (
        history
        .groupby(
            history["date"].dt.to_period("M")
        )["sales"]
        .sum()
    )

    monthly_sales.index = (
        monthly_sales.index
        .astype(str)
    )

    return monthly_sales


# ============================================================
# MONTHLY SALES BY PRODUCT FAMILY
# ============================================================

def get_monthly_sales_by_family(
    family_number
):

    return get_monthly_sales(
        family_number
    )


# ============================================================
# SALES BY ALL STORES
# ============================================================

def get_sales_by_all_stores():

    result = (
        df.groupby("store_nbr")["sales"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    return result



# ============================================================
# SALES BY STORE AND PRODUCT FAMILY
# ============================================================

def get_sales_by_store_family(store_number, family_name):

    result = df[
        (df["store_nbr"] == int(store_number)) &
        (df["family"].str.upper() == family_name.upper())
    ]["sales"].sum()

    return result


# ============================================================
# SALES BY ALL PRODUCT FAMILIES
# ============================================================

def get_sales_by_all_families():

    family_sales = (
        df.groupby("family")["sales"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    # --------------------------------------------------------
    # REVERSE FAMILY MAPPING
    # --------------------------------------------------------

    reverse_family_mapping = {

        int(number): name

        for name, number
        in family_mapping.items()

    }

    # --------------------------------------------------------
    # CONVERT FAMILY NUMBERS -> FAMILY NAMES
    # --------------------------------------------------------

    new_index = []

    for family_number in family_sales.index:

        family_name = (
            reverse_family_mapping.get(
                int(family_number)
            )
        )

        if family_name is None:

            family_name = (
                f"Family {family_number}"
            )

        new_index.append(
            family_name
        )

    family_sales.index = new_index

    return family_sales


# ============================================================
# RUN SQL QUESTION
# ============================================================

def run_sql_question(question):

    """
    Simple fallback SQL question handler.

    The main application should normally use:

        extract_sql_parameters()
        execute_sql_intent()

    """

    question_lower = (
        question
        .lower()
        .strip()
    )


    # ========================================================
    # TOTAL SALES
    # ========================================================

    if (
        "total sales" in question_lower
        or "overall sales" in question_lower
        or "how much did we sell" in question_lower
    ):

        return get_total_sales()


    # ========================================================
    # AVERAGE SALES
    # ========================================================

    elif (
        "average sales" in question_lower
        or "avg sales" in question_lower
        or "mean sales" in question_lower
    ):

        return get_average_sales()


    # ========================================================
    # MAXIMUM SALES
    # ========================================================

    elif (
        "maximum sales" in question_lower
        or "max sales" in question_lower
        or "highest sale" in question_lower
    ):

        return get_max_sales()


    # ========================================================
    # MINIMUM SALES
    # ========================================================

    elif (
        "minimum sales" in question_lower
        or "min sales" in question_lower
        or "lowest sale" in question_lower
    ):

        return get_min_sales()


    # ========================================================
    # TOP STORE
    # ========================================================

    elif (
        "top store" in question_lower
        or "best store" in question_lower
        or "store sold the most" in question_lower
        or "highest selling store" in question_lower
    ):

        return get_top_store()


    # ========================================================
    # TOP FAMILY
    # ========================================================

    elif (
        "top family" in question_lower
        or "best family" in question_lower
        or "family sold the most" in question_lower
        or "highest selling family" in question_lower
    ):

        return get_top_family()


    # ========================================================
    # ALL FAMILY SALES
    # ========================================================

    elif (
        "sales by family" in question_lower
        or "sales by families" in question_lower
        or "sales by product family" in question_lower
        or "sales for all families" in question_lower
        or "sales for each family" in question_lower
    ):

        return get_sales_by_all_families()


    # ========================================================
    # MONTHLY SALES
    # ========================================================

    elif (
        "monthly sales" in question_lower
        or "sales by month" in question_lower
        or "sales month wise" in question_lower
        or "month wise sales" in question_lower
        or "monthly sales trend" in question_lower
        or "sales for each month" in question_lower
    ):

        return get_monthly_sales()


    # ========================================================
    # UNKNOWN
    # ========================================================

    else:

        return None