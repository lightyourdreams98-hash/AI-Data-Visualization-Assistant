from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os 
import pandas as pd
import io

from app.modules.cleaner import clean_dataframe
from app.modules.profiler import profile_dataframe
from app.modules.statistics import generate_statistics
from app.modules.trends import calculate_trends
from app.modules.recommendations import recommend_charts
from app.modules.type_detector import detect_types
from app.modules.transformer import transform_dataframe
from app.modules.insights import generate_insights
from app.question_engine import analyze_question
from app.llm_service import generate_llm_answer
# =====================================================
# CREATE FASTAPI APPLICATION
# =====================================================

app = FastAPI(
    title="AI Data Visualization Analytics Service",
    version="1.0.0"
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():

    return {
        "success": True,
        "message": "Analytics service is running"
    }


# =====================================================
# HEALTH
# =====================================================

@app.get("/health")
def health():

    return {
        "success": True,
        "message": "FastAPI analytics service is healthy"
    }


# =====================================================
# PROFILE
# =====================================================

@app.post("/profile")
async def profile_dataset(
    file: UploadFile = File(...)
):

    contents = await file.read()

    df = pd.read_csv(
        io.BytesIO(contents)
    )

    profile = profile_dataframe(df)

    return {
        "success": True,
        "filename": file.filename,
        "profile": profile
    }


# =====================================================
# CLEAN
# =====================================================

@app.post("/clean")
async def clean_dataset(
    file: UploadFile = File(...)
):

    contents = await file.read()

    df = pd.read_csv(
        io.BytesIO(contents)
    )

    cleaned_df, cleaning_report = clean_dataframe(df)

    return {
        "success": True,
        "filename": file.filename,
        "rows_before": len(df),
        "rows_after": len(cleaned_df),
        "cleaning_report": cleaning_report
    }


# =====================================================
# STATISTICS
# =====================================================

@app.post("/statistics")
async def calculate_dataset_statistics(
    file: UploadFile = File(...)
):

    contents = await file.read()

    df = pd.read_csv(
        io.BytesIO(contents)
    )

    cleaned_df, cleaning_report = clean_dataframe(df)

    statistics = generate_statistics(
        cleaned_df
    )

    return {
        "success": True,
        "filename": file.filename,
        "rows_before_cleaning": len(df),
        "rows_after_cleaning": len(cleaned_df),
        "cleaning_report": cleaning_report,
        "statistics": statistics
    }


# =====================================================
# TRENDS
# =====================================================

@app.post("/trends")
async def analyze_dataset_trends(
    file: UploadFile = File(...)
):

    contents = await file.read()

    df = pd.read_csv(
        io.BytesIO(contents)
    )

    cleaned_df, cleaning_report = clean_dataframe(
        df
    )

    trends = calculate_trends(
        cleaned_df
    )

    return {
        "success": True,
        "filename": file.filename,
        "rows": len(cleaned_df),
        "trends": trends
    }


# =====================================================
# RECOMMENDATIONS
# =====================================================

@app.post("/recommendations")
async def recommend_dataset_charts(
    file: UploadFile = File(...)
):

    contents = await file.read()

    df = pd.read_csv(
        io.BytesIO(contents)
    )

    cleaned_df, cleaning_report = clean_dataframe(
        df
    )

    recommendations = recommend_charts(
        cleaned_df
    )

    return {
        "success": True,
        "filename": file.filename,
        "rows": len(cleaned_df),
        "recommendations": recommendations
    }


# =====================================================
# DETECT TYPES
# =====================================================

@app.post("/detect-types")
async def detect_dataset_types(
    file: UploadFile = File(...)
):

    contents = await file.read()

    df = pd.read_csv(
        io.BytesIO(contents)
    )

    detected_types = detect_types(df)

    return {
        "success": True,
        "filename": file.filename,
        "detected_types": detected_types
    }


# =====================================================
# TRANSFORM
# =====================================================

@app.post("/transform")
async def transform_dataset(
    file: UploadFile = File(...)
):

    contents = await file.read()

    df = pd.read_csv(
        io.BytesIO(contents)
    )

    detected_types = detect_types(df)

    transformed_df = transform_dataframe(
        df,
        detected_types
    )

    return {
        "success": True,
        "filename": file.filename,
        "detected_types": detected_types,
        "columns": transformed_df.columns.tolist(),
        "data": transformed_df.head(10).to_dict(
            orient="records"
        )
    }


# =====================================================
# AUTOMATIC DASHBOARD
# =====================================================


@app.post("/dashboard")
async def generate_dashboard(
    file: UploadFile = File(...)
):
    contents = await file.read()

    df = pd.read_csv(
        io.BytesIO(contents)
    )

    # Clean dataset
    cleaned_df, cleaning_report = clean_dataframe(df)

    # Statistics
    statistics = generate_statistics(
        cleaned_df
    )

    # Trends
    trends = calculate_trends(
        cleaned_df
    )

    # Chart recommendations
    recommendations = recommend_charts(
        cleaned_df
    )

    # Detect column types
    detected_types = detect_types(
        cleaned_df
    )

    return {
        "success": True,
        "filename": file.filename,

        "rows": len(cleaned_df),

        "columns": len(
            cleaned_df.columns
        ),

        "statistics": statistics,

        "trends": trends,

        "recommendations": recommendations,

        "detected_types": detected_types,

        # IMPORTANT
        "data": cleaned_df.to_dict(
            orient="records"
        )
    }

@app.post("/insights")
async def generate_dataset_insights(
    file: UploadFile = File(...)
):

    contents = await file.read()

    df = pd.read_csv(
        io.BytesIO(contents)
    )

    # Clean dataset
    cleaned_df, cleaning_report = clean_dataframe(df)

    # Generate statistics
    statistics = generate_statistics(
        cleaned_df
    )

    # Generate AI-style insights
    insights = generate_insights(
        cleaned_df,
        statistics
    )

    return {
        "success": True,
        "filename": file.filename,
        "rows": len(cleaned_df),
        "insights": insights
    }


@app.post("/ask")
async def ask_question(
    file: UploadFile = File(...),
    question: str = Form(...)
):

    try:

        # -----------------------------------------
        # Save uploaded file temporarily
        # -----------------------------------------

        suffix = os.path.splitext(file.filename)[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp:

            contents = await file.read()

            temp.write(contents)

            temp_path = temp.name


        # -----------------------------------------
        # Read CSV
        # -----------------------------------------

        df = pd.read_csv(temp_path)


        # -----------------------------------------
        # Clean column names
        # -----------------------------------------

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )


        # -----------------------------------------
        # Normalize question
        # -----------------------------------------

        q = question.lower().strip()


        # =========================================
        # QUESTION 1
        # Highest sales
        # =========================================

        if "highest sales" in q or "maximum sales" in q:

            numeric_columns = [
                col for col in df.columns
                if pd.api.types.is_numeric_dtype(df[col])
            ]

            sales_column = next(
                (
                    col for col in numeric_columns
                    if "sales" in col.lower()
                ),
                None
            )

            if sales_column:

                total_sales = (
                    df[sales_column]
                    .sum()
                )

                answer = (
                    f"The total sales are "
                    f"{total_sales:,.2f}."
                )

            else:

                answer = "No Sales column was found."


        # =========================================
        # QUESTION 2
        # Highest selling product
        # =========================================

        elif (
            "highest selling product" in q
            or "product highest sales" in q
            or "which product" in q and "sales" in q
        ):

            product_column = next(
                (
                    col for col in df.columns
                    if col.lower() == "product"
                ),
                None
            )

            sales_column = next(
                (
                    col for col in df.columns
                    if "sales" in col.lower()
                    and pd.api.types.is_numeric_dtype(df[col])
                ),
                None
            )

            if product_column and sales_column:

                result = (
                    df.groupby(product_column)[sales_column]
                    .sum()
                    .sort_values(ascending=False)
                )

                product = result.index[0]
                value = result.iloc[0]

                answer = (
                    f"{product} has the highest total "
                    f"sales of {value:,.2f}."
                )

            else:

                answer = (
                    "I could not find Product and "
                    "Sales columns."
                )


        # =========================================
        # QUESTION 3
        # Highest profit
        # =========================================

        elif (
            "highest profit" in q
            or "maximum profit" in q
        ):

            profit_column = next(
                (
                    col for col in df.columns
                    if "profit" in col.lower()
                    and pd.api.types.is_numeric_dtype(df[col])
                ),
                None
            )

            if profit_column:

                value = df[profit_column].max()

                answer = (
                    f"The maximum Profit is "
                    f"{value:,.2f}."
                )

            else:

                answer = "No Profit column was found."


        # =========================================
        # QUESTION 4
        # Average sales
        # =========================================

        elif (
            "average sales" in q
            or "mean sales" in q
        ):

            sales_column = next(
                (
                    col for col in df.columns
                    if "sales" in col.lower()
                    and pd.api.types.is_numeric_dtype(df[col])
                ),
                None
            )

            if sales_column:

                value = df[sales_column].mean()

                answer = (
                    f"The average Sales are "
                    f"{value:,.2f}."
                )

            else:

                answer = "No Sales column was found."


        # =========================================
        # QUESTION 5
        # Dataset size
        # =========================================

        elif (
            "how many rows" in q
            or "number of rows" in q
            or "dataset size" in q
        ):

            answer = (
                f"The dataset contains "
                f"{len(df)} rows and "
                f"{len(df.columns)} columns."
            )


        # =========================================
        # QUESTION 6
        # Correlation
        # =========================================

        elif (
            "relationship" in q
            or "correlation" in q
            or "related" in q
        ):

            numeric_df = df.select_dtypes(
                include="number"
            )

            correlation = numeric_df.corr()

            answer = (
                "The correlation matrix is:\n"
                + correlation.to_string()
            )


        # =========================================
        # UNKNOWN QUESTION
        # =========================================

        else:

            answer = (
                "I could not understand this question yet. "
                "Try asking about sales, profit, products, "
                "rows, columns, averages, or correlations."
            )


        # -----------------------------------------
        # Delete temporary file
        # -----------------------------------------

        os.remove(temp_path)


        # -----------------------------------------
        # Response
        # -----------------------------------------

        return {
            "success": True,
            "filename": file.filename,
            "question": question,
            "answer": answer
        }


    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

def generate_answer(question, analysis):

    intent = analysis.get("intent")


    # =========================================
    # DATASET INFO
    # =========================================

    if intent == "dataset_info":

        result = analysis["result"]

        return (
            f"The dataset contains "
            f"{result['rows']} rows and "
            f"{result['columns']} columns."
        )


    # =========================================
    # TOTAL
    # =========================================

    if intent == "total":

        if "error" in analysis:

            return analysis["error"]

        metric = analysis["metric"]

        value = analysis["value"]

        return (
            f"The total {metric} is "
            f"{value:,.2f}."
        )


    # =========================================
    # AVERAGE
    # =========================================

    if intent == "average":

        if "error" in analysis:

            return analysis["error"]

        metric = analysis["metric"]

        value = analysis["value"]

        return (
            f"The average {metric} is "
            f"{value:,.2f}."
        )


    # =========================================
    # MAXIMUM
    # =========================================

    if intent == "maximum":

        if "error" in analysis:

            return analysis["error"]

        metric = analysis["metric"]

        value = analysis["value"]

        return (
            f"The maximum {metric} is "
            f"{value:,.2f}."
        )


    # =========================================
    # MINIMUM
    # =========================================

    if intent == "minimum":

        if "error" in analysis:

            return analysis["error"]

        metric = analysis["metric"]

        value = analysis["value"]

        return (
            f"The minimum {metric} is "
            f"{value:,.2f}."
        )


    # =========================================
    # HIGHEST CATEGORY
    # =========================================

    if intent == "highest_category":

        if "error" in analysis:

            return analysis["error"]

        category = analysis["category"]

        metric = analysis["metric"]

        category_value = analysis["category_value"]

        value = analysis["value"]

        return (
            f"{category_value} has the highest total "
            f"{metric} among {category} categories, "
            f"with a value of {value:,.2f}."
        )


    # =========================================
    # LOWEST CATEGORY
    # =========================================

    if intent == "lowest_category":

        if "error" in analysis:

            return analysis["error"]

        category = analysis["category"]

        metric = analysis["metric"]

        category_value = analysis["category_value"]

        value = analysis["value"]

        return (
            f"{category_value} has the lowest total "
            f"{metric} among {category} categories, "
            f"with a value of {value:,.2f}."
        )


    # =========================================
    # CORRELATION
    # =========================================

    if intent == "correlation":

        if "error" in analysis:

            return analysis["error"]

        correlations = analysis["correlation"]

        pairs = []

        columns = list(correlations.keys())

        for i in range(len(columns)):

            for j in range(i + 1, len(columns)):

                col1 = columns[i]

                col2 = columns[j]

                value = correlations[col1][col2]

                pairs.append(
                    f"{col1} and {col2}: "
                    f"{value:.3f}"
                )

        return (
            "Correlation results: "
            + "; ".join(pairs)
        )


    # =========================================
    # UNKNOWN
    # =========================================

    return analysis.get(
        "error",
        "Unable to generate an answer."
    )


@app.post("/ask")
async def ask_question(
    file: UploadFile = File(...),
    question: str = Form(...)
):

    temp_path = None

    try:

        # -----------------------------------------
        # Read uploaded CSV
        # -----------------------------------------

        contents = await file.read()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".csv"
        ) as temp:

            temp.write(contents)

            temp_path = temp.name


        # -----------------------------------------
        # Load dataset
        # -----------------------------------------

        df = pd.read_csv(temp_path)


        # -----------------------------------------
        # Clean column names
        # -----------------------------------------

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )


        # -----------------------------------------
        # Analyze question
        # -----------------------------------------

        analysis = analyze_question(
            question,
            df
        )


        # -----------------------------------------
        # Generate readable answer
        # -----------------------------------------

        answer = generate_answer(
            question,
            analysis
        )

        dataset_info = {
    "rows": len(df),
    "columns": len(df.columns),
    "column_names": list(df.columns)
}       

        answer = generate_llm_answer(
    question=question,
    analysis=analysis,
    dataset_info=dataset_info
)


        return {

            "success": True,

            "filename": file.filename,

            "question": question,

            "understanding": analysis,

            "answer": answer

        }


    except Exception as e:

        print("Q&A ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


    finally:

        if temp_path and os.path.exists(temp_path):

            os.remove(temp_path)