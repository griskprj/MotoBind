<template>
    <div v-if="isOpen" class="modal-wrapper">
        <div class="modal-container">
            <div class="modal-header">
                <p class="modal-title">{{ title }}</p>
                <button @click="$emit('close')" class="close-btn">
                    <i class="fa fa-close"></i>
                </button>
            </div>

            <div class="modal-body">
                <slot />
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        isOpen: Boolean,
        title: String
    }
}
</script>