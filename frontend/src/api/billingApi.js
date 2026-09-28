import api from "./axios";

export const getBillingHistory = async () => {
    const response = await api.get(
        "/subscriptions/billing-history"
    );

    return response.data;
};