function formatDate(dateString) {
    if (!dateString) return '—';

    try {
        let date;

        if (dateString instanceof Date) {
            date = dateString;
        } else {
            date = new Date(dateString);
        }

        if (isNaN(date.getTime())) {
            return '—';
        }

        return date.toLocaleDateString('ru-RU', {
            day: '2-digit',
            month: 'short',
            year: 'numeric',
        });
    } catch (error) {
        console.error('Error formatting date:', dateString, error);
        return '—';
    }
}

export default formatDate;