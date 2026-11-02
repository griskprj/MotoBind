import { backendRequest } from '../../utils/backend'

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)
  const routePath = getRouterParam(event, 'path')

  if (!routePath || routePath.includes('..')) {
    throw createError({ statusCode: 400, statusMessage: 'Invalid API path' })
  }

  const apiPrefix = String(config.flaskApiPrefix || '/api').replace(/^\/+|\/+$/g, '')
  const path = `/${apiPrefix}/${routePath}`
  const method = getMethod(event)

  let body: unknown
  if (!['GET', 'HEAD'].includes(method)) {
    const contentType = getHeader(event, 'content-type') || ''
    if (contentType.includes('multipart/form-data')) {
      body = await readRawBody(event, false)
    } else {
      body = await readBody(event)
    }
  }

  return backendRequest(event, path, {
    method,
    query: getQuery(event),
    body,
    headers: {
      ...(getHeader(event, 'content-type')
        ? { 'Content-Type': getHeader(event, 'content-type')! }
        : {})
    }
  })
})
