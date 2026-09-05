import pandas as pd


def clean_dataframe(df: pd.DataFrame):

    # Make a copy so that the original DataFrame
    # is not modified directly
    cleaned_df = df.copy()

    cleaning_report = {
        "missing_values_filled": {},
        "duplicate_rows_removed": 0,
        "outliers_detected": {}
    }

    # ------------------------------------------------
    # 1. Remove duplicate rows
    # ------------------------------------------------

    duplicate_count = int(
        cleaned_df.duplicated().sum()
    )

    cleaned_df = cleaned_df.drop_duplicates()

    cleaning_report["duplicate_rows_removed"] = duplicate_count

    # ------------------------------------------------
    # 2. Fill missing numerical values with median
    # ------------------------------------------------

    numerical_columns = cleaned_df.select_dtypes(
        include=["number"]
    ).columns

    for column in numerical_columns:

        missing_count = int(
            cleaned_df[column].isna().sum()
        )

        if missing_count > 0:

            median_value = cleaned_df[column].median()

            cleaned_df[column] = cleaned_df[column].fillna(
                median_value
            )

            cleaning_report[
                "missing_values_filled"
            ][column] = {
                "method": "median",
                "count": missing_count,
                "value": float(median_value)
            }

    # ------------------------------------------------
    # 3. Fill missing categorical values with mode
    # ------------------------------------------------

    categorical_columns = cleaned_df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns

    for column in categorical_columns:

        missing_count = int(
            cleaned_df[column].isna().sum()
        )

        if missing_count > 0:

            mode_values = cleaned_df[column].mode()

            if not mode_values.empty:

                mode_value = mode_values.iloc[0]

                cleaned_df[column] = cleaned_df[column].fillna(
                    mode_value
                )

                cleaning_report[
                    "missing_values_filled"
                ][column] = {
                    "method": "mode",
                    "count": missing_count,
                    "value": str(mode_value)
                }

    # ------------------------------------------------
    # 4. Detect numerical outliers using IQR
    # ------------------------------------------------

    for column in numerical_columns:

        Q1 = cleaned_df[column].quantile(0.25)
        Q3 = cleaned_df[column].quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)

        outlier_mask = (
            (cleaned_df[column] < lower_bound) |
            (cleaned_df[column] > upper_bound)
        )

        outlier_count = int(
            outlier_mask.sum()
        )

        cleaning_report[
            "outliers_detected"
        ][column] = {
            "count": outlier_count,
            "lower_bound": float(lower_bound),
            "upper_bound": float(upper_bound)
        }

    return cleaned_df, cleaning_report