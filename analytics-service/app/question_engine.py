import pandas as pd


# ============================================================
# QUESTION ENGINE
# ============================================================

def understand_question(question: str, df: pd.DataFrame):

    q = question.lower().strip()

    # --------------------------------------------------------
    # Find important columns
    # --------------------------------------------------------

    numeric_columns = [
        col
        for col in df.columns
        if pd.api.types.is_numeric_dtype(df[col])
    ]

    categorical_columns = [
        col
        for col in df.columns
        if not pd.api.types.is_numeric_dtype(df[col])
    ]

    # --------------------------------------------------------
    # Detect metric
    # --------------------------------------------------------

    metric = None

    if "sales" in q:

        metric = next(
            (
                col for col in numeric_columns
                if "sales" in col.lower()
            ),
            None
        )

    elif "profit" in q:

        metric = next(
            (
                col for col in numeric_columns
                if "profit" in col.lower()
            ),
            None
        )

    # --------------------------------------------------------
    # Detect category
    # --------------------------------------------------------

    category = None

    for column in categorical_columns:

        if column.lower() in q:

            category = column
            break

    # Also support common natural-language terms

    if category is None:

        if "product" in q:

            category = next(
                (
                    col for col in df.columns
                    if col.lower() == "product"
                ),
                None
            )

        elif "region" in q:

            category = next(
                (
                    col for col in df.columns
                    if col.lower() == "region"
                ),
                None
            )

        elif "date" in q:

            category = next(
                (
                    col for col in df.columns
                    if col.lower() == "date"
                ),
                None
            )

    # --------------------------------------------------------
    # Detect intent
    # --------------------------------------------------------

    intent = "unknown"

    # Highest / best
    if (
        "highest" in q
        or "maximum" in q
        or "max" in q
        or "best" in q
        or "top" in q
    ):

        if category and metric:

            intent = "highest_category"

        elif metric:

            intent = "maximum"

    # Lowest / worst
    elif (
        "lowest" in q
        or "minimum" in q
        or "min" in q
        or "worst" in q
    ):

        if category and metric:

            intent = "lowest_category"

        elif metric:

            intent = "minimum"

    # Average
    elif (
        "average" in q
        or "mean" in q
    ):

        intent = "average"

    # Total
    elif (
        "total" in q
        or "sum" in q
        or "overall" in q
    ):

        intent = "total"

    # Correlation / relationship
    elif (
        "correlation" in q
        or "relationship" in q
        or "related" in q
    ):

        intent = "correlation"

    # Dataset information
    elif (
        "how many rows" in q
        or "number of rows" in q
        or "rows" in q
        or "columns" in q
        or "dataset size" in q
    ):

        intent = "dataset_info"

    # --------------------------------------------------------
    # Return structured understanding
    # --------------------------------------------------------

    return {

        "intent": intent,

        "metric": metric,

        "category": category,

        "question": question

    }


# ============================================================
# ANALYZE QUESTION
# ============================================================

def analyze_question(question: str, df: pd.DataFrame):

    understanding = understand_question(
        question,
        df
    )

    intent = understanding["intent"]
    metric = understanding["metric"]
    category = understanding["category"]

    # --------------------------------------------------------
    # DATASET INFORMATION
    # --------------------------------------------------------

    if intent == "dataset_info":

        return {

            "intent": intent,

            "result": {

                "rows": len(df),

                "columns": len(df.columns),

                "column_names": list(df.columns)

            }

        }

    # --------------------------------------------------------
    # TOTAL
    # --------------------------------------------------------

    if intent == "total":

        if not metric:

            return {

                "intent": intent,

                "error": "No numerical metric was detected."

            }

        value = df[metric].sum()

        return {

            "intent": intent,

            "metric": metric,

            "value": float(value)

        }

    # --------------------------------------------------------
    # AVERAGE
    # --------------------------------------------------------

    if intent == "average":

        if not metric:

            return {

                "intent": intent,

                "error": "No numerical metric was detected."

            }

        value = df[metric].mean()

        return {

            "intent": intent,

            "metric": metric,

            "value": float(value)

        }

    # --------------------------------------------------------
    # MAXIMUM
    # --------------------------------------------------------

    if intent == "maximum":

        if not metric:

            return {

                "intent": intent,

                "error": "No numerical metric was detected."

            }

        value = df[metric].max()

        return {

            "intent": intent,

            "metric": metric,

            "value": float(value)

        }

    # --------------------------------------------------------
    # MINIMUM
    # --------------------------------------------------------

    if intent == "minimum":

        if not metric:

            return {

                "intent": intent,

                "error": "No numerical metric was detected."

            }

        value = df[metric].min()

        return {

            "intent": intent,

            "metric": metric,

            "value": float(value)

        }

    # --------------------------------------------------------
    # HIGHEST CATEGORY
    # --------------------------------------------------------

    if intent == "highest_category":

        if not category or not metric:

            return {

                "intent": intent,

                "error": (
                    "Could not determine category "
                    "and numerical metric."
                )

            }

        grouped = (
            df.groupby(category)[metric]
            .sum()
            .sort_values(ascending=False)
        )

        best_category = grouped.index[0]

        best_value = grouped.iloc[0]

        return {

            "intent": intent,

            "category": category,

            "metric": metric,

            "category_value": str(best_category),

            "value": float(best_value)

        }

    # --------------------------------------------------------
    # LOWEST CATEGORY
    # --------------------------------------------------------

    if intent == "lowest_category":

        if not category or not metric:

            return {

                "intent": intent,

                "error": (
                    "Could not determine category "
                    "and numerical metric."
                )

            }

        grouped = (
            df.groupby(category)[metric]
            .sum()
            .sort_values(ascending=True)
        )

        lowest_category = grouped.index[0]

        lowest_value = grouped.iloc[0]

        return {

            "intent": intent,

            "category": category,

            "metric": metric,

            "category_value": str(lowest_category),

            "value": float(lowest_value)

        }

    # --------------------------------------------------------
    # CORRELATION
    # --------------------------------------------------------

    if intent == "correlation":

        numeric_df = df.select_dtypes(
            include="number"
        )

        if len(numeric_df.columns) < 2:

            return {

                "intent": intent,

                "error": (
                    "At least two numerical "
                    "columns are required."
                )

            }

        correlation = numeric_df.corr()

        return {

            "intent": intent,

            "correlation": correlation.to_dict()

        }

    # --------------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------------

    return {

        "intent": "unknown",

        "error": (
            "I could not understand the question. "
            "Try asking about sales, profit, products, "
            "regions, averages, totals, maximum, "
            "minimum, or correlations."
        )

    }