import {
    useEffect,
    useState,
} from "react";

import {
    MessageCircle,
    Send,
    Loader2,
} from "lucide-react";

import {
    getComments,
    createComment,
} from "../api/commentsApi";

import "./Comments.css";


const Comments = ({
    postId,
}) => {

    const [comments, setComments] = useState([]);

    const [text, setText] = useState("");

    const [loading, setLoading] = useState(true);

    const [sending, setSending] = useState(false);

    const [error, setError] = useState("");


    // ==========================================
    // LOAD COMMENTS
    // ==========================================

    const loadComments = async () => {

        try {

            setLoading(true);

            setError("");

            const data =
                await getComments(postId);

            setComments(
                Array.isArray(data)
                    ? data
                    : []
            );

        } catch (error) {

            console.error(
                "Load comments error:",
                error
            );

            const detail =
                error.response?.data?.detail;

            if (
                typeof detail === "string"
            ) {

                setError(detail);

            } else {

                setError(
                    "Failed to load comments."
                );
            }

        } finally {

            setLoading(false);
        }
    };


    // ==========================================
    // LOAD WHEN POST ID CHANGES
    // ==========================================

    useEffect(() => {

        if (postId) {

            loadComments();
        }

    }, [postId]);


    // ==========================================
    // ADD COMMENT
    // ==========================================

    const handleSubmit = async (
        event
    ) => {

        event.preventDefault();

        const trimmedText =
            text.trim();

        if (!trimmedText) {

            return;
        }


        try {

            setSending(true);

            setError("");

            const newComment =
                await createComment(
                    postId,
                    trimmedText
                );


            setComments(
                (previousComments) => [
                    ...previousComments,
                    newComment,
                ]
            );


            setText("");

        } catch (error) {

            console.error(
                "Create comment error:",
                error
            );

            const detail =
                error.response?.data?.detail;

            if (
                typeof detail === "string"
            ) {

                setError(detail);

            } else {

                setError(
                    "Failed to add comment."
                );
            }

        } finally {

            setSending(false);
        }
    };


    return (
        <section className="comments-section">

            {/* ================================= */}
            {/* HEADER */}
            {/* ================================= */}

            <div className="comments-header">

                <div className="comments-title">

                    <MessageCircle
                        size={20}
                    />

                    <h3>
                        Comments
                    </h3>

                    <span>
                        {comments.length}
                    </span>

                </div>

            </div>


            {/* ================================= */}
            {/* ERROR */}
            {/* ================================= */}

            {error && (

                <div className="comments-error">

                    {error}

                </div>

            )}


            {/* ================================= */}
            {/* LOADING */}
            {/* ================================= */}

            {loading ? (

                <div className="comments-loading">

                    <Loader2
                        size={18}
                        className="comments-spinner"
                    />

                    Loading comments...

                </div>

            ) : comments.length === 0 ? (

                <div className="no-comments">

                    <MessageCircle
                        size={30}
                    />

                    <p>
                        No comments yet.
                    </p>

                    <span>
                        Be the first to comment.
                    </span>

                </div>

            ) : (

                <div className="comments-list">

                    {comments.map(
                        (comment) => (

                            <div
                                className="comment-item"
                                key={comment.id}
                            >

                                <div className="comment-avatar">

                                    {(
                                        comment.username ||
                                        comment.user?.username ||
                                        "U"
                                    )
                                        .charAt(0)
                                        .toUpperCase()}

                                </div>


                                <div className="comment-body">

                                    <div className="comment-meta">

                                        <strong>

                                            {
                                                comment.username ||
                                                comment.user?.username ||
                                                "User"
                                            }

                                        </strong>


                                        {comment.created_at && (

                                            <span>

                                                {new Date(
                                                    comment.created_at
                                                ).toLocaleString()}

                                            </span>

                                        )}

                                    </div>


                                    <p>

                                        {
                                            comment.text ||
                                            comment.content ||
                                            ""
                                        }

                                    </p>

                                </div>

                            </div>

                        )
                    )}

                </div>

            )}


            {/* ================================= */}
            {/* ADD COMMENT */}
            {/* ================================= */}

            <form
                className="comment-form"
                onSubmit={handleSubmit}
            >

                <input
                    type="text"
                    value={text}
                    onChange={(event) =>
                        setText(
                            event.target.value
                        )
                    }
                    placeholder="Write a comment..."
                    maxLength={1000}
                    disabled={sending}
                />


                <button
                    type="submit"
                    disabled={
                        sending ||
                        !text.trim()
                    }
                >

                    {sending ? (

                        <Loader2
                            size={17}
                            className="comments-spinner"
                        />

                    ) : (

                        <Send
                            size={17}
                        />

                    )}

                    <span>
                        {sending
                            ? "Sending..."
                            : "Send"
                        }
                    </span>

                </button>

            </form>

        </section>
    );
};


export default Comments;