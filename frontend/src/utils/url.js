export function normalizeWebsite(url) {
    if (!url) return ''
    const trimmed = String(url).trim()
    if (!trimmed) return ''
    if (/^https?:\/\//i.test(trimmed)) return trimmed
    return `https://${trimmed}`
}
