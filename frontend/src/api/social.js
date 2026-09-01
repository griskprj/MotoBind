import api from './api'

export default {
    // Посты
    createPost(formData) {
        return api.post('/social/posts', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })
    },
    getPosts(page = 1, perPage = 20, userId = null, includeComments = false) {
        return api.get('/social/posts', {
            params: { page, per_page: perPage, user_id: userId, include_comments: includeComments }
        })
    },
    getPost(postId, includeComments = true) {
        return api.get(`/social/posts/${postId}`, {
            params: { include_comments: includeComments }
        })
    },
    updatePost(postId, formData) {
        return api.put(`/social/posts/${postId}`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })
    },
    deletePost(postId) {
        return api.delete(`/social/posts/${postId}`)
    },
    
    // Лайки
    toggleLike(postId) {
        return api.post(`/social/posts/${postId}/like`)
    },
    
    // Комментарии
    addComment(postId, content) {
        return api.post(`/social/posts/${postId}/comments`, { content })
    },
    deleteComment(commentId) {
        return api.delete(`/social/comments/${commentId}`)
    }
}