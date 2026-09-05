import { useState } from "react";
import { askQuestion } from "../services/qaServices";

function AIQuestionAnswer({ file }) {

    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleAsk = async () => {

        if (!file) {
            setError("Please upload a CSV file first.");
            return;
        }

        if (!question.trim()) {
            setError("Please enter a question.");
            return;
        }

        try {

            setLoading(true);
            setError("");
            setAnswer("");

            const result = await askQuestion(
                file,
                question
            );

            console.log(
                "AI Q&A RESPONSE:",
                result
            );

            if (result.success) {

                setAnswer(result.answer);

            } else {

                setError(
                    result.error ||
                    "Unable to answer the question."
                );

            }

        } catch (err) {

            console.error(
                "AI Q&A ERROR:",
                err
            );

            setError(
                err.response?.data?.detail ||
                err.message ||
                "Failed to get answer."
            );

        } finally {

            setLoading(false);

        }
    };


    return (

        <div className="bg-white rounded-xl shadow-md p-6 mt-8">

            <h2 className="text-2xl font-bold">
                AI Data Q&A
            </h2>

            <p className="text-gray-500 mt-2">
                Ask questions about your dataset.
            </p>


            <textarea
                value={question}
                onChange={(e) =>
                    setQuestion(e.target.value)
                }
                placeholder="Example: Which product has the highest sales?"
                className="w-full border rounded-lg p-4 mt-5"
                rows="3"
            />


            <button
                onClick={handleAsk}
                disabled={!file || loading}
                className="mt-4 bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg disabled:bg-gray-400"
            >

                {loading
                    ? "Analyzing..."
                    : "Ask AI"
                }

            </button>


            {error && (

                <div className="mt-4 bg-red-100 text-red-700 p-4 rounded-lg">
                    ✗ {error}
                </div>

            )}


            {answer && (

                <div className="mt-6 bg-gray-100 p-5 rounded-lg">

                    <h3 className="font-bold mb-2">
                        AI Answer
                    </h3>

                    <p className="text-gray-700 whitespace-pre-line">
                        {answer}
                    </p>

                </div>

            )}

        </div>

    );
}

export default AIQuestionAnswer;