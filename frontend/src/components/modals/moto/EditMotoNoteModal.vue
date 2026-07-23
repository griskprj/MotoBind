<script>
import ModalWrapper from '../ModalWrapper.vue';

export default {
    components: {
        ModalWrapper
    },

    props: {
        isOpen: {
            type: Boolean,
            default: false,
            required: true
        },
        motorcycle: {
            type: Object,
            default: null
        }
    },

    data() {
        return {
            form: {
                id: null,
                note: ''
            }
        }
    },

    watch: {
        isOpen(newVal) {
            if (newVal && this.motorcycle) {
                this.form = {
                    id: this.motorcycle.id,
                    note: this.motorcycle.note || ''
                }
            }
        },

        motorcycle: {
            handler(newVal) {
                if (this.isOpen && newVal) {
                    this.form = {
                        id: newVal.id,
                        note: newVal.note || ''
                    }
                }
            },
            deep: true
        }
    },

    methods: {
        resetForm() {
            this.form = {
                id: null,
                note: ''
            }
        },

        submit() {
            this.$emit('submit', this.form)
            this.resetForm()
            this.$emit('close')
        }
    }
}
</script>

<template>
    <ModalWrapper
        :is-open="isOpen"
        title="Редактирование заметок"
        subtitle="Заметки помогают хранить важную информацию о мотоцикле: особенности, доработки, личные наблюдения и другое"
        icon="file"
        @close="$emit('close')"
    >
        <div class="form-group">
            <label class="form-label">Заметки</label>
            <textarea 
                v-model="form.note" 
                maxlength="128"
                class="form-textarea"
                placeholder="Введите заметки о мотоцикле..."
            ></textarea>
            <div class="char-counter">{{ form.note?.length || 0 }}/128</div>
        </div>

        <div class="modal-actions">
            <button class="cancel-btn" @click="$emit('close')">Отмена</button>
            <button @click="submit" class="submit-btn">
                <i class="fa fa-check"></i> Сохранить
            </button>
        </div>
    </ModalWrapper>
</template>

<style scoped>
.modal-actions {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin-top: 20px;
}

.modal-actions button {
    font-weight: 600;
    padding: 10px 16px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
}

.cancel-btn {
    background: rgba(255, 255, 255, 0.05);
    color: #8b8b9e;
}

.cancel-btn:hover {
    background: rgba(255, 255, 255, 0.1);
}

.submit-btn {
    background: #7c3aed;
    color: #fff;
}

.submit-btn:hover {
    background: #6d28d9;
}

.form-group {
    margin-bottom: 16px;
}

.form-label {
    display: block;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 8px;
    color: #8b8b9e;
}

.form-textarea {
    width: 100%;
    min-height: 120px;
    padding: 12px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.03);
    color: #fff;
    font-size: 14px;
    resize: vertical;
    transition: border-color 0.2s;
}

.form-textarea:focus {
    outline: none;
    border-color: #7c3aed;
}

.char-counter {
    text-align: right;
    font-size: 12px;
    color: #8b8b9e;
    margin-top: 4px;
}
</style>