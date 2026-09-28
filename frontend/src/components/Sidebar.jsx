import {
    LayoutDashboard,
    FileText,
    MessageCircle,
    CreditCard,
    Bell,
    User,
    LogOut,
    Bot,
} from "lucide-react";

import {
    NavLink,
    useNavigate,
} from "react-router-dom";

import {
    useAuth0,
} from "@auth0/auth0-react";

import {
    useAuth,
} from "../context/AuthContext";


const Sidebar = () => {

    const navigate = useNavigate();

    const { logout } = useAuth();

    const {
        logout: auth0Logout,
    } = useAuth0();


    const handleLogout = () => {

        // Logout from our application
        logout();

        // Logout from Auth0 / Google
        auth0Logout({
            logoutParams: {
                returnTo: window.location.origin,
            },
        });
    };


    return (
        <aside className="sidebar">

            <div className="sidebar-logo">

                <h2>
                    Blog Manager
                </h2>

            </div>


            <nav className="sidebar-nav">

                <NavLink
                    to="/dashboard"
                    className="sidebar-link"
                >
                    <LayoutDashboard size={20} />

                    <span>
                        Dashboard
                    </span>
                </NavLink>


                <NavLink
                    to="/posts"
                    className="sidebar-link"
                >
                    <FileText size={20} />

                    <span>
                        Posts
                    </span>
                </NavLink>


                <NavLink
                    to="/comments"
                    className="sidebar-link"
                >
                    <MessageCircle size={20} />

                    <span>
                        Comments
                    </span>
                </NavLink>


                <NavLink
                    to="/subscriptions"
                    className="sidebar-link"
                >
                    <CreditCard size={20} />

                    <span>
                        Subscriptions
                    </span>
                </NavLink>


                <NavLink
                    to="/billing"
                    className="sidebar-link"
                >
                    <CreditCard size={20} />

                    <span>
                        Billing
                    </span>
                </NavLink>


                <NavLink
                    to="/notifications"
                    className="sidebar-link"
                >
                    <Bell size={20} />

                    <span>
                        Notifications
                    </span>
                </NavLink>


                <NavLink
                    to="/profile"
                    className="sidebar-link"
                >
                    <User size={20} />

                    <span>
                        Profile
                    </span>
                </NavLink>


                <NavLink
                    to="/ai-support"
                    className="sidebar-link"
                >
                    <Bot size={20} />

                    <span>
                        AI Support
                    </span>
                </NavLink>

            </nav>


            <div className="sidebar-bottom">

                <button
                    type="button"
                    className="logout-button"
                    onClick={handleLogout}
                >

                    <LogOut size={20} />

                    <span>
                        Logout
                    </span>

                </button>

            </div>

        </aside>
    );
};


export default Sidebar;