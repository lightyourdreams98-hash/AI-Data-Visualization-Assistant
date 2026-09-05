import json
import pandas as pd
import plotly.express as px


def generate_chart(
    df: pd.DataFrame,
    chart_type: str,
    x_column: str = None,
    y_column: str = None
):

    # -----------------------------------------
    # Validate columns
    # -----------------------------------------

    if x_column and x_column not in df.columns:
        raise ValueError(
            f"X column '{x_column}' not found"
        )

    if y_column and y_column not in df.columns:
        raise ValueError(
            f"Y column '{y_column}' not found"
        )

    # -----------------------------------------
    # Bar
    # -----------------------------------------

    if chart_type == "bar":

        if not x_column or not y_column:
            raise ValueError(
                "Bar chart requires x_column and y_column"
            )

        fig = px.bar(
            df,
            x=x_column,
            y=y_column,
            title=f"{y_column} by {x_column}"
        )

    # -----------------------------------------
    # Line
    # -----------------------------------------

    elif chart_type == "line":

        if not x_column or not y_column:
            raise ValueError(
                "Line chart requires x_column and y_column"
            )

        fig = px.line(
            df,
            x=x_column,
            y=y_column,
            title=f"{y_column} over {x_column}"
        )

    # -----------------------------------------
    # Pie
    # -----------------------------------------

    elif chart_type == "pie":

        if not x_column or not y_column:
            raise ValueError(
                "Pie chart requires x_column and y_column"
            )

        fig = px.pie(
            df,
            names=x_column,
            values=y_column,
            title=f"{y_column} Distribution by {x_column}"
        )

    # -----------------------------------------
    # Scatter
    # -----------------------------------------

    elif chart_type == "scatter":

        if not x_column or not y_column:
            raise ValueError(
                "Scatter plot requires x_column and y_column"
            )

        fig = px.scatter(
            df,
            x=x_column,
            y=y_column,
            title=f"{y_column} vs {x_column}"
        )

    # -----------------------------------------
    # Histogram
    # -----------------------------------------

    elif chart_type == "histogram":

        if not x_column:
            raise ValueError(
                "Histogram requires x_column"
            )

        fig = px.histogram(
            df,
            x=x_column,
            title=f"Distribution of {x_column}"
        )

    # -----------------------------------------
    # Box Plot
    # -----------------------------------------

    elif chart_type == "box":

        if not x_column or not y_column:
            raise ValueError(
                "Box plot requires x_column and y_column"
            )

        fig = px.box(
            df,
            x=x_column,
            y=y_column,
            title=f"{y_column} by {x_column}"
        )

    else:

        raise ValueError(
            f"Unsupported chart type: {chart_type}"
        )

    # -----------------------------------------
    # Convert Plotly object to JSON-safe dict
    # -----------------------------------------

    return json.loads(
        fig.to_json()
    )