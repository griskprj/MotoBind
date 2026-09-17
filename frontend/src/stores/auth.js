import { computed, ref } from "vue";
import { defineStore } from "pinia";

const TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'
const USER_KEY = 'user'

function readUserFromStorage() {
    const raw = localStorage.getItem(USER_KEY)
    if (!raw) return null
    try {
        return JSON.parse(raw)
    } catch {
        return null
    }
}

export const useAuthStore = defineStore('auth', () => {
    // ---- state ----
    const accessToken = ref(localStorage.getItem(TOKEN_KEY))
    const refreshToken = ref(localStorage.getItem(REFRESH_TOKEN_KEY))
    const user = ref(readUserFromStorage())

    // ---- getters ----
    const isAuthenticated = computed(() => !!accessToken.value)
    const isAdmin = computed(() => user.value?.role === 'admin')
    const isPremium = computed(() => user.value?.is_premium === true)

    // ---- actions ----
    function setTokens(newAccess, newRefresh) {
        accessToken.value = newAccess
        refreshToken.value = newRefresh
        localStorage.setItem(TOKEN_KEY, newAccess)
        localStorage.setItem(REFRESH_TOKEN_KEY, newRefresh)
    }

    /**
     * Используется интерцептором api.js после успешного refresh.
     * Не пишет в localStorage - уже обновлено интерцептором
     */
    function setTokensFromRefresh(newAccess, newRefresh) {
        accessToken.value = newAccess
        refreshToken.value = newRefresh
    }

    function setUser(newUser) {
        user.value = newUser
        if (newUser) {
            localStorage.setItem(USER_KEY, JSON.stringify(newUser))
        } else {
            localStorage.removeItem(USER_KEY)
        }
    }

    function logout() {
        accessToken.value = null
        refreshToken.value = null
        user.value = null
        localStorage.removeItem(TOKEN_KEY)
        localStorage.removeItem(REFRESH_TOKEN_KEY)
        localStorage.removeItem(USER_KEY)
    }

    return {
        accessToken,
        refreshToken,
        user,
        isAuthenticated,
        isPremium,
        isAdmin,
        setTokens,
        setTokensFromRefresh,
        setUser,
        logout,
    }
})