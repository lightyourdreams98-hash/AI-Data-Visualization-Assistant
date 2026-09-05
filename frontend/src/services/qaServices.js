import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:8000"
});

export const askQuestion = async (file, question) => {

    const formData = new FormData();

    formData.append("file", file);
    formData.append("question", question);

    const response = await API.post(
        "/ask",
        formData
    );

    return response.data;
};