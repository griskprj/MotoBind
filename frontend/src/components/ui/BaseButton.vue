<template>
    <button 
        class="base-btn"
        :class="[
            `base-btn--${variant}`,
            { 'base-btn--small': size === 'small' },
            { 'base-btn--large': size === 'large' },
            { 'base-btn--full': fullWidth }
        ]"
        :disabled="disabled"
        @click="$emit('click')"
    >
        <i v-if="icon" :class="`fa fa-${icon}`"></i>
        <slot />
    </button>
</template>

<script>
export default {
    name: 'BaseButton',
    props: {
        variant: {
            type: String,
            default: 'primary',
            validator: value => ['primary', 'secondary', 'outline', 'danger', 'success', 'warning'].includes(value)
        },
        size: {
            type: String,
            default: 'medium',
            validator: value => ['small', 'medium', 'large'].includes(value)
        },
        icon: {
            type: String,
            default: null
        },
        fullWidth: {
            type: Boolean,
            default: false
        },
        disabled: {
            type: Boolean,
            default: false
        }
    },
    emits: ['click']
}
</script>

<style scoped>
.base-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 500;
    line-height: 1;
    border-radius: 10px;
    border: 1px solid transparent;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
    white-space: nowrap;
}

.base-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

/* Размеры */
.base-btn--small {
    padding: 6px 12px;
    font-size: 12px;
    border-radius: 8px;
}

.base-btn--large {
    padding: 14px 28px;
    font-size: 16px;
    border-radius: 12px;
}

.base-btn--full {
    width: 100%;
    justify-content: center;
}

/* Варианты */
.base-btn--primary {
    background: var(--accent);
    color: #fff;
}
.base-btn--primary:hover:not(:disabled) {
    background: var(--accent-hover);
    transform: translateY(-2px);
}

.base-btn--secondary {
    background: var(--bg-secondary);
    border-color: var(--border-color);
    color: var(--text-primary);
}
.base-btn--secondary:hover:not(:disabled) {
    background: var(--border-color);
}

.base-btn--outline {
    background: transparent;
    border-color: var(--accent);
    color: var(--accent);
}
.base-btn--outline:hover:not(:disabled) {
    background: var(--accent-light);
}

.base-btn--danger {
    background: var(--danger);
    color: #fff;
}
.base-btn--danger:hover:not(:disabled) {
    background: var(--danger-hover);
    transform: translateY(-2px);
}

.base-btn--success {
    background: var(--success);
    color: #fff;
}
.base-btn--success:hover:not(:disabled) {
    background: var(--success-hover);
    transform: translateY(-2px);
}

.base-btn--warning {
    background: var(--warning);
    color: #fff;
}
.base-btn--warning:hover:not(:disabled) {
    background: var(--warning-hover);
    transform: translateY(-2px);
}
</style>