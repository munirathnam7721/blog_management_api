import {
    User,
    Mail,
    Shield,
    LogOut,
    Hash,
    CheckCircle,
} from "lucide-react";

import {
    useEffect,
    useState,
} from "react";

import {
    useNavigate,
} from "react-router-dom";

import {
    useAuth,
} from "../context/AuthContext";

import api from "../api/axios";

import "./Profile.css";


const Profile = () => {

    const navigate = useNavigate();

    const {
        logout,
    } = useAuth();


    const [user, setUser] = useState(null);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");


    // ==========================================
    // LOAD PROFILE
    // ==========================================

    const loadProfile = async () => {

        try {

            setLoading(true);

            setError("");


            const response = await api.get(
                "/auth/me"
            );


            setUser(response.data);

        } catch (error) {

            console.error(
                "Profile loading error:",
                error
            );


            if (
                error.response &&
                error.response.data &&
                error.response.data.detail
            ) {

                setError(
                    error.response.data.detail
                );

            } else {

                setError(
                    "Unable to load profile."
                );
            }

        } finally {

            setLoading(false);

        }
    };


    // ==========================================
    // INITIAL LOAD
    // ==========================================

    useEffect(() => {

        loadProfile();

    }, []);


    // ==========================================
    // LOGOUT
    // ==========================================

    const handleLogout = () => {

        logout();

        navigate("/login");

    };


    // ==========================================
    // LOADING
    // ==========================================

    if (loading) {

        return (

            <div className="profile-page">

                <div className="profile-loading">

                    Loading profile...

                </div>

            </div>

        );
    }


    // ==========================================
    // ERROR
    // ==========================================

    if (error) {

        return (

            <div className="profile-page">

                <div className="profile-error">

                    <p>
                        {error}
                    </p>

                    <button
                        type="button"
                        onClick={loadProfile}
                    >
                        Try Again
                    </button>

                </div>

            </div>

        );
    }


    // ==========================================
    // PROFILE
    // ==========================================

    return (

        <div className="profile-page">

            <div className="profile-container">


                {/* ================================= */}
                {/* PAGE HEADER */}
                {/* ================================= */}

                <div className="profile-page-header">

                    <div>

                        <h1>
                            My Profile
                        </h1>

                        <p>
                            Manage your account information
                            and authentication details.
                        </p>

                    </div>


                    <div className="profile-status">

                        <CheckCircle size={17} />

                        <span>
                            Active Account
                        </span>

                    </div>

                </div>


                {/* ================================= */}
                {/* PROFILE OVERVIEW */}
                {/* ================================= */}

                <div className="profile-overview">


                    {/* AVATAR */}

                    <div className="profile-avatar-large">

                        <User size={42} />

                    </div>


                    {/* USER INFORMATION */}

                    <div className="profile-overview-info">

                        <h2>
                            {user?.username || "User"}
                        </h2>

                        <p>
                            {user?.email || "Email not available"}
                        </p>

                    </div>


                    {/* PROVIDER */}

                    <div className="profile-provider">

                        <span>
                            Login method
                        </span>

                        <strong>
                            {user?.provider
                                ? user.provider.toUpperCase()
                                : "LOCAL"
                            }
                        </strong>

                    </div>

                </div>


                {/* ================================= */}
                {/* ACCOUNT INFORMATION */}
                {/* ================================= */}

                <div className="profile-section">

                    <div className="profile-section-header">

                        <h2>
                            Account Information
                        </h2>

                        <p>
                            Your registered account details
                        </p>

                    </div>


                    <div className="profile-info-grid">


                        {/* USERNAME */}

                        <div className="profile-info-card">

                            <div className="profile-info-icon">

                                <User size={21} />

                            </div>


                            <div className="profile-info-content">

                                <span>
                                    Username
                                </span>

                                <strong>
                                    {user?.username ||
                                        "Not available"
                                    }
                                </strong>

                            </div>

                        </div>


                        {/* EMAIL */}

                        <div className="profile-info-card">

                            <div className="profile-info-icon">

                                <Mail size={21} />

                            </div>


                            <div className="profile-info-content">

                                <span>
                                    Email Address
                                </span>

                                <strong>
                                    {user?.email ||
                                        "Not available"
                                    }
                                </strong>

                            </div>

                        </div>


                        {/* USER ID */}

                        <div className="profile-info-card">

                            <div className="profile-info-icon">

                                <Hash size={21} />

                            </div>


                            <div className="profile-info-content">

                                <span>
                                    User ID
                                </span>

                                <strong>
                                    #{user?.id || "-"}
                                </strong>

                            </div>

                        </div>


                        {/* AUTHENTICATION */}

                        <div className="profile-info-card">

                            <div className="profile-info-icon">

                                <Shield size={21} />

                            </div>


                            <div className="profile-info-content">

                                <span>
                                    Authentication
                                </span>

                                <strong>
                                    {user?.provider
                                        ? user.provider.toUpperCase()
                                        : "LOCAL"
                                    }
                                </strong>

                            </div>

                        </div>

                    </div>

                </div>


                {/* ================================= */}
                {/* SECURITY */}
                {/* ================================= */}

                <div className="profile-security">

                    <div className="security-icon">

                        <Shield size={22} />

                    </div>


                    <div className="security-content">

                        <h3>
                            Account Security
                        </h3>

                        <p>
                            Your account is protected with
                            secure authentication.
                        </p>

                    </div>


                    <div className="security-status">

                        <CheckCircle size={17} />

                        Secured

                    </div>

                </div>


                {/* ================================= */}
                {/* LOGOUT */}
                {/* ================================= */}

                <div className="profile-logout-section">

                    <div>

                        <h3>
                            Sign out
                        </h3>

                        <p>
                            Sign out from your current account.
                        </p>

                    </div>


                    <button
                        type="button"
                        className="profile-logout-button"
                        onClick={handleLogout}
                    >

                        <LogOut size={18} />

                        <span>
                            Logout
                        </span>

                    </button>

                </div>

            </div>

        </div>

    );
};


export default Profile;