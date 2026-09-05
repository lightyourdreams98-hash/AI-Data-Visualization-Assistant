import { useState, useEffect } from "react";

import { checkBackend } from "./services/api";
import FileUpload from "./components/FileUpload";
import Dashboard from "./components/Dashboard";
import QA from "./components/QA";
function App() {

    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    const [file, setFile] = useState(null);

    // ---------------------------------------
    // Check backend
    // ---------------------------------------

    useEffect(() => {

        const testConnection = async () => {

            try {

                const data = await checkBackend();

                setMessage(data.message);

            } catch (err) {

                console.error(err);

                setError("Backend connection failed");

            }

        };

        testConnection();

    }, []);


    return (

        <div className="min-h-screen bg-gray-100 p-10">

            <div className="max-w-5xl mx-auto">

                {/* HEADER */}

                <h1 className="text-4xl font-bold text-center mb-10">
                    AI Data Visualization Assistant
                </h1>


                {/* BACKEND STATUS */}

                <div className="text-center mb-8">

                    {message && (
                        <p className="text-green-600">
                            ✓ {message}
                        </p>
                    )}

                    {error && (
                        <p className="text-red-600">
                            ✗ {error}
                        </p>
                    )}

                </div>


                {/* FILE UPLOAD */}

                <div className="flex justify-center">

                    <FileUpload
                        onFileSelect={setFile}
                    />

                </div>


                {/* DASHBOARD */}

                
            
            <Dashboard file={file} />

<QA file={file} />
            </div>

        </div>

    );

}

export default App;