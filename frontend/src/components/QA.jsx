
import { useState } from "react";
import { askQuestion } from "../services/qaServices";

function QA({ file }) {

    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleAskQuestion = async () => {

        // ---------------------------------------
        // Validate file
        // ---------------------------------------

        if (!file) {
            setError("Please select a CSV file first.");
            return;
        }

        // ---------------------------------------
        // Validate question
        // ---------------------------------------

        if (!question.trim()) {
            setError("Please enter a question.");
            return;
        }

        try {

            setLoading(true);
            setError("");
            setAnswer("");

            console.log(
                "Sending question:",
                question
            );

            console.log(
                "Sending file:",
                file.name
            );

            // ---------------------------------------
            // Call FastAPI
            // ---------------------------------------

            const result = await askQuestion(
                file,
                question
            );

            console.log(
                "Q&A response:",
                result
            );

            // ---------------------------------------
            // Display answer
            // ---------------------------------------

            setAnswer(
                result.answer ||
                "No answer was generated."
            );

        } catch (err) {

            console.error(
                "Q&A ERROR:",
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
                "Failed to get answer."
            );

        } finally {

            setLoading(false);

        }
    };


    // ============================================
    // UI
    // ============================================

    return (

        <div className="mt-10 bg-white rounded-xl shadow-md p-8">

            {/* -------------------------------- */}
            {/* Header */}
            {/* -------------------------------- */}

            <h2 className="text-2xl font-bold">

                Ask Questions About Your Data

            </h2>

            <p className="text-gray-500 mt-2">

                Ask questions in natural language
                about your uploaded dataset.

            </p>


            {/* -------------------------------- */}
            {/* Selected File */}
            {/* -------------------------------- */}

            {file && (

                <div className="mt-5 bg-gray-100 rounded-lg p-4">

                    <p className="text-sm text-gray-500">

                        Dataset

                    </p>

                    <p className="font-semibold">

                        {file.name}

                    </p>

                </div>

            )}


            {/* -------------------------------- */}
            {/* Question Input */}
            {/* -------------------------------- */}

            <div className="mt-6">

                <label className="block font-semibold mb-2">

                    Your Question

                </label>

                <textarea

                    value={question}

                    onChange={(e) =>
                        setQuestion(e.target.value)
                    }

                    placeholder="Example: Which product has the highest sales?"

                    rows={3}

                    className="w-full border border-gray-300 rounded-lg p-4 focus:outline-none focus:ring-2 focus:ring-purple-500"

                />

            </div>


            {/* -------------------------------- */}
            {/* Ask Button */}
            {/* -------------------------------- */}

            <button

                onClick={handleAskQuestion}

                disabled={!file || loading}

                className="mt-5 bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg disabled:bg-gray-400"

            >

                {loading
                    ? "Analyzing..."
                    : "Ask Question"
                }

            </button>


            {/* -------------------------------- */}
            {/* Error */}
            {/* -------------------------------- */}

            {error && (

                <div className="mt-5 bg-red-50 border border-red-200 rounded-lg p-4">

                    <p className="text-red-600">

                        ✗ {error}

                    </p>

                </div>

            )}


            {/* -------------------------------- */}
            {/* Answer */}
            {/* -------------------------------- */}

            {answer && (

                <div className="mt-6 bg-purple-50 border border-purple-200 rounded-lg p-6">

                    <h3 className="font-bold text-lg mb-2">

                        Answer

                    </h3>

                    <p className="text-gray-700 leading-relaxed">

                        {answer}

                    </p>

                </div>

            )}


            {/* -------------------------------- */}
            {/* Example Questions */}
            {/* -------------------------------- */}

            <div className="mt-8">

                <p className="font-semibold mb-3">

                    Try asking:

                </p>

                <div className="flex flex-wrap gap-2">

                    {[
                        "Which product has the highest sales?",
                        "Which region has the highest profit?",
                        "What is the average sales?",
                        "What is the maximum profit?",
                        "What is the total sales?",
                        "What is the relationship between sales and profit?"
                    ].map((example) => (

                        <button

                            key={example}

                            onClick={() =>
                                setQuestion(example)
                            }

                            className="text-sm bg-gray-100 hover:bg-gray-200 px-3 py-2 rounded-lg"

                        >

                            {example}

                        </button>

                    ))}

                </div>

            </div>

        </div>

    );
}

export default QA;