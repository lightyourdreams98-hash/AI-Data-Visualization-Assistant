import pandas as pd
import plotly.express as px
import json


def convert_figure_to_json(figure):
    """
    Convert Plotly Figure into a normal Python dictionary
    containing only JSON-compatible values.
    """

    return json.loads(figure.to_json())


def generate_dashboard(df: pd.DataFrame):

    dashboard = {
        "summary": {
            "rows": int(len(df)),
            "columns": int(len(df.columns))
        },
        "charts": []
    }

    # --------------------------------------------------
    # Detect columns
    # --------------------------------------------------

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    date_columns = df.select_dtypes(
        include=["datetime64[ns]", "datetime64[ns, UTC]"]
    ).columns.tolist()

    # --------------------------------------------------
    # Numerical + Categorical
    # Bar Chart
    # --------------------------------------------------

    if numerical_columns and categorical_columns:

        category = categorical_columns[0]
        numerical = numerical_columns[0]

        temp_df = df[[category, numerical]].dropna()

        if len(temp_df) > 0:

            grouped = (
                temp_df
                .groupby(category, as_index=False)[numerical]
                .sum()
                .sort_values(
                    numerical,
                    ascending=False
                )
                .head(10)
            )

            figure = px.bar(
                grouped,
                x=category,
                y=numerical,
                title=f"{numerical} by {category}"
            )

            dashboard["charts"].append({
                "type": "bar",
                "title": f"{numerical} by {category}",
                "data": convert_figure_to_json(figure)
            })

    # --------------------------------------------------
    # Numerical Columns
    # Histogram
    # --------------------------------------------------

    if numerical_columns:

        numerical = numerical_columns[0]

        temp_df = df[[numerical]].dropna()

        if len(temp_df) > 0:

            figure = px.histogram(
                temp_df,
                x=numerical,
                title=f"Distribution of {numerical}"
            )

            dashboard["charts"].append({
                "type": "histogram",
                "title": f"Distribution of {numerical}",
                "data": convert_figure_to_json(figure)
            })

    # --------------------------------------------------
    # Two Numerical Columns
    # Scatter Plot
    # --------------------------------------------------

    if len(numerical_columns) >= 2:

        x_column = numerical_columns[0]
        y_column = numerical_columns[1]

        temp_df = df[
            [x_column, y_column]
        ].dropna()

        if len(temp_df) > 0:

            figure = px.scatter(
                temp_df,
                x=x_column,
                y=y_column,
                title=f"{y_column} vs {x_column}"
            )

            dashboard["charts"].append({
                "type": "scatter",
                "title": f"{y_column} vs {x_column}",
                "data": convert_figure_to_json(figure)
            })

    # --------------------------------------------------
    # Categorical Column
    # Pie Chart
    # --------------------------------------------------

    if categorical_columns:

        category = categorical_columns[0]

        counts = (
            df[category]
            .dropna()
            .astype(str)
            .value_counts()
            .head(10)
            .reset_index()
        )

        counts.columns = [
            category,
            "count"
        ]

        if len(counts) > 0:

            figure = px.pie(
                counts,
                names=category,
                values="count",
                title=f"{category} Distribution"
            )

            dashboard["charts"].append({
                "type": "pie",
                "title": f"{category} Distribution",
                "data": convert_figure_to_json(figure)
            })

    # --------------------------------------------------
    # Date + Numerical
    # Line Chart
    # --------------------------------------------------

    if date_columns and numerical_columns:

        date_column = date_columns[0]
        numerical = numerical_columns[0]

        temp_df = df[
            [date_column, numerical]
        ].dropna()

        if len(temp_df) > 0:

            temp_df = temp_df.sort_values(
                date_column
            )

            figure = px.line(
                temp_df,
                x=date_column,
                y=numerical,
                title=f"{numerical} Trend"
            )

            dashboard["charts"].append({
                "type": "line",
                "title": f"{numerical} Trend",
                "data": convert_figure_to_json(figure)
                
            })

    # --------------------------------------------------
    # Dataset Information
    # --------------------------------------------------

    dashboard["detected_columns"] = {
        "numerical": numerical_columns,
        "categorical": categorical_columns,
        "date": date_columns
    }

    dashboard["chart_count"] = int(
        len(dashboard["charts"])
    )

    return dashboard