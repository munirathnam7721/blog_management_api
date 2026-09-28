import { useEffect, useState } from "react";
import { MessageCircle, Loader2 } from "lucide-react";

import { getMyPosts } from "../api/postsApi";
import { getComments } from "../api/commentsApi";

import "../components/Comments.css";

const Comments = () => {
    const [posts, setPosts] = useState([]);
    const [comments, setComments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        loadComments();
    }, []);

    const loadComments = async () => {
        try {
            setLoading(true);
            setError("");

            const myPosts = await getMyPosts();

            setPosts(myPosts);

            const allComments = [];

            for (const post of myPosts) {
                try {
                    const postComments =
                        await getComments(post.id);

                    postComments.forEach((comment) => {
                        allComments.push({
                            ...comment,
                            post_title: post.title,
                        });
                    });
                } catch (commentError) {
                    console.error(
                        `Failed to load comments for post ${post.id}`,
                        commentError
                    );
                }
            }

            setComments(allComments);
        } catch (error) {
            console.error(
                "Failed to load comments:",
                error
            );

            setError(
                error.response?.data?.detail ||
                "Failed to load comments"
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="comments-page">
            <div className="comments-page-header">
                <div>
                    <h1>Comments</h1>
                    <p>
                        Comments received on your posts
                    </p>
                </div>

                <div className="comments-page-count">
                    <MessageCircle size={20} />
                    <span>
                        {comments.length} Comments
                    </span>
                </div>
            </div>

            {loading && (
                <div className="comments-loading">
                    <Loader2
                        size={22}
                        className="comments-spinner"
                    />
                    Loading comments...
                </div>
            )}

            {!loading && error && (
                <div className="comments-error">
                    {error}
                </div>
            )}

            {!loading &&
                !error &&
                comments.length === 0 && (
                    <div className="no-comments">
                        <MessageCircle size={40} />

                        <h3>No comments yet</h3>

                        <p>
                            Comments from your posts
                            will appear here.
                        </p>
                    </div>
                )}

            {!loading &&
                !error &&
                comments.length > 0 && (
                    <div className="all-comments-list">
                        {comments.map((comment) => (
                            <div
                                className="all-comment-card"
                                key={comment.id}
                            >
                                <div className="comment-avatar">
                                    {(comment.username ||
                                        comment.user?.username ||
                                        "U")
                                        .charAt(0)
                                        .toUpperCase()}
                                </div>

                                <div className="all-comment-content">
                                    <div className="all-comment-top">
                                        <strong>
                                            {comment.username ||
                                                comment.user
                                                    ?.username ||
                                                "User"}
                                        </strong>

                                        <span>
                                            {comment.created_at
                                                ? new Date(
                                                      comment.created_at
                                                  ).toLocaleString()
                                                : ""}
                                        </span>
                                    </div>

                                    <p>
                                        {comment.text ||
                                            comment.content ||
                                            ""}
                                    </p>

                                    <div className="comment-post-name">
                                        On:{" "}
                                        <strong>
                                            {
                                                comment.post_title
                                            }
                                        </strong>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
        </div>
    );
};

export default Comments;