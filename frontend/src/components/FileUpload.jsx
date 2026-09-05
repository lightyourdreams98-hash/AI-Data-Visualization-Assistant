import { useState } from "react";
import { uploadCSV } from "../services/api";

function FileUpload({ onFileSelect }) {

    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);


    // ---------------------------------------
    // File selection
    // ---------------------------------------

    const handleFileChange = (event) => {

        const selectedFile = event.target.files[0];

        setMessage("");
        setError("");

        if (!selectedFile) {
            setFile(null);
            onFileSelect(null);
            return;
        }

        if (!selectedFile.name.toLowerCase().endsWith(".csv")) {

            setError("Please select a CSV file.");

            setFile(null);
            onFileSelect(null);

            return;
        }

        setFile(selectedFile);

        // Send selected file to App.jsx
        onFileSelect(selectedFile);

    };


    // ---------------------------------------
    // Upload CSV
    // ---------------------------------------

    const handleUpload = async () => {

        if (!file) {

            setError("Please select a CSV file first.");

            return;
        }

        try {

            setLoading(true);
            setError("");
            setMessage("");

            const result = await uploadCSV(file);

            console.log("Upload response:", result);

            setMessage(
                result.message || "CSV uploaded successfully"
            );

        } catch (err) {

            console.error(err);

            setError(
                err.response?.data?.message ||
                err.message ||
                "Upload failed"
            );

        } finally {

            setLoading(false);

        }

    };


    return (

        <div className="bg-white rounded-xl shadow-md p-8 w-full max-w-xl">

            <h2 className="text-2xl font-bold mb-6">
                Upload Dataset
            </h2>


            {/* File input */}

            <input
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                className="w-full border border-gray-400 rounded-lg p-3"
            />


            {/* Selected file */}

            {file && (

                <p className="text-gray-600 mt-4">
                    Selected: {file.name}
                </p>

            )}


            {/* Upload button */}

            <button
                onClick={handleUpload}
                disabled={!file || loading}
                className="w-full mt-5 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg disabled:bg-gray-400"
            >

                {loading
                    ? "Uploading..."
                    : "Upload CSV"
                }

            </button>


            {/* Success */}

            {message && (

                <p className="text-green-600 mt-4">
                    ✓ {message}
                </p>

            )}


            {/* Error */}

            {error && (

                <p className="text-red-600 mt-4">
                    ✗ {error}
                </p>

            )}

        </div>

    );

}

export default FileUpload;