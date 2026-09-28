import api from "./axios";

// GET NOTIFICATIONS
export const getNotifications = async () => {
    const response = await api.get(
        "/notifications"
    );

    return response.data;
};

// MARK ONE NOTIFICATION AS READ
export const markNotificationAsRead = async (
    notificationId
) => {
    const response = await api.patch(
        `/notifications/${notificationId}/read`
    );

    return response.data;
};

// MARK ONE NOTIFICATION AS UNREAD
export const markNotificationAsUnread = async (
    notificationId
) => {
    const response = await api.patch(
        `/notifications/${notificationId}/unread`
    );

    return response.data;
};

// MARK ALL NOTIFICATIONS AS READ
export const markAllNotificationsAsRead =
    async () => {
        const response = await api.patch(
            "/notifications/read-all"
        );

        return response.data;
    };