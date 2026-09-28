import {
    useEffect,
    useState,
} from "react";

import {
    X,
    Upload,
    FileText,
    Send,
    CalendarClock,
} from "lucide-react";
import "./PostForm.css";
const PostForm = ({
    onSubmit,
    onCancel,
    editingPost = null,
    saving = false,
}) => {

    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");

    const [images, setImages] = useState([]);

    const [postStatus, setPostStatus] =
        useState("draft");

    const [scheduledAt, setScheduledAt] =
        useState("");

    const [error, setError] =
        useState("");

    // ========================================================
    // LOAD EDITING POST
    // ========================================================

    useEffect(() => {

        if (editingPost) {

            setTitle(
                editingPost.title || ""
            );

            setContent(
                editingPost.content || ""
            );

            setPostStatus(
                editingPost.status || "draft"
            );

            if (
                editingPost.status === "scheduled" &&
                editingPost.scheduled_at
            ) {

                const date = new Date(
                    editingPost.scheduled_at
                );

                const localDateTime =
                    new Date(
                        date.getTime()
                        - date.getTimezoneOffset() * 60000
                    )
                        .toISOString()
                        .slice(0, 16);

                setScheduledAt(
                    localDateTime
                );

            } else {

                setScheduledAt("");

            }

        } else {

            setTitle("");
            setContent("");
            setImages([]);
            setPostStatus("draft");
            setScheduledAt("");
            setError("");

        }

    }, [editingPost]);


    // ========================================================
    // IMAGE CHANGE
    // ========================================================

    const handleImageChange = (
        event
    ) => {

        const selectedFiles =
            Array.from(
                event.target.files || []
            );

        setImages(
            selectedFiles
        );
    };


    // ========================================================
    // SUBMIT
    // ========================================================

    const handleSubmit = async (
        event
    ) => {

        event.preventDefault();

        setError("");

        // ====================================================
        // BASIC VALIDATION
        // ====================================================

        if (!title.trim()) {

            setError(
                "Please enter a title."
            );

            return;
        }

        if (!content.trim()) {

            setError(
                "Please enter post content."
            );

            return;
        }


        // ====================================================
        // SCHEDULE VALIDATION
        // ====================================================

        if (
            postStatus === "scheduled"
        ) {

            if (!scheduledAt) {

                setError(
                    "Please select a future date and time."
                );

                return;
            }

            const selectedDate =
                new Date(
                    scheduledAt
                );

            const currentDate =
                new Date();

            if (
                selectedDate <= currentDate
            ) {

                setError(
                    "Scheduled date and time must be in the future."
                );

                return;
            }
        }


        // ====================================================
        // CONVERT LOCAL TIME TO UTC
        // ====================================================

        let utcScheduledAt = null;

        if (
            postStatus === "scheduled" &&
            scheduledAt
        ) {

            utcScheduledAt =
                new Date(
                    scheduledAt
                ).toISOString();
        }


        // ====================================================
        // SEND DATA
        // ====================================================

        try {

            await onSubmit({

                title: title.trim(),

                content: content.trim(),

                images,

                postStatus,

                scheduledAt:
                    utcScheduledAt,

            });

        } catch (submitError) {

            console.error(
                "Post submit error:",
                submitError
            );

            setError(
                "Failed to save post."
            );
        }
    };


    return (
        <div className="post-form-overlay">

            <div className="post-form-container">

                {/* ==================================================
                    HEADER
                ================================================== */}

                <div className="post-form-header">

                    <div>

                        <h2>
                            {editingPost
                                ? "Edit Post"
                                : "Create Post"}
                        </h2>

                        <p>
                            {editingPost
                                ? "Update your blog post"
                                : "Create and publish your blog post"}
                        </p>

                    </div>


                    <button
                        type="button"
                        className="close-form-button"
                        onClick={onCancel}
                    >
                        <X size={22} />
                    </button>

                </div>


                {/* ==================================================
                    FORM
                ================================================== */}

                <form
                    onSubmit={handleSubmit}
                    className="post-form"
                >

                    {/* ==================================================
                        ERROR
                    ================================================== */}

                    {error && (

                        <div className="post-form-error">

                            {error}

                        </div>

                    )}


                    {/* ==================================================
                        TITLE
                    ================================================== */}

                    <div className="form-group">

                        <label htmlFor="post-title">
                            Title
                        </label>

                        <input
                            id="post-title"
                            type="text"
                            value={title}
                            onChange={(event) =>
                                setTitle(
                                    event.target.value
                                )
                            }
                            placeholder="Enter post title"
                            maxLength={200}
                            required
                        />

                    </div>


                    {/* ==================================================
                        CONTENT
                    ================================================== */}

                    <div className="form-group">

                        <label htmlFor="post-content">
                            Content
                        </label>

                        <textarea
                            id="post-content"
                            value={content}
                            onChange={(event) =>
                                setContent(
                                    event.target.value
                                )
                            }
                            placeholder="Write your post content..."
                            rows={8}
                            required
                        />

                    </div>


                    {/* ==================================================
                        IMAGE
                    ================================================== */}

                    <div className="form-group">

                        <label
                            htmlFor="post-images"
                            className="upload-label"
                        >

                            <Upload size={18} />

                            Upload Images

                        </label>

                        <input
                            id="post-images"
                            type="file"
                            accept="image/jpeg,image/png,image/webp"
                            multiple
                            onChange={
                                handleImageChange
                            }
                        />

                        {images.length > 0 && (

                            <p className="selected-files">

                                {images.length} image
                                {images.length > 1
                                    ? "s"
                                    : ""} selected

                            </p>

                        )}

                    </div>


                    {/* ==================================================
                        POST STATUS
                    ================================================== */}

                    <div className="post-status-section">

                        <label className="status-section-title">

                            Publishing Options

                        </label>


                        {/* ==================================================
                            DRAFT
                        ================================================== */}

                        <label
                            className={`status-option ${
                                postStatus === "draft"
                                    ? "active"
                                    : ""
                            }`}
                        >

                            <div className="status-icon">

                                <FileText
                                    size={20}
                                />

                            </div>

                            <div className="status-content">

                                <strong>
                                    Save as Draft
                                </strong>

                                <span>
                                    Save the post without publishing it.
                                </span>

                            </div>

                            <input
                                type="radio"
                                name="postStatus"
                                value="draft"
                                checked={
                                    postStatus ===
                                    "draft"
                                }
                                onChange={() => {

                                    setPostStatus(
                                        "draft"
                                    );

                                    setScheduledAt(
                                        ""
                                    );

                                }}
                            />

                        </label>


                        {/* ==================================================
                            PUBLISH NOW
                        ================================================== */}

                        <label
                            className={`status-option ${
                                postStatus === "published"
                                    ? "active"
                                    : ""
                            }`}
                        >

                            <div className="status-icon">

                                <Send
                                    size={20}
                                />

                            </div>

                            <div className="status-content">

                                <strong>
                                    Publish Now
                                </strong>

                                <span>
                                    Publish this post immediately.
                                </span>

                            </div>

                            <input
                                type="radio"
                                name="postStatus"
                                value="published"
                                checked={
                                    postStatus ===
                                    "published"
                                }
                                onChange={() => {

                                    setPostStatus(
                                        "published"
                                    );

                                    setScheduledAt(
                                        ""
                                    );

                                }}
                            />

                        </label>


                        {/* ==================================================
                            SCHEDULE
                        ================================================== */}

                        <label
                            className={`status-option ${
                                postStatus === "scheduled"
                                    ? "active"
                                    : ""
                            }`}
                        >

                            <div className="status-icon">

                                <CalendarClock
                                    size={20}
                                />

                            </div>

                            <div className="status-content">

                                <strong>
                                    Schedule Post
                                </strong>

                                <span>
                                    Publish the post at a future date and time.
                                </span>

                            </div>

                            <input
                                type="radio"
                                name="postStatus"
                                value="scheduled"
                                checked={
                                    postStatus ===
                                    "scheduled"
                                }
                                onChange={() => {

                                    setPostStatus(
                                        "scheduled"
                                    );

                                }}
                            />

                        </label>


                        {/* ==================================================
                            SCHEDULE DATE
                        ================================================== */}

                        {postStatus ===
                            "scheduled" && (

                            <div className="schedule-section">

                                <label
                                    htmlFor="scheduled-at"
                                >
                                    Schedule Date & Time
                                </label>

                                <input
                                    id="scheduled-at"
                                    type="datetime-local"
                                    value={
                                        scheduledAt
                                    }
                                    onChange={(event) =>
                                        setScheduledAt(
                                            event.target.value
                                        )
                                    }
                                    required
                                />

                                <small>
                                    Select a future date and time.
                                </small>

                            </div>

                        )}

                    </div>


                    {/* ==================================================
                        FORM ACTIONS
                    ================================================== */}

                    <div className="post-form-actions">

                        <button
                            type="button"
                            className="cancel-button"
                            onClick={onCancel}
                            disabled={saving}
                        >
                            Cancel
                        </button>


                        <button
                            type="submit"
                            className="submit-post-button"
                            disabled={saving}
                        >

                            {saving
                                ? "Saving..."
                                : postStatus ===
                                  "draft"
                                    ? "Save Draft"
                                    : postStatus ===
                                      "published"
                                        ? "Publish Now"
                                        : "Schedule Post"}

                        </button>

                    </div>

                </form>

            </div>

        </div>
    );
};

export default PostForm;