import pandas as pd


def profile_dataframe(df: pd.DataFrame):

    # -----------------------------
    # Basic information
    # -----------------------------

    rows = len(df)
    columns = len(df.columns)

    # -----------------------------
    # Detect column types
    # -----------------------------

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    date_columns = []

    # Try to detect date columns
    for column in df.columns:

        if column in numerical_columns:
            continue

        try:

            converted = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            valid_ratio = converted.notna().mean()

            if valid_ratio >= 0.8:
                date_columns.append(column)

        except Exception:
            pass

    # Remove date columns from categorical columns
    categorical_columns = [
        column
        for column in categorical_columns
        if column not in date_columns
    ]

    # -----------------------------
    # Missing values
    # -----------------------------

    missing_values = {}

    for column in df.columns:

        missing_count = int(df[column].isna().sum())

        missing_values[column] = missing_count

    # -----------------------------
    # Duplicate rows
    # -----------------------------

    duplicate_rows = int(
        df.duplicated().sum()
    )

    # -----------------------------
    # Unique values
    # -----------------------------

    unique_values = {}

    for column in df.columns:

        unique_values[column] = int(
            df[column].nunique(dropna=True)
        )

    # -----------------------------
    # Data types
    # -----------------------------

    data_types = {}

    for column in df.columns:

        data_types[column] = str(
            df[column].dtype
        )

    # -----------------------------
    # Return profile
    # -----------------------------

    return {

        "rows": rows,

        "columns": columns,

        "column_names": df.columns.tolist(),

        "numerical_columns": numerical_columns,

        "categorical_columns": categorical_columns,

        "date_columns": date_columns,

        "data_types": data_types,

        "missing_values": missing_values,

        "duplicate_rows": duplicate_rows,

        "unique_values": unique_values

    }