import api from './api'

export default {
    /**
     * Получить настройки уведомлений.
     * @returns {Promise} — { email_notifications_enabled, email_newsletter_enabled, email_verification_enabled, reminders_mileage_enabled, reminders_maintenance_enabled }
     */
    getNotificationSettings() {
        return api.get('/user/notification-settings')
    },

    /**
     * Обновить настройки уведомлений.
     * @param {object} settings - любые из 5 флагов
     */
    updateNotificationSettings(settings) {
        return api.put('/user/notification-settings', settings)
    },
}