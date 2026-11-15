// Проверка Origin/Referer на всех не-GET запросах.
// Защищает от CSRF

const ALLOWED_ORIGINS = [
    'https://motobind.ru',
    'https://www.motobind.ru',
    'http://localhost:3000'
]

export default defineEventHandler((event) => {
    const method = getMethod(event)

    if (['GET', 'HEAD', 'OPTIONS'].includes(method)) return

    const origin = getHeader(event, 'origin')
    const referer = getHeader(event, 'referer')

    const source = origin || referer

    if (!source) {
        throw createError({
            statusCode: 403,
            statusMessage: 'CSRF: missing Origin/Referer',
        })
    }

    const isAllowed = ALLOWED_ORIGINS.some((allowed) => 
        source === allowed || source.startsWith(allowed + '/')
    )

    if (!isAllowed) {
        throw createError({
            statusCode: 403,
            statusMessage: 'CSRF: origin not allowed'
        })
    }
})