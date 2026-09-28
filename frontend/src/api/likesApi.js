import api from "./axios";

// LIKE A POST
export const likePost = async (postId) => {
    const response = await api.post(
        `/posts/${postId}/like`
    );

    return response.data;
};

// UNLIKE A POST
export const unlikePost = async (postId) => {
    const response = await api.delete(
        `/posts/${postId}/like`
    );

    return response.data;
};

// GET LIKE COUNT
export const getLikeCount = async (postId) => {
    const response = await api.get(
        `/posts/${postId}/likes`
    );

    return response.data;
};