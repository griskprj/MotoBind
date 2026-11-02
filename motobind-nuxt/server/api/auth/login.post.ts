import { setAuthCookies } from '../../utils/auth'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const config = useRuntimeConfig(event)

  const result = await $fetch<{
    message: string
    access_token: string
    refresh_token: string | null
    user: Record<string, unknown>
  }>(
    `${config.flaskApiBase}${config.flaskAuthPrefix}/login`,
    {
      method: 'POST',
      body: {
        email: body.email,
        password: body.password,
        rememberMe: Boolean(body.rememberMe)
      }
    }
  )

  setAuthCookies(event, result.access_token, result.refresh_token)

  return {
    message: result.message,
    user: result.user
  }
})
