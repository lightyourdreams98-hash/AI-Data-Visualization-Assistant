import pandas as pd
import numpy as np


def detect_date_columns(df: pd.DataFrame):

    date_columns = []

    for column in df.columns:

        # Already datetime
        if pd.api.types.is_datetime64_any_dtype(
            df[column]
        ):
            date_columns.append(column)
            continue

        # Try converting object/string columns
        if df[column].dtype == "object":

            converted = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            valid_ratio = converted.notna().mean()

            # Consider it a date column if most values
            # can successfully be interpreted as dates
            if valid_ratio >= 0.8:
                date_columns.append(column)

    return date_columns


def calculate_trends(
    df: pd.DataFrame,
    moving_average_window: int = 3
):

    date_columns = detect_date_columns(df)

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    trends = {}

    if not date_columns:
        return {
            "date_columns": [],
            "trend_analysis": {}
        }

    for date_column in date_columns:

        temp_df = df.copy()

        temp_df[date_column] = pd.to_datetime(
            temp_df[date_column],
            errors="coerce"
        )

        # Remove invalid dates
        temp_df = temp_df.dropna(
            subset=[date_column]
        )

        # Sort chronologically
        temp_df = temp_df.sort_values(
            by=date_column
        )

        date_results = {}

        for numerical in numerical_columns:

            series_df = temp_df[
                [date_column, numerical]
            ].dropna()

            if series_df.empty:
                continue

            # Percentage change
            series_df["percentage_change"] = (
                series_df[numerical]
                .pct_change()
                * 100
            )

            # Moving average
            series_df["moving_average"] = (
                series_df[numerical]
                .rolling(
                    window=moving_average_window,
                    min_periods=1
                )
                .mean()
            )

            records = []

            for _, row in series_df.iterrows():

                date_value = row[date_column]

                if pd.isna(date_value):
                    date_value = None
                else:
                    date_value = date_value.strftime(
                        "%Y-%m-%d"
                    )

                value = row[numerical]

                percentage_change = (
                    row["percentage_change"]
                )

                moving_average = (
                    row["moving_average"]
                )

                records.append({
                    "date": date_value,
                    "value": (
                        float(value)
                        if pd.notna(value)
                        else None
                    ),
                    "percentage_change": (
                        float(percentage_change)
                        if pd.notna(
                            percentage_change
                        )
                        else None
                    ),
                    "moving_average": (
                        float(moving_average)
                        if pd.notna(
                            moving_average
                        )
                        else None
                    )
                })

            date_results[numerical] = records

        trends[date_column] = date_results

    return {
        "date_columns": date_columns,
        "trend_analysis": trends
    }