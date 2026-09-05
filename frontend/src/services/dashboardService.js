import axios from "axios";


const API = axios.create({
    baseURL: "http://127.0.0.1:8000"
});


// =====================================================
// GENERATE DASHBOARD
// =====================================================

export const generateDashboard = async (file) => {

    const formData = new FormData();

    formData.append("file", file);


    const response = await API.post(
        "/dashboard",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        }
    );


    return response.data;

};


// =====================================================
// GENERATE INSIGHTS
// =====================================================

export const generateInsights = async (file) => {

    const formData = new FormData();

    formData.append("file", file);


    const response = await API.post(
        "/insights",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        }
    );


    return response.data;

};