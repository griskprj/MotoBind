function drawSplash(width, height) {
    const canvas = document.getElementById('splashCanvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');
    
    const grad = ctx.createLinearGradient(0, 0, width, height);
    grad.addColorStop(0, '#0A0A0F');
    grad.addColorStop(0.5, '#111118');
    grad.addColorStop(1, '#1A1A24');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, width, height);
    
    const iconSize = Math.min(width, height) * 0.18;
    const iconX = (width - iconSize) / 2;
    const iconY = height * 0.32;
    const radius = iconSize * 0.25;
    
    ctx.shadowColor = 'rgba(139, 92, 246, 0.4)';
    ctx.shadowBlur = 40;
    
    ctx.beginPath();
    ctx.moveTo(iconX + radius, iconY);
    ctx.lineTo(iconX + iconSize - radius, iconY);
    ctx.quadraticCurveTo(iconX + iconSize, iconY, iconX + iconSize, iconY + radius);
    ctx.lineTo(iconX + iconSize, iconY + iconSize - radius);
    ctx.quadraticCurveTo(iconX + iconSize, iconY + iconSize, iconX + iconSize - radius, iconY + iconSize);
    ctx.lineTo(iconX + radius, iconY + iconSize);
    ctx.quadraticCurveTo(iconX, iconY + iconSize, iconX, iconY + iconSize - radius);
    ctx.lineTo(iconX, iconY + radius);
    ctx.quadraticCurveTo(iconX, iconY, iconX + radius, iconY);
    ctx.closePath();
    
    const iconGrad = ctx.createLinearGradient(iconX, iconY, iconX + iconSize, iconY + iconSize);
    iconGrad.addColorStop(0, '#8B5CF6');
    iconGrad.addColorStop(1, '#7C3AED');
    ctx.fillStyle = iconGrad;
    ctx.fill();
    
    ctx.shadowBlur = 0;
    
    const img = new Image();
    img.onload = function() {
        const padding = iconSize * 0.12;
        ctx.drawImage(img, iconX + padding, iconY + padding, iconSize - padding * 2, iconSize - padding * 2);
    };
    img.src = '/icons/icon-192x192.png';
    
    const textSize = Math.min(width, height) * 0.065;
    ctx.fillStyle = '#F8FAFC';
    ctx.font = `700 ${textSize}px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('MotoBind', width/2, height * 0.60);
    
    const subSize = textSize * 0.5;
    ctx.fillStyle = '#64748B';
    ctx.font = `400 ${subSize}px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`;
    ctx.fillText('Сервис для мотоциклистов', width/2, height * 0.68);
    
    const dotSize = Math.min(width, height) * 0.006;
    const dotY = height * 0.85;
    const dotGap = dotSize * 3;
    const totalWidth = dotSize * 3 + dotGap * 2;
    const startX = (width - totalWidth) / 2;
    
    for (let i = 0; i < 3; i++) {
        ctx.beginPath();
        ctx.arc(startX + i * (dotSize + dotGap), dotY, dotSize, 0, Math.PI * 2);
        ctx.fillStyle = i === 1 ? '#8B5CF6' : '#2D2D3A';
        ctx.fill();
    }
    
    return canvas;
}