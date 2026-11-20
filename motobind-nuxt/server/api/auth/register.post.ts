
import { setAuthCookies } from '../../utils/auth'
import { forwardApiError } from '../../utils/forwardApiError'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const config = useRuntimeConfig(event)

  if (!body?.email || !body?.username || !body?.password) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Bad Request',
      message: 'Email, имя пользователя и пароль обязательны',
    })
  }

  let result

  try {
    result = await $fetch<{
      message: string
      access_token: string
      refresh_token: string | null
      user: Record<string, unknown>
    }>(
      `${config.flaskApiBase}${config.flaskAuthPrefix}/register`,
      {
        method: 'POST',
        body: {
          email: body.email,
          username: body.username,
          password: body.password,
          role: body.role || 'motorcyclist',
        },
      }
    )
  } catch (error) {
    forwardApiError(error)
  }

  setAuthCookies(event, result.access_token, result.refresh_token)

  return {
    message: result.message,
    user: result.user,
  }
})
