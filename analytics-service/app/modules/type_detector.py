import pandas as pd
import re


def detect_column_type(series: pd.Series):

    # Remove missing values and convert everything to string
    non_null = (
        series
        .dropna()
        .astype(str)
        .str.strip()
    )

    if len(non_null) == 0:
        return "unknown"

    # =========================================
    # 1. Numerical Detection
    # =========================================

    numeric_values = pd.to_numeric(
        non_null,
        errors="coerce"
    )

    numeric_ratio = numeric_values.notna().mean()

    if numeric_ratio >= 0.8:
        return "numerical"

    # =========================================
    # 2. Currency Detection
    # =========================================

    currency_pattern = re.compile(
        r"(\d+(\.\d+)?)\s*(lpa|lakhs?|k|cr|crore)",
        re.IGNORECASE
    )

    currency_matches = non_null.apply(
        lambda x: bool(
            currency_pattern.search(x)
        )
    )

    currency_ratio = currency_matches.mean()

    if currency_ratio >= 0.5:
        return "currency"

    # =========================================
    # 3. Date Detection
    # =========================================

    date_formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%y",
        "%d-%m-%y",
        "%d %b %Y",
        "%d %B %Y",
        "%b %d, %Y",
        "%B %d, %Y"
    ]

    best_date_ratio = 0

    for date_format in date_formats:

        converted = pd.to_datetime(
            non_null,
            format=date_format,
            errors="coerce"
        )

        ratio = converted.notna().mean()

        best_date_ratio = max(
            best_date_ratio,
            ratio
        )

    if best_date_ratio >= 0.8:
        return "date"

    # =========================================
    # 4. Binary Detection
    # =========================================

    unique_values = set(
        value.lower()
        for value in non_null.unique()
    )

    binary_values = {
        "yes",
        "no",
        "true",
        "false",
        "y",
        "n"
    }

    if unique_values.issubset(binary_values):
        return "binary"

    # =========================================
    # 5. Categorical
    # =========================================

    return "categorical"


def detect_types(df: pd.DataFrame):

    detected_types = {}

    for column in df.columns:

        detected_types[column] = detect_column_type(
            df[column]
        )

    return detected_types