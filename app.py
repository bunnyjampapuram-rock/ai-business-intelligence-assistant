
import streamlit as st

from llm_tools import extract_forecast_parameters

from llm_sql_tools import (
    extract_sql_parameters,
    execute_sql_intent
)

from Tools.forecast_tool import (
    forecast_sales,
    family_mapping
)

from Tools.sql_tools import (
    get_sales_by_all_stores,
    get_sales_by_all_families
)

from router import route_question

from utils.text_normalizer import normalize_question

# ALL RAG IMPORTS

from rag_loader import load_documents
from rag_chunker import chunk_documents
from rag_embeddings import embed_documents
from rag_search import search_documents
from rag_answer import generate_rag_answer

DEBUG_MODE = True


# PAGE CONFIGURATION

st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    page_icon="🤖",
    layout="centered"
)
 


# TITLE


st.title("🤖 AI Business Intelligence Assistant")

st.write(
    "Hey dear! you can ask questions  about sales, forecasts, or company documents, I will help you with that ."
)


# here creating memory state for storing Q&A for being given and ask 
#and also parameteres memory too
if "messages" not in st.session_state:

    st.session_state.messages = []


if "forecast_parameters" not in st.session_state:

    st.session_state.forecast_parameters = {
        "store_number": None,
        "family_name": None,
        "forecast_date": None
    }


if "sql_context" not in st.session_state:

    st.session_state.sql_context = {
        "last_intent": None,
        "last_store_number": None,
        "last_family_name": None,
        "last_result": None
    }


# LOAD RAG DOCUMENTS


if "rag_embedded_chunks" not in st.session_state:

    try:

        documents = load_documents()

        chunks = chunk_documents(
            documents
        )

        embedded_chunks = embed_documents(
            chunks
        )

        st.session_state.rag_embedded_chunks = (
            embedded_chunks
        )

        if DEBUG_MODE:

            st.write(
                f"Loaded {len(documents)} documents."
            )

            st.write(
                f"Created {len(chunks)} chunks."
            )

            st.write(
                f"Created {len(embedded_chunks)} embeddings."
            )

    except Exception as e:

        st.session_state.rag_embedded_chunks = []

        if DEBUG_MODE:

            st.exception(e)



# RESET CONVERSATION

if st.button("🗑️ Reset Conversation"):

    st.session_state.messages = []

    st.session_state.forecast_parameters = {
        "store_number": None,
        "family_name": None,
        "forecast_date": None
    }

    st.session_state.sql_context = {
        "last_intent": None,
        "last_store_number": None,
        "last_family_name": None,
        "last_result": None
    }

    st.rerun()


# ============================================================
# DISPLAY PREVIOUS MESSAGES
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

user_question = st.chat_input(
    "Ask a forecast sales or sales or company policy question..."
)
    

# ============================================================
# PROCESS QUESTION
# ============================================================

if user_question:

    # ========================================================
    # NORMALIZE QUESTION
    # ========================================================

    try:

        corrected_question = normalize_question(
            user_question
        )

        if not corrected_question:

            corrected_question = user_question

        corrected_question = str(
            corrected_question
        ).strip()

        if not corrected_question:

            corrected_question = user_question

    except Exception as e:

        corrected_question = user_question

        if DEBUG_MODE:

            print(
                "Question normalization failed:"
            )

            print(e)


    # ========================================================
    # USER MESSAGE
    # ========================================================

    with st.chat_message("user"):

        st.markdown(
            user_question
        )

        if (
            corrected_question.strip().lower()
            != user_question.strip().lower()
        ):

            st.caption(
                f"💡Did you mean: **{corrected_question}**?"
            )


    # ========================================================
    # SAVE USER MESSAGE
    # ========================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )


    # ========================================================
    # ASSISTANT
    # ========================================================

    with st.chat_message("assistant"):

        try:

            # ==================================================
            # CHECK FORECAST MEMORY
            # ==================================================

            current_parameters = (
                st.session_state.forecast_parameters
            )

            forecast_in_progress = any(
                value is not None
                for value in current_parameters.values()
            )


            # ==================================================
            # ROUTING
            # ==================================================

            if forecast_in_progress:

                route = "FORECAST"

            else:

                if DEBUG_MODE:

                    st.write(
                        "🔄 Understanding your question..."
                    )

                route = route_question(
                    corrected_question
                )

                route = str(
                    route
                ).strip().upper()


            # ==================================================
            # DEBUG ROUTE
            # ==================================================

            if DEBUG_MODE:

                st.write(
                    f"Route: **{route}**"
                )


            # ==================================================
            # FORECAST ROUTE
            # ==================================================

            if route == "FORECAST":

                if DEBUG_MODE:

                    st.write(
                        "🔄 Understanding your forecast request..."
                    )


                # ------------------------------------------------
                # EXTRACT FORECAST PARAMETERS
                # ------------------------------------------------

                parameters = extract_forecast_parameters(
                    corrected_question
                )


                if DEBUG_MODE:

                    st.write(
                        "Parameters extracted:"
                    )

                    st.json(
                        parameters
                    )


                # ------------------------------------------------
                # GET OLD PARAMETERS
                # ------------------------------------------------

                old_parameters = (
                    st.session_state.forecast_parameters
                )


                # ------------------------------------------------
                # UPDATE PARAMETERS
                # ------------------------------------------------

                for key in (
                    "store_number",
                    "family_name",
                    "forecast_date"
                ):

                    value = parameters.get(
                        key
                    )

                    if value is not None:

                        old_parameters[key] = value


                st.session_state.forecast_parameters = (
                    old_parameters
                )


                # ------------------------------------------------
                # READ PARAMETERS
                # ------------------------------------------------

                store_number = old_parameters.get(
                    "store_number"
                )

                family_name = old_parameters.get(
                    "family_name"
                )

                forecast_date = old_parameters.get(
                    "forecast_date"
                )


                # ------------------------------------------------
                # CHECK MISSING INFORMATION
                # ------------------------------------------------

                missing = []


                if store_number is None:

                    missing.append(
                        "store number"
                    )


                if family_name is None:

                    missing.append(
                        "product family"
                    )


                if forecast_date is None:

                    missing.append(
                        "forecast date"
                    )


                # ------------------------------------------------
                # ASK FOR MISSING INFORMATION
                # ------------------------------------------------

                if missing:

                    answer = (
                        "I need the following information: "
                        + ", ".join(missing)
                        + "."
                    )

                    st.warning(
                        answer
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                    st.stop()


                # ------------------------------------------------
                # RUN FORECAST
                # ------------------------------------------------

                if DEBUG_MODE:

                    st.write(
                        "🔄 Running sales forecast..."
                    )


                prediction = forecast_sales(
                    store_number,
                    family_name,
                    forecast_date
                )


                if prediction is None:

                    raise ValueError(
                        "Forecast function returned None."
                    )


                # ------------------------------------------------
                # FORECAST ANSWER
                # ------------------------------------------------

                answer = f"""
### 📈 Sales Forecast

**Store:** {store_number}

**Product Family:** {family_name}

**Forecast Date:** {forecast_date}

### Predicted Sales

# {float(prediction):,.2f}
"""


                st.markdown(
                    answer
                )


                st.metric(
                    "Predicted Sales",
                    f"{float(prediction):,.2f}"
                )


                # ------------------------------------------------
                # SAVE ANSWER
                # ------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )


                
                # CLEAR FORECAST MEMORY
                

                st.session_state.forecast_parameters = {
                    "store_number": None,
                    "family_name": None,
                    "forecast_date": None
                }


            
            # SQL ROUTE
            

            elif route == "SQL":

                if DEBUG_MODE:

                    st.write(
                        "🔄 Understanding your business question..."
                    )


            
                # EXTRACT SQL PARAMETERS
                
                sql_parameters = extract_sql_parameters(
                    corrected_question
                )


                if DEBUG_MODE:

                    st.write(
                        "SQL parameters:"
                    )

                    st.json(
                        sql_parameters
                    )


                # ------------------------------------------------
                # EXECUTE SQL INTENT
                # ------------------------------------------------

                if DEBUG_MODE:

                    st.write(
                        "🔄 Analyzing sales data..."
                    )


                result = execute_sql_intent(
                    sql_parameters
                )


                # ------------------------------------------------
                # SAVE SQL CONTEXT
                # ------------------------------------------------

                st.session_state.sql_context = {
                    "last_intent": sql_parameters.get(
                        "intent"
                    ),

                    "last_store_number": sql_parameters.get(
                        "store_number"
                    ),

                    "last_family_name": sql_parameters.get(
                        "family_name"
                    ),

                    "last_result": result
                }


                # ------------------------------------------------
                # GET INTENT
                # ------------------------------------------------

                intent = sql_parameters.get(
                    "intent"
                )


                # ==================================================
                # TOTAL SALES
                # ==================================================

                if intent == "TOTAL_SALES":

                    answer = f"""
### 💰 Total Sales

**Total Sales:** {float(result):,.2f}
"""

                    st.markdown(
                        answer
                    )

                    st.metric(
                        "Total Sales",
                        f"{float(result):,.2f}"
                    )


                # ==================================================
                # AVERAGE SALES
                # ==================================================

                elif intent == "AVERAGE_SALES":

                    answer = f"""
### 📊 Average Sales

**Average Sales:** {float(result):,.2f}
"""

                    st.markdown(
                        answer
                    )

                    st.metric(
                        "Average Sales",
                        f"{float(result):,.2f}"
                    )


                # ==================================================
                # MAX SALES
                # ==================================================

                elif intent == "MAX_SALES":

                    answer = f"""
### 📈 Maximum Sales

**Maximum Sales:** {float(result):,.2f}
"""

                    st.markdown(
                        answer
                    )

                    st.metric(
                        "Maximum Sales",
                        f"{float(result):,.2f}"
                    )


                # ==================================================
                # MIN SALES
                # ==================================================

                elif intent == "MIN_SALES":

                    answer = f"""
### 📉 Minimum Sales

**Minimum Sales:** {float(result):,.2f}
"""

                    st.markdown(
                        answer
                    )

                    st.metric(
                        "Minimum Sales",
                        f"{float(result):,.2f}"
                    )


                # ==================================================
                # TOP STORE
                # ==================================================

                elif intent == "TOP_STORE":

                    store_number, sales = result

                    answer = f"""
### 🏆 Top Performing Store

**Store:** {int(store_number)}

**Total Sales:** {float(sales):,.2f}
"""

                    st.markdown(
                        answer
                    )


                    st.subheader(
                        "📊 Top Stores by Sales"
                    )


                    store_data = (
                        get_sales_by_all_stores()
                    )


                    top_stores = (
                        store_data
                        .head(10)
                        .sort_values(
                            ascending=True
                        )
                    )


                    st.bar_chart(
                        top_stores
                    )


                # ==================================================
                # TOP FAMILY
                # ==================================================

                elif intent == "TOP_FAMILY":

                    family_name, sales = result

                    answer = f"""
### 🏆 Top Product Family

**Product Family:** {family_name}

**Total Sales:** {float(sales):,.2f}
"""

                    st.markdown(
                        answer
                    )


                    st.subheader(
                        "📊 Top Product Families by Sales"
                    )


                    family_data = (
                        get_sales_by_all_families()
                    )


                    top_families = (
                        family_data
                        .head(10)
                        .sort_values(
                            ascending=True
                        )
                    )


                    st.bar_chart(
                        top_families
                    )


                # ==================================================
                # STORE SALES
                # ==================================================

                elif intent == "STORE_SALES":

                    store_number = (
                        sql_parameters.get(
                            "store_number"
                        )
                    )


                    answer = f"""
### 🏪 Store Sales

**Store:** {store_number}

**Total Sales:** {float(result):,.2f}
"""

                    st.markdown(
                        answer
                    )


                    st.metric(
                        "Store Sales",
                        f"{float(result):,.2f}"
                    )


                    st.subheader(
                        "📊 Store Sales Comparison"
                    )


                    store_data = (
                        get_sales_by_all_stores()
                    )


                    top_stores = (
                        store_data
                        .head(10)
                    )


                    requested_store = int(
                        store_number
                    )


                    chart_data = (
                        top_stores.copy()
                    )


                    if (
                        requested_store
                        not in chart_data.index
                    ):

                        if (
                            requested_store
                            in store_data.index
                        ):

                            requested_sales = (
                                store_data.loc[
                                    requested_store
                                ]
                            )

                        else:

                            requested_sales = (
                                float(result)
                            )


                        chart_data.loc[
                            requested_store
                        ] = requested_sales


                    chart_data = (
                        chart_data
                        .sort_values(
                            ascending=True
                        )
                    )


                    st.bar_chart(
                        chart_data
                    )


                # ==================================================
                # FAMILY SALES
                # ==================================================

                elif intent == "FAMILY_SALES":

                    family_name = (
                        sql_parameters.get(
                            "family_name"
                        )
                    )


                    answer = f"""
### 🛒 Product Family Sales

**Product Family:** {family_name}

**Total Sales:** {float(result):,.2f}
"""

                    st.markdown(
                        answer
                    )


                    st.metric(
                        "Family Sales",
                        f"{float(result):,.2f}"
                    )


                    # ------------------------------------------------
                    # FAMILY COMPARISON
                    # ------------------------------------------------

                    st.subheader(
                        "📊 Product Family Sales Comparison"
                    )


                    family_data = (
                        get_sales_by_all_families()
                    )


                    top_families = (
                        family_data
                        .head(10)
                    )


                    requested_family = (
                        str(family_name)
                        .upper()
                        .strip()
                    )


                    chart_data = (
                        top_families.copy()
                    )


                    matching_family = None


                    for name in family_data.index:

                        if (
                            str(name)
                            .upper()
                            .strip()
                            == requested_family
                        ):

                            matching_family = name

                            break


                    if (
                        matching_family is not None
                        and matching_family
                        not in chart_data.index
                    ):

                        chart_data.loc[
                            matching_family
                        ] = family_data.loc[
                            matching_family
                        ]


                    chart_data = (
                        chart_data
                        .sort_values(
                            ascending=True
                        )
                    )


                    st.bar_chart(
                        chart_data
                    )


                # ==================================================
                # MONTHLY SALES
                # ==================================================

                elif intent == "MONTHLY_SALES":

                    family_name = (
                        sql_parameters.get(
                            "family_name"
                        )
                    )


                    if family_name is not None:

                        answer = f"""
### 📊 Monthly Sales — {family_name}

Here are the monthly sales for **{family_name}**.
"""

                    else:

                        answer = """
### 📊 Monthly Sales

Here are the overall monthly sales.
"""


                    st.markdown(
                        answer
                    )


                    monthly_data = (
                        result.copy()
                    )


                    monthly_data = (
                        monthly_data.rename(
                            "Sales"
                        )
                    )


                    st.dataframe(
                        monthly_data,
                        use_container_width=True
                    )


                    st.subheader(
                        "📈 Monthly Sales Trend"
                    )


                    chart_data = (
                        result.copy()
                    )


                    chart_data.index.name = (
                        "Month"
                    )


                    st.line_chart(
                        chart_data
                    )


                # ==================================================
                # ALL FAMILY SALES
                # ==================================================

                elif intent == "FAMILY_SALES_ALL":

                    st.subheader(
                        "🛒 Sales by Product Family"
                    )


                    family_data = (
                        get_sales_by_all_families()
                    )


                    st.dataframe(
                        family_data.rename(
                            "Total Sales"
                        ),
                        use_container_width=True
                    )


                    st.subheader(
                        "📊 Sales by Product Family"
                    )


                    chart_data = (
                        family_data
                        .sort_values(
                            ascending=True
                        )
                    )


                    st.bar_chart(
                        chart_data
                    )


                    answer = """
### 🛒 Sales by Product Family

The chart above shows total sales for each product family.
"""


                    st.markdown(
                        answer
                    )


                # ==================================================
                # ALL STORE SALES
                # ==================================================

                elif intent == "STORE_SALES_ALL":

                    st.subheader(
                        "🏪 Sales by Store"
                    )


                    store_data = (
                        get_sales_by_all_stores()
                    )


                    st.dataframe(
                        store_data.rename(
                            "Total Sales"
                        ),
                        use_container_width=True
                    )


                    st.subheader(
                        "📊 Sales by Store"
                    )


                    chart_data = (
                        store_data
                        .sort_values(
                            ascending=True
                        )
                    )


                    st.bar_chart(
                        chart_data
                    )


                    answer = """
### 🏪 Sales by Store

The chart above shows total sales for every store.
"""


                    st.markdown(
                        answer
                    )


                # ==================================================
                # UNKNOWN SQL
                # ==================================================

                else:

                    answer = f"""
### 📊 Sales Analysis

Result:

**{result}**
"""

                    st.markdown(
                        answer
                    )


                # ==================================================
                # SAVE SQL ANSWER
                # ==================================================

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )


            # ==================================================
            # RAG ROUTE
            # ==================================================

            elif route == "RAG":

                if DEBUG_MODE:

                    st.write(
                        "🔄 Searching company documents..."
                    )


                # ------------------------------------------------
                # GET EMBEDDED DOCUMENTS
                # ------------------------------------------------

                embedded_chunks = (
                    st.session_state.rag_embedded_chunks
                )


                # ------------------------------------------------
                # CHECK RAG DATA
                # ------------------------------------------------

                if not embedded_chunks:

                    raise ValueError(
                        "No RAG documents or embeddings are available."
                    )


                # ------------------------------------------------
                # SEARCH DOCUMENTS
                # ------------------------------------------------

                results = search_documents(
                    corrected_question,
                    embedded_chunks
                )


                if DEBUG_MODE:

                    st.write(
                        "Relevant document chunks:"
                    )

                    st.json(
                        results
                    )


                # ------------------------------------------------
                # GENERATE ANSWER
                # ------------------------------------------------

                answer = generate_rag_answer(
                    corrected_question,
                    results
                )


                # ------------------------------------------------
                # DISPLAY ANSWER
                # ------------------------------------------------

                st.markdown(
                    answer
                )


                # ------------------------------------------------
                # OPTIONAL SOURCE INFORMATION
                # ------------------------------------------------

                if DEBUG_MODE and results:

                    st.caption(
                        "📚 Source: "
                        + str(
                            results[0].get(
                                "filename",
                                "Unknown"
                            )
                        )
                    )


                # ------------------------------------------------
                # SAVE ANSWER
                # ------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )


            # ==================================================
            # UNKNOWN ROUTE
            # ==================================================

            else:

                answer = """
I'm not sure how to handle that question yet.

You can ask me about:

- 📈 Sales forecasting
- 💰 Historical sales
- 🏪 Store performance
- 🛒 Product family sales
- 📊 Sales visualizations
- 📚 Company documents and policies
"""

                st.markdown(
                    answer
                )


                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )


        # ======================================================
        # ERROR HANDLING
        # ======================================================

        except Exception as e:

            error_message = (
                "❌ Something went wrong.\n\n"
                f"**Error:** `{str(e)}`"
            )


            st.error(
                "❌ Something went wrong."
            )


            if DEBUG_MODE:

                st.exception(
                    e
                )


            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message
                }
            )
