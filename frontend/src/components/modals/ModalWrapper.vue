<template>
    <div v-if="isOpen" class="modal-wrapper">
        <div class="modal-container">
            <div class="modal-header">
                <div class="header-wrapper actions">
                    <div class="header-icon" :style="{background: bgIconColor, color: iconColor}">
                        <i class="fa" :class="'fa-' + icon"></i>
                    </div>
                    <button @click="$emit('close')" class="btn-small">
                        <i class="fa fa-close"></i>
                    </button>
                </div>
                <div class="header-wrapper">
                    <p class="modal-title">{{ title }}</p>
                    <p class="modal-subtitle">{{ subtitle }}</p>
                </div>
            </div>

            <div class="modal-body">
                <div class="modal-group">
                    <slot />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        isOpen: Boolean,
        title: String,
        subtitle: String,
        icon: String,
        bgIconColor: String,
        iconColor: String
    }
}
</script>

<style scoped>
.modal-container {
    background-color: var(--bg-primary);
}
.modal-header {
    display: flex;
    flex-direction: column;
    align-items: start;
}

.modal-title {
    font-size: 21px;
    margin-bottom: 4px;
}

.modal-subtitle {
    font-size: 14px;
    color: var(--text-secondary);
}

.header-wrapper.actions {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    width: 100%;
}

.header-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--accent-trans);
    color: var(--accent);
    border-radius: 12px;
}
</style>