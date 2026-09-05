import pandas as pd


def generate_insights(df, statistics):

    insights = []

    # =====================================================
    # 1. DATASET OVERVIEW
    # =====================================================

    insights.append({
        "type": "overview",
        "message": (
            f"The dataset contains {len(df)} rows "
            f"and {len(df.columns)} columns."
        )
    })

    # =====================================================
    # 2. NUMERICAL INSIGHTS
    # =====================================================

    descriptive = statistics.get(
        "descriptive_statistics",
        {}
    )

    for column, values in descriptive.items():

        maximum = values.get("maximum")
        minimum = values.get("minimum")
        mean = values.get("mean")

        if maximum is not None:

            insights.append({
                "type": "maximum",
                "column": column,
                "value": maximum,
                "message": (
                    f"{column} has a maximum value of "
                    f"{maximum:,.2f}."
                )
            })

        if minimum is not None:

            insights.append({
                "type": "minimum",
                "column": column,
                "value": minimum,
                "message": (
                    f"{column} has a minimum value of "
                    f"{minimum:,.2f}."
                )
            })

        if (
            mean is not None
            and maximum is not None
            and maximum > mean * 1.5
        ):

            insights.append({
                "type": "variation",
                "column": column,
                "message": (
                    f"{column} shows significant variation "
                    f"because its maximum value is considerably "
                    f"higher than its average."
                )
            })

    # =====================================================
    # 3. CORRELATION INSIGHTS
    # =====================================================

    correlations = statistics.get(
        "correlations",
        {}
    )

    processed_pairs = set()

    for column, values in correlations.items():

        if not isinstance(values, dict):
            continue

        for other_column, correlation in values.items():

            if column == other_column:
                continue

            pair = tuple(
                sorted([column, other_column])
            )

            if pair in processed_pairs:
                continue

            processed_pairs.add(pair)

            if not isinstance(
                correlation,
                (int, float)
            ):
                continue

            if correlation >= 0.8:

                insights.append({
                    "type": "correlation",
                    "columns": [
                        column,
                        other_column
                    ],
                    "correlation": correlation,
                    "message": (
                        f"{column} and {other_column} have "
                        f"a strong positive relationship "
                        f"with a correlation of "
                        f"{correlation:.3f}."
                    )
                })

            elif correlation <= -0.8:

                insights.append({
                    "type": "correlation",
                    "columns": [
                        column,
                        other_column
                    ],
                    "correlation": correlation,
                    "message": (
                        f"{column} and {other_column} have "
                        f"a strong negative relationship "
                        f"with a correlation of "
                        f"{correlation:.3f}."
                    )
                })

    # =====================================================
    # 4. CATEGORY PERFORMANCE
    # =====================================================

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns

    for category_column in categorical_columns:

        # Avoid processing columns with too many categories
        if df[category_column].nunique() > 20:
            continue

        for numerical_column in numerical_columns:

            try:

                grouped = (
                    df.groupby(category_column)[
                        numerical_column
                    ]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                )

            except Exception:
                continue

            if grouped.empty:
                continue

            best_category = grouped.index[0]
            best_value = grouped.iloc[0]

            insights.append({
                "type": "category_performance",
                "category_column": category_column,
                "value_column": numerical_column,
                "category": str(best_category),
                "value": float(best_value),
                "message": (
                    f"{best_category} has the highest total "
                    f"{numerical_column} among "
                    f"{category_column} categories, "
                    f"with a value of "
                    f"{best_value:,.2f}."
                )
            })

    return insights