import api from "./axios";


// ==========================================
// GET COMMENTS FOR A POST
// ==========================================

export const getComments = async (postId) => {

    const response = await api.get(
        `/posts/${postId}/comments`
    );

    return response.data;
};


// ==========================================
// CREATE COMMENT
// ==========================================

export const createComment = async (
    postId,
    text
) => {

    const response = await api.post(
        `/posts/${postId}/comments`,
        {
            text,
        }
    );

    return response.data;
};