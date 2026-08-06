<template>
  <div class="register-wizard-container">
    <div class="wizard-card animate-slide-in">
      <!-- Фоновое изображение (десктоп) -->
      <div class="background-image"></div>
      
      <!-- Затемнение для читаемости -->
      <div class="background-overlay"></div>

      <!-- Прогресс -->
      <div class="progress-section">
        <div class="step-indicator">{{ currentStep }} из {{ totalSteps }}</div>
        <div class="progress-bar">
          <div
            class="progress-fill"
            :style="{ width: progressPercent + '%' }"
          ></div>
        </div>
      </div>

      <!-- Шаги -->
      <div class="step-content">
        <!-- Шаг 7: Завершение -->
        <div v-if="currentStep === 7" class="step completion-step">
          <div class="completion-glow"></div>
          
          <div class="particles-container">
            <div
              v-for="i in 40"
              :key="i"
              class="particle"
              :style="getParticleStyle(i)"
            ></div>
          </div>
          
          <div class="blur-blobs">
            <div class="blob blob-1"></div>
            <div class="blob blob-2"></div>
            <div class="blob blob-3"></div>
          </div>

          <div class="completion-icon">
            <i class="fa fa-check-circle"></i>
          </div>
          <h2 class="step-title">Вы всё настроили!</h2>
          <p class="step-subtitle">
            Ваш мотоцикл добавлен. Теперь вы можете вести учет обслуживания и
            получать напоминания о ТО.
          </p>

          <div class="step-actions">
            <button
              class="btn btn-primary"
              :disabled="loading"
              @click="finishRegistration"
            >
              <span v-if="!loading">Перейти в приложение</span>
              <span v-else>Загрузка...</span>
            </button>
          </div>
        </div>

        <!-- Остальные шаги -->
        <div v-else-if="currentStep === 1" class="step">
          <h2 class="step-title">Выберите, что вас описывает</h2>
          <p class="step-subtitle">Мы настроим приложение под ваши задачи.</p>

          <div class="role-cards">
            <div
              class="role-card"
              :class="{ selected: formData.role === 'motorcyclist' }"
              @click="selectRole('motorcyclist')"
            >
              <div class="role-icon">
                <i class="fa fa-motorcycle"></i>
              </div>
              <div class="role-info">
                <h3>Я владелец мотоцикла</h3>
                <p>Хочу вести учет обслуживания своего мотоцикла.</p>
              </div>
              <div class="role-check" v-if="formData.role === 'motorcyclist'">
                <i class="fa fa-check-circle"></i>
              </div>
            </div>

            <div
              class="role-card"
              :class="{ selected: formData.role === 'motoclub' }"
              @click="error='Эта роль находится в разработке'"
            >
              <div class="role-icon">
                <i class="fa fa-store"></i>
              </div>
              <div class="role-info">
                <h3>Я представляю сервис</h3>
                <p>Хочу управлять мотоциклами клиентов.</p>
              </div>
              <div class="role-check" v-if="formData.role === 'motoclub'">
                <i class="fa fa-check-circle"></i>
              </div>
            </div>
          </div>

          <div class="step-actions">
            <button
              class="btn btn-primary"
              :disabled="!formData.role"
              @click="nextStep"
            >
              Продолжить
            </button>
          </div>
        </div>

        <div v-else-if="currentStep === 2" class="step">
          <h2 class="step-title">Давайте познакомимся</h2>
          <p class="step-subtitle">Это поможет сделать MotoBind удобнее для вас.</p>

          <div class="form-group">
            <label for="username">
              <i class="fa fa-user"></i> Как к вам обращаться?
            </label>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              placeholder="Ваше имя"
              required
            />
          </div>

          <div class="form-group">
            <label for="email">
              <i class="fa fa-envelope"></i> Email
            </label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              placeholder="motorcycle@moto.com"
              required
            />
          </div>

          <div class="form-group">
            <label for="password">
              <i class="fa fa-lock"></i> Пароль
            </label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              placeholder="Минимум 6 символов"
              required
            />
          </div>

          <div class="step-actions">
            <button class="btn btn-secondary" @click="prevStep">Назад</button>
            <button
              class="btn btn-primary"
              :disabled="!isStep2Valid"
              @click="nextStep"
            >
              Продолжить
            </button>
          </div>
        </div>

        <div v-else-if="currentStep === 3" class="step">
          <h2 class="step-title">Добавьте свой первый мотоцикл</h2>
          <p class="step-subtitle">
            Начнем с основного мотоцикла. Потом можно добавить еще.
          </p>

          <div class="empty-moto-card">
            <i class="fa fa-motorcycle empty-icon"></i>
            <h3>Мотоциклов пока нет</h3>
            <p>Добавьте свой мотоцикл, чтобы начать вести учет обслуживания.</p>
            <button class="btn btn-primary" @click="addMotorcycle">
              Добавить мотоцикл
            </button>
          </div>

          <div class="step-actions">
            <button class="btn btn-secondary" @click="prevStep">Назад</button>
            <button class="btn btn-outline" @click="skipMotorcycle">
              Добавить позже
            </button>
          </div>
        </div>

        <div v-else-if="currentStep === 4" class="step">
          <h2 class="step-title">Добавление мотоцикла</h2>

          <div class="form-group">
            <label for="motoName">Название <span class="required">*</span></label>
            <input
              id="motoName"
              v-model="formData.motorcycle.name"
              type="text"
              placeholder="Например: Honda CBR600RR"
              required
            />
          </div>

          <div class="form-group">
            <label for="motoYear">Год выпуска</label>
            <input
              id="motoYear"
              v-model.number="formData.motorcycle.years"
              type="number"
              placeholder="2020"
              min="1900"
              :max="new Date().getFullYear()"
            />
          </div>

          <div class="form-group">
            <label for="motoVolume">Объем двигателя (см³)</label>
            <input
              id="motoVolume"
              v-model.number="formData.motorcycle.volume"
              type="number"
              placeholder="600"
              min="49"
              max="4000"
            />
          </div>

          <div class="step-actions">
            <button class="btn btn-secondary" @click="prevStep">Назад</button>
            <button
              class="btn btn-primary"
              :disabled="!formData.motorcycle.name"
              @click="nextStep"
            >
              Продолжить
            </button>
          </div>
        </div>

        <div v-else-if="currentStep === 5" class="step">
          <h2 class="step-title">Добавление мотоцикла</h2>

          <div class="form-group">
            <label for="motoColor">Цвет</label>
            <input
              id="motoColor"
              v-model="formData.motorcycle.color"
              type="color"
              value="#8B5CF6"
            />
          </div>

          <div class="form-group">
            <label for="motoMileage">Пробег (км)</label>
            <input
              id="motoMileage"
              v-model.number="formData.motorcycle.mileage"
              type="number"
              placeholder="0"
              min="0"
            />
          </div>

          <div class="form-group">
            <label for="motoPlate">Гос номер (необязательно)</label>
            <input
              id="motoPlate"
              v-model="formData.motorcycle.licensePlate"
              type="text"
              placeholder="A123BC"
            />
          </div>

          <div class="step-actions">
            <button class="btn btn-secondary" @click="prevStep">Назад</button>
            <button class="btn btn-primary" @click="nextStep">
              Продолжить
            </button>
          </div>
        </div>

        <div v-else-if="currentStep === 6" class="step">
          <h2 class="step-title">Добавление мотоцикла</h2>

          <div class="form-group">
            <label for="motoVin">VIN (необязательно)</label>
            <input
              id="motoVin"
              v-model="formData.motorcycle.vin"
              type="text"
              placeholder="17 символов"
              maxlength="17"
            />
          </div>

          <div class="form-group">
            <label for="motoNote">Заметки (необязательно)</label>
            <textarea
              id="motoNote"
              v-model="formData.motorcycle.note"
              rows="3"
              placeholder="Дополнительная информация"
            ></textarea>
          </div>

          <div class="form-group">
            <label>Фото мотоцикла</label>
            <div class="upload-card" @click="$refs.fileInput.click()">
              <div class="upload-icon">
                <i class="fa fa-cloud-upload-alt"></i>
              </div>
              <div class="upload-info">
                <p>Добавить фото мотоцикла</p>
                <span>JPG, PNG до 10 МБ</span>
              </div>
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                @change="handleFileUpload"
                style="display: none"
              />
            </div>
            <div v-if="formData.motorcycle.photo" class="photo-preview">
              <img :src="formData.motorcycle.photo" alt="Мотоцикл" />
              <button class="btn btn-danger btn-small" @click="removePhoto">
                <i class="fa fa-times"></i>
              </button>
            </div>
          </div>

          <div class="step-actions">
            <button class="btn btn-secondary" @click="prevStep">Назад</button>
            <button class="btn btn-primary" @click="nextStep">
              Сохранить мотоцикл
            </button>
          </div>
        </div>
      </div>

      <!-- Ошибка -->
      <div v-if="error" class="error-message">
        <i class="fa fa-exclamation-circle"></i> {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../api/api';
import { setTokens, setUser } from '../../api/auth';

export default {
  name: 'RegisterWizard',
  data() {
    return {
      currentStep: 1,
      totalSteps: 7,
      formData: {
        role: '',
        username: '',
        email: '',
        password: '',
        motorcycle: {
          name: '',
          years: null,
          volume: null,
          color: '#8B5CF6',
          mileage: null,
          licensePlate: '',
          vin: '',
          note: '',
          photo: null,
        },
      },
      error: null,
      loading: false,
      skipMotorcycleMode: false, // Флаг для режима пропуска
    };
  },
  computed: {
    progressPercent() {
      return ((this.currentStep - 1) / (this.totalSteps - 1)) * 100;
    },
    isStep2Valid() {
      return (
        this.formData.username.length >= 2 &&
        this.formData.email.includes('@') &&
        this.formData.password.length >= 6
      );
    },
  },
  methods: {
    selectRole(role) {
      this.formData.role = role;
    },
    nextStep() {
      if (this.currentStep < this.totalSteps) {
        this.currentStep++;
        this.error = null;
      }
    },
    prevStep() {
      if (this.currentStep > 1) {
        this.currentStep--;
        this.error = null;
      }
    },
    addMotorcycle() {
      // Переход на шаг добавления мотоцикла
      this.skipMotorcycleMode = false;
      this.currentStep = 4;
    },
    skipMotorcycle() {
      // Устанавливаем флаг пропуска и переходим на финальный шаг
      this.skipMotorcycleMode = true;
      this.currentStep = 7; // Переход на финальный экран
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.formData.motorcycle.photo = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    removePhoto() {
      this.formData.motorcycle.photo = null;
      this.$refs.fileInput.value = '';
    },
    getParticleStyle(index) {
      const size = Math.random() * 6 + 2;
      const x = Math.random() * 100;
      const y = Math.random() * 100;
      const duration = Math.random() * 20 + 15;
      const delay = Math.random() * 10;
      const opacity = Math.random() * 0.4 + 0.1;
      
      return {
        width: size + 'px',
        height: size + 'px',
        left: x + '%',
        top: y + '%',
        animationDuration: duration + 's',
        animationDelay: delay + 's',
        opacity: opacity,
      };
    },
    async finishRegistration() {
      this.error = null;
      this.loading = true;

      try {
        // 1. Регистрация пользователя
        const registerPayload = {
          email: this.formData.email,
          username: this.formData.username,
          password: this.formData.password,
          role: this.formData.role,
        };

        const registerResponse = await api.post('/auth/register', registerPayload);
        const { access_token, refresh_token, user } = registerResponse.data;

        if (!access_token || !refresh_token || !user) {
          throw new Error('Сервер не вернул токены авторизации');
        }

        setTokens(access_token, refresh_token);
        setUser(user);

        // 2. Создаём мотоцикл только если не в режиме пропуска
        if (!this.skipMotorcycleMode && this.formData.motorcycle.name) {
          const motoPayload = {
            name: this.formData.motorcycle.name,
            years: this.formData.motorcycle.years || null,
            volume: this.formData.motorcycle.volume || null,
            color: this.formData.motorcycle.color || null,
            mileage: this.formData.motorcycle.mileage || null,
            licensePlate: this.formData.motorcycle.licensePlate || null,
            vin: this.formData.motorcycle.vin || null,
            note: this.formData.motorcycle.note || null,
          };

          await api.post('/motorcycle/', motoPayload, {
            headers: { Authorization: `Bearer ${access_token}` },
          });
        }

        // 3. Перенаправление
        const role = user.role || this.formData.role;
        const targetRoute = role === 'admin' ? '/admin/panel' : '/home';
        this.$router.push(targetRoute);
      } catch (err) {
        if (err.response?.data?.detail) {
          const details = err.response.data.detail;
          if (Array.isArray(details)) {
            this.error = details.map(d => d.msg || d).join(', ');
          } else {
            this.error = details;
          }
        } else {
          this.error = err.response?.data?.error || err.message || 'Ошибка регистрации. Попробуйте снова.';
        }

        if (this.error.includes('email') || this.error.includes('username') || this.error.includes('password')) {
          this.currentStep = 2;
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Основной контейнер */
.register-wizard-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.wizard-card {
  max-width: 700px;
  width: 100%;
  background-color: var(--bg-card);
  border-radius: var(--radius);
  padding: 32px 40px;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-color);
  position: relative;
  overflow: hidden;
}

/* Фоновое изображение (десктоп) */
.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('/16x9Auth-Bg.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0.15;
  z-index: 0;
}

/* Затемнение для читаемости */
.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(10, 10, 15, 0.92) 0%,
    rgba(10, 10, 15, 0.85) 50%,
    rgba(10, 10, 15, 0.92) 100%
  );
  z-index: 1;
}

.animate-slide-in {
  animation: slideInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(30px);
}

/* Прогресс */
.progress-section {
  margin-bottom: 32px;
  position: relative;
  z-index: 2;
}

.step-indicator {
  text-align: center;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background-color: var(--bg-secondary);
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--accent-hover));
  transition: width 0.4s ease;
  border-radius: 10px;
}

/* Шаги */
.step-content {
  min-height: 400px;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 2;
}

.step {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: fadeIn 0.3s ease;
  position: relative;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.step-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
  color: var(--text-primary);
}

.step-subtitle {
  color: var(--text-secondary);
  font-size: 1rem;
  margin-top: -12px;
  margin-bottom: 4px;
}

.required {
  color: var(--danger);
}

/* ============================================ */
/* ФИНАЛЬНЫЙ ШАГ С ПАРТИКЛАМИ */
/* ============================================ */
.completion-step {
  align-items: center;
  text-align: center;
  min-height: 400px;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.completion-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  height: 60%;
  background: radial-gradient(
    ellipse at center,
    rgba(139, 92, 246, 0.25) 0%,
    rgba(139, 92, 246, 0.08) 40%,
    transparent 70%
  );
  animation: pulseGlow 4s ease-in-out infinite;
  pointer-events: none;
  z-index: 1;
}

@keyframes pulseGlow {
  0%, 100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.8;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.2);
    opacity: 1;
  }
}

.blur-blobs {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
  z-index: 1;
}

.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.08;
}

.blob-1 {
  width: 200px;
  height: 200px;
  background: var(--accent);
  top: 10%;
  right: -10%;
  animation: floatBlob 12s ease-in-out infinite;
}

.blob-2 {
  width: 150px;
  height: 150px;
  background: #a78bfa;
  bottom: 10%;
  left: -10%;
  animation: floatBlob 16s ease-in-out infinite reverse;
}

.blob-3 {
  width: 120px;
  height: 120px;
  background: #7c3aed;
  top: 40%;
  left: 30%;
  animation: floatBlob 14s ease-in-out infinite 2s;
}

@keyframes floatBlob {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(20px, -30px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

.particles-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
  z-index: 1;
}

.particle {
  position: absolute;
  border-radius: 50%;
  background: var(--accent);
  animation: floatParticle linear infinite;
  pointer-events: none;
  will-change: transform;
  box-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
}

@keyframes floatParticle {
  0% {
    transform: translate(0, 0) scale(1);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translate(calc(var(--dx, 30px)), calc(var(--dy, -80px))) scale(0.5);
    opacity: 0;
  }
}

.particle:nth-child(odd) {
  --dx: 40px;
  --dy: -100px;
}

.particle:nth-child(even) {
  --dx: -30px;
  --dy: -70px;
}

.particle:nth-child(3n) {
  --dx: 50px;
  --dy: -60px;
}

.particle:nth-child(5n) {
  --dx: -50px;
  --dy: -90px;
}

.particle:nth-child(7n) {
  --dx: 20px;
  --dy: -120px;
}

.completion-icon {
  text-align: center;
  font-size: 64px;
  color: var(--accent);
  margin: 16px 0 8px;
  position: relative;
  z-index: 2;
  filter: drop-shadow(0 0 30px var(--accent-trans));
}

.completion-step .step-title,
.completion-step .step-subtitle,
.completion-step .step-actions {
  position: relative;
  z-index: 2;
}

.completion-step .step-title {
  margin-bottom: 8px;
}

.completion-step .step-subtitle {
  max-width: 440px;
  margin-left: auto;
  margin-right: auto;
}

/* ============================================ */
/* ОСТАЛЬНЫЕ СТИЛИ */
/* ============================================ */

.role-cards {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin: 8px 0 16px;
}

.role-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px 20px;
  background-color: var(--bg-secondary);
  border: 2px solid transparent;
  border-radius: var(--radius);
  cursor: pointer;
  transition: all 0.2s;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.role-card:hover {
  background-color: var(--bg-card-hover);
  transform: translateY(-2px);
}

.role-card.selected {
  border-color: var(--accent);
  background-color: var(--accent-light);
  box-shadow: 0 0 0 2px rgba(138, 92, 246, 0.2);
}

.role-icon {
  font-size: 28px;
  color: var(--accent);
  width: 48px;
  text-align: center;
}

.role-info {
  flex: 1;
}

.role-info h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 4px 0;
}

.role-info p {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin: 0;
}

.role-check {
  font-size: 24px;
  color: var(--accent);
}

.empty-moto-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 24px;
  background-color: var(--bg-secondary);
  border-radius: var(--radius);
  border: 2px dashed var(--border-color);
  gap: 12px;
  text-align: center;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.empty-icon {
  font-size: 48px;
  color: var(--text-muted);
}

.empty-moto-card h3 {
  margin: 0;
  font-size: 1.2rem;
}

.empty-moto-card p {
  color: var(--text-secondary);
  margin: 0 0 8px 0;
}

.empty-moto-card .btn {
  width: 100%;
  max-width: 280px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-group label {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 6px;
}

.form-group label i {
  color: var(--accent);
  font-size: 14px;
}

.form-group input,
.form-group textarea {
  padding: 0.7rem 1rem;
  border-radius: 10px;
  border: 2px solid var(--border-color);
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 0.95rem;
  transition: border 0.2s;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: var(--accent);
  outline: none;
  box-shadow: 0 0 0 3px rgba(138, 92, 246, 0.15);
}

.form-group input[type="color"] {
  padding: 4px;
  height: 48px;
  cursor: pointer;
}

.upload-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  background-color: var(--bg-secondary);
  border: 2px dashed var(--border-color);
  border-radius: var(--radius);
  cursor: pointer;
  transition: all 0.2s;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.upload-card:hover {
  border-color: var(--accent);
  background-color: var(--bg-card-hover);
  transform: translateY(-2px);
}

.upload-icon {
  font-size: 32px;
  color: var(--accent);
}

.upload-info p {
  margin: 0;
  font-weight: 500;
}

.upload-info span {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.photo-preview {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
}

.photo-preview img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 10px;
  border: 2px solid var(--border-color);
}

.step-actions {
  display: flex;
  gap: 12px;
  margin-top: auto;
  padding-top: 20px;
  justify-content: flex-end;
}

.step-actions .btn {
  min-width: 120px;
  padding: 0.8rem 1.5rem;
  border-radius: 40px;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.step-actions .btn-secondary {
  background-color: var(--bg-secondary);
  border: 2px solid var(--border-color);
  color: var(--text-primary);
}

.step-actions .btn-secondary:hover {
  background-color: var(--border-color);
}

.step-actions .btn-outline {
  background: transparent;
  border: 2px solid var(--accent);
  color: var(--accent);
}

.step-actions .btn-outline:hover {
  background: var(--accent-trans);
}

.error-message {
  margin-top: 16px;
  padding: 12px 16px;
  background-color: var(--danger-trans);
  border: 1px solid var(--danger);
  border-radius: 10px;
  color: var(--danger);
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
  z-index: 2;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

/* ============================================ */
/* АДАПТИВНОСТЬ ДЛЯ МОБИЛЬНЫХ УСТРОЙСТВ */
/* ============================================ */
@media (max-width: 768px) {
  .register-wizard-container {
    padding: 0;
    align-items: stretch;
  }

  .wizard-card {
    max-width: 100%;
    border-radius: 0;
    min-height: 100vh;
    padding: 24px 20px;
    box-shadow: none;
    border: none;
    display: flex;
    flex-direction: column;
  }

  /* Фоновое изображение на весь экран */
  .background-image {
    opacity: 0.25;
    background-image: url('/9x16Auth-Bg.png');
    background-size: cover;
    background-position: center;
  }

  .background-overlay {
    background: linear-gradient(
      180deg,
      rgba(10, 10, 15, 0.85) 0%,
      rgba(10, 10, 15, 0.75) 30%,
      rgba(10, 10, 15, 0.85) 70%,
      rgba(10, 10, 15, 0.95) 100%
    );
  }

  .step-content {
    flex: 1;
    min-height: auto;
  }

  .step {
    min-height: auto;
    gap: 16px;
  }

  .step-title {
    font-size: 1.5rem;
  }

  .step-subtitle {
    font-size: 0.95rem;
    margin-top: -8px;
  }

  .role-card {
    padding: 14px 16px;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
  }

  .role-icon {
    font-size: 24px;
    width: 40px;
  }

  .role-info h3 {
    font-size: 1rem;
  }

  .role-info p {
    font-size: 0.85rem;
  }

  .form-group input,
  .form-group textarea {
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
  }

  .step-actions {
    flex-wrap: wrap;
    justify-content: center;
    padding-top: 16px;
  }

  .step-actions .btn {
    min-width: 100%;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
  }

  .empty-moto-card {
    padding: 24px 16px;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
  }

  .upload-card {
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
  }

  /* Финальный шаг */
  .completion-step {
    min-height: auto;
    padding: 20px 0;
  }

  .completion-icon {
    font-size: 48px;
  }

  .completion-glow {
    width: 90%;
    height: 50%;
  }

  .blob {
    display: none;
  }

  .particles-container {
    opacity: 0.6;
  }
}

@media (max-width: 480px) {
  .wizard-card {
    padding: 20px 16px;
  }

  .step-title {
    font-size: 1.3rem;
  }

  .progress-section {
    margin-bottom: 20px;
  }

  .role-card {
    padding: 12px 14px;
    gap: 12px;
  }

  .role-icon {
    font-size: 20px;
    width: 32px;
  }

  .completion-icon {
    font-size: 40px;
  }

  .empty-moto-card {
    padding: 20px 16px;
  }

  .empty-icon {
    font-size: 36px;
  }

  .upload-card {
    padding: 16px;
  }

  .upload-icon {
    font-size: 24px;
  }

  .background-image {
    opacity: 0.2;
  }
}
</style>