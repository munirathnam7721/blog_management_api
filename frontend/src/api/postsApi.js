import api from "./axios";


// ==========================================
// GET ALL POSTS
// ==========================================
// Public endpoint
// Returns only published posts
// Supports pagination and search
// ==========================================

export const getAllPosts = async (
    page = 1,
    limit = 10,
    search = ""
) => {

    const response = await api.get(
        "/posts/",
        {
            params: {
                page,
                limit,
                search: search || undefined,
            },
        }
    );

    return response.data;
};


// ==========================================
// GET MY POSTS
// ==========================================
// Authenticated endpoint
//
// Returns the logged-in user's:
// - Draft posts
// - Scheduled posts
// - Published posts
//
// Supports:
// - Pagination
// - Search
// ==========================================

export const getMyPosts = async (
    page = 1,
    limit = 10,
    search = ""
) => {

    const response = await api.get(
        "/posts/mine/list",
        {
            params: {
                page,
                limit,
                search: search || undefined,
            },
        }
    );

    return response.data;
};


// ==========================================
// GET SINGLE POST
// ==========================================

export const getPost = async (
    postId
) => {

    const response = await api.get(
        `/posts/${postId}`
    );

    return response.data;
};


// ==========================================
// CREATE POST
// ==========================================
// Supports:
// - Draft
// - Publish Now
// - Schedule Post
// - Multiple images
// ==========================================

export const createPost = async ({
    title,
    content,
    images = [],
    postStatus = "draft",
    scheduledAt = null,
}) => {

    const formData = new FormData();


    // ==========================================
    // TITLE
    // ==========================================

    formData.append(
        "title",
        title
    );


    // ==========================================
    // CONTENT
    // ==========================================

    formData.append(
        "content",
        content
    );


    // ==========================================
    // POST STATUS
    // ==========================================
    //
    // Frontend:
    // postStatus
    //
    // Backend:
    // post_status
    //
    // ==========================================

    formData.append(
        "post_status",
        postStatus
    );


    // ==========================================
    // SCHEDULED DATE
    // ==========================================
    //
    // Only send scheduled_at when the
    // selected status is "scheduled".
    //
    // ==========================================

    if (
        postStatus === "scheduled"
        && scheduledAt
    ) {

        formData.append(
            "scheduled_at",
            scheduledAt
        );

    }


    // ==========================================
    // IMAGES
    // ==========================================

    images.forEach((image) => {

        formData.append(
            "images",
            image
        );

    });


    // ==========================================
    // API REQUEST
    // ==========================================

    const response = await api.post(
        "/posts/",
        formData
    );

    return response.data;
};


// ==========================================
// UPDATE POST
// ==========================================
// Supports:
// - Edit title
// - Edit content
// - Change status
// - Schedule post
// - Publish post
// - Save draft
// - Replace images
// ==========================================

export const updatePost = async (
    postId,
    {
        title,
        content,
        images = [],
        postStatus,
        scheduledAt = null,
    }
) => {

    const formData = new FormData();


    // ==========================================
    // TITLE
    // ==========================================

    if (
        title !== undefined
    ) {

        formData.append(
            "title",
            title
        );

    }


    // ==========================================
    // CONTENT
    // ==========================================

    if (
        content !== undefined
    ) {

        formData.append(
            "content",
            content
        );

    }


    // ==========================================
    // POST STATUS
    // ==========================================
    //
    // Frontend:
    // postStatus
    //
    // Backend:
    // post_status
    //
    // ==========================================

    if (
        postStatus !== undefined
    ) {

        formData.append(
            "post_status",
            postStatus
        );

    }


    // ==========================================
    // SCHEDULED DATE
    // ==========================================
    //
    // Only send scheduled_at when status
    // is "scheduled".
    //
    // ==========================================

    if (
        postStatus === "scheduled"
        && scheduledAt
    ) {

        formData.append(
            "scheduled_at",
            scheduledAt
        );

    }


    // ==========================================
    // IMAGES
    // ==========================================

    images.forEach((image) => {

        formData.append(
            "images",
            image
        );

    });


    // ==========================================
    // API REQUEST
    // ==========================================

    const response = await api.put(
        `/posts/${postId}`,
        formData
    );

    return response.data;
};


// ==========================================
// DELETE POST
// ==========================================

export const deletePost = async (
    postId
) => {

    const response = await api.delete(
        `/posts/${postId}`
    );

    return response.data;
};