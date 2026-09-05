import pandas as pd


def recommend_charts(df: pd.DataFrame):

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    recommendations = []

    # --------------------------------------------
    # 1. Categorical + Numerical → Bar Chart
    # --------------------------------------------

    for category in categorical_columns:

        cardinality = df[category].nunique(
            dropna=True
        )

        if cardinality == 0 or cardinality > 20:
            continue

        for numerical in numerical_columns:

            score = 0.0
            reasons = []

            score += 0.35
            reasons.append(
                "categorical column suitable for grouping"
            )

            score += 0.35
            reasons.append(
                "numerical column suitable for measurement"
            )

            score += 0.20
            reasons.append(
                "category has manageable cardinality"
            )

            score += 0.10
            reasons.append(
                "numerical values can be aggregated"
            )

            recommendations.append({
                "chart_type": "bar",
                "x_column": category,
                "y_column": numerical,
                "score": round(score, 2),
                "reason": reasons
            })

    # --------------------------------------------
    # 2. Numerical + Numerical → Scatter Plot
    # --------------------------------------------

    for i in range(len(numerical_columns)):

        for j in range(i + 1, len(numerical_columns)):

            x_column = numerical_columns[i]
            y_column = numerical_columns[j]

            score = 0.0
            reasons = []

            score += 0.40

            reasons.append(
                "both columns are numerical"
            )

            correlation = df[
                [x_column, y_column]
            ].corr().iloc[0, 1]

            if pd.notna(correlation):

                if abs(correlation) >= 0.7:

                    score += 0.30

                    reasons.append(
                        "strong relationship detected"
                    )

                elif abs(correlation) >= 0.4:

                    score += 0.20

                    reasons.append(
                        "moderate relationship detected"
                    )

                else:

                    score += 0.10

                    reasons.append(
                        "numerical relationship can be explored"
                    )

            score += 0.30

            recommendations.append({
                "chart_type": "scatter",
                "x_column": x_column,
                "y_column": y_column,
                "score": round(score, 2),
                "reason": reasons
            })

    # --------------------------------------------
    # 3. Numerical Distribution → Histogram
    # --------------------------------------------

    for numerical in numerical_columns:

        score = 0.70

        reasons = [
            "numerical column",
            "distribution can be analyzed"
        ]

        recommendations.append({
            "chart_type": "histogram",
            "x_column": numerical,
            "y_column": None,
            "score": round(score, 2),
            "reason": reasons
        })

    # --------------------------------------------
    # Sort recommendations
    # --------------------------------------------

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations