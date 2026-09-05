import axios from "axios";

const ANALYTICS_API = "http://127.0.0.1:8000";

export const generateInsights = async (file) => {
    const formData = new FormData();

    formData.append("file", file);

    const response = await axios.post(
        `${ANALYTICS_API}/insights`,
        formData
    );

    return response.data;
};