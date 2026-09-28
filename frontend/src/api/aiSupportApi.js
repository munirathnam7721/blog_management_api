import api from "./axios";

export const sendAIMessage = async (message) => {
    const response = await api.post(
        "/api/ai-support/",
        {
            message,
        }
    );

    return response.data;
};