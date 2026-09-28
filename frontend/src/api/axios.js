import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use(
    (config) => {

        const token = localStorage.getItem(
            "access_token"
        );

        if (token) {
            config.headers.Authorization =
                `Bearer ${token}`;
        }

        // ==========================================
        // HANDLE FORMDATA REQUESTS
        // ==========================================

        if (config.data instanceof FormData) {

            // Let the browser/Axios automatically
            // set multipart/form-data with boundary
            delete config.headers["Content-Type"];

        } else {

            // Normal JSON requests
            config.headers["Content-Type"] =
                "application/json";
        }

        return config;
    },

    (error) => {
        return Promise.reject(error);
    }
);

export default api;