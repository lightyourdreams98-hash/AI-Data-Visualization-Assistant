import pandas as pd
import numpy as np
import math


# ------------------------------------------------
# Convert Pandas / NumPy values to JSON-safe values
# ------------------------------------------------

def json_safe(value):

    # Missing values
    if value is None:
        return None

    if pd.isna(value):
        return None

    # NumPy values
    if isinstance(value, np.generic):
        value = value.item()

    # Python float
    if isinstance(value, float):

        if not math.isfinite(value):
            return None

        return value

    # Python integer
    if isinstance(value, int):
        return value

    # Python boolean
    if isinstance(value, bool):
        return value

    # Everything else
    return value


# ------------------------------------------------
# Descriptive Statistics
# ------------------------------------------------

def calculate_descriptive_statistics(df: pd.DataFrame):

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns

    statistics = {}

    for column in numerical_columns:

        series = df[column].dropna()

        # No valid values
        if series.empty:

            statistics[column] = {
                "mean": None,
                "median": None,
                "minimum": None,
                "maximum": None,
                "standard_deviation": None,
                "variance": None
            }

            continue

        statistics[column] = {

            "mean": json_safe(
                series.mean()
            ),

            "median": json_safe(
                series.median()
            ),

            "minimum": json_safe(
                series.min()
            ),

            "maximum": json_safe(
                series.max()
            ),

            "standard_deviation": json_safe(
                series.std(ddof=0)
            ),

            "variance": json_safe(
                series.var(ddof=0)
            )
        }

    return statistics


# ------------------------------------------------
# Group-by Statistics
# ------------------------------------------------

def calculate_groupby_statistics(df: pd.DataFrame):

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns

    groupby_results = {}

    for category in categorical_columns:

        # Skip columns with too many unique values
        if df[category].nunique(
            dropna=True
        ) > 50:

            continue

        for numerical in numerical_columns:

            grouped = (
                df.groupby(category)[numerical]
                .agg([
                    "count",
                    "sum",
                    "mean"
                ])
                .reset_index()
            )

            records = []

            for record in grouped.to_dict(
                orient="records"
            ):

                safe_record = {}

                for key, value in record.items():

                    safe_record[str(key)] = json_safe(
                        value
                    )

                records.append(safe_record)

            groupby_results[
                f"{category}_by_{numerical}"
            ] = records

    return groupby_results


# ------------------------------------------------
# Pearson Correlation
# ------------------------------------------------

def calculate_correlations(df: pd.DataFrame):

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    if len(numerical_columns) < 2:
        return {}

    correlation_matrix = df[
        numerical_columns
    ].corr(
        method="pearson"
    )

    correlations = {}

    for column1 in numerical_columns:

        correlations[column1] = {}

        for column2 in numerical_columns:

            value = correlation_matrix.loc[
                column1,
                column2
            ]

            correlations[column1][column2] = (
                json_safe(value)
            )

    return correlations


# ------------------------------------------------
# Master Statistics Function
# ------------------------------------------------

def generate_statistics(
    df: pd.DataFrame
):

    descriptive = (
        calculate_descriptive_statistics(df)
    )

    groupby = (
        calculate_groupby_statistics(df)
    )

    correlations = (
        calculate_correlations(df)
    )

    return {

        "descriptive_statistics":
            descriptive,

        "groupby_statistics":
            groupby,

        "correlations":
            correlations

    }