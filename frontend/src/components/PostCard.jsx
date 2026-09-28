import {
    useEffect,
    useState,
} from "react";

import {
    Edit,
    Trash2,
    MessageCircle,
    Heart,
    Calendar,
} from "lucide-react";

import Comments from "./Comments";

import {
    likePost,
    unlikePost,
    getLikeCount,
} from "../api/likesApi";

const API_URL =
    import.meta.env.VITE_API_URL ||
    "http://127.0.0.1:8000";


const PostCard = ({
    post,
    onEdit,
    onDelete,
}) => {

    const [showComments, setShowComments] =
        useState(false);

    const [likeCount, setLikeCount] =
        useState(0);

    const [isLiked, setIsLiked] =
        useState(false);

    const [likeLoading, setLikeLoading] =
        useState(false);

    const [likeError, setLikeError] =
        useState("");


    // ==========================================
    // LOAD LIKE COUNT
    // ==========================================

    useEffect(() => {
        loadLikeCount();
    }, [post.id]);


    const loadLikeCount = async () => {

        try {

            const data =
                await getLikeCount(post.id);

            setLikeCount(
                data.like_count
            );

        } catch (error) {

            console.error(
                "Failed to load like count:",
                error
            );
        }
    };


    // ==========================================
    // IMAGE URL
    // ==========================================

    const getImageUrl = (image) => {

        if (!image) {
            return "";
        }

        if (image.startsWith("http")) {
            return image;
        }

        return `${API_URL}${image}`;
    };


    // ==========================================
    // POST IMAGES
    // ==========================================

    const postImages = [];

    if (post.image) {

        postImages.push(
            post.image
        );
    }

    if (Array.isArray(post.images)) {

        post.images.forEach(
            (imageObject) => {

                if (imageObject?.image) {

                    postImages.push(
                        imageObject.image
                    );
                }
            }
        );
    }


    // ==========================================
    // LIKE / UNLIKE
    // ==========================================

    const handleLike = async () => {

        if (likeLoading) {
            return;
        }

        try {

            setLikeLoading(true);

            setLikeError("");

            if (isLiked) {

                await unlikePost(
                    post.id
                );

                setIsLiked(false);

                setLikeCount(
                    (previousCount) =>
                        Math.max(
                            0,
                            previousCount - 1
                        )
                );

            } else {

                await likePost(
                    post.id
                );

                setIsLiked(true);

                setLikeCount(
                    (previousCount) =>
                        previousCount + 1
                );
            }

        } catch (error) {

            console.error(
                "Like error:",
                error
            );

            const detail =
                error.response?.data?.detail;

            setLikeError(
                typeof detail === "string"
                    ? detail
                    : "Failed to update like"
            );

        } finally {

            setLikeLoading(false);
        }
    };


    // ==========================================
    // COMMENTS
    // ==========================================

    const handleCommentsToggle = () => {

        setShowComments(
            (previous) => !previous
        );
    };


    // ==========================================
    // STATUS
    // ==========================================

    const status =
        post.status || "draft";


    // ==========================================
    // DATE
    // ==========================================

    const formattedDate =
        post.created_at
            ? new Date(
                post.created_at
            ).toLocaleDateString(
                "en-IN",
                {
                    day: "2-digit",
                    month: "short",
                    year: "numeric",
                }
            )
            : "";


    return (

        <article className="post-card">

            {/* ======================================
                IMAGE
            ====================================== */}

            {postImages.length > 0 && (

                <div
                    className={
                        postImages.length > 1
                            ? "post-images multiple-images"
                            : "post-images"
                    }
                >

                    {postImages.map(
                        (
                            image,
                            index
                        ) => (

                            <img
                                key={`${post.id}-${index}`}
                                src={getImageUrl(
                                    image
                                )}
                                alt={
                                    post.title
                                }
                                className="post-image"
                            />

                        )
                    )}

                </div>

            )}


            {/* ======================================
                CARD BODY
            ====================================== */}

            <div className="post-card-body">

                {/* ==================================
                    TITLE + STATUS
                ================================== */}

                <div className="post-title-row">

                    <h2>
                        {post.title}
                    </h2>

                    <span
                        className={`post-status ${status}`}
                    >
                        {status}
                    </span>

                </div>


                {/* ==================================
                    CONTENT
                ================================== */}

                <p className="post-content">
                    {post.content}
                </p>


                {/* ==================================
                    META
                ================================== */}

                <div className="post-meta">

                    {/* DATE */}

                    <span className="post-meta-item">

                        <Calendar
                            size={15}
                        />

                        {formattedDate}

                    </span>


                    {/* LIKE */}

                    <button
                        type="button"
                        className={`like-button ${
                            isLiked
                                ? "liked"
                                : ""
                        }`}
                        onClick={
                            handleLike
                        }
                        disabled={
                            likeLoading
                        }
                    >

                        <Heart
                            size={15}
                            fill={
                                isLiked
                                    ? "currentColor"
                                    : "none"
                            }
                        />

                        <span>
                            {likeCount}
                        </span>

                        <span>
                            Likes
                        </span>

                    </button>


                    {/* COMMENTS */}

                    <button
                        type="button"
                        className={`comments-toggle ${
                            showComments
                                ? "active"
                                : ""
                        }`}
                        onClick={
                            handleCommentsToggle
                        }
                    >

                        <MessageCircle
                            size={15}
                        />

                        <span>
                            Comments
                        </span>

                    </button>

                </div>


                {/* ==================================
                    LIKE ERROR
                ================================== */}

                {likeError && (

                    <p className="like-error">
                        {likeError}
                    </p>

                )}


                {/* ==================================
                    ACTIONS
                ================================== */}

                <div className="post-actions">

                    <button
                        type="button"
                        className="edit-post-button"
                        onClick={() =>
                            onEdit(post)
                        }
                    >

                        <Edit
                            size={15}
                        />

                        <span>
                            Edit
                        </span>

                    </button>


                    <button
                        type="button"
                        className="delete-post-button"
                        onClick={() =>
                            onDelete(
                                post.id
                            )
                        }
                    >

                        <Trash2
                            size={15}
                        />

                        <span>
                            Delete
                        </span>

                    </button>

                </div>


                {/* ==================================
                    COMMENTS
                ================================== */}

                {showComments && (

                    <div className="comments-section">

                        <Comments
                            postId={
                                post.id
                            }
                        />

                    </div>

                )}

            </div>

        </article>
    );
};


export default PostCard;