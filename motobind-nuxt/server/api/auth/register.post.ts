import { setAuthCookies } from '../../utils/auth'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const config = useRuntimeConfig(event)

  if (!body?.email || !body?.username || !body?.password) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Email, имя пользователя и пароль обязательны',
    })
  }

  const result = await $fetch<{
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

  setAuthCookies(event, result.access_token, result.refresh_token)

  return {
    message: result.message,
    user: result.user,
  }
})
