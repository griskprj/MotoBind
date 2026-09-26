<template>
  <div class="welcome-container">
    <div class="welcome-card animate-slide-in">
      <div class="background-image"></div>

      <div class="content-wrapper">
        <div class="top-content">
          <p class="right-title">MotoBind</p>
        </div>

        <div class="bottom-content">
          <h1 class="welcome-title">
            Добро пожаловать <br />в MotoBind
          </h1>
          <p class="right-text">
            Ваш помощник в обслуживании мотоцикла.<br />Всё под контролем.
          </p>

          <div class="right-actions">
            <BaseButton variant="primary" block @click="goToRegister">
              Начать
            </BaseButton>
            <p class="login-hint">
              Уже есть аккаунт?
              <router-link to="/login" class="login-link">Войти</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { BaseButton } from '@/components/ui'

const router = useRouter()

function goToRegister() {
  router.push('/register')
}
</script>

<style scoped>
.welcome-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.welcome-card {
  position: relative;
  max-width: 1100px;
  width: 100%;
  border-radius: var(--radius);
  overflow: hidden;
  background-color: var(--bg-card);
  box-shadow: var(--shadow-lg);
  min-height: 600px;
  display: flex;
  align-items: center;
}

.animate-slide-in {
  animation: slideInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(30px);
}

.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 50%;
  height: 100%;
  background-image: url('/16x9Auth-Bg.webp');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.content-wrapper {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
  min-height: 600px;
}

.top-content {
  padding: 32px 36px 0 36px;
  display: flex;
  justify-content: flex-start;
}

.right-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--accent);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin: 0;
}

.bottom-content {
  padding: 0 36px 40px 36px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: flex-start;
  gap: 16px;
  max-width: 50%;
  margin-left: auto;
}

.welcome-title {
  font-size: 2.2rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.2;
}

.right-text {
  color: var(--text-secondary);
  font-size: 1rem;
  max-width: 340px;
  margin: 0;
}

.right-actions {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 4px;
}

.right-actions > :first-child {
  max-width: 280px;
}

.login-hint {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin: 0;
}

.login-link {
  color: var(--accent);
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s;
}

.login-link:hover {
  color: var(--accent-hover);
  text-decoration: underline;
}

@media (max-width: 820px) {
  .welcome-container {
    padding: 0;
    align-items: stretch;
  }

  .welcome-card {
    max-width: 100%;
    border-radius: 0;
    min-height: 100vh;
    box-shadow: none;
  }

  .background-image {
    width: 100%;
    height: 100%;
    background-image: url('/9x16Auth-Bg.webp');
  }

  .content-wrapper {
    min-height: 100vh;
    justify-content: space-between;
    padding: 0;
  }

  .top-content {
    padding: 24px 24px 0 24px;
    justify-content: center;
  }

  .right-title {
    margin-top: 16px;
    font-size: 1.2rem;
    color: white;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
  }

  .bottom-content {
    padding: 40px 24px 32px 24px;
    max-width: 100%;
    margin-left: 0;
    align-items: center;
    text-align: center;
    background: linear-gradient(to top, rgba(10, 10, 15, 0.8) 0%, transparent 100%);
  }

  .welcome-title {
    font-size: 1.8rem;
    color: white;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
  }

  .right-text {
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.95rem;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
  }

  .right-actions > :first-child {
    max-width: 100%;
  }

  .login-hint {
    color: rgba(255, 255, 255, 0.7);
  }

  .login-link {
    color: #a78bfa;
  }
}

@media (max-width: 480px) {
  .top-content {
    padding: 20px 20px 0 20px;
  }

  .bottom-content {
    padding: 32px 20px 24px 20px;
  }

  .welcome-title {
    font-size: 1.6rem;
  }

  .right-title {
    font-size: 1rem;
  }
}
</style>
