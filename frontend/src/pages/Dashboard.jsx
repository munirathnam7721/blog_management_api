import {
    useEffect,
    useState,
} from "react";

import {
    FileText,
    MessageCircle,
    Heart,
    Eye,
} from "lucide-react";

import {
    ResponsiveContainer,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
} from "recharts";

import DashboardLayout from "../layouts/DashboardLayout";

import { getDashboard } from "../api/dashboardApi";


const Dashboard = () => {

    const [dashboard, setDashboard] = useState(null);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");


    useEffect(() => {

        const loadDashboard = async () => {

            try {

                const data = await getDashboard();

                setDashboard(data);

            } catch (error) {

                console.error(
                    "Dashboard error:",
                    error
                );

                setError(
                    "Unable to load dashboard data."
                );

            } finally {

                setLoading(false);
            }
        };


        loadDashboard();

    }, []);


    if (loading) {

        return (
            <DashboardLayout>

                <div className="loading">
                    Loading dashboard...
                </div>

            </DashboardLayout>
        );
    }


    if (error) {

        return (
            <DashboardLayout>

                <div className="error-message">
                    {error}
                </div>

            </DashboardLayout>
        );
    }


    const statistics =
        dashboard?.statistics || {};


    const analytics =
        dashboard?.post_analytics || [];


    const chartData = analytics.map(
        (post) => ({
            name:
                post.post_title.length > 15
                    ? post.post_title.substring(
                        0,
                        15
                    ) + "..."
                    : post.post_title,

            likes: post.likes,

            comments: post.comments,
        })
    );


    return (
        <DashboardLayout>

            {/* ============================== */}
            {/* WELCOME */}
            {/* ============================== */}

            <div className="dashboard-header">

                <div>

                    <h1>
                        Welcome back,{" "}
                        {dashboard?.user?.username}
                    </h1>

                    <p>
                        Here's what's happening
                        with your blog.
                    </p>

                </div>

            </div>


            {/* ============================== */}
            {/* STATISTICS */}
            {/* ============================== */}

            <div className="stats-grid">


                {/* POSTS */}

                <div className="stat-card">

                    <div className="stat-icon posts-icon">

                        <FileText size={24} />

                    </div>

                    <div>

                        <p>
                            Total Posts
                        </p>

                        <h2>
                            {statistics.total_posts ?? 0}
                        </h2>

                    </div>

                </div>


                {/* COMMENTS */}

                <div className="stat-card">

                    <div className="stat-icon comments-icon">

                        <MessageCircle size={24} />

                    </div>

                    <div>

                        <p>
                            Total Comments
                        </p>

                        <h2>
                            {statistics.total_comments ?? 0}
                        </h2>

                    </div>

                </div>


                {/* LIKES */}

                <div className="stat-card">

                    <div className="stat-icon likes-icon">

                        <Heart size={24} />

                    </div>

                    <div>

                        <p>
                            Likes Received
                        </p>

                        <h2>
                            {statistics.total_likes_received ?? 0}
                        </h2>

                    </div>

                </div>


                {/* VIEWS */}

                <div className="stat-card">

                    <div className="stat-icon views-icon">

                        <Eye size={24} />

                    </div>

                    <div>

                        <p>
                            Total Views
                        </p>

                        <h2>
                            {statistics.total_views ?? 0}
                        </h2>

                    </div>

                </div>

            </div>


            {/* ============================== */}
            {/* ANALYTICS */}
            {/* ============================== */}

            <div className="analytics-card">

                <div className="analytics-header">

                    <div>

                        <h2>
                            Post Analytics
                        </h2>

                        <p>
                            Likes and comments
                            for your posts
                        </p>

                    </div>

                </div>


                {chartData.length === 0 ? (

                    <div className="empty-state">

                        <FileText size={40} />

                        <p>
                            No posts available
                            for analytics.
                        </p>

                    </div>

                ) : (

                    <div className="chart-container">

                        <ResponsiveContainer
                            width="100%"
                            height={350}
                        >

                            <BarChart
                                data={chartData}
                            >

                                <CartesianGrid
                                    strokeDasharray="3 3"
                                />

                                <XAxis
                                    dataKey="name"
                                />

                                <YAxis />

                                <Tooltip />

                                <Bar
                                    dataKey="likes"
                                    name="Likes"
                                />

                                <Bar
                                    dataKey="comments"
                                    name="Comments"
                                />

                            </BarChart>

                        </ResponsiveContainer>

                    </div>

                )}

            </div>


            {/* ============================== */}
            {/* POST ANALYTICS TABLE */}
            {/* ============================== */}

            <div className="analytics-card">

                <h2>
                    Your Posts
                </h2>


                {analytics.length === 0 ? (

                    <p className="empty-text">
                        You haven't created
                        any posts yet.
                    </p>

                ) : (

                    <div className="table-wrapper">

                        <table>

                            <thead>

                                <tr>

                                    <th>
                                        Post
                                    </th>

                                    <th>
                                        Likes
                                    </th>

                                    <th>
                                        Comments
                                    </th>

                                    <th>
                                        Created
                                    </th>

                                </tr>

                            </thead>


                            <tbody>

                                {analytics.map(
                                    (post) => (

                                        <tr
                                            key={
                                                post.post_id
                                            }
                                        >

                                            <td>
                                                {
                                                    post.post_title
                                                }
                                            </td>

                                            <td>
                                                {
                                                    post.likes
                                                }
                                            </td>

                                            <td>
                                                {
                                                    post.comments
                                                }
                                            </td>

                                            <td>
                                                {new Date(
                                                    post.created_at
                                                ).toLocaleDateString()}
                                            </td>

                                        </tr>

                                    )
                                )}

                            </tbody>

                        </table>

                    </div>

                )}

            </div>

        </DashboardLayout>
    );
};


export default Dashboard;