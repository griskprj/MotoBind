import api from './api'

export default {
    /**
     * Список напоминаний текущего пользователя.
     * @param {string} status - 'pending' | 'dismissed' | undefined
     */
    getReminders(status) {
        const params = {}
        if (status) params.status = status
        return api.get('/reminders/', { params })
    },

    /**
     * Счётчик активных напоминаний для бейджа.
     */
    getCount() {
        return api.get('/reminders/count')
    },

    /**
     * Скрыть напоминание навсегда.
     */
    dismiss(reminderId) {
        return api.put(`/reminders/${reminderId}/dismiss`)
    },

    /**
     * Отложить напоминание на N дней.
     * @param {number} days - 1..30, по умолчанию 7
     */
    snooze(reminderId, days = 7) {
        return api.put(`/reminders/${reminderId}/snooze`, { days })
    },
}
