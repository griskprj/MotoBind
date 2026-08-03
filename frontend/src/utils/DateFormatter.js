function formatDate(dateString) {
    if (!dateString) return '—';
    
    try {
        if (dateString instanceof Date) {
            return dateString.toLocaleDateString('ru-RU', {
                day: '2-digit',
                month: 'short',
                year: 'numeric'
            });
        }
        
        const date = new Date(dateString);
        
        if (isNaN(date.getTime())) {
            return '—';
        }
        
        return date.toLocaleDateString('ru-RU', {
            day: '2-digit',
            month: 'short',
            year: 'numeric'
        });
    } catch (error) {
        console.error('Error formatting date:', dateString, error);
        return '—';
    }
};

export default formatDate;