import api from './api';

export default {
    getNotifications(page = 1, perPage = 20, unreadOnly = false) {
        return api.get('/notifications/', {
            params: { page, per_page: perPage, unreadOnly: unreadOnly }
        })
    },
    getUnreadCount() {
        return api.get('/notifications/unread-count')
    },
    markAsRead(id) {
        return api.put(`/notifications/${id}/read`)
    },
    markAllRead() {
        return api.put('/notifications/read-all')
    },
    deleteNotification(id) {
        return api.delete(`/notifications/${id}`)
    }
}