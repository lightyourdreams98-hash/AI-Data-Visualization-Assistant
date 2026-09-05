const express = require("express");
const cors = require("cors");
const multer = require("multer");
const path = require("path");
const fs = require("fs");

require("dotenv").config();

const app = express();

const PORT = process.env.PORT || 5000;

// ------------------------------------
// Middleware
// ------------------------------------

app.use(cors());

app.use(express.json());

// ------------------------------------
// Upload Directory
// ------------------------------------

// Always create uploads inside backend/
const uploadDir = path.join(__dirname, "uploads");

if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir, { recursive: true });
}

console.log("Upload directory:", uploadDir);

// ------------------------------------
// Multer Configuration
// ------------------------------------

const storage = multer.diskStorage({

    destination: (req, file, cb) => {

        cb(null, uploadDir);

    },

    filename: (req, file, cb) => {

        const uniqueName =
            Date.now() +
            "-" +
            file.originalname;

        cb(null, uniqueName);

    }

});

const upload = multer({

    storage: storage,

    fileFilter: (req, file, cb) => {

        const extension =
            path.extname(file.originalname).toLowerCase();

        if (extension !== ".csv") {

            return cb(
                new Error("Only CSV files are allowed")
            );

        }

        cb(null, true);

    },

    limits: {
        fileSize: 10 * 1024 * 1024
    }

});

// ------------------------------------
// Health Check
// ------------------------------------

app.get("/api/health", (req, res) => {

    res.json({

        success: true,

        message: "Backend is connected successfully"

    });

});

// ------------------------------------
// CSV Upload
// ------------------------------------

app.post(
    "/api/upload",
    upload.single("file"),
    (req, res) => {

        try {

            if (!req.file) {

                return res.status(400).json({

                    success: false,

                    message: "No CSV file uploaded"

                });

            }

            console.log(
                "CSV uploaded:",
                req.file.filename
            );

            res.status(200).json({

                success: true,

                message: "CSV uploaded successfully",

                file: {

                    originalName:
                        req.file.originalname,

                    filename:
                        req.file.filename,

                    path:
                        req.file.path,

                    size:
                        req.file.size

                }

            });

        } catch (error) {

            console.error(
                "Upload error:",
                error
            );

            res.status(500).json({

                success: false,

                message: "File upload failed"

            });

        }

    }
);

// ------------------------------------
// Serve uploaded files
// ------------------------------------

app.use(
    "/uploads",
    express.static(uploadDir)
);

// ------------------------------------
// Error Handler
// ------------------------------------

app.use((err, req, res, next) => {

    console.error("Server error:", err);

    res.status(400).json({

        success: false,

        message: err.message

    });

});

// ------------------------------------
// Start Server
// ------------------------------------

app.listen(PORT, () => {

    console.log(
        `Backend running on http://localhost:${PORT}`
    );

    console.log(
        `Upload folder: ${uploadDir}`
    );

});