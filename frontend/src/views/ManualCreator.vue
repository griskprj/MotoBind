<template>
    <div class="container">
        <LoadingOverlay :isLoading="isSubmitting" text="Создание мануала..."/>
        
        <!-- === HEADER === -->
        <Header
            title="Конструктор мануалов"
            subtitle="Создание подробной инструкции по ремонту и обслуживанию"
        />

        <!-- === FORM === -->
        <section class="form-section">
            <div class="info-banner">
                <i class="fa fa-info-circle"></i>
                <span>Правила оформления мануалов <a href='/manual/rules' target='_blank'>здесь</a>.</span>
            </div>
            
            <form @submit.prevent="submitManual" enctype="multipart/form-data">
                <!-- ===== БЛОК 1: О МАНУАЛЕ ===== -->
                <div class="form-card">
                    <div class="form-card-header">
                        <i class="fa fa-info-circle"></i>
                        <h3>1. О мануале</h3>
                    </div>

                    <div class="form-card-body">
                        <div class="form-group">
                            <label>
                                Название процедуры*
                                <input 
                                    type="text" 
                                    v-model="form.title" 
                                    required
                                    placeholder="Например: Замена масла в двигателе"
                                    :class="{ 'error': errors.title }"
                                >
                                <span v-if="errors.title" class="error-message">{{ errors.title }}</span>
                            </label>
                        </div>

                        <div class="form-group">
                            <label>
                                Краткое описание*
                                <textarea 
                                    v-model="form.description" 
                                    required
                                    rows="2"
                                    placeholder="Краткое описание процедуры, её важность и интервалы"
                                    :class="{ 'error': errors.description }"
                                ></textarea>
                                <span v-if="errors.description" class="error-message">{{ errors.description }}</span>
                            </label>
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label>
                                    Модель мотоцикла*
                                    <input 
                                        type="text" 
                                        v-model="form.motorcycle" 
                                        required
                                        placeholder="Например: BMW S1000RR (2018+)"
                                        :class="{ 'error': errors.motorcycle }"
                                    >
                                    <span v-if="errors.motorcycle" class="error-message">{{ errors.motorcycle }}</span>
                                </label>
                            </div>

                            <div class="form-group">
                                <label>
                                    Сложность*
                                    <select v-model="form.difficult" required>
                                        <option value="">Выберите сложность</option>
                                        <option value="easy">Легко</option>
                                        <option value="medium">Средне</option>
                                        <option value="hard">Сложно</option>
                                    </select>
                                </label>
                            </div>
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label>
                                    Ориентировочное время
                                    <input 
                                        type="text" 
                                        v-model="form.time_estimate" 
                                        placeholder="Например: 15–20 минут"
                                    >
                                </label>
                            </div>

                            <div class="form-group">
                                <label>
                                    Периодичность
                                    <input 
                                        type="text" 
                                        v-model="form.interval" 
                                        placeholder="Например: каждые 10 000 км или раз в год"
                                    >
                                </label>
                            </div>
                        </div>

                        <div class="form-group">
                            <label>
                                Категория
                                <select v-model="form.category">
                                    <option value="">Выберите категорию</option>
                                    <option value="engine">Двигатель</option>
                                    <option value="drive">Привод</option>
                                    <option value="steering">Рулевое управление</option>
                                    <option value="suspension">Подвеска</option>
                                    <option value="electronics">Электроника</option>
                                    <option value="wheel">Колеса/Шины</option>
                                    <option value="brakes">Тормозная система</option>
                                    <option value="fuel">Топливная система</option>
                                    <option value="cooling">Система охлаждения</option>
                                </select>
                            </label>
                        </div>
                    </div>
                </div>

                <!-- ===== БЛОК 2: БЕЗОПАСНОСТЬ И ПОДГОТОВКА ===== -->
                <div class="form-card">
                    <div class="form-card-header">
                        <i class="fa fa-shield"></i>
                        <h3>2. Безопасность и подготовка</h3>
                    </div>

                    <div class="form-card-body">
                        <div class="form-group">
                            <label>
                                Общие рекомендации
                                <textarea 
                                    v-model="form.safety_tip" 
                                    rows="2"
                                    placeholder="Общие рекомендации по выполнению процедуры"
                                ></textarea>
                            </label>
                        </div>

                        <div class="form-group">
                            <label>
                                ⚠️ Предупреждения (что категорически нельзя делать)
                                <textarea 
                                    v-model="form.warnings" 
                                    rows="2"
                                    placeholder="Например: Не запускайте двигатель без масла"
                                ></textarea>
                            </label>
                        </div>

                        <div class="form-group">
                            <label>
                                Необходимые условия
                                <textarea 
                                    v-model="form.conditions" 
                                    rows="2"
                                    placeholder="Например: Двигатель холодный, мотоцикл на центральной подставке"
                                ></textarea>
                            </label>
                        </div>
                    </div>
                </div>

                <!-- ===== БЛОК 3: ИНСТРУМЕНТЫ И МАТЕРИАЛЫ ===== -->
                <div class="form-card">
                    <div class="form-card-header">
                        <i class="fa fa-wrench"></i>
                        <h3>3. Инструменты и материалы</h3>
                    </div>

                    <div class="form-card-body">
                        <div class="form-group">
                            <label>
                                Инструменты
                                <input 
                                    type="text" 
                                    v-model="form.instruments" 
                                    placeholder="Ключ на 18мм, ветошь, динамометрический ключ, ёмкость для слива"
                                >
                            </label>
                        </div>

                        <div class="form-group">
                            <label>
                                Материалы и запчасти
                                <input 
                                    type="text" 
                                    v-model="form.parts" 
                                    placeholder="Масло моторное 10W-40 (3.2L), масляный фильтр, уплотнительное кольцо"
                                >
                            </label>
                        </div>
                    </div>
                </div>

                <!-- ===== БЛОК 4: ССЫЛКИ НА ДОКУМЕНТАЦИЮ ===== -->
                <div class="form-card">
                    <div class="form-card-header">
                        <i class="fa fa-link"></i>
                        <h3>4. Ссылки на официальную документацию</h3>
                    </div>

                    <div class="form-card-body">
                        <div class="form-group">
                            <label>
                                Ссылки на документацию
                                <div class="links-list">
                                    <div 
                                        v-for="(link, index) in form.docs_links" 
                                        :key="index" 
                                        class="link-item"
                                    >
                                        <input 
                                            type="url" 
                                            v-model="form.docs_links[index]" 
                                            placeholder="https://example.com/manual.pdf"
                                            class="link-input"
                                        >
                                        <button 
                                            type="button" 
                                            class="btn-remove-link" 
                                            @click="removeLink(index)"
                                        >
                                            <i class="fa fa-times"></i>
                                        </button>
                                    </div>
                                </div>
                                <button type="button" class="btn-add-link" @click="addLink">
                                    <i class="fa fa-plus"></i> Добавить ссылку
                                </button>
                            </label>
                        </div>
                    </div>
                </div>

                <!-- ===== БЛОК 5: ТЕХНИЧЕСКИЕ ДАННЫЕ ===== -->
                <div class="form-card">
                    <div class="form-card-header">
                        <i class="fa fa-table"></i>
                        <h3>5. Технические данные</h3>
                    </div>

                    <div class="form-card-body">
                        <div class="form-group">
                            <label>
                                Моменты затяжки (JSON)
                                <textarea 
                                    v-model="form.specs_json" 
                                    rows="6"
                                    placeholder='{
  "torque": [
    {"name": "Болт сливной пробки", "nm": 25, "note": "сухой"},
    {"name": "Болт крепления фильтра", "nm": 12, "note": "сухой"}
  ],
  "fluids": {
    "oil": "3.2L (с фильтром)",
    "coolant": "1.5L"
  },
  "tolerances": {
    "chain": "2-5 мм"
  }
}'
                                    class="code-input"
                                ></textarea>
                                <span class="field-hint">Введите данные в формате JSON</span>
                            </label>
                        </div>

                        <div class="form-group">
                            <label>Быстрый редактор моментов затяжки</label>
                            <div class="torque-editor">
                                <div 
                                    v-for="(item, index) in torqueItems" 
                                    :key="index" 
                                    class="torque-row"
                                >
                                    <input 
                                        v-model="item.name" 
                                        placeholder="Название болта"
                                        class="torque-name"
                                    >
                                    <input 
                                        v-model="item.nm" 
                                        placeholder="Н·м"
                                        type="number"
                                        class="torque-nm"
                                    >
                                    <input 
                                        v-model="item.note" 
                                        placeholder="Примечание"
                                        class="torque-note"
                                    >
                                    <button 
                                        type="button" 
                                        class="btn-remove-torque" 
                                        @click="removeTorqueItem(index)"
                                    >
                                        <i class="fa fa-times"></i>
                                    </button>
                                </div>
                                <button type="button" class="btn-add-torque" @click="addTorqueItem">
                                    <i class="fa fa-plus"></i> Добавить момент затяжки
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ===== БЛОК 6: ШАГИ ===== -->
                <div class="form-card">
                    <div class="form-card-header">
                        <i class="fa fa-list-ol"></i>
                        <h3>6. Шаги инструкции</h3>
                        <span class="steps-count">{{ form.steps.length }} шаг(ов)</span>
                    </div>

                    <div class="form-card-body">
                        <div v-if="form.steps.length === 0" class="empty-state">
                            <i class="fa fa-hand-pointer"></i>
                            <p>Нажмите "Добавить шаг", чтобы создать инструкцию</p>
                        </div>

                        <div v-for="(step, index) in form.steps" :key="step.id" class="step-card">
                            <div class="step-header">
                                <span class="step-number">Шаг {{ index + 1 }}</span>
                                <button type="button" class="btn-remove-step" @click="removeStep(index)">
                                    <i class="fa fa-times"></i>
                                </button>
                            </div>
                            
                            <div class="step-content">
                                <div class="form-group">
                                    <label>
                                        Заголовок шага*
                                        <input 
                                            type="text" 
                                            v-model="step.title" 
                                            required
                                            :placeholder="`Что нужно сделать на шаге ${index + 1}?`"
                                            :class="{ 'error': step.errors && step.errors.title }"
                                        >
                                        <span v-if="step.errors && step.errors.title" class="error-message">{{ step.errors.title }}</span>
                                    </label>
                                </div>

                                <div class="form-group">
                                    <label>
                                        Описание шага
                                        <textarea 
                                            v-model="step.text" 
                                            rows="3"
                                            :placeholder="`Подробное описание шага ${index + 1}`"
                                        ></textarea>
                                    </label>
                                </div>

                                <div class="form-row">
                                    <div class="form-group">
                                        <label>
                                            ⚠️ Предупреждение
                                            <input 
                                                type="text"
                                                v-model="step.warning"
                                                placeholder="Чего нельзя делать на этом шаге"
                                            >
                                        </label>
                                    </div>

                                    <div class="form-group">
                                        <label>
                                            💡 Совет
                                            <input 
                                                type="text"
                                                v-model="step.tip"
                                                placeholder="Лайфхак или рекомендация"
                                            >
                                        </label>
                                    </div>
                                </div>

                                <div class="form-group">
                                    <label>
                                        🎯 Результат шага
                                        <input 
                                            type="text"
                                            v-model="step.result"
                                            placeholder="Как понять, что шаг выполнен правильно"
                                        >
                                    </label>
                                </div>

                                <div class="form-group">
                                    <label>
                                        📷 Изображение шага
                                        <div class="image-upload" @click="$refs['fileInput' + index].click()">
                                            <input 
                                                :ref="'fileInput' + index"
                                                type="file" 
                                                accept="image/*"
                                                @change="handleImageUpload(index, $event)"
                                                class="file-input"
                                            >
                                            <span class="file-name" v-if="step.imageFile">
                                                {{ step.imageFile.name }}
                                            </span>
                                            <span class="file-name" v-else>Выберите файл</span>
                                            <button 
                                                v-if="step.imageFile" 
                                                type="button" 
                                                class="btn-remove-image" 
                                                @click.stop="removeImage(index)"
                                            >
                                                <i class="fa fa-times"></i>
                                            </button>
                                        </div>
                                        <div v-if="step.imagePreview" class="image-preview">
                                            <img :src="step.imagePreview" :alt="step.title" />
                                        </div>
                                    </label>
                                </div>
                            </div>
                        </div>

                        <button type="button" class="btn-add-step" @click="addStep">
                            <i class="fa fa-plus"></i> Добавить шаг
                        </button>
                    </div>
                </div>

                <!-- ===== БЛОК 7: ПОСЛЕ ЗАВЕРШЕНИЯ ===== -->
                <div class="form-card">
                    <div class="form-card-header">
                        <i class="fa fa-check-circle"></i>
                        <h3>7. После завершения</h3>
                    </div>

                    <div class="form-card-body">
                        <div class="form-group">
                            <label>
                                Финальная проверка
                                <textarea 
                                    v-model="form.aftercare" 
                                    rows="3"
                                    placeholder="Что проверить после работы: уровень масла, отсутствие течей, затяжку болтов..."
                                ></textarea>
                            </label>
                        </div>
                    </div>
                </div>

                <!-- Кнопки отправки -->
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" @click="resetForm">Отменить</button>
                    <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                        <i v-if="isSubmitting" class="fa fa-spinner fa-spin"></i>
                        <span v-else><i class="fa fa-check"></i> Создать мануал</span>
                    </button>
                </div>
            </form>
        </section>
    </div>
</template>

<script>
import api from '../api/api';
import Header from '../components/Header.vue';
import LoadingOverlay from '../components/LoadingOverlay.vue';

export default {
    name: 'ManualCreator',
    components: { Header, LoadingOverlay },
    
    data() {
        return {
            form: {
                title: '',
                description: '',
                motorcycle: '',
                difficult: '',
                time_estimate: '',
                interval: '',
                category: '',
                safety_tip: '',
                warnings: '',
                conditions: '',
                instruments: '',
                parts: '',
                docs_links: [],
                specs: {},
                specs_json: '',
                steps: [],
                aftercare: '',
                tip: ''
            },
            errors: {},
            isSubmitting: false,
            stepIdCounter: 0,
            torqueItems: []
        };
    },

    watch: {
        torqueItems: {
            handler(newVal) {
                if (newVal.length > 0) {
                    const torque = newVal.filter(item => item.name || item.nm).map(item => ({
                        name: item.name || 'Болт',
                        nm: item.nm ? Number(item.nm) : 0,
                        note: item.note || ''
                    }));
                    this.updateSpecs('torque', torque);
                }
            },
            deep: true
        },
        specs_json: {
            handler(newVal) {
                try {
                    if (newVal && newVal.trim()) {
                        this.form.specs = JSON.parse(newVal);
                    }
                } catch (e) {
                    // Невалидный JSON - игнорируем
                }
            },
            deep: true
        }
    },

    methods: {
        addStep() {
            this.form.steps.push({
                id: ++this.stepIdCounter,
                title: '',
                text: '',
                warning: '',
                tip: '',
                result: '',
                imageFile: null,
                imagePreview: null,
                errors: {}
            });
        },

        removeStep(index) {
            if (this.form.steps.length <= 1) {
                alert('Мануал должен содержать хотя бы один шаг');
                return;
            }
            this.form.steps.splice(index, 1);
        },

        handleImageUpload(index, event) {
            const file = event.target.files[0];
            if (!file) return;

            if (file.size > 5 * 1024 * 1024) {
                alert('Размер файла не должен превышать 5MB');
                event.target.value = '';
                return;
            }

            if (!file.type.startsWith('image/')) {
                alert('Пожалуйста, загрузите изображение');
                event.target.value = '';
                return;
            }

            this.form.steps[index].imageFile = file;
            
            const reader = new FileReader();
            reader.onload = (e) => {
                this.form.steps[index].imagePreview = e.target.result;
            };
            reader.readAsDataURL(file);
        },

        removeImage(index) {
            this.form.steps[index].imageFile = null;
            this.form.steps[index].imagePreview = null;
            const input = this.$refs['fileInput' + index];
            if (input) input.value = '';
        },

        addLink() {
            this.form.docs_links.push('');
        },

        removeLink(index) {
            this.form.docs_links.splice(index, 1);
        },

        updateSpecs(key, value) {
            if (!this.form.specs) {
                this.form.specs = {};
            }
            this.form.specs[key] = value;
            this.specs_json = JSON.stringify(this.form.specs, null, 2);
        },

        addTorqueItem() {
            this.torqueItems.push({ name: '', nm: '', note: '' });
        },

        removeTorqueItem(index) {
            this.torqueItems.splice(index, 1);
        },

        validateForm() {
            this.errors = {};
            let isValid = true;

            if (!this.form.title || this.form.title.trim().length < 3) {
                this.errors.title = 'Название должно содержать минимум 3 символа';
                isValid = false;
            }

            if (!this.form.description || this.form.description.trim().length < 10) {
                this.errors.description = 'Описание должно содержать минимум 10 символов';
                isValid = false;
            }

            if (!this.form.motorcycle || this.form.motorcycle.trim().length < 2) {
                this.errors.motorcycle = 'Укажите модель мотоцикла';
                isValid = false;
            }

            if (!this.form.difficult) {
                this.errors.difficult = 'Выберите сложность';
                isValid = false;
            }

            this.form.steps.forEach((step, index) => {
                step.errors = {};
                if (!step.title || step.title.trim().length < 2) {
                    step.errors.title = 'Заголовок шага обязателен';
                    isValid = false;
                }
            });

            if (this.form.steps.length === 0) {
                isValid = false;
            }

            return isValid;
        },

        async submitManual() {
            if (!this.validateForm()) {
                const firstError = document.querySelector('.error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
                return;
            }

            this.isSubmitting = true;

            try {
                // Создаём FormData для отправки файлов
                const formData = new FormData();
                
                // Текстовые поля
                const payload = {
                    title: this.form.title.trim(),
                    description: this.form.description.trim(),
                    category: this.form.category || 'general',
                    difficult: this.form.difficult,
                    motorcycle: this.form.motorcycle.trim(),
                    time_estimate: this.form.time_estimate.trim() || null,
                    interval: this.form.interval.trim() || null,
                    safety_tip: this.form.safety_tip.trim() || null,
                    warnings: this.form.warnings.trim() || null,
                    conditions: this.form.conditions.trim() || null,
                    docs_links: this.form.docs_links.filter(link => link.trim()),
                    specs: this.form.specs || null,
                    aftercare: this.form.aftercare.trim() || null,
                    instruments: this.form.instruments.trim() || null,
                    parts: this.form.parts.trim() || null,
                    tip: this.form.tip.trim() || null,
                    steps: this.form.steps.map((step, index) => ({
                        order: index + 1,
                        title: step.title.trim(),
                        text: step.text.trim() || null,
                        warning: step.warning.trim() || null,
                        tip: step.tip.trim() || null,
                        result: step.result.trim() || null
                    }))
                };

                // Добавляем JSON данные как строку
                formData.append('data', JSON.stringify(payload));

                // Добавляем файлы изображений
                this.form.steps.forEach((step, index) => {
                    if (step.imageFile) {
                        formData.append(`image_${index + 1}`, step.imageFile);
                    }
                });

                const response = await api.post('/manual/new-manual', formData, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });

                if (response.status === 201) {
                    alert('Мануал успешно создан!');
                    this.resetForm();
                    this.$router.push('/manuals');
                }
            } catch (error) {
                console.error('Ошибка создания мануала:', error);
                
                let errorMessage = 'Произошла ошибка при создании мануала';
                if (error.response?.data?.message) {
                    errorMessage = error.response.data.message;
                } else if (error.response?.data?.error) {
                    errorMessage = error.response.data.error;
                } else if (error.message) {
                    errorMessage = error.message;
                }
                
                alert(`Ошибка: ${errorMessage}`);
            } finally {
                this.isSubmitting = false;
            }
        },

        resetForm() {
            this.form = {
                title: '',
                description: '',
                motorcycle: '',
                difficult: '',
                time_estimate: '',
                interval: '',
                category: '',
                safety_tip: '',
                warnings: '',
                conditions: '',
                instruments: '',
                parts: '',
                docs_links: [],
                specs: {},
                specs_json: '',
                steps: [],
                aftercare: '',
                tip: ''
            };
            this.errors = {};
            this.stepIdCounter = 0;
            this.torqueItems = [];
            this.addStep();
        },

        async logout() {
            try {
                await api.post('/auth/logout');
            } catch(err) { console.error(err) }
            finally {
                const { removeTokens } = await import('../api/auth');
                removeTokens();
                this.$router.push('/login');
            }
        }
    },

    mounted() {
        this.addStep();
    }
};
</script>

<style scoped>
/* ===== FORM SECTION ===== */
.form-section {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.info-banner {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 16px;
    background: var(--accent-trans);
    border: 1px solid var(--accent-light);
    border-radius: 10px;
    color: var(--text-secondary);
    font-size: 14px;
}

.info-banner a {
    color: var(--accent-text);
    text-decoration: underline;
}

/* ===== FORM CARD ===== */
.form-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 16px;
}

.form-card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 20px;
    border-bottom: 1px solid var(--border-color);
    background: var(--bg-secondary);
}

.form-card-header i {
    font-size: 18px;
    color: var(--accent);
}

.form-card-header h3 {
    font-size: 16px;
    font-weight: 600;
    margin: 0;
    color: var(--text-primary);
}

.steps-count {
    margin-left: auto;
    font-size: 13px;
    color: var(--text-secondary);
    background: var(--bg-secondary);
    padding: 2px 12px;
    border-radius: 20px;
    border: 1px solid var(--border-color);
}

.form-card-body {
    padding: 20px;
}

/* ===== FORM ELEMENTS ===== */
.form-group {
    margin-bottom: 16px;
}

.form-group:last-child {
    margin-bottom: 0;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

.form-group label {
    display: block;
    font-weight: 500;
    color: var(--text-secondary);
    margin-bottom: 6px;
    font-size: 14px;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 10px 14px;
    font-size: 14px;
    font-family: inherit;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 10px;
    color: var(--text-primary);
    transition: all 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-trans);
}

.form-group input::placeholder,
.form-group textarea::placeholder {
    color: var(--text-muted);
}

.form-group input.error,
.form-group textarea.error {
    border-color: var(--danger);
}

.form-group input.error:focus,
.form-group textarea.error:focus {
    box-shadow: 0 0 0 3px var(--danger-trans);
}

.form-group textarea {
    resize: vertical;
    min-height: 60px;
}

.code-input {
    font-family: 'Courier New', monospace;
    font-size: 13px !important;
}

.error-message {
    display: block;
    color: var(--danger);
    font-size: 13px;
    margin-top: 4px;
}

.field-hint {
    display: block;
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 4px;
}

/* ===== LINKS ===== */
.links-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 8px;
}

.link-item {
    display: flex;
    gap: 8px;
    align-items: center;
}

.link-input {
    flex: 1;
    padding: 8px 12px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 8px;
    color: var(--text-primary);
    font-size: 14px;
}

.btn-remove-link {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 6px;
    transition: all 0.2s;
}

.btn-remove-link:hover {
    background: var(--danger-trans);
    color: var(--danger);
}

.btn-add-link {
    padding: 6px 14px;
    font-size: 13px;
    background: transparent;
    border: 1px dashed var(--accent-trans);
    border-radius: 8px;
    color: var(--accent-text);
    cursor: pointer;
    transition: all 0.2s;
}

.btn-add-link:hover {
    background: var(--accent-trans);
}

/* ===== TORQUE EDITOR ===== */
.torque-editor {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.torque-row {
    display: grid;
    grid-template-columns: 2fr 1fr 2fr auto;
    gap: 8px;
    align-items: center;
}

.torque-name,
.torque-note {
    padding: 6px 10px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 6px;
    color: var(--text-primary);
    font-size: 13px;
}

.torque-nm {
    padding: 6px 10px;
    background: var(--bg-input);
    border: 1px solid var(--border-input);
    border-radius: 6px;
    color: var(--text-primary);
    font-size: 13px;
    width: 80px;
}

.btn-remove-torque {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 6px;
}

.btn-remove-torque:hover {
    background: var(--danger-trans);
    color: var(--danger);
}

.btn-add-torque {
    padding: 6px 14px;
    font-size: 13px;
    background: transparent;
    border: 1px dashed var(--accent-trans);
    border-radius: 8px;
    color: var(--accent-text);
    cursor: pointer;
    transition: all 0.2s;
    margin-top: 4px;
}

.btn-add-torque:hover {
    background: var(--accent-trans);
}

/* ===== STEPS ===== */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 2px dashed var(--border-color);
    text-align: center;
    margin-bottom: 16px;
}

.empty-state i {
    font-size: 32px;
    color: var(--accent);
    margin-bottom: 12px;
}

.empty-state p {
    font-size: 16px;
    color: var(--text-secondary);
    margin: 0;
}

.step-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    transition: border-color 0.2s;
}

.step-card:hover {
    border-color: var(--accent-trans);
}

.step-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.step-number {
    font-weight: 600;
    font-size: 14px;
    color: var(--accent-text);
    background: var(--accent-trans);
    padding: 2px 14px;
    border-radius: 20px;
}

.btn-remove-step {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 6px;
    transition: all 0.2s;
    font-size: 16px;
}

.btn-remove-step:hover {
    background: var(--danger-trans);
    color: var(--danger);
}

.step-content .form-group {
    margin-bottom: 12px;
}

.step-content .form-group:last-child {
    margin-bottom: 0;
}

/* ===== IMAGE UPLOAD ===== */
.image-upload {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    background: var(--bg-input);
    border: 1px dashed var(--border-input);
    border-radius: 8px;
    cursor: pointer;
    transition: border-color 0.2s;
}

.image-upload:hover {
    border-color: var(--accent);
}

.file-input {
    display: none;
}

.file-name {
    flex: 1;
    font-size: 13px;
    color: var(--text-muted);
}

.btn-remove-image {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 6px;
}

.btn-remove-image:hover {
    background: var(--danger-trans);
    color: var(--danger);
}

.image-preview {
    margin-top: 8px;
    border-radius: 8px;
    overflow: hidden;
    max-width: 300px;
}

.image-preview img {
    width: 100%;
    height: auto;
    max-height: 200px;
    object-fit: cover;
    border-radius: 8px;
    border: 1px solid var(--border-color);
}

/* ===== BUTTONS ===== */
.btn-add-step {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 500;
    border-radius: 10px;
    border: 1px dashed var(--accent-trans);
    background: transparent;
    color: var(--accent-text);
    cursor: pointer;
    transition: all 0.2s;
    width: 100%;
    justify-content: center;
}

.btn-add-step:hover {
    background: var(--accent-trans);
    border-color: var(--accent);
}

.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px 24px;
    font-size: 14px;
    font-weight: 500;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-primary {
    background: var(--accent);
    color: #fff;
}

.btn-primary:hover:not(:disabled) {
    background: var(--accent-hover);
    transform: translateY(-2px);
}

.btn-secondary {
    background: transparent;
    color: var(--text-secondary);
    border: 1px solid var(--border-input);
}

.btn-secondary:hover:not(:disabled) {
    background: var(--border-color);
}

/* ===== FORM ACTIONS ===== */
.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    padding-top: 20px;
    border-top: 1px solid var(--border-color);
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .form-row {
        grid-template-columns: 1fr;
        gap: 0;
    }

    .torque-row {
        grid-template-columns: 1fr;
        gap: 4px;
    }

    .torque-nm {
        width: 100%;
    }

    .form-card-header {
        flex-wrap: wrap;
    }

    .steps-count {
        margin-left: 0;
        width: 100%;
    }

    .form-actions {
        flex-direction: column-reverse;
    }

    .form-actions .btn {
        width: 100%;
        justify-content: center;
    }

    .step-card {
        padding: 12px;
    }

    .image-preview {
        max-width: 100%;
    }
}

@media (max-width: 480px) {
    .form-card-body {
        padding: 16px;
    }

    .empty-state {
        padding: 24px;
    }

    .empty-state i {
        font-size: 24px;
    }

    .empty-state p {
        font-size: 14px;
    }

    .link-item {
        flex-direction: column;
    }

    .btn-remove-link {
        align-self: flex-end;
    }
}

.fa-spin {
    animation: fa-spin 1s linear infinite;
}

@keyframes fa-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>