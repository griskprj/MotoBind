import { RateLimiterMemory } from 'rate-limiter-flexible'

const limiter = new RateLimiterMemory({
    points: 10,
    duration: 60,
})

export default defineEventHandler(async (event) => {
    const url = getRequestURL(event)
    const protecredPaths = ['/api/auth/login', '/api/auth/register', '/api/auth/forgot-password']

    if (!protecredPaths.includes(url.pathname)) return

    const ip = getRequestHeader(event, 'x-forwarded-for') || event.node.req.socket.remoteAddress || 'unknow'

    try {
        await limiter.consume(ip)
    } catch {
        throw createError({
            statusCode: 429,
            statusMessage: 'Слишком много попыток. Пожалуйста, подождите минуту.',
        })
    }
})