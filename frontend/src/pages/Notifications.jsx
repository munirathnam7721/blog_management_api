import {
    useEffect,
    useState,
} from "react";

import {
    Bell,
    Check,
    CheckCheck,
    Loader2,
} from "lucide-react";

import {
    getNotifications,
    markNotificationAsRead,
    markAllNotificationsAsRead,
} from "../api/notificationsApi";

import "./Notifications.css";

const Notifications = () => {
    const [notifications, setNotifications] =
        useState([]);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState("");

    const [actionLoading, setActionLoading] =
        useState(null);

    const loadNotifications = async () => {
        try {
            setLoading(true);
            setError("");

            const data =
                await getNotifications();

            setNotifications(data);
        } catch (error) {
            console.error(
                "Load notifications error:",
                error
            );

            setError(
                error.response?.data?.detail ||
                "Failed to load notifications"
            );
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadNotifications();
    }, []);

    const handleMarkAsRead = async (
        notificationId
    ) => {
        try {
            setActionLoading(notificationId);

            const updatedNotification =
                await markNotificationAsRead(
                    notificationId
                );

            setNotifications(
                (previousNotifications) =>
                    previousNotifications.map(
                        (notification) =>
                            notification.id ===
                            notificationId
                                ? updatedNotification
                                : notification
                    )
            );
        } catch (error) {
            console.error(
                "Mark notification as read error:",
                error
            );

            setError(
                error.response?.data?.detail ||
                "Failed to mark notification as read"
            );
        } finally {
            setActionLoading(null);
        }
    };

    const handleMarkAllAsRead = async () => {
        try {
            setActionLoading("all");

            await markAllNotificationsAsRead();

            setNotifications(
                (previousNotifications) =>
                    previousNotifications.map(
                        (notification) => ({
                            ...notification,
                            is_read: true,
                        })
                    )
            );
        } catch (error) {
            console.error(
                "Mark all notifications as read error:",
                error
            );

            setError(
                error.response?.data?.detail ||
                "Failed to mark all notifications as read"
            );
        } finally {
            setActionLoading(null);
        }
    };

    const unreadCount =
        notifications.filter(
            (notification) =>
                !notification.is_read
        ).length;

    const formatDate = (date) => {
        return new Date(date).toLocaleString(
            "en-IN",
            {
                day: "2-digit",
                month: "2-digit",
                year: "numeric",
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
            }
        );
    };

    if (loading) {
        return (
            <div className="notifications-page">
                <div className="notifications-loading">
                    <Loader2
                        size={30}
                        className="notification-spinner"
                    />
                    <p>
                        Loading notifications...
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="notifications-page">
            <div className="notifications-header">
                <div>
                    <div className="notifications-title">
                        <Bell size={28} />

                        <div>
                            <h1>
                                Notifications
                            </h1>

                            <p>
                                Stay updated with
                                your account
                                activity.
                            </p>
                        </div>
                    </div>
                </div>

                {unreadCount > 0 && (
                    <button
                        type="button"
                        className="mark-all-button"
                        onClick={
                            handleMarkAllAsRead
                        }
                        disabled={
                            actionLoading ===
                            "all"
                        }
                    >
                        {actionLoading ===
                        "all" ? (
                            <Loader2
                                size={17}
                                className="notification-spinner"
                            />
                        ) : (
                            <CheckCheck
                                size={17}
                            />
                        )}

                        Mark all as read
                    </button>
                )}
            </div>

            {error && (
                <div className="notifications-error">
                    {error}
                </div>
            )}

            <div className="notifications-summary">
                <strong>
                    {unreadCount}
                </strong>{" "}
                unread notification
                {unreadCount !== 1
                    ? "s"
                    : ""}
            </div>

            {notifications.length === 0 ? (
                <div className="no-notifications">
                    <Bell size={42} />

                    <h3>
                        No notifications
                    </h3>

                    <p>
                        You don't have any
                        notifications yet.
                    </p>
                </div>
            ) : (
                <div className="notifications-list">
                    {notifications.map(
                        (notification) => (
                            <div
                                key={
                                    notification.id
                                }
                                className={`notification-card ${
                                    notification.is_read
                                        ? "read"
                                        : "unread"
                                }`}
                            >
                                <div className="notification-icon">
                                    <Bell
                                        size={20}
                                    />
                                </div>

                                <div className="notification-content">
                                    <p className="notification-message">
                                        {
                                            notification.message
                                        }
                                    </p>

                                    <span className="notification-date">
                                        {formatDate(
                                            notification.created_at
                                        )}
                                    </span>

                                    <span className="notification-type">
                                        {
                                            notification.notification_type
                                        }
                                    </span>
                                </div>

                                {!notification.is_read && (
                                    <button
                                        type="button"
                                        className="mark-read-button"
                                        onClick={() =>
                                            handleMarkAsRead(
                                                notification.id
                                            )
                                        }
                                        disabled={
                                            actionLoading ===
                                            notification.id
                                        }
                                    >
                                        {actionLoading ===
                                        notification.id ? (
                                            <Loader2
                                                size={
                                                    15
                                                }
                                                className="notification-spinner"
                                            />
                                        ) : (
                                            <Check
                                                size={
                                                    15
                                                }
                                            />
                                        )}

                                        Mark as read
                                    </button>
                                )}

                                {notification.is_read && (
                                    <span className="read-label">
                                        <Check
                                            size={
                                                15
                                            }
                                        />
                                        Read
                                    </span>
                                )}
                            </div>
                        )
                    )}
                </div>
            )}
        </div>
    );
};

export default Notifications;