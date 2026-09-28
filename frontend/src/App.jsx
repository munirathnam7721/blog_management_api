import {
    BrowserRouter,
    Routes,
    Route,
} from "react-router-dom";


import Login from "./pages/Login";

import Dashboard from "./pages/Dashboard";

import Posts from "./pages/Posts";

import Comments from "./pages/Comments";

import Subscriptions from "./pages/Subscriptions";

import Billing from "./pages/Billing";

import Notifications from "./pages/Notifications";

import Profile from "./pages/Profile";

import AISupport from "./components/AISupport";

import ProtectedRoute from "./components/ProtectedRoute";


function App() {

    return (

        <BrowserRouter>

            <Routes>


                {/* ================================= */}
                {/* LOGIN */}
                {/* ================================= */}

                <Route
                    path="/login"
                    element={
                        <Login />
                    }
                />


                {/* ================================= */}
                {/* DASHBOARD */}
                {/* ================================= */}

                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>

                            <Dashboard />

                        </ProtectedRoute>
                    }
                />


                {/* ================================= */}
                {/* POSTS */}
                {/* ================================= */}

                <Route
                    path="/posts"
                    element={
                        <ProtectedRoute>

                            <Posts />

                        </ProtectedRoute>
                    }
                />


                {/* ================================= */}
                {/* COMMENTS */}
                {/* ================================= */}

                <Route
                    path="/comments"
                    element={
                        <ProtectedRoute>

                            <Comments />

                        </ProtectedRoute>
                    }
                />


                {/* ================================= */}
                {/* SUBSCRIPTIONS */}
                {/* ================================= */}

                <Route
                    path="/subscriptions"
                    element={
                        <ProtectedRoute>

                            <Subscriptions />

                        </ProtectedRoute>
                    }
                />


                {/* ================================= */}
                {/* BILLING */}
                {/* ================================= */}

                <Route
                    path="/billing"
                    element={
                        <ProtectedRoute>

                            <Billing />

                        </ProtectedRoute>
                    }
                />


                {/* ================================= */}
                {/* NOTIFICATIONS */}
                {/* ================================= */}

                <Route
                    path="/notifications"
                    element={
                        <ProtectedRoute>

                            <Notifications />

                        </ProtectedRoute>
                    }
                />


                {/* ================================= */}
                {/* PROFILE */}
                {/* ================================= */}

                <Route
                    path="/profile"
                    element={
                        <ProtectedRoute>

                            <Profile />

                        </ProtectedRoute>
                    }
                />


                {/* ================================= */}
                {/* AI SUPPORT */}
                {/* ================================= */}

                <Route
                    path="/ai-support"
                    element={
                        <ProtectedRoute>

                            <AISupport />

                        </ProtectedRoute>
                    }
                />


                {/* ================================= */}
                {/* DEFAULT */}
                {/* ================================= */}

                <Route
                    path="*"
                    element={
                        <Login />
                    }
                />

            </Routes>

        </BrowserRouter>
    );
}


export default App;