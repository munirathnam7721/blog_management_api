import {
    Bell,
    User,
    Heart,
    MessageCircle,
    Star,
    RefreshCw,
    Check,
} from "lucide-react";


import {
    useEffect,
    useState,
} from "react";


import {
    useNavigate,
} from "react-router-dom";


import {
    getNotifications,
    markNotificationAsRead,
    markNotificationAsUnread,
    markAllNotificationsAsRead,
} from "../api/notificationApi";


const Navbar = () => {

    const navigate = useNavigate();


    const [notifications, setNotifications] =
        useState([]);


    const [showNotifications, setShowNotifications] =
        useState(false);


    const [loading, setLoading] =
        useState(false);


    // ==========================================
    // LOAD NOTIFICATIONS
    // ==========================================

    const loadNotifications = async () => {

        try {

            const data =
                await getNotifications();

            setNotifications(data);

        } catch (error) {

            console.error(
                "Notification loading error:",
                error
            );
        }
    };


    // ==========================================
    // INITIAL LOAD
    // ==========================================

    useEffect(() => {

        loadNotifications();

    }, []);


    // ==========================================
    // AUTO REFRESH
    // EVERY 10 SECONDS
    // ==========================================

    useEffect(() => {

        const interval =
            setInterval(() => {

                loadNotifications();

            }, 10000);


        return () => {

            clearInterval(interval);

        };

    }, []);


    // ==========================================
    // UNREAD COUNT
    // ==========================================

    const unreadCount =
        notifications.filter(
            (notification) =>
                notification.is_read === false
        ).length;


    // ==========================================
    // NOTIFICATION ICON
    // ==========================================

    const getNotificationIcon = (
        notificationType
    ) => {

        switch (notificationType) {

            case "like":

                return (
                    <Heart size={18} />
                );


            case "comment":

                return (
                    <MessageCircle size={18} />
                );


            case "subscription":

                return (
                    <Star size={18} />
                );


            case "subscription_renewal":

                return (
                    <RefreshCw size={18} />
                );


            default:

                return (
                    <Bell size={18} />
                );
        }
    };


    // ==========================================
    // MARK INDIVIDUAL AS READ
    // ==========================================

    const handleMarkAsRead = async (
        notification
    ) => {

        if (notification.is_read) {

            return;
        }


        try {

            await markNotificationAsRead(
                notification.id
            );


            setNotifications(
                (previousNotifications) =>
                    previousNotifications.map(
                        (item) =>
                            item.id ===
                            notification.id
                                ? {
                                    ...item,
                                    is_read: true,
                                }
                                : item
                    )
            );

        } catch (error) {

            console.error(
                "Unable to mark notification as read:",
                error
            );
        }
    };


    // ==========================================
    // MARK AS UNREAD
    // ==========================================

    const handleMarkAsUnread = async (
        notification
    ) => {

        try {

            await markNotificationAsUnread(
                notification.id
            );


            setNotifications(
                (previousNotifications) =>
                    previousNotifications.map(
                        (item) =>
                            item.id ===
                            notification.id
                                ? {
                                    ...item,
                                    is_read: false,
                                }
                                : item
                    )
            );

        } catch (error) {

            console.error(
                "Unable to mark notification as unread:",
                error
            );
        }
    };


    // ==========================================
    // MARK ALL AS READ
    // ==========================================

    const handleMarkAllAsRead = async () => {

        if (unreadCount === 0) {

            return;
        }


        setLoading(true);


        try {

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
                "Unable to mark all notifications as read:",
                error
            );

        } finally {

            setLoading(false);

        }
    };


    // ==========================================
    // SHOW ONLY RECENT 10
    // ==========================================

    const recentNotifications =
        notifications.slice(0, 10);


    return (

        <header className="navbar">


            <div className="navbar-title">

                <h2>
                    Dashboard
                </h2>

            </div>


            <div className="navbar-actions">


                {/* ================================= */}
                {/* NOTIFICATION BELL */}
                {/* ================================= */}

                <div className="notification-wrapper">

                    <button
                        type="button"
                        className="icon-button notification-button"
                        title="Notifications"
                        onClick={() =>
                            setShowNotifications(
                                (previous) =>
                                    !previous
                            )
                        }
                    >

                        <Bell size={22} />


                        {unreadCount > 0 && (

                            <span className="notification-badge">

                                {unreadCount > 99
                                    ? "99+"
                                    : unreadCount
                                }

                            </span>

                        )}

                    </button>


                    {/* ================================= */}
                    {/* NOTIFICATION DROPDOWN */}
                    {/* ================================= */}

                    {showNotifications && (

                        <div className="notification-dropdown">


                            <div className="notification-header">

                                <div>

                                    <h3>
                                        Notifications
                                    </h3>

                                    <span>
                                        {unreadCount} unread
                                    </span>

                                </div>


                                {unreadCount > 0 && (

                                    <button
                                        type="button"
                                        className="mark-all-button"
                                        onClick={
                                            handleMarkAllAsRead
                                        }
                                        disabled={loading}
                                    >

                                        <Check size={15} />

                                        {loading
                                            ? "Updating..."
                                            : "Mark all as read"
                                        }

                                    </button>

                                )}

                            </div>


                            <div className="notification-list">


                                {recentNotifications.length === 0 ? (

                                    <div className="no-notifications">

                                        <Bell size={32} />

                                        <p>
                                            No notifications
                                        </p>

                                    </div>

                                ) : (

                                    recentNotifications.map(
                                        (notification) => (

                                            <div
                                                key={
                                                    notification.id
                                                }
                                                className={
                                                    notification.is_read
                                                        ? "notification-item"
                                                        : "notification-item unread"
                                                }
                                            >


                                                <div className="notification-icon">

                                                    {getNotificationIcon(
                                                        notification.notification_type
                                                    )}

                                                </div>


                                                <div className="notification-content">

                                                    <p>
                                                        {
                                                            notification.message
                                                        }
                                                    </p>


                                                    <span>

                                                        {new Date(
                                                            notification.created_at
                                                        ).toLocaleString()}

                                                    </span>


                                                    <div className="notification-actions">


                                                        {!notification.is_read ? (

                                                            <button
                                                                type="button"
                                                                onClick={() =>
                                                                    handleMarkAsRead(
                                                                        notification
                                                                    )
                                                                }
                                                            >
                                                                Mark as read
                                                            </button>

                                                        ) : (

                                                            <button
                                                                type="button"
                                                                onClick={() =>
                                                                    handleMarkAsUnread(
                                                                        notification
                                                                    )
                                                                }
                                                            >
                                                                Mark as unread
                                                            </button>

                                                        )}

                                                    </div>

                                                </div>

                                            </div>

                                        )
                                    )

                                )}

                            </div>

                        </div>

                    )}

                </div>


                {/* ================================= */}
                {/* PROFILE */}
                {/* ================================= */}

                <button
                    type="button"
                    className="profile-button"
                    title="Profile"
                    onClick={() =>
                        navigate("/profile")
                    }
                >

                    <User size={22} />

                </button>


            </div>

        </header>
    );
};


export default Navbar;