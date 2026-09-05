import pandas as pd
import re


def convert_currency_value(value):

    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    # Remove commas and currency symbols
    value = value.replace(",", "")
    value = value.replace("₹", "")
    value = value.replace("$", "")

    # Extract number
    match = re.search(r"\d+(\.\d+)?", value)

    if not match:
        return None

    number = float(match.group())

    # Convert LPA / lakh to rupees
    if "lpa" in value or "lakh" in value:
        return number * 100000

    # Convert crore
    if "crore" in value or "cr" in value:
        return number * 10000000

    # Convert thousand
    if "k" in value:
        return number * 1000

    return number


def transform_dataframe(
    df: pd.DataFrame,
    detected_types: dict
):

    transformed_df = df.copy()

    for column, column_type in detected_types.items():

        if column not in transformed_df.columns:
            continue

        # -----------------------------------------
        # Numerical
        # -----------------------------------------

        if column_type == "numerical":

            transformed_df[column] = pd.to_numeric(
                transformed_df[column],
                errors="coerce"
            )

        # -----------------------------------------
        # Currency
        # -----------------------------------------

        elif column_type == "currency":

            transformed_df[column] = (
                transformed_df[column]
                .apply(convert_currency_value)
            )

        # -----------------------------------------
        # Date
        # -----------------------------------------

        elif column_type == "date":

            transformed_df[column] = pd.to_datetime(
                transformed_df[column],
                errors="coerce"
            )

        # -----------------------------------------
        # Binary
        # -----------------------------------------

        elif column_type == "binary":

            transformed_df[column] = (
                transformed_df[column]
                .astype(str)
                .str.strip()
                .str.lower()
                .map({
                    "yes": 1,
                    "y": 1,
                    "true": 1,
                    "no": 0,
                    "n": 0,
                    "false": 0
                })
            )

    return transformed_df