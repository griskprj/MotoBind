<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-icon">
        <i class="fa fa-envelope"></i>
      </div>
      <h2>Подтвердите email</h2>
      <p class="subtitle">
        Мы отправили письмо с ссылкой для подтверждения на <strong>{{ email }}</strong>
      </p>
      
      <div class="info-box">
        <i class="fa fa-info-circle"></i>
        <span>После подтверждения вы сможете пользоваться всеми функциями сервиса.</span>
      </div>
      
      <div class="actions">
        <button class="btn btn-outline" @click="resend" :disabled="resending">
          <i class="fa fa-refresh" :class="{ 'fa-spin': resending }"></i>
          {{ resending ? 'Отправка...' : 'Отправить повторно' }}
        </button>
        <button class="btn btn-primary" @click="checkVerification" :disabled="checking">
          <i class="fa fa-check" :class="{ 'fa-spin': checking }"></i>
          {{ checking ? 'Проверка...' : 'Я подтвердил' }}
        </button>
      </div>
      
      <p class="hint">
        Не пришло письмо? Проверьте папку "Спам" или <a @click="resend">отправьте повторно</a>
      </p>
      
      <button class="close-btn" @click="close">
        <i class="fa fa-times"></i>
      </button>
    </div>
  </div>
</template>

<script>
import api from '../../api/api'

export default {
  name: 'VerificationModal',
  props: {
    isOpen: {
      type: Boolean,
      default: false
    },
    email: {
      type: String,
      default: ''
    },
    userId: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      resending: false,
      checking: false,
      timer: null
    }
  },
  methods: {
    async resend() {
      this.resending = true
      try {
        await api.post('/auth/send-verification')
        alert('Письмо отправлено повторно! Проверьте почту.')
      } catch (err) {
        alert('Ошибка отправки письма. Попробуйте позже.')
      } finally {
        this.resending = false
      }
    },
    async checkVerification() {
      this.checking = true
      try {
        const response = await api.get('/auth/check-verification')
        if (response.data.is_verified) {
          this.$emit('verified')
          this.close()
        } else {
          alert('Email ещё не подтверждён. Проверьте почту.')
        }
      } catch (err) {
        alert('Ошибка проверки. Попробуйте позже.')
      } finally {
        this.checking = false
      }
    },
    close() {
      this.$emit('close')
    }
  },
  watch: {
    isOpen(val) {
      if (val) {
        // Автоматически проверяем статус каждые 5 секунд
        clearInterval(this.timer)
        this.timer = setInterval(() => {
          this.checkVerification()
        }, 5000)
      } else {
        clearInterval(this.timer)
      }
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  max-width: 440px;
  width: 100%;
  background: #181824;
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 16px;
  padding: 40px 32px;
  text-align: center;
  position: relative;
  animation: fadeIn 0.3s ease;
}

.modal-icon {
  font-size: 56px;
  color: #8B5CF6;
  margin-bottom: 16px;
}

.modal-content h2 {
  font-size: 24px;
  margin: 0 0 8px 0;
}

.modal-content .subtitle {
  color: #8b8b9e;
  font-size: 15px;
  margin: 0 0 24px 0;
  line-height: 1.6;
}

.info-box {
  background: rgba(139, 92, 246, 0.08);
  border: 1px solid rgba(139, 92, 246, 0.15);
  border-radius: 10px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  text-align: left;
  margin-bottom: 24px;
}

.info-box i {
  color: #8B5CF6;
  font-size: 18px;
  flex-shrink: 0;
}

.info-box span {
  font-size: 14px;
  color: #8b8b9e;
}

.actions {
  display: flex;
  gap: 12px;
}

.actions .btn {
  flex: 1;
  padding: 12px 16px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-outline {
  background: transparent;
  border: 2px solid #2d2d3d;
  color: #8b8b9e;
}

.btn-outline:hover {
  border-color: #8B5CF6;
  color: #8B5CF6;
}

.btn-outline:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: #8B5CF6;
  color: #fff;
}

.btn-primary:hover {
  background: #7C3AED;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.hint {
  font-size: 13px;
  color: #5a5a72;
  margin-top: 20px;
}

.hint a {
  color: #8B5CF6;
  cursor: pointer;
}

.hint a:hover {
  text-decoration: underline;
}

.close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: transparent;
  border: none;
  color: #5a5a72;
  font-size: 20px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 8px;
  transition: 0.2s;
}

.close-btn:hover {
  background: rgba(255,255,255,0.05);
  color: #fff;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>