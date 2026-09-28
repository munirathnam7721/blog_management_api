import {
    useEffect,
    useState,
} from "react";

import {
    getMyPosts,
    createPost,
    updatePost,
    deletePost,
} from "../api/postsApi";
import "./Posts.css";

import PostForm from "../components/PostForm";
import PostCard from "../components/PostCard";


function Posts() {

    const [posts, setPosts] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");

    const [search, setSearch] = useState("");

    const [page, setPage] = useState(1);

    const [totalPages, setTotalPages] = useState(0);

    const [showForm, setShowForm] = useState(false);

    const [editingPost, setEditingPost] = useState(null);

    const [saving, setSaving] = useState(false);

    const limit = 10;


    // ============================================
    // LOAD MY POSTS
    // ============================================

    const loadPosts = async () => {

        try {

            setLoading(true);

            setError("");

            const data = await getMyPosts(
                page,
                limit,
                search
            );

            setPosts(
                data.posts || []
            );

            setTotalPages(
                data.total_pages || 0
            );

        } catch (error) {

            console.error(
                "Failed to load posts:",
                error
            );

            const detail =
                error.response?.data?.detail;

            if (Array.isArray(detail)) {

                setError(
                    detail
                        .map((item) =>
                            item.msg
                        )
                        .join(", ")
                );

            } else {

                setError(
                    detail ||
                    "Failed to load posts."
                );
            }

        } finally {

            setLoading(false);
        }
    };


    // ============================================
    // LOAD POSTS WHEN PAGE OR SEARCH CHANGES
    // ============================================

    useEffect(() => {

        loadPosts();

    }, [page, search]);


    // ============================================
    // CREATE / UPDATE POST
    // ============================================

    const handleSubmit = async (formData) => {

        try {

            setSaving(true);

            setError("");

            if (editingPost) {

                await updatePost(
                    editingPost.id,
                    {
                        title: formData.title,
                        content: formData.content,
                        images:
                            formData.images || [],
                        postStatus:
                            formData.postStatus,
                        scheduledAt:
                            formData.scheduledAt,
                    }
                );

            } else {

                await createPost(
                    {
                        title: formData.title,
                        content: formData.content,
                        images:
                            formData.images || [],
                        postStatus:
                            formData.postStatus,
                        scheduledAt:
                            formData.scheduledAt,
                    }
                );
            }


            // Close form
            setShowForm(false);

            // Clear editing post
            setEditingPost(null);

            // Reload posts
            await loadPosts();

        } catch (error) {

            console.error(
                "Failed to save post:",
                error
            );

            const detail =
                error.response?.data?.detail;

            if (Array.isArray(detail)) {

                setError(
                    detail
                        .map((item) =>
                            item.msg
                        )
                        .join(", ")
                );

            } else {

                setError(
                    detail ||
                    "Failed to save post."
                );
            }

        } finally {

            setSaving(false);
        }
    };


    // ============================================
    // EDIT POST
    // ============================================

    const handleEdit = (post) => {

        setEditingPost(post);

        setShowForm(true);

        setError("");
    };


    // ============================================
    // DELETE POST
    // ============================================

    const handleDelete = async (postId) => {

        const confirmed =
            window.confirm(
                "Are you sure you want to delete this post?"
            );

        if (!confirmed) {
            return;
        }


        try {

            setError("");

            await deletePost(
                postId
            );

            await loadPosts();

        } catch (error) {

            console.error(
                "Failed to delete post:",
                error
            );

            const detail =
                error.response?.data?.detail;

            if (Array.isArray(detail)) {

                setError(
                    detail
                        .map((item) =>
                            item.msg
                        )
                        .join(", ")
                );

            } else {

                setError(
                    detail ||
                    "Failed to delete post."
                );
            }
        }
    };


    // ============================================
    // CREATE NEW POST
    // ============================================

    const handleCreate = () => {

        setEditingPost(null);

        setShowForm(true);

        setError("");
    };


    // ============================================
    // CANCEL FORM
    // ============================================

    const handleCancel = () => {

        setShowForm(false);

        setEditingPost(null);

        setError("");
    };


    // ============================================
    // SEARCH
    // ============================================

    const handleSearch = (event) => {

        setSearch(
            event.target.value
        );

        // Go back to first page
        setPage(1);
    };


    // ============================================
    // PREVIOUS PAGE
    // ============================================

    const handlePreviousPage = () => {

        if (page > 1) {

            setPage(
                page - 1
            );
        }
    };


    // ============================================
    // NEXT PAGE
    // ============================================

    const handleNextPage = () => {

        if (
            page < totalPages
        ) {

            setPage(
                page + 1
            );
        }
    };


    return (

        <div className="posts-page">

            {/* ================================= */}
            {/* HEADER */}
            {/* ================================= */}

            <div className="posts-header">

                <div>

                    <h1>
                        My Posts
                    </h1>

                    <p>
                        Create and manage your blog posts
                    </p>

                </div>


                <button
                    type="button"
                    onClick={handleCreate}
                    className="create-post-button"
                >
                    + Create Post
                </button>

            </div>


            {/* ================================= */}
            {/* SEARCH */}
            {/* ================================= */}

            <div className="posts-search">

                <input
                    type="text"
                    value={search}
                    onChange={handleSearch}
                    placeholder="Search your posts..."
                />

            </div>


            {/* ================================= */}
            {/* ERROR */}
            {/* ================================= */}

            {error && (

                <div className="posts-error">

                    {error}

                </div>

            )}


            {/* ================================= */}
            {/* POST FORM */}
            {/* ================================= */}

            {showForm && (

                <PostForm
                    post={editingPost}
                    onSubmit={handleSubmit}
                    onCancel={handleCancel}
                    saving={saving}
                />

            )}


            {/* ================================= */}
            {/* LOADING */}
            {/* ================================= */}

            {loading ? (

                <div className="posts-loading">

                    Loading posts...

                </div>

            ) : posts.length === 0 ? (

                /* ================================= */
                /* NO POSTS */
                /* ================================= */

                <div className="no-posts">

                    <h3>
                        No posts found
                    </h3>

                    <p>
                        Create your first blog post.
                    </p>

                </div>

            ) : (

                /* ================================= */
                /* POSTS LIST */
                /* ================================= */

                <div className="posts-list">

                    {posts.map((post) => (

                        <PostCard
                            key={post.id}
                            post={post}
                            onEdit={handleEdit}
                            onDelete={handleDelete}
                        />

                    ))}

                </div>

            )}


            {/* ================================= */}
            {/* PAGINATION */}
            {/* ================================= */}

            {!loading &&
                posts.length > 0 &&
                totalPages > 0 && (

                    <div className="pagination">

                        <button
                            type="button"
                            onClick={
                                handlePreviousPage
                            }
                            disabled={
                                page === 1
                            }
                        >
                            Previous
                        </button>


                        <span>

                            Page {page} of {totalPages}

                        </span>


                        <button
                            type="button"
                            onClick={
                                handleNextPage
                            }
                            disabled={
                                page === totalPages
                            }
                        >
                            Next
                        </button>

                    </div>

                )}

        </div>
    );
}


export default Posts;