import api from "./axios";

// GET ALL ACTIVE PLANS
export const getSubscriptionPlans = async () => {
    const response = await api.get(
        "/subscriptions/plans"
    );

    return response.data;
};

// GET MY ACTIVE SUBSCRIPTION
export const getMySubscription = async () => {
    const response = await api.get(
        "/subscriptions/my-subscription"
    );

    return response.data;
};

// SUBSCRIBE TO A PLAN
export const subscribeToPlan = async (planId) => {
    const response = await api.post(
        "/subscriptions/subscribe",
        {
            plan_id: planId,
        }
    );

    return response.data;
};

// RENEW SUBSCRIPTION
export const renewSubscription = async () => {
    const response = await api.post(
        "/subscriptions/renew"
    );

    return response.data;
};

// GET BILLING HISTORY
export const getBillingHistory = async () => {
    const response = await api.get(
        "/subscriptions/billing-history"
    );

    return response.data;
};