<template>
  <div class="login-container">
    <div class="login-card animate-slide-in">
      <!-- Левая часть с изображением -->
      <div class="left-side"></div>
      <div class="image-overlay">
      </div>

      <!-- Правая часть с формой -->
      <div class="right-side">
        <div class="login-header">
          <i class="fa fa-motorcycle"></i>
          <h1 class="login-title">Вход в MotoBind</h1>
          <p class="login-subtitle">Войдите в свой аккаунт, чтобы продолжить</p>
        </div>

        <form @submit.prevent="login" class="login-form">
          <div class="form-group">
            <label for="email">
              <i class="fa fa-envelope"></i> Email
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="motorcycle@moto.com"
              required
              autocomplete="email"
            />
          </div>

          <div class="form-group">
            <label for="password">
              <i class="fa fa-lock"></i> Пароль
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="Введите пароль"
              required
              autocomplete="current-password"
            />
          </div>

          <div class="form-options">
            <div class="checkbox-group">
              <input type="checkbox" id="remember" />
              <label for="remember" class="checkbox-label">Запомнить меня</label>
            </div>
            <router-link to="/forgot-password" class="forgot-link">
              Забыли пароль?
            </router-link>
          </div>

          <button class="btn btn-primary submit-btn" type="submit">
            <i class="fa fa-sign-in-alt"></i> Войти
          </button>
        </form>

        <div v-if="error" class="error-message">
          <i class="fa fa-exclamation-circle"></i> {{ error }}
        </div>

        <div v-if="$route.query.registered" class="success-message">
          <i class="fa fa-check-circle"></i> Регистрация успешна! Теперь войдите.
        </div>

        <div class="register-link">
          <span>Нет аккаунта?</span>
          <router-link to="/register" class="register-btn">
            Зарегистрироваться
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../api/api';
import { setTokens, setUser } from '../../api/auth';

export default {
  data() {
    return {
      email: '',
      password: '',
      error: null,
    };
  },

  methods: {
    async login() {
      this.error = null;
      try {
        const response = await api.post('/auth/login', {
          email: this.email,
          password: this.password,
        });
        const { access_token, refresh_token } = response.data;
        setTokens(access_token, refresh_token);
        setUser(response.data.user);

        const role = response.data.user.role;
        if (role === 'admin') {
          this.$router.push('/admin/panel');
        } else {
          this.$router.push('/home');
        }
      } catch (err) {
        this.error = err.response?.data?.error || 'Ошибка входа. Проверьте email и пароль.';
      }
    },
  },
};
</script>

<style scoped>
/* Контейнер */
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

/* Карточка входа */
.login-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1100px;
  width: 100%;
  border-radius: var(--radius);
  overflow: hidden;
  background-color: var(--bg-card);
  box-shadow: var(--shadow-lg);
  position: relative;
  min-height: 600px;
}

/* Анимация появления */
.animate-slide-in {
  animation: slideInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(30px);
}

/* Левая сторона — изображение */
.left-side {
  position: relative;
  min-height: 400px;
  background-image: url('/16x9Auth-Bg.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* Оверлей с текстом по центру */
.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 50%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.overlay-text {
  display: inline-block;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  padding: 10px 28px;
  border-radius: 40px;
  font-size: 1.3rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  color: #fff;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.12);
}

/* Правая сторона — форма */
.right-side {
  padding: 48px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: var(--bg-card);
}

/* Заголовок */
.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-header i {
  font-size: 48px;
  color: var(--accent);
  margin-bottom: 12px;
}

.login-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.login-subtitle {
  color: var(--text-muted);
  font-size: 0.95rem;
  margin: 0;
}

/* Форма */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 6px;
}

.form-group label i {
  font-size: 14px;
  color: var(--accent);
  margin: 0;
}

.form-group input {
  padding: 0.75rem 1rem;
  border-radius: 10px;
  border: 2px solid var(--border-color);
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 0.95rem;
  transition: all 0.3s;
}

.form-group input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(138, 92, 246, 0.15);
  outline: none;
}

.form-group input::placeholder {
  color: var(--text-muted);
}

/* Опции формы */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 4px 0 8px 0;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.checkbox-group input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: var(--accent);
  cursor: pointer;
}

.checkbox-label {
  font-size: 0.875rem;
  font-weight: 400;
  color: var(--text-secondary);
  cursor: pointer;
  margin: 0;
}

.forgot-link {
  font-size: 0.875rem;
  color: var(--accent);
  text-decoration: none;
  transition: color 0.2s;
}

.forgot-link:hover {
  color: var(--accent-hover);
  text-decoration: underline;
}

/* Кнопка входа */
.submit-btn {
  width: 100%;
  padding: 0.9rem 1.5rem;
  font-size: 1rem;
  border-radius: 40px;
  background-color: var(--accent);
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.submit-btn:hover {
  background-color: var(--accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(138, 92, 246, 0.3);
}

.submit-btn:active {
  transform: translateY(0);
}

.submit-btn i {
  font-size: 16px;
  color: white;
  margin: 0;
}

/* Сообщения */
.error-message {
  margin-top: 16px;
  padding: 12px 16px;
  background-color: var(--danger-trans);
  border: 1px solid var(--danger);
  border-radius: 10px;
  color: var(--danger);
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.success-message {
  margin-top: 16px;
  padding: 12px 16px;
  background-color: var(--success-trans);
  border: 1px solid var(--success);
  border-radius: 10px;
  color: var(--success);
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Ссылка регистрации */
.register-link {
  margin-top: 24px;
  text-align: center;
  font-size: 0.95rem;
  color: var(--text-secondary);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.register-btn {
  color: var(--accent);
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.register-btn:hover {
  color: var(--accent-hover);
  text-decoration: underline;
}

/* ===== Адаптивность ===== */
@media (max-width: 820px) {
  .login-container {
    padding: 0;
    align-items: stretch;
  }

  .login-card {
    grid-template-columns: 1fr;
    max-width: 100%;
    border-radius: 0;
    min-height: 100vh;
    box-shadow: none;
  }

  /* Фон на весь экран */
  .left-side {
    position: absolute;
    inset: 0;
    min-height: unset;
    background-image: url('/9x16Auth-Bg.png');
    background-size: cover;
    background-position: center;
    z-index: 0;
  }

  .image-overlay {
    width: 100%;
    height: 100%;
    z-index: 1;
  }

  .overlay-text {
    font-size: 1.1rem;
    padding: 8px 20px;
    background: rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(2px);
    -webkit-backdrop-filter: blur(2px);
  }

  .right-side {
    position: relative;
    z-index: 2;
    background: rgba(10, 10, 15, 0.75);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    padding: 32px 24px;
    margin: 16px;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    min-height: auto;
    max-height: 90vh;
    overflow-y: auto;
  }

  .login-header i {
    font-size: 40px;
  }

  .login-title {
    font-size: 1.6rem;
  }
}

@media (max-width: 480px) {
  .right-side {
    padding: 24px 16px;
    margin: 12px;
  }

  .login-title {
    font-size: 1.4rem;
  }

  .form-options {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .overlay-text {
    font-size: 1rem;
    padding: 6px 16px;
  }
}
</style>