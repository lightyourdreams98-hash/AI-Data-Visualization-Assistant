import { useState } from "react";
import Plot from "react-plotly.js";

import {
    generateDashboard,
    generateInsights
} from "../services/dashboardService";


function Dashboard({ file }) {

    const [dashboard, setDashboard] = useState(null);
    const [insights, setInsights] = useState(null);

    const [loading, setLoading] = useState(false);
    const [insightsLoading, setInsightsLoading] = useState(false);

    const [error, setError] = useState("");
    const [insightsError, setInsightsError] = useState("");


    // =====================================================
    // GENERATE DASHBOARD
    // =====================================================

    const handleGenerateDashboard = async () => {

        console.log("FILE RECEIVED BY DASHBOARD:", file);

        if (!file) {

            setError("Please select a CSV file first.");

            return;
        }


        try {

            setLoading(true);

            setError("");

            setDashboard(null);
            setInsights(null);


            console.log(
                "Sending file to FastAPI Dashboard:",
                file.name
            );


            // -----------------------------------------
            // Generate Dashboard
            // -----------------------------------------

            const dashboardData =
                await generateDashboard(file);


            console.log(
                "FASTAPI DASHBOARD RESPONSE:",
                dashboardData
            );


            setDashboard(dashboardData);


            // -----------------------------------------
            // Generate Insights
            // -----------------------------------------

            setInsightsLoading(true);

            setInsightsError("");


            console.log(
                "Sending file to FastAPI Insights:",
                file.name
            );


            const insightData =
                await generateInsights(file);


            console.log(
                "FASTAPI INSIGHTS RESPONSE:",
                insightData
            );


            setInsights(insightData);


        } catch (err) {

            console.error(
                "DASHBOARD ERROR:",
                err
            );


            console.error(
                "Response:",
                err.response?.data
            );


            setError(
                err.response?.data?.detail ||
                err.response?.data?.message ||
                err.message ||
                "Dashboard generation failed"
            );

        } finally {

            setLoading(false);
            setInsightsLoading(false);

        }

    };


    // =====================================================
    // NO FILE
    // =====================================================

    if (!file) {

        return (

            <div className="mt-8 bg-white rounded-xl shadow-md p-8">

                <h2 className="text-2xl font-bold">
                    Automatic Dashboard
                </h2>

                <p className="text-gray-500 mt-2">
                    Select a CSV file to generate your dashboard.
                </p>

            </div>

        );

    }


    // =====================================================
    // MAIN UI
    // =====================================================

    return (

        <div className="mt-8">


            {/* ================================================= */}
            {/* DASHBOARD CONTROL */}
            {/* ================================================= */}

            <div className="bg-white rounded-xl shadow-md p-8">

                <h2 className="text-2xl font-bold">
                    Automatic Dashboard
                </h2>


                <p className="text-gray-500 mt-2">
                    Automatically generated analytics from your dataset.
                </p>


                <p className="text-gray-600 mt-4">

                    File received:

                    <strong className="ml-1">
                        {file.name}
                    </strong>

                </p>


                <button
                    onClick={handleGenerateDashboard}
                    disabled={loading}
                    className="mt-5 bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg disabled:bg-gray-400"
                >

                    {loading
                        ? "Generating Dashboard..."
                        : "Generate Dashboard"
                    }

                </button>


                {error && (

                    <p className="text-red-600 mt-4">
                        ✗ {error}
                    </p>

                )}

            </div>


            {/* ================================================= */}
            {/* DASHBOARD RESULT */}
            {/* ================================================= */}

            {dashboard && (

                <DashboardContent
                    dashboard={dashboard}
                    insights={insights}
                    insightsLoading={insightsLoading}
                    insightsError={insightsError}
                />

            )}

        </div>

    );

}


// ============================================================
// DASHBOARD CONTENT
// ============================================================

function DashboardContent({
    dashboard,
    insights,
    insightsLoading,
    insightsError
}) {

    return (

        <div className="mt-8">


            {/* ================================================= */}
            {/* TITLE */}
            {/* ================================================= */}

            <div className="bg-white rounded-xl shadow-md p-6 mb-6">

                <h2 className="text-3xl font-bold">
                    {dashboard.filename}
                </h2>

                <p className="text-gray-500 mt-2">
                    Dashboard generated successfully.
                </p>

            </div>


            {/* ================================================= */}
            {/* KPI CARDS */}
            {/* ================================================= */}

            <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">


                <KPICard
                    title="Total Rows"
                    value={dashboard.rows}
                />


                <KPICard
                    title="Total Columns"
                    value={dashboard.columns}
                />


                <KPICard
                    title="Recommended Charts"
                    value={
                        dashboard.recommendations?.length || 0
                    }
                />

            </div>


            {/* ================================================= */}
            {/* DETECTED COLUMN TYPES */}
            {/* ================================================= */}

            <DetectedTypes
                types={dashboard.detected_types}
            />


            {/* ================================================= */}
            {/* STATISTICS */}
            {/* ================================================= */}

            <StatisticsSection
                statistics={dashboard.statistics}
            />


            {/* ================================================= */}
            {/* CHARTS */}
            {/* ================================================= */}

            <ChartsSection
                dashboard={dashboard}
            />


            {/* ================================================= */}
            {/* CORRELATION */}
            {/* ================================================= */}

            <CorrelationSection
                statistics={dashboard.statistics}
            />


            {/* ================================================= */}
            {/* INSIGHTS */}
            {/* ================================================= */}

            <InsightsSection
                insights={insights}
                loading={insightsLoading}
                error={insightsError}
            />


            {/* ================================================= */}
            {/* DATA PREVIEW */}
            {/* ================================================= */}

            <DatasetPreview
                data={dashboard.data}
            />

        </div>

    );

}


// ============================================================
// KPI CARD
// ============================================================

function KPICard({ title, value }) {

    return (

        <div className="bg-white rounded-xl shadow-md p-6">

            <p className="text-gray-500">
                {title}
            </p>

            <h3 className="text-3xl font-bold mt-2">
                {value}
            </h3>

        </div>

    );

}


// ============================================================
// DETECTED TYPES
// ============================================================

function DetectedTypes({ types }) {

    if (!types) {
        return null;
    }


    return (

        <div className="bg-white rounded-xl shadow-md p-6 mb-8">

            <h2 className="text-2xl font-bold mb-5">
                Detected Column Types
            </h2>


            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

                {Object.entries(types).map(
                    ([column, type]) => (

                        <div
                            key={column}
                            className="bg-gray-100 rounded-lg p-4"
                        >

                            <p className="font-semibold">
                                {column}
                            </p>

                            <p className="text-gray-600 mt-1">
                                {type}
                            </p>

                        </div>

                    )
                )}

            </div>

        </div>

    );

}


// ============================================================
// STATISTICS
// ============================================================

function StatisticsSection({ statistics }) {

    if (!statistics?.descriptive_statistics) {
        return null;
    }


    const data =
        statistics.descriptive_statistics;


    return (

        <div className="mb-8">

            <h2 className="text-2xl font-bold mb-4">
                Statistical Summary
            </h2>


            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                {Object.entries(data).map(
                    ([column, values]) => (

                        <div
                            key={column}
                            className="bg-white rounded-xl shadow-md p-6"
                        >

                            <h3 className="text-xl font-bold mb-4">
                                {column}
                            </h3>


                            <div className="grid grid-cols-2 gap-4">

                                <Stat
                                    label="Mean"
                                    value={values.mean}
                                />

                                <Stat
                                    label="Median"
                                    value={values.median}
                                />

                                <Stat
                                    label="Minimum"
                                    value={values.minimum}
                                />

                                <Stat
                                    label="Maximum"
                                    value={values.maximum}
                                />

                                <Stat
                                    label="Std. Deviation"
                                    value={values.standard_deviation}
                                />

                                <Stat
                                    label="Variance"
                                    value={values.variance}
                                />

                            </div>

                        </div>

                    )
                )}

            </div>

        </div>

    );

}


// ============================================================
// STAT
// ============================================================

function Stat({ label, value }) {

    return (

        <div className="bg-gray-100 rounded-lg p-3">

            <p className="text-gray-500 text-sm">
                {label}
            </p>

            <p className="font-semibold mt-1">

                {typeof value === "number"
                    ? value.toFixed(2)
                    : value}

            </p>

        </div>

    );

}


// ============================================================
// CHARTS
// ============================================================

function ChartsSection({ dashboard }) {

    const recommendations =
        dashboard.recommendations || [];


    const groupStats =
        dashboard.statistics?.groupby_statistics || {};


    return (

        <div className="mb-8">

            <h2 className="text-2xl font-bold mb-4">
                Automatically Generated Charts
            </h2>


            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

                {recommendations
                    .slice(0, 6)
                    .map((recommendation, index) => (

                        <ChartCard
                            key={index}
                            recommendation={recommendation}
                            groupStats={groupStats}
                            data={dashboard.data || []}
                        />

                    ))}

            </div>

        </div>

    );

}


// ============================================================
// CHART CARD
// ============================================================

function ChartCard({
    recommendation,
    groupStats,
    data
}) {

    const {
        chart_type,
        x_column,
        y_column,
        score,
        reason
    } = recommendation;


    // ========================================================
    // BAR CHART
    // ========================================================

    if (chart_type === "bar") {

        const statsKey =
            `${x_column}_by_${y_column}`;


        const values =
            groupStats[statsKey] || [];


        const xValues =
            values.map(item => item[x_column]);


        const yValues =
            values.map(item => item.sum);


        return (

            <div className="bg-white rounded-xl shadow-md p-5">

                <div className="mb-3">

                    <h3 className="text-xl font-bold">
                        {y_column} by {x_column}
                    </h3>

                    <p className="text-gray-500 text-sm">
                        Chart type: {chart_type}
                    </p>

                    <p className="text-gray-500 text-sm">
                        Score: {Number(score || 0).toFixed(2)}
                    </p>

                </div>


                <Plot

                    data={[
                        {
                            x: xValues,
                            y: yValues,
                            type: "bar"
                        }
                    ]}


                    layout={{

                        autosize: true,

                        margin: {
                            l: 60,
                            r: 30,
                            t: 20,
                            b: 70
                        },

                        xaxis: {
                            title: x_column
                        },

                        yaxis: {
                            title: y_column
                        }

                    }}


                    style={{
                        width: "100%",
                        height: "400px"
                    }}


                    useResizeHandler={true}


                    config={{
                        responsive: true
                    }}

                />


                {/* WHY */}

                {reason && (

                    <div className="mt-4">

                        <p className="font-semibold">
                            Why this chart?
                        </p>

                        <ul className="list-disc ml-5 mt-2 text-gray-600">

                            {reason.map(
                                (item, index) => (

                                    <li key={index}>
                                        {item}
                                    </li>

                                )
                            )}

                        </ul>

                    </div>

                )}

            </div>

        );

    }


    // ========================================================
    // SCATTER CHART
    // ========================================================

    if (chart_type === "scatter") {

        const xValues =
            data.map(row => row[x_column]);


        const yValues =
            data.map(row => row[y_column]);


        return (

            <div className="bg-white rounded-xl shadow-md p-5">

                <h3 className="text-xl font-bold">
                    {x_column} vs {y_column}
                </h3>


                <p className="text-gray-500 text-sm mb-3">
                    Chart type: scatter
                </p>


                <Plot

                    data={[
                        {
                            x: xValues,
                            y: yValues,
                            mode: "markers",
                            type: "scatter"
                        }
                    ]}


                    layout={{

                        autosize: true,

                        margin: {
                            l: 60,
                            r: 30,
                            t: 20,
                            b: 70
                        },

                        xaxis: {
                            title: x_column
                        },

                        yaxis: {
                            title: y_column
                        }

                    }}


                    style={{
                        width: "100%",
                        height: "400px"
                    }}


                    useResizeHandler={true}


                    config={{
                        responsive: true
                    }}

                />

            </div>

        );

    }


    return null;

}


// ============================================================
// CORRELATION
// ============================================================

function CorrelationSection({ statistics }) {

    const correlations =
        statistics?.correlations;


    if (!correlations) {
        return null;
    }


    return (

        <div className="bg-white rounded-xl shadow-md p-6 mb-8">

            <h2 className="text-2xl font-bold mb-4">
                Correlation Analysis
            </h2>


            {Object.entries(correlations).map(
                ([column, values]) => (

                    <div
                        key={column}
                        className="mb-4"
                    >

                        <h3 className="font-semibold">
                            {column}
                        </h3>


                        {Object.entries(values).map(
                            ([otherColumn, value]) => {

                                if (
                                    column === otherColumn
                                ) {
                                    return null;
                                }


                                return (

                                    <p
                                        key={otherColumn}
                                        className="text-gray-600"
                                    >

                                        {column} ↔ {otherColumn}

                                        {" : "}

                                        {Number(value).toFixed(3)}

                                    </p>

                                );

                            }
                        )}

                    </div>

                )
            )}

        </div>

    );

}


// ============================================================
// INSIGHTS
// ============================================================

function InsightsSection({
    insights,
    loading,
    error
}) {

    return (

        <div className="bg-white rounded-xl shadow-md p-6 mb-8">

            <h2 className="text-2xl font-bold mb-5">
                AI Data Insights
            </h2>


            {loading && (

                <p className="text-gray-500">
                    Generating insights...
                </p>

            )}


            {error && (

                <p className="text-red-600">
                    ✗ {error}
                </p>

            )}


            {!loading &&
                !error &&
                insights?.insights?.length > 0 && (

                    <div className="space-y-4">

                        {insights.insights.map(
                            (insight, index) => (

                                <div
                                    key={index}
                                    className="bg-gray-100 rounded-lg p-4"
                                >

                                    <p className="font-semibold capitalize">
                                        {insight.type?.replace(
                                            "_",
                                            " "
                                        )}
                                    </p>


                                    <p className="text-gray-700 mt-1">
                                        {insight.message}
                                    </p>

                                </div>

                            )
                        )}

                    </div>

                )}


            {!loading &&
                !error &&
                (!insights ||
                    !insights.insights ||
                    insights.insights.length === 0) && (

                    <p className="text-gray-500">
                        No insights available.
                    </p>

                )}

        </div>

    );

}


// ============================================================
// DATASET PREVIEW
// ============================================================

function DatasetPreview({ data }) {

    if (!data || data.length === 0) {
        return null;
    }


    const columns =
        Object.keys(data[0]);


    return (

        <div className="bg-white rounded-xl shadow-md p-6 mb-8">

            <h2 className="text-2xl font-bold mb-5">
                Dataset Preview
            </h2>


            <div className="overflow-x-auto">

                <table className="w-full border-collapse">

                    <thead>

                        <tr>

                            {columns.map(column => (

                                <th
                                    key={column}
                                    className="border px-4 py-3 text-left bg-gray-100"
                                >
                                    {column}
                                </th>

                            ))}

                        </tr>

                    </thead>


                    <tbody>

                        {data.slice(0, 10).map(
                            (row, rowIndex) => (

                                <tr key={rowIndex}>

                                    {columns.map(column => (

                                        <td
                                            key={column}
                                            className="border px-4 py-3"
                                        >
                                            {String(
                                                row[column] ?? ""
                                            )}
                                        </td>

                                    ))}

                                </tr>

                            )
                        )}

                    </tbody>

                </table>

            </div>

        </div>

    );

}


export default Dashboard;