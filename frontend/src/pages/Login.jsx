import {
    useEffect,
    useRef,
    useState,
} from "react";

import {
    useNavigate,
} from "react-router-dom";

import {
    useAuth0,
} from "@auth0/auth0-react";

import {
    Eye,
    EyeOff,
    Lock,
    Mail,
} from "lucide-react";

import {
    loginUser,
} from "../api/authApi";

import api from "../api/axios";

import {
    useAuth,
} from "../context/AuthContext";

import "./Login.css";


const Login = () => {

    const navigate = useNavigate();

    const {
        login,
    } = useAuth();


    const {
        loginWithRedirect,
        getIdTokenClaims,
        isLoading: auth0Loading,
        isAuthenticated: auth0Authenticated,
    } = useAuth0();


    const [email, setEmail] =
        useState("");

    const [password, setPassword] =
        useState("");

    const [showPassword, setShowPassword] =
        useState(false);

    const [error, setError] =
        useState("");

    const [loading, setLoading] =
        useState(false);


    const auth0ExchangeStarted =
        useRef(false);


    // ==========================================
    // AUTH0 → FASTAPI
    // ==========================================

    useEffect(() => {

        const exchangeAuth0Token = async () => {

            if (!auth0Authenticated) {
                return;
            }

            if (auth0ExchangeStarted.current) {
                return;
            }

            auth0ExchangeStarted.current = true;

            try {

                setError("");
                setLoading(true);

                const claims =
                    await getIdTokenClaims();

                if (
                    !claims ||
                    !claims.__raw
                ) {

                    throw new Error(
                        "Auth0 ID token not found"
                    );
                }

                const auth0IdToken =
                    claims.__raw;


                const response =
                    await api.post(
                        "/auth/auth0",
                        {
                            access_token:
                                auth0IdToken,
                        }
                    );


                const applicationToken =
                    response.data.access_token;


                if (!applicationToken) {

                    throw new Error(
                        "Application token not received"
                    );
                }


                login(
                    applicationToken
                );


                navigate(
                    "/dashboard"
                );

            } catch (error) {

                console.error(
                    "Auth0 backend login error:",
                    error
                );

                auth0ExchangeStarted.current =
                    false;


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
                        "Google login failed. Please try again."
                    );
                }

            } finally {

                setLoading(false);
            }
        };


        exchangeAuth0Token();

    }, [
        auth0Authenticated,
        getIdTokenClaims,
        login,
        navigate,
    ]);


    // ==========================================
    // EMAIL / PASSWORD LOGIN
    // ==========================================

    const handleSubmit = async (
        event
    ) => {

        event.preventDefault();

        setError("");
        setLoading(true);

        try {

            const data =
                await loginUser(
                    email,
                    password
                );


            login(
                data.access_token
            );


            navigate(
                "/dashboard"
            );

        } catch (error) {

            console.error(
                "Login error:",
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
                    "Login failed. Please check your email and password."
                );
            }

        } finally {

            setLoading(false);
        }
    };


    // ==========================================
    // GOOGLE LOGIN
    // ==========================================

    const handleGoogleLogin =
        async () => {

            setError("");

            try {

                await loginWithRedirect({
                    authorizationParams: {
                        connection:
                            "google-oauth2",
                    },
                });

            } catch (error) {

                console.error(
                    "Google login error:",
                    error
                );

                setError(
                    "Google login failed."
                );
            }
        };


    // ==========================================
    // FACEBOOK LOGIN
    // ==========================================

    const handleFacebookLogin =
        async () => {

            setError("");

            try {

                await loginWithRedirect({
                    authorizationParams: {
                        connection:
                            "facebook",
                    },
                });

            } catch (error) {

                console.error(
                    "Facebook login error:",
                    error
                );

                setError(
                    "Facebook login failed."
                );
            }
        };


    return (

        <div className="login-page">

            {/* Background decoration */}

            <div className="background-circle circle-one"></div>

            <div className="background-circle circle-two"></div>


            <div className="login-container">


                {/* ==========================================
                    LEFT SIDE
                ========================================== */}

                <div className="login-brand">

                    <div className="brand-content">

                        <div className="brand-logo">
                            B
                        </div>

                        <h1>
                            Blog Management
                        </h1>

                        <p>
                            Manage your posts,
                            connect with your
                            audience and grow
                            your blog.
                        </p>

                    </div>

                </div>


                {/* ==========================================
                    RIGHT SIDE
                ========================================== */}

                <div className="login-section">

                    <div className="login-card">


                        <div className="login-header">

                            <h2>
                                Welcome back
                            </h2>

                            <p>
                                Sign in to continue
                                to your account
                            </p>

                        </div>


                        {/* ERROR */}

                        {error && (

                            <div className="login-error">

                                {error}

                            </div>

                        )}


                        {/* ==========================================
                            LOGIN FORM
                        ========================================== */}

                        <form
                            onSubmit={
                                handleSubmit
                            }
                        >


                            {/* EMAIL */}

                            <div className="input-group">

                                <label>
                                    Email address
                                </label>


                                <div className="input-wrapper">

                                    <Mail
                                        size={19}
                                        className="input-icon"
                                    />


                                    <input
                                        type="email"
                                        value={email}
                                        onChange={(
                                            event
                                        ) =>
                                            setEmail(
                                                event.target.value
                                            )
                                        }
                                        placeholder="Enter your email"
                                        autoComplete="email"
                                        required
                                    />

                                </div>

                            </div>


                            {/* PASSWORD */}

                            <div className="input-group">

                                <label>
                                    Password
                                </label>


                                <div className="input-wrapper">

                                    <Lock
                                        size={19}
                                        className="input-icon"
                                    />


                                    <input
                                        type={
                                            showPassword
                                                ? "text"
                                                : "password"
                                        }
                                        value={
                                            password
                                        }
                                        onChange={(
                                            event
                                        ) =>
                                            setPassword(
                                                event.target.value
                                            )
                                        }
                                        placeholder="Enter your password"
                                        autoComplete="current-password"
                                        required
                                    />


                                    <button
                                        type="button"
                                        className="password-toggle"
                                        onClick={() =>
                                            setShowPassword(
                                                !showPassword
                                            )
                                        }
                                    >

                                        {showPassword ? (
                                            <EyeOff
                                                size={19}
                                            />
                                        ) : (
                                            <Eye
                                                size={19}
                                            />
                                        )}

                                    </button>

                                </div>

                            </div>


                            {/* LOGIN BUTTON */}

                            <button
                                type="submit"
                                className="login-button"
                                disabled={
                                    loading ||
                                    auth0Loading
                                }
                            >

                                {loading
                                    ? "Signing in..."
                                    : "Sign in"
                                }

                            </button>

                        </form>


                        {/* DIVIDER */}

                        <div className="divider">

                            <span>
                                OR
                            </span>

                        </div>


                        {/* SOCIAL LOGIN */}

                        <div className="social-buttons">


                            {/* GOOGLE */}

                            <button
                                type="button"
                                className="social-button"
                                onClick={
                                    handleGoogleLogin
                                }
                                disabled={
                                    loading ||
                                    auth0Loading
                                }
                            >

                                <span className="google-icon">
                                    G
                                </span>

                                <span>
                                    Continue with Google
                                </span>

                            </button>


                            {/* FACEBOOK */}

                            <button
                                type="button"
                                className="social-button"
                                onClick={
                                    handleFacebookLogin
                                }
                                disabled={
                                    loading ||
                                    auth0Loading
                                }
                            >

                                <span className="facebook-icon">
                                    f
                                </span>

                                <span>
                                    Continue with Facebook
                                </span>

                            </button>

                        </div>


                        <p className="login-footer">

                            By continuing, you agree
                            to our Terms of Service
                            and Privacy Policy.

                        </p>

                    </div>

                </div>

            </div>

        </div>
    );
};


export default Login;