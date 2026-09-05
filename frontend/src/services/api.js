import axios from "axios";

const API = axios.create({
    baseURL: "http://localhost:5000/api",
});

export const checkBackend = async () => {

    const response = await API.get("/health");

    return response.data;
};

export const uploadCSV = async (file) => {

    const formData = new FormData();

    formData.append("file", file);

    const response = await API.post(
        "/upload",
        formData
    );

    return response.data;
};